import streamlit as st
# import jsons
# from streamlit_option_menu import option_menu
# from streamlit_image_comparison import image_comparison
# import numpy as np
# import tempfile

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
st.subheader("按主题文本生成")

st.markdown('''<style>

hr {
    margin: 0px;
}
</style>''', unsafe_allow_html=True)
st.write("---")
st.text("主题素材训练集: " + "4686b70330d5f6dd68c7f1c93c85dd12")
st.text("主题名称: " + "Glass Fiber Reinforced Gypsum")
st.text("主题描述: " + "关于玻纤维强化石膏板的介绍素材")
st.text("总训练词数: " + "4015")
st.write("---")

plm = st.selectbox("选择基础预训练模型", ["GPT2-Large", "GPT2-XL"])

#
# ag_news_label = {1: "World",
#                          2: "Sports",
#                          3: "Business",
#                          4: "Science"}
#
# cols = st.columns(2)
# with cols[0]:
#     spc_sp = st.selectbox("选择已上传的软提示参数", ["ag_news_world_2022_03_27.3", "ag_news_sports_2022_03_27.1"])
# with cols[1]:
#     spc_params = st.file_uploader("上传软提示参数", help="请上传软提示参数pt文件", type=["pt"])
#
#
# st.write("请选择人工前缀提示的主题类型")
# cols = st.columns(5)
# with cols[0]:
#     spc_world = st.checkbox("World", value=True)
# with cols[1]:
#     spc_sports = st.checkbox("Sports", value=False)
# with cols[2]:
#     spc_Business = st.checkbox("Business", value=False)
# with cols[3]:
#     spc_science = st.checkbox("Science", value=False)

# 生成解码参数高级
with st.expander("生成控制参数", False):
    st.text("高级控制参数")

init_text = st.text_input("输入生成引导短语", "GRG is a good materials for building wall, ")
if st.button("生成文本"):
    pass

st.write("生成耗时:" + "7.035秒")
st.text_area("生成结果：", height = 200, value="""
ceiling and floors because they are strong as steel without the strength of steel. Unlike steel, GRG does not rust or corrode over time. It is non-magnetic (meaning that it cannot attract other iron). This means that when you want to use it in your construction, you don't even have to worry about damaging it or its ability to stand up to stress.\xa0\nGRG can be made with virtually any thickness, from 0.5mm to 7mm, so you will need a few different thicknesses depending on what project you plan to construct. The thicker the fabric, the more durable it becomes. GRG works well with plywood, wood or tile walls; however you can also do this with foam, plastic, fiberboard or anything else with a low enough profile such as a coffee table. \xa0\nYou may have noticed I mentioned the material I used in building my home - plywood. There were two reasons for using plywood instead of the cheaper, stronger glass. First, there was no way of making an angle grinder into a plywood machine. Also, the glue I used would easily melt if exposed to heat.
""")



