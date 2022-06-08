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

# parameters = streamlit_parameters.parameters.Parameters()
# parameters.register_string_list_parameter(key="action", default_value=["new", "edit"])
#
# parameters.set_url_fields()
#action = parameters.action.value[0]


st.header("用户动态主题的可控文本生成原型系统")
st.markdown("#### 主题属性参数管理")
st.button("新建主题素材训练集")
# st.markdown("##### 新建主题素材训练集")


# st.button("下载主题素材训练集")


st.markdown('''<style>

hr {
    margin: 0px;
}
</style>''', unsafe_allow_html=True)

st.markdown("##### 主题属性参数列表")
col1, col2, col3 = st.columns((8,2,16))
col1.text_input("主题过滤")

st.write("---")
# # Show user table
cols_def = (1, 7, 6, 11, 3, 3, 3, 3, 3, 3)
colms = st.columns(cols_def)
fields = ["id", '主题素材训练集编号', '主题', '主题描述', '软嵌入长度', "训练总词数", "预训练模型", "训练完成时间", "操作", ""]
for col, field_name in zip(colms, fields):
    # header
    col.write(field_name)


st.write("---")

user_tables = [
    ["4686b70330d5f6dd68c7f1c93c85dd12", "Glass Fiber Reinforced Gypsum", "关于玻纤维强化石膏板的介绍素材", "5", "4015", "GPT2-Large", "2022-04-19 15:30:15"],
    ["56ddcd1295ea74a33ee4257e0e42ecae", "World", "Ag News Word Topic 1000 samples", "20", "43299", "GPT2-Large", "2022-04-12 9:30:11"],
    ["df0918317c8a4aaea23efb65c0078cce", "World", "Ag News Word Topic 5000 samples", "20", "221032", "GPT2-Large", "2022-04-12 9:22:53"],
    ["cc8c1f34471d33c735bf85e264db17ce", "World", "Ag News Word Topic 100 samples", "20", "4018", "GPT2-Large", "2022-04-12 9:07:10"],
    ["adc971f89904f0087cc47bd34592314a", "World", "Ag News Word Topic", "20", "123781", "GPT2-Large",  "2022-04-11 11:30:15"],
    ["adc971f89904f0087cc47bd34592314a", "World", "Ag News Word Topic", "5", "123781", "GPT2-Large",  "2022-04-11 11:21:21"],
    ["adc971f89904f0087cc47bd34592314a", "World", "Ag News Word Topic", "1", "123781", "GPT2-Large",  "2022-04-11 11:10:03"],
    ["adc971f89904f0087cc47bd34592314a", "World", "Ag News Word Topic", "100", "123781", "GPT2-Large", "2022-04-11 10:30:15"],
    ["adc971f89904f0087cc47bd34592314a", "World", "Ag News Word Topic", "50", "123781", "GPT2-Large", "2022-04-11 10:13:15"],
]

for x, user_table in enumerate(user_tables):
    col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(cols_def)
    col1.write(x)  # index
    col2.write(user_table[0])
    col3.write(user_table[1])
    col4.write(user_table[2])
    col5.write(user_table[3])
    col6.write(user_table[4])
    col7.write(user_table[5])
    col8.write(user_table[6])
    button_phold1 = col9.empty()  # create a placeholder
    edit_action = button_phold1.button("训练集", key=str(x)+"edit")
    button_phold2 = col10.empty()
    test_action = button_phold2.button("测试生成", key=str(x)+"test")
    if test_action:
         pass # do some action with a row's data
         button_phold1.empty()  #  remove button







