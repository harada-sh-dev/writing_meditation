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
        date TEXT,
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
        'date':None,
        'start_date':None,
        'end_date':None,
        'discharge_notice':'',
        'charge_notice':''
    }

if "delete_expander_open" not in st.session_state:
    st.session_state.delete_expander_open = False

#テーブル作成の実行
create_tables()

#ページ遷移のみ（１クリックで遷移させるため）
def set_page(page_name):
    st.session_state.page = page_name
def page_button(label, page_name):
    st.button(label, on_click=set_page, args=(page_name,))

#TOP画面
def top_page():
    st.title('書く瞑想 ~Writing Meditation')
    st.markdown("""
    日々の思考や感情を書き出し、  
    **週単位で振り返ること**を目的とした記録ツールです。
    """)

    st.markdown("---")

    st.markdown("""
    ### このアプリでできること
    - 日々の感情や思考を「書いて整理」する  
    - １週間分をまとめて振り返る  
    - 自分の思考や感情の癖に気づく
    """)

    st.markdown("まずは今日の記録から始めてみましょう。")

    def change_page(page_name):
        st.session_state.page = page_name

    page_button('📝 日次ログを書く', 'daily')
    page_button('📅 週次ログを書く', 'weekly')
    page_button('🔍 週次ログを見返す', 'weekly_list')
    st.markdown("---")
    page_button('日次ログの修正・削除', 'daily_edit')
    page_button('週次ログの修正・削除', 'weekly_edit')

#日次ログ入力画面
def daily_page():
    st.title('📝 日次ログを書く')

    daily_log = st.session_state.daily_log

    selected_date = st.date_input('作成日',value=daily_log['date'] if daily_log['date'] else None)

    discharge_log = st.text_area(
         '放電ログ：1日の中で、あなたの感情、気分、エネルギーを【下げたもの】を単語で記入',
        value=daily_log['discharge_log'],
        height=68
        )
    discharge_talk = st.text_area(
        '放電セルフトーク：１つの感情から初めて、芋づる式に書き綴る。文章形式。独り言のように書く。',
        value=daily_log['discharge_talk'],
        height=136
        )
    charge_log = st.text_area(
        '充電ログ：1日の中で、あなたの感情、気分、エネルギーを【上げたもの】を単語で記入',
        value=daily_log['charge_log'],
        height=68
        )
    charge_talk = st.text_area(
        '充電セルフトーク：１つの感情から初めて、芋づる式に書き綴る。文章形式。独り言のように書く。',
        value=daily_log['charge_talk'],
        height=136
        )

    def go_daily_confirm():
        st.session_state.daily_log = {
            'date': selected_date,
            'discharge_log': discharge_log,
            'discharge_talk': discharge_talk,
            'charge_log': charge_log,
            'charge_talk': charge_talk
        }
        st.session_state.page = 'daily_confirm'
    st.button('確認へ進む', on_click=go_daily_confirm)

    page_button('TOPに戻る', 'top')

#週次ログ入力画面
def weekly_page():
    st.title('📅 週次ログを書く')

    daily_logs = []
    weekly_log = st.session_state.weekly_log
    selected_date = st.date_input('作成日',value=weekly_log['date'] if weekly_log['date'] else None)
    start_date = st.date_input('抽出開始日',value=weekly_log['start_date'])
    end_date = st.date_input('抽出終了日',value=weekly_log['end_date'])

    if not start_date or not end_date:
        st.info("抽出期間を選択してください")
    else:
        conn, cur = get_db_connection()
        cur.execute(
            """
            SELECT date, discharge_talk, charge_talk
            FROM daily_log
            WHERE date BETWEEN ? AND ?
            ORDER BY date
            """,
            (start_date.isoformat(), end_date.isoformat())
        )
        daily_logs = cur.fetchall()
        conn.close()

    st.markdown('＜対象期間の放電セルフトーク＞')
    for log in daily_logs:
        st.write(f"{log['date']}：{log['discharge_talk']}")
    discharge_notice = st.text_area(
        '放電の気づき：対象期間の放電セルフトークを読んだ感想を記録',
        value=weekly_log['discharge_notice']
        )
    st.markdown("---")    
    st.markdown('＜対象期間の充電セルフトーク＞')
    for log in daily_logs:
        st.write(f"{log['date']}：{log['charge_talk']}")
    charge_notice = st.text_area(
        '充電の気づき：対象期間の充電セルフトークを読んだ感想を記録',
        value=weekly_log['charge_notice']
        )
    
    st.markdown("---")    

    def go_weekly_confirm():
        st.session_state.weekly_log = {
            'date': selected_date,
            'start_date': start_date,
            'end_date': end_date,
            'discharge_notice': discharge_notice,
            'charge_notice': charge_notice
        }
        st.session_state.page = 'weekly_confirm'
    st.button('確認へ進む', on_click=go_weekly_confirm)

    page_button('TOPに戻る', 'top')

#日次ログ確認画面
def daily_confirm_page():
    st.title('日次ログ内容確認')

    daily_log = st.session_state.daily_log

    st.write(daily_log['date'])
    st.write(daily_log['discharge_log'])
    st.write(daily_log['discharge_talk'])
    st.write(daily_log['charge_log'])
    st.write(daily_log['charge_talk'])

    def save_daily_log():
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

        st.session_state.daily_log = {
            'date': None,
            'discharge_log': '',
            'discharge_talk': '',
            'charge_log': '',
            'charge_talk': ''
            }
        st.session_state.page = 'top'
    st.button('保存', on_click=save_daily_log)

    page_button('修正する', 'daily')

#週次ログ確認画面
def weekly_confirm_page():
    st.title('週次ログ内容確認')

    weekly_log = st.session_state.weekly_log

    st.write(weekly_log['date'])
    st.write(weekly_log['start_date'])
    st.write(weekly_log['end_date'])
    st.write(weekly_log['discharge_notice'])    
    st.write(weekly_log['charge_notice'])

    def save_weekly_log():
        new_weekly_log = {
            'date': weekly_log['date'],
            'start_date': weekly_log['start_date'],
            'end_date': weekly_log['end_date'],
            'discharge_notice': weekly_log['discharge_notice'],
            'charge_notice': weekly_log['charge_notice'],
        }

        conn, cur = get_db_connection()
        cur.execute("""
            INSERT INTO weekly_log
                (date, start_date, end_date, discharge_notice, charge_notice)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                new_weekly_log['date'],
                new_weekly_log['start_date'].isoformat(),
                new_weekly_log['end_date'].isoformat(),
                new_weekly_log['discharge_notice'],
                new_weekly_log['charge_notice']
            )
        )
        conn.commit()
        conn.close()

        st.session_state.weekly_log = {
            'date': None,
            'start_date': None,
            'end_date': None,
            'discharge_notice': '',
            'charge_notice': ''
            }
        st.session_state.page = 'top'
    st.button('保存', on_click=save_weekly_log)
    
    page_button('修正する', 'weekly')

#週次ログ一覧表示画面
def weekly_list_page():
    st.title('🔍 週次ログを見返す')

    conn, cur = get_db_connection()
    cur.execute("SELECT * FROM weekly_log ORDER BY date DESC")
    st.session_state.weekly_logs = cur.fetchall()
    conn.close()

    for log in st.session_state.weekly_logs:
        st.markdown(f"**作成日：{log['date']}（{log['start_date']} 〜 {log['end_date']}）**")

        col1,col2 = st.columns(2)

        with col1:
            st.markdown('放電の気づき')
            with st.expander(log['discharge_notice'][:15]+'...'):
                st.write(log['discharge_notice'])
        with col2:
            st.markdown('充電の気づき')
            with st.expander(log['charge_notice'][:15]+'...'):
                st.write(log['charge_notice'])

        st.divider()
        
    page_button('TOPに戻る', 'top')

#日次ログ修正・削除画面
def daily_edit_page():
    st.title('日次ログ修正・削除')

    conn, cur = get_db_connection()
    cur.execute("SELECT * FROM daily_log ORDER BY date DESC")
    st.session_state.daily_logs = cur.fetchall()
    conn.close()

    dates = [log['date'] for log in st.session_state.daily_logs]
    selected_date = st.selectbox(
        '修正する日付を選択し文章を修正する、もしくは削除を行なってください',
        dates,
        key='daily_edit_date'
        )

    same_date_logs = [
        dict(log) for log in st.session_state.daily_logs
        if log['date'] == selected_date
    ]

    if not same_date_logs:
        st.warning("該当するログが見つかりません")
        page_button('TOPに戻る', 'top')
        return

    if len(same_date_logs) == 1:
        selected_log = same_date_logs[0]

    else:
        st.warning('同日のログが複数あります')
        selected_log = st.radio(
            '修正または削除するログを選んでください',
            same_date_logs,
            format_func = lambda log : f"ID:{log['id']} 放電:{log['discharge_log'][:30]}..."
        )

    st.markdown(f"**作成日:{selected_log['date']}**")
    discharge_log = st.text_area('放電ログ',value=selected_log['discharge_log'])
    discharge_talk = st.text_area('放電セルフトーク',value=selected_log['discharge_talk'])
    charge_log = st.text_area('充電ログ',value=selected_log['charge_log'])
    charge_talk = st.text_area('充電セルフトーク',value=selected_log['charge_talk'])
    
    if st.button('上記の内容で上書きする'):
        conn, cur = get_db_connection()
        cur.execute(
            """
            UPDATE daily_log
            SET
                discharge_log = ?,
                discharge_talk = ?,
                charge_log = ?,
                charge_talk = ?
            WHERE id = ?
            """,
            (
                discharge_log,
                discharge_talk,
                charge_log,
                charge_talk,
                selected_log['id']
            )
        )
        conn.commit()
        conn.close()
        st.success('修正しました')
    
    with st.expander('削除（元には戻せません）',expanded = st.session_state.delete_expander_open):
        if st.button('本当に削除する'):
            conn, cur = get_db_connection()
            cur.execute(
                "DELETE FROM daily_log WHERE id = ?",
                (selected_log['id'],)
            )
            conn.commit()
            conn.close()
            st.success('削除しました')
            st.session_state.delete_expander_open = False
            st.rerun()
    
    page_button('TOPに戻る', 'top')

#週次ログ修正・削除画面
def weekly_edit_page():
    st.title('週次ログ修正・削除')

    conn, cur = get_db_connection()
    cur.execute("SELECT * FROM weekly_log ORDER BY date DESC")
    st.session_state.weekly_logs = cur.fetchall()
    conn.close()

    dates = [log['date'] for log in st.session_state.weekly_logs]
    selected_date = st.selectbox(
        '修正する日付を選択し文章を修正する、もしくは削除を行なってください',
        dates,
        key='weekly_edit_date'
        )

    same_date_logs = [
        dict(log) for log in st.session_state.weekly_logs
        if log['date'] == selected_date
    ]

    if not same_date_logs:
        st.warning("該当するログが見つかりません")
        page_button('TOPに戻る', 'top')
        return

    if len(same_date_logs) == 1:
        selected_log = same_date_logs[0]

    else:
        st.warning('同日のログが複数あります')
        selected_log = st.radio(
            '修正または削除するログを選んでください',
            same_date_logs,
            format_func = lambda log : f"ID:{log['id']} 放電の気づき:{log['discharge_notice'][:30]}..."
        )

    st.markdown(f"**作成日：{selected_log['date']}（{selected_log['start_date']} 〜 {selected_log['end_date']}）**")
    discharge_notice = st.text_area('放電の気づき',value=selected_log['discharge_notice'])
    charge_notice = st.text_area('充電の気づき',value=selected_log['charge_notice'])
    
    if st.button('上記の内容で上書きする'):
        conn, cur = get_db_connection()
        cur.execute(
            """
            UPDATE weekly_log
            SET
                discharge_notice = ?,
                charge_notice = ?
            WHERE id = ?
            """,
            (
                discharge_notice,
                charge_notice,
                selected_log['id']
            )
        )
        conn.commit()
        conn.close()
        st.success('修正しました')
    
    with st.expander('削除（元には戻せません）',expanded = st.session_state.delete_expander_open):
        if st.button('本当に削除する'):
            conn, cur = get_db_connection()
            cur.execute(
                "DELETE FROM weekly_log WHERE id = ?",
                (selected_log['id'],)
            )
            conn.commit()
            conn.close()
            st.success('削除しました')
            st.session_state.delete_expander_open = False
            st.rerun()
    
    page_button('TOPに戻る', 'top')

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
elif st.session_state.page == 'daily_edit':
    daily_edit_page()
elif st.session_state.page == 'weekly_edit':
    weekly_edit_page()