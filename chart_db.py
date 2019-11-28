import sqlite3
from contextlib import closing
import textwrap


def chart_db_insert(dbfile, insert_value):

    with closing(sqlite3.connect(dbfile)) as conn:
        c = conn.cursor()

        # OPENTIMEを条件に登録済か確認
        select_sql = 'select count(*) from CHART where OPENTIME=?'
        c.execute(select_sql, (insert_value[0],))
        result = c.fetchall()

        # 登録済の場合、削除処理
        if result[0][0] != 0:
            delete_sql = 'delete from CHART where OPENTIME=?'
            c.execute(delete_sql, (insert_value[0],))

        # SQL文に値をセットする場合は，Pythonのformatメソッドなどは使わずに，
        # セットしたい場所に?を記述し，executeメソッドの第2引数に?に当てはめる値を
        # タプルで渡す．
        sql = textwrap.dedent('''\
            insert into CHART (
            OPENTIME,CLOSETIME,OPEN,HIGH,LOW,CLOSE,VOLUME,BASEVOLUME,
            OPEN_JPY,HIGH_JPY,LOW_JPY,CLOSE_JPY,
            OPEN_USD,HIGH_USD,LOW_USD,CLOSE_USD )
            values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ''')
        c.execute(sql, insert_value)
        conn.commit()

        return 1


def chart_db_select(dbfile):

    with closing(sqlite3.connect(dbfile)) as conn:
        conn.row_factory = dict_factory
        c = conn.cursor()
        # chart.dbの中身を素直にselect
        select_sql = textwrap.dedent('''\
            select
            OPENTIME,CLOSETIME,OPEN,HIGH,LOW,CLOSE,VOLUME,BASEVOLUME,
            OPEN_JPY,HIGH_JPY,LOW_JPY,CLOSE_JPY,
            OPEN_USD,HIGH_USD,LOW_USD,CLOSE_USD from CHART
            order by OPENTIME desc
        ''')
        c.execute(select_sql)
        result = c.fetchall()

        # dictを返却
        return result


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
