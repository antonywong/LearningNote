# -*- coding: utf-8 -*-
import schedule
import time
import streamlit as st
import option
from option import option_info


left_column, right_column = st.sidebar.columns(2)
option_info_sync = left_column.button('option_info_sync')
option_info_sync_msg = ""
if option_info_sync:
    option_info.sync()
    option_info_sync_msg = "option_info_sync!"
right_column.write(option_info_sync_msg)


options = {1:"所有数据", 2:"分析数据"}
selected_option = st.sidebar.selectbox('Select an option', options=options.keys(), format_func=lambda x: options[x])
st.sidebar.write('You selected: ', selected_option)


resultText = ""
def analyze():
    global resultText
    df = option_info.collect()
    resultText = option_info.analyze(df)

    print(time.strftime('%Y-%m-%d %H:%M:%S'))

schedule.every(30).seconds.do(analyze)

analyze()
st.write(resultText)

# # run the scheduled job in a loop
# while True:
#     schedule.run_pending()
#     time.sleep(1)