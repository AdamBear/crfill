import pdb
import cv2
import os
from collections import OrderedDict

import numpy as np
from werkzeug.utils import secure_filename
from flask import Flask, url_for, render_template, request, redirect, send_from_directory
from PIL import Image
import base64
import io
import random


from options.test_options import TestOptions
import models
import torch

opt = TestOptions().parse()
model = models.create_model(opt)
model.eval()

max_size = 1024
max_num_examples = 200
UPLOAD_FOLDER = 'static/images'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'jpeg', 'bmp'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

port = opt.port
filelist = "./static/images/example.txt"
with open(filelist, "r") as f:
    list_examples = f.readlines()
list_examples = [n.strip("\n") for n in list_examples]

def process_image(img, mask, name, opt, save_to_input=True):
    img = img.convert("RGB")

    w_raw, h_raw = img.size

    h_t, w_t = h_raw // 8 * 8, w_raw // 8 * 8
    img = img.resize((w_t, h_t))
    img_raw = np.array(img)

    img = np.array(img).transpose((2, 0, 1))

    mask = mask.resize((w_t, h_t))
    mask_raw = np.array(mask)[..., None] > 0

    mask = np.array(mask)
    mask = (torch.Tensor(mask) > 0).float()
    img = (torch.Tensor(img)).float()
    img = (img / 255 - 0.5) / 0.5
    img = img[None]
    mask = mask[None, None]

    with torch.no_grad():
        generated, _ = model(
            {'image': img, 'mask': mask},
            mode='inference')
    generated = torch.clamp(generated, -1, 1)
    generated = (generated + 1) / 2 * 255
    generated = generated.cpu().numpy().astype(np.uint8)
    generated = generated[0].transpose((1, 2, 0))
    result = generated * mask_raw + img_raw * (1 - mask_raw)
    # result = generated*mask+img*(1-mask)

    result = result.astype(np.uint8)

    result = Image.fromarray(result).resize((w_raw, h_raw))
    result = np.array(result)
    result = Image.fromarray(result.astype(np.uint8))

    result.save(f"static/results/{name}")
    if save_to_input:
        result.save(f"static/images/{name}")
    return result


@app.route('/', methods=['GET', 'POST'])
def hello(name=None):
    if 'example' in request.form:
        filename= request.form['example']
        image = Image.open(os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
        W, H = image.size
        return render_template('hello.html', name=name, image_name=filename, image_width=W,
                image_height=H,list_examples=list_examples)
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                image = Image.open(file)
                W, H = image.size
                if max(W, H) > max_size:
                    ratio = float(max_size) / max(W, H)
                    W = int(W*ratio)
                    H = int(H*ratio)
                    image = image.resize((W, H))
                    filename = "resize_"+filename
                image.save(os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
                return render_template('hello.html', name=name, image_name=filename, image_width=W,
                        image_height=H,list_examples=list_examples)
            else:
                filename=list_examples[0]
                image = Image.open(os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
                W, H = image.size
                return render_template('hello.html', name=name, image_name=filename, image_width=W, image_height=H,
                        is_alert=True,list_examples=list_examples)
        if 'mask' in request.form:
            filename = request.form['imgname']
            mask_data = request.form['mask']
            mask_data = mask_data.replace('data:image/png;base64,', '')
            mask_data = mask_data.replace(' ', '+')
            mask = base64.b64decode(mask_data)
            maskname = '.'.join(filename.split('.')[:-1]) + '.png'
            maskname = maskname.replace("/","_")
            maskname = "{}_{}".format(random.randint(0, 1000), maskname)
            with open(os.path.join('static/masks', maskname), "wb") as fh:
                fh.write(mask)
            mask = io.BytesIO(mask)
            mask = Image.open(mask).convert("L")
            image = Image.open(os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
            W, H = image.size
            list_op = ["result"]
            for op in list_op:
                process_image(image, mask, f"{op}_"+maskname, op, save_to_input=True)
            return render_template('hello.html', name=name, image_name=filename, #f"{args.opt[0]}_"+maskname
                    mask_name=maskname, image_width=W, image_height=H, list_opt=list_op,list_examples=list_examples)
    else:
        filename=list_examples[0]
        image = Image.open(os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
        W, H = image.size
        return render_template('hello.html', name=name, image_name=filename, image_width=W, image_height=H,
                list_examples=list_examples)



if __name__ == "__main__":

    app.run(host='0.0.0.0', debug=True, port=port, threaded=True)
