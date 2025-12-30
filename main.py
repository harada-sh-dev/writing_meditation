import streamlit as st

#初期状態の定義
if 'page' not in st.session_state:
    st.session_state.page = 'top'

#TOP画面
def top_page():
    st.title('Writing Meditation')
    st.write('「書く瞑想」（Writing Meditation）は、毎日の思考を整理するために行われます')

    if st.button('日次入力'):
        st.session_state.page = 'daily'

    if st.button('週次入力'):
        st.write('※　週次入力画面は今後実装予定です')

#日次ログ入力画面
def daily_page():
    st.title('日次ログ入力')

    date = st.date_input('日付')

    st.write('「放電ログ」')
    st.write('・1日の中で、あなたの感情、気分、エネルギーを【下げたもの】を単語で記入')
    discharge_log = st.text_area('放電ログ')
    st.write('「放電セルフトーク」')
    st.write('・１つの感情から初めて、芋づる式に書き綴る。文章形式。独り言のように書く。')
    discharge_talk = st.text_area('放電セルフトーク')

    st.write('「充電ログ」')
    st.write('・1日の中で、あなたの感情、気分、エネルギーを【上げたもの】を単語で記入')
    charge_log = st.text_area('充電ログ')
    st.write('「充電セルフトーク」')
    st.write('・１つの感情から初めて、芋づる式に書き綴る。文章形式。独り言のように書く。')
    charge_talk = st.text_area('充電セルフトーク')

    if st.button('保存（仮）'):
        st.write('※ 保存処理は今後実装予定です')

    if st.button('TOPに戻る'):
        st.session_state.page = 'top'

#画面切り替え処理
if st.session_state.page == 'top':
    top_page()
elif st.session_state.page == 'daily':
    daily_page()