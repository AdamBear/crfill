import streamlit as st
import jsons
from streamlit_option_menu import option_menu
from streamlit_image_comparison import image_comparison
import numpy as np
import tempfile

class tqdm:
    def __init__(self, iterable, st_progress_bar):
        self.prog_bar = st_progress_bar.progress(0)
        self.iterable = iterable
        self.length = len(iterable)
        self.i = 0

    def __iter__(self):
        for obj in self.iterable:
            yield obj
            self.i += 1
            current_prog = self.i / self.length
            self.prog_bar.progress(current_prog)

    def __enter__(self):
        return self

    def __exit__(self ,type, value, traceback):
        return False

    def update(self):
        self.i += 1
        current_prog = self.i / self.length
        self.prog_bar.progress(current_prog)


# 所有的demo都需要转换成接口，其中的resize方法原来改进，最终需要出原图比例
st.set_page_config(
     page_title="用户动态主题的可控文本生成原型系统",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'About': "#慧抖销工具服务，厦门书生企友通科技"
     }
 )

st.header("用户动态主题的可控文本生成原型系统")
st.subheader("主题素材管理功能")

# cols = st.columns(5)
# with cols[0]:
#     st.text("基础预训练模型")
# with cols[1]:
plm = st.selectbox("选择基础预训练模型", ["GPT2-Large", "GPT2-XL"])


ag_news_label = {1: "World",
                         2: "Sports",
                         3: "Business",
                         4: "Science"}

cols = st.columns(2)
with cols[0]:
    spc_sp = st.selectbox("选择已上传的软提示参数", ["ag_news_world_2022_03_27.3", "ag_news_sports_2022_03_27.1"])
with cols[1]:
    spc_params = st.file_uploader("上传软提示参数", help="请上传软提示参数pt文件", type=["pt"])


st.write("请选择人工前缀提示的主题类型")
cols = st.columns(5)
with cols[0]:
    spc_world = st.checkbox("World", value=True)
with cols[1]:
    spc_sports = st.checkbox("Sports", value=False)
with cols[2]:
    spc_Business = st.checkbox("Business", value=False)
with cols[3]:
    spc_science = st.checkbox("Science", value=False)

init_text = st.text_input("输入前导短语(可选)")
if st.button("生成文本"):
    pass

st.write("生成耗时:" + "7.834秒")
st.text_area("生成结果：", height = 300)



