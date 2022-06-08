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

st.markdown('''<style>

hr {
    margin: 0px;
}
</style>''', unsafe_allow_html=True)

st.header("用户动态主题的可控文本生成原型系统")
st.markdown("#### 主题属性参数训练")
st.write("---")
st.text("主题素材训练集: " + "4686b70330d5f6dd68c7f1c93c85dd12")
st.text("主题名称: " + "Glass Fiber Reinforced Gypsum")
st.text("主题描述: " + "关于玻纤维强化石膏板的介绍素材")
st.text("总训练词数: " + "803")
st.write("---")

st.text("主题属性控制参数配置")
st.slider("软嵌入词长", min_value=5, max_value=20, value=5)
st.slider("训练轮次", min_value=1, max_value=10, value=5)
plm = st.selectbox("选择基础预训练模型", ["GPT2-Large", "GPT2-XL"])
st.button("训练")

st.progress(value=100)

st.text("训练耗时:" + "38.172秒")

st.button("测试生成")





