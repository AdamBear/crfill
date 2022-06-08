import streamlit as st
import pandas as pd
import jsons
#from streamlit_option_menu import option_menu
#from streamlit_image_comparison import image_comparison
import numpy as np
import tempfile
import streamlit
import streamlit.cli
import streamlit_parameters
import streamlit.components.v1 as components
from st_aggrid import AgGrid

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

parameters = streamlit_parameters.parameters.Parameters()
parameters.register_string_list_parameter(key="action", default_value=["new", "edit"])

####################
# Set URL
####################
parameters.set_url_fields()

# ####################
# # Usage
# ####################
# streamlit.write("## Usage")
# usage = f"**Foo**: {parameters.foo.value}  \n"
# usage += f"**Bar**: {parameters.bar.value}  \n"
# usage += f"**Start Date**: {parameters.start_date.value}  \n"
# usage += f"**End Date**: {parameters.end_date.value}  \n"
# usage += f"**Category**: {parameters.category.value}"
# streamlit.write(usage)
#
# ####################
# # Debugging
# ####################
# streamlit.write("## Debugging")
#
# streamlit.write("#### Query String")
# query_string: typing.Dict[str, str] = streamlit.experimental_get_query_params()
# streamlit.write(query_string)

# streamlit.write("#### Parameters")
# streamlit.write(parameters.as_dict())
# st.write(parameters.action.value[0])

action = parameters.action.value[0]

st.header("用户动态主题的可控文本生成原型系统")
st.markdown("#### 主题素材样本管理")
st.markdown("##### 新建主题素材训练集")

#constrained_height = 50
#large_text_output = "".join([f"Line number {i}\n" for i in range(100)])
# components.html(
#     "<h3>主题素材管理功能</h3>",
#     height=30,
#     scrolling=True,
# )


topic = st.text_input("主题名称:", max_chars=35, value="Glass Fiber Reinforced Gypsum")
desc = st.text_input("主题描述:", value="关于玻纤维强化石膏板的介绍素材")

col1, col2, col3 = st.columns((5, 1, 5))

# st.write("生成耗时:" + "7.834秒")
col1.text_area("训练素材文本", height = 280)
col1.file_uploader("上传素材txt文件", type=["txt"])

col2.write("\r\n")
col2.write("\r\n")
col2.button("添加到样本")

df = pd.DataFrame(
    ['GFRG contains high-density, alpha-based gypsum and glass fiber reinforcement',
     'GFRG requires little maintenance and, due to its strength it is resistant to high impacts.',
     'Due to the lightness of the material, shipping costs are minimized.',
     'GFRG can address any design intent specified at a lower cost than traditional materials.',
     'The gypsum plaster tends to be neutral or has low alkalinity so that it can mix well with the glass fibers that are typically used. Additives are also commonly used in the plaster industry, which are acceptable as part of the mixture for GFRG if they align with the gypsum manufacturer’s recommendations.',
     'Glass Fiber Reinforced Gypsum including Glass Fiber Reinforced Gypsum, also known as GFRG. This article provides information on the development of this material and how it can be used today for remodeling and construction projects.',
     'The material was originally developed in England and came to the United States and Canada in the late 1970s as a potential alternative building material to traditional concrete. It has also gone by other names, such as Fiberglass Reinforced Gypsum (FRG) and Glass Reinforced Gypsum (GRG).',
     'GFRG was valued for its ability to offer strength despite being thin and light in weight. With these benefits, it was not long before companies in North America began offering GFRG as a construction material. As a pioneer in creating a better GFRG material, Stromberg Architectural began to introduce new techniques and technology associated with the material in the 1980s. Today, it is commonly used in the construction industry.',
     'Glass Fiber Reinforced Gypsum Applications',
     'The applications for GFRG are those construction projects or architectural products where there is no exposure to dampness, including where it will be hit by rain or subjected to a wet location like a fountain or pool. However, GFRG is perfect for applications where a fire-retardant, lightweight, and durable material is needed. Some applications include',
     'This material does not burn. Acting like a thermal regulator, GFRG also protects the materials behind it from the heat of a flame for up to two hours.',
     'GFRG is easy to install compared to heavier materials like natural stone or plaster. Its light weight makes it easy to transport, handle, and install.',
     'It is known for its durability and long-lasting beauty, offering a cost-effective way to add specific types of architectural features to a building’s interior.',
     'The material is flexible and versatile; it can be cast to virtually any shape imaginable.',
     'GFRG is available in white so that it can be finished with virtually any paint so the color possibilities are endless.',
     'GFRG (Glass Fiber Reinforced Gypsum) is the interior alternative to GFRC (Glass Fiber Reinforced Concrete) and sometimes abbreviated as GRG, or GRC. ',
     'GFRC is used for exterior projects as it is similar to concrete in strength and durability with only a fraction of the weight. GFRG is a reinforced gypsum product having high strength with lighter weight for interior projects.',
     'Glass Fiber Reinforced Gypsum (GFRG) consists of high strength resistant glass fibers bonded with high density gypsum cement to produce panels that traditionally were done with plaster castings. The GFRG is lighter in weight, superior in strength and much easier to install than the traditional plaster castings. GFRG is lighter than traditional gypsum and can be formed to a better detail.',
     'There are hundreds of in stock molds available for column covers (straight/tapered/fluted), capitals, bases, moldings, baseboards, coves and sconces, ceiling vaults, and cornices. These products serve both “functionality” along with aesthetically pleasing and innovative design. ',
     'GFRG can also be used for wide range of entry way and door surrounds. GFRG can also be used medallions, intricate moldings and decorative pieces to dress up the ceilings and walls. It is often used to replicate historical interiors found in hotels and restaurants and period homes or where ornamentation is a significant part of the overall look of the property.',
     'The savings arise since GFRG is made in a factory setting at not at the job site. The molds are designed to create shapes and integrated supports that enhance the overall look and design of a room.',
     'For quotes, more information, and all things related to GFRG check out UP Ceilings and Walls, our top manufacturer of GFRG products.',
     'GFRG is a cost effective panel that offers significant benefits over plaster castings:',
     'It requires minimal structural support when installing the panels making the installation process simpler and cost effective.',
     'The panels can be formed in to complex shapes expanding its usage significantly.',
     'The panels can be made in extra-large sizes.',
     'Plaster is normally cast in place at the job site, where as GFRG products are pre-made. All you need on the job site is installation. This makes deployment of GFRG products much simpler.',
     'Given its production process, the panels can be colored to match any aesthetic on any project.'],
    columns=(['样本句子']))


col3.text("训练样本句子列表")
with col3:
    #AgGrid(df)
    col3.dataframe(df, height=400, width=650)  # Same as st.write(df)

col11, col12, col13 = st.columns((1, 1, 8))
col11.metric("样本句子数", 28)
col12.metric("总词数", 803)

col11, col12, col13 = st.columns((1, 1, 20))
col11.button("保存")
col12.button("训练")
# st.button("下载主题素材训练集")






