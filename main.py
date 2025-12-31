import streamlit as st

#初期状態の定義
if 'page' not in st.session_state:
    st.session_state.page = 'top'

if 'daily_log' not in st.session_state:
    st.session_state.daily_log = {
            'date':None,
            'discharge_log':'',
            'discharge_talk':'',
            'charge_log':'',
            'charge_talk':''
        }

if 'weekly_log' not in st.session_state:
    st.session_state.weekly_log = {
        'start_date':None,
        'end_date':None,
        'discharge_notice':'',
        'charge_notice':''
    }

####ダミーデータの挿入
###daily_logsは今後抽出したものを入れる変数filterd_daily_logsとする
###############################################
if 'daily_logs' not in st.session_state:
    st.session_state.daily_logs = [
        {
            'date': '2024-12-01',
            'discharge_talk': '仕事で思うように進まず落ち込んだ',
            'charge_talk': '帰宅後にゆっくりできて少し回復した'
        },
        {
            'date': '2024-12-02',
            'discharge_talk': '時間が足りず焦った',
            'charge_talk': '優先順位を整理できた'
        }
    ]
###################################################

#TOP画面
def top_page():
    st.title('Writing Meditation')
    st.write('「書く瞑想」（Writing Meditation）は、毎日の思考を整理するために行われます')

    if st.button('日次入力'):
        st.session_state.page = 'daily'

    if st.button('週次入力'):
        st.session_state.page = 'weekly'

#日次ログ入力画面
def daily_page():
    st.title('日次ログ入力')

    daily_log = st.session_state.daily_log

    date = st.date_input('日付',value=daily_log['date'] if daily_log['date'] else None)

    st.write('「放電ログ」')
    st.write('・1日の中で、あなたの感情、気分、エネルギーを【下げたもの】を単語で記入')
    discharge_log = st.text_area('放電ログ',value=daily_log['discharge_log'])
    st.write('「放電セルフトーク」')
    st.write('・１つの感情から初めて、芋づる式に書き綴る。文章形式。独り言のように書く。')
    discharge_talk = st.text_area('放電セルフトーク',value=daily_log['discharge_talk'])

    st.write('「充電ログ」')
    st.write('・1日の中で、あなたの感情、気分、エネルギーを【上げたもの】を単語で記入')
    charge_log = st.text_area('充電ログ',value=daily_log['charge_log'])
    st.write('「充電セルフトーク」')
    st.write('・１つの感情から初めて、芋づる式に書き綴る。文章形式。独り言のように書く。')
    charge_talk = st.text_area('充電セルフトーク',value=daily_log['charge_talk'])

    if st.button('確認へ進む'):
        st.session_state.daily_log = {
            'date':date,
            'discharge_log':discharge_log,
            'discharge_talk':discharge_talk,
            'charge_log':charge_log,
            'charge_talk':charge_talk
        }
        st.session_state.page = 'daily_confirm'

    if st.button('TOPに戻る'):
        st.session_state.page = 'top'

#週次ログ入力画面
def weekly_page():
    st.title('週次ログ入力')

    weekly_log = st.session_state.weekly_log

    start_date = st.date_input('抽出開始日',value=weekly_log['start_date'])
    end_date = st.date_input('抽出終了日',value=weekly_log['end_date'])


    st.subheader('放電セルフトーク（対象期間）')
    for log in st.session_state.daily_logs:
        st.write(f"{log['date']}：{log['discharge_talk']}")

    st.subheader('充電セルフトーク（対象期間）')
    for log in st.session_state.daily_logs:
        st.write(f"{log['date']}：{log['charge_talk']}")

    st.write('放電の気づき')
    discharge_notice = st.text_area('放電の気づき',value=weekly_log['discharge_notice'])
    st.write('充電の気づき')
    charge_notice = st.text_area('充電の気づき',value=weekly_log['charge_notice'])

    if st.button('確認へ進む'):
        st.session_state.weekly_log = {
            'start_date':start_date,
            'end_date':end_date,
            'discharge_notice':discharge_notice,
            'charge_notice':charge_notice
        }
        st.session_state.page = 'weekly_confirm'

    if st.button('TOPに戻る'):
        st.session_state.page = 'top'

#日次ログ確認画面
def daily_confirm_page():
    st.title('日次ログ内容確認')

    log = st.session_state.daily_log

    st.write(log['date'])
    st.write(log['discharge_log'])
    st.write(log['discharge_talk'])
    st.write(log['charge_log'])
    st.write(log['charge_talk'])

    if st.button('保存（仮）'):
        st.write('※ 保存処理は今後実装予定です')

    if st.button('修正する'):
        st.session_state.page = 'daily'

#画面切り替え処理
if st.session_state.page == 'top':
    top_page()
elif st.session_state.page == 'daily':
    daily_page()
elif st.session_state.page == 'daily_confirm':
    daily_confirm_page()
elif st.session_state.page == 'weekly':
    weekly_page()