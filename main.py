import streamlit as st
import sqlite3
from datetime import date

#DB接続
def get_db_connection():
    conn = sqlite3.connect('data/app.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    return conn, cur

#テーブル作成
def create_tables():
    conn, cur = get_db_connection()

    #日次ログ用テーブル
    cur.execute("""
    CREATE TABLE IF NOT EXISTS daily_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        discharge_log TEXT,
        discharge_talk TEXT,
        charge_log TEXT,
        charge_talk TEXT
    )
    """)

    #週次ログ用テーブル
    cur.execute("""
    CREATE TABLE IF NOT EXISTS weekly_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT,
        start_date TEXT,
        end_date TEXT,
        discharge_notice TEXT,
        charge_notice TEXT
    )
    """)

    conn.commit()
    conn.close()

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

#テーブル作成の実行
create_tables()

####ダミーデータの挿入（DBの実装までの仮）
###daily_logsは今後抽出したものを入れる変数filterd_daily_logsとする
###weekly_logsは週次ログ一覧表示用のダミー（DB連携後置き換え予定）
###############################################
if False:
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

    if 'weekly_logs' not in st.session_state:
        st.session_state.weekly_logs = [
            {
                'created_at': '2024-12-08',
                'start_date': '2024-12-02',
                'end_date': '2024-12-08',
                'discharge_notice': (
                    '今週は仕事の進め方に対する迷いが強く、常に頭の中で'
                    '「このやり方で本当に合っているのか」と考えていた。'
                    '特に成果が見えにくい作業が続いたことで、自己評価が下がり、'
                    '必要以上に疲労感を感じていたことに気づいた。'
                ),
                'charge_notice': (
                    '一方で、夜に散歩をする時間を意識的に取ったことで、'
                    '頭の中が整理される感覚があった。歩きながら考えることで'
                    '仕事と自分を少し切り離して捉えられ、'
                    '気持ちが落ち着く瞬間が増えたのは大きな収穫だった。'
                ),
            },
            {
                'created_at': '2024-12-15',
                'start_date': '2024-12-09',
                'end_date': '2024-12-15',
                'discharge_notice': (
                    '人との比較をしてしまう場面が多く、自分は遅れているのでは'
                    'ないかという不安が強まった一週間だった。'
                    'SNSや周囲の話を聞くたびに焦りが生まれ、'
                    '集中力が散漫になっていたことを振り返って実感した。'
                ),
                'charge_notice': (
                    'ただ、学習した内容を一度ノートに書き出して整理したことで、'
                    '自分なりに理解が進んでいる部分も確かにあると認識できた。'
                    '小さな積み重ねでも、振り返ることで自信につながるのだと感じた。'
                ),
            },
            {
                'created_at': '2024-12-22',
                'start_date': '2024-12-16',
                'end_date': '2024-12-22',
                'discharge_notice': (
                    'やるべきことを詰め込みすぎてしまい、'
                    '結果的にどれも中途半端になってしまった感覚が残った。'
                    '優先順位を決めきれず、気持ちばかりが先行していたことが'
                    '今週の反省点だと思う。'
                ),
                'charge_notice': (
                    'その一方で、週末にあえて何もしない時間を作ったことで、'
                    '久しぶりに「何をしたいか」を落ち着いて考えられた。'
                    '余白を持つことが、次の行動へのエネルギーになると実感した。'
                ),
            },
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

    if st.button('週次ログ一覧表示'):
        st.session_state.page = 'weekly_list'

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

    daily_log = st.session_state.daily_log

    st.write(daily_log['date'])
    st.write(daily_log['discharge_log'])
    st.write(daily_log['discharge_talk'])
    st.write(daily_log['charge_log'])
    st.write(daily_log['charge_talk'])

    if st.button('保存'):
        new_daily_log = {
            'date':daily_log['date'],
            'discharge_log':daily_log['discharge_log'],
            'discharge_talk':daily_log['discharge_talk'],
            'charge_log':daily_log['charge_log'],
            'charge_talk':daily_log['charge_talk']
        }

        conn, cur = get_db_connection()
        cur.execute("""
            INSERT INTO daily_log
                (date, discharge_log, discharge_talk, charge_log, charge_talk)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                new_daily_log['date'],
                new_daily_log['discharge_log'],
                new_daily_log['discharge_talk'],
                new_daily_log['charge_log'],
                new_daily_log['charge_talk']
            )
        )
        conn.commit()
        conn.close()

        st.session_state.daily_log = {}
        st.session_state.page = 'top'

    if st.button('修正する'):
        st.session_state.page = 'daily'

#週次ログ確認画面
def weekly_confirm_page():
    st.title('週次ログ内容確認')

    weekly_log = st.session_state.weekly_log

    st.write(weekly_log['start_date'])
    st.write(weekly_log['end_date'])
    st.write(weekly_log['discharge_notice'])    
    st.write(weekly_log['charge_notice'])

    if st.button('保存'):
        new_weekly_log = {
            'created_at': date.today().isoformat(),
            'start_date': weekly_log['start_date'],
            'end_date': weekly_log['end_date'],
            'discharge_notice': weekly_log['discharge_notice'],
            'charge_notice': weekly_log['charge_notice'],
        }

        conn, cur = get_db_connection()
        cur.execute("""
            INSERT INTO weekly_log
                (created_at, start_date, end_date, discharge_notice, charge_notice)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                new_weekly_log['created_at'],
                new_weekly_log['start_date'],
                new_weekly_log['end_date'],
                new_weekly_log['discharge_notice'],
                new_weekly_log['charge_notice']
            )
        )
        conn.commit()
        conn.close()

        st.session_state.weekly_log = {}
        st.session_state.page = 'top'

    
    if st.button('修正する'):
        st.session_state.page = 'weekly'

#週次ログ一覧表示画面
def weekly_list_page():
    st.title('週次ログ一覧表示')

    conn, cur = get_db_connection()
    cur.execute("SELECT * FROM weekly_log ORDER BY created_at DESC")
    st.session_state.weekly_logs = cur.fetchall()
    conn.close()

    for log in st.session_state.weekly_logs:
        st.markdown(f"**作成日：{log['created_at']}（{log['start_date']} 〜 {log['end_date']}）**")

        col1,col2 = st.columns(2)

        with col1:
            with st.expander(f'放電：{log['discharge_notice'][:30]}...'):
                st.write(log['discharge_notice'][30:])
        with col2:
            with st.expander(f'充電：{log['charge_notice'][:30]}...'):
                st.write(log['charge_notice'][30:])

        st.divider()
        
    if st.button('TOPに戻る'):
        st.session_state.page = 'top'

#画面切り替え処理
if st.session_state.page == 'top':
    top_page()
elif st.session_state.page == 'daily':
    daily_page()
elif st.session_state.page == 'daily_confirm':
    daily_confirm_page()
elif st.session_state.page == 'weekly':
    weekly_page()
elif st.session_state.page == 'weekly_confirm':
    weekly_confirm_page()
elif st.session_state.page == 'weekly_list':
    weekly_list_page()