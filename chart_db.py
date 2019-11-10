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


def numbers_trainingdata_select(dbfile, keta):

    with closing(sqlite3.connect(dbfile)) as conn:
        c = conn.cursor()

        # ランダムフォレストの学習用にリハ後と抽せん後の角度ペアを取得
        if keta == '1':
            select_sql = 'select N3_H_PRESET as t, N3_H_AFTERDEGREE as a '
        elif keta == '2':
            # select_sql = 'select N3_J_PRESET as t, N3_J_AFTERDEGREE as a '
            select_sql = 'select N3_J_TESTSHOT as t, N3_J_AFTERDEGREE as a '
        elif keta == '3':
            select_sql = 'select N3_I_PRESET as t, N3_I_AFTERDEGREE as a '
        elif keta == '4':
            # select_sql = 'select N4_S_PRESET as t, N4_S_AFTERDEGREE as a '
            select_sql = 'select N4_S_TESTSHOT as t, N4_S_AFTERDEGREE as a '
        elif keta == '5':
            # select_sql = 'select N4_H_PRESET as t, N4_H_AFTERDEGREE as a '
            select_sql = 'select N4_H_TESTSHOT as t, N4_H_AFTERDEGREE as a '
        elif keta == '6':
            # select_sql = 'select N4_J_PRESET as t, N4_J_AFTERDEGREE as a '
            select_sql = 'select N4_J_TESTSHOT as t, N4_J_AFTERDEGREE as a '
        elif keta == '7':
            # select_sql = 'select N4_I_PRESET as t, N4_I_AFTERDEGREE as a '
            select_sql = 'select N4_I_TESTSHOT as t, N4_I_AFTERDEGREE as a '
        elif keta == 'p1':
            select_sql = 'select N3_H_TESTSHOT as t, N3_H_PRESET as a '
        elif keta == 'p2':
            select_sql = 'select N3_J_TESTSHOT as t, N3_J_PRESET as a '
        elif keta == 'p3':
            select_sql = 'select N3_I_TESTSHOT as t, N3_I_PRESET as a '
        elif keta == 'p4':
            select_sql = 'select N4_S_TESTSHOT as t, N4_S_PRESET as a '
        elif keta == 'p5':
            select_sql = 'select N4_H_TESTSHOT as t, N4_H_PRESET as a '
        elif keta == 'p6':
            select_sql = 'select N4_J_TESTSHOT as t, N4_J_PRESET as a '
        elif keta == 'p7':
            select_sql = 'select N4_I_TESTSHOT as t, N4_I_PRESET as a '
        select_sql += 'from N_RESULT where KAI >= 5235 order by KAI asc'
        c.execute(select_sql)
        result = c.fetchall()

        return result
