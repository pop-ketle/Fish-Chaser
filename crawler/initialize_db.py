import os
import sqlite3
import numpy as np
import pandas as pd
from datetime import date

'''
初めにDBを作成した時に色々失敗したので、再構築が必要な場合は再構築を行う
変更事項
    テーブル名: data -> fishery_data に変換
    テーブル名: suion_data
        カラムを変更
'''

DB_NAME = 'data.db'
DATABASE_PATH = '../datasets/'
IDEAL_TABELE_NAMES = ['fishery_data', 'suion_data']


class MyDB():
    def __init__(self, path, filename):
        con = sqlite3.connect(os.path.join(path, filename))
        self.con = con
        self.c = con.cursor()
    
    def get_tablenames(self):
        '''データベース中のテーブル名を取得'''
        sql = 'SELECT name FROM sqlite_master WHERE TYPE="table"'
        return [x[0] for x in self.c.execute(sql)]
        
    def get_columnsname(self, table):
        '''テーブルの中のカラム名を取得'''
        sql = f'SELECT name FROM PRAGMA_TABLE_INFO("{table}")'
        return [x[0] for x in self.c.execute(sql)]

    def typeof_column(self, table):
        '''テーブルのカラムのタイプを取得'''
        sql = f'SELECT typeof(name) FROM PRAGMA_TABLE_INFO("{table}")'
        return [x[0] for x in self.c.execute(sql)]

    def get_all_data(self, table):
        '''テーブルの全データを日付でソートして取得'''
        sql = f'SELECT * FROM "{table}" ORDER BY 日付 asc'
        return [list(x) for x in self.c.execute(sql)]

    def edit_time_columns(self, table):
        '''場所と日付をプライマリーキーにして扱いやすいように、時間を行を分けずにまとめる'''
        sql = f'SELECT 場所 FROM "{table}" GROUP BY 場所'
        places = [x[0] for x in self.c.execute(sql)]

        sql = f'SELECT 日付 FROM "{table}" GROUP BY 日付'
        dates = [x[0] for x in self.c.execute(sql)]
        
        ls = []
        for place in places:
            for date in dates:
                sql = f'''
                    SELECT 時間, 水温 FROM "{table}"
                    WHERE 場所 = "{place}"
                        AND 日付 = "{date}"
                    ORDER BY 日付 asc
                    '''
                data = {x[0]: x[1] for x in self.c.execute(sql)}
                data['場所'] = place.replace('湾', '')
                data['日付'] = date
                ls.append(data)
        _df = pd.DataFrame(ls)
        _df = _df.reindex(columns=['場所','日付','0 時','1 時','2 時','3 時','4 時','5 時','6 時','7 時','8 時','9 時','10 時','11 時','12 時','13 時','14 時','15 時','16 時','17 時','18 時','19 時','20 時','21 時','22 時','23 時','日平均','日最大','日最小'])
        return _df

    def create_table(self):
        '''データベースのテーブルを作成(特にsqlを渡さず決め打ち作成)'''
        # 漁業データテーブル
        sql = """
            CREATE TABLE IF NOT EXISTS fishery_data (
                '場所' text,
                '日付' text,
                '漁業種類' text,
                '隻数' text,
                '魚種' text,
                '規格' text,
                '本数' text,
                '水揚量' text,
                '高値' text,
                '平均値' text,
                '安値' text,
                primary key(場所,日付,漁業種類,魚種)
            )
            """
        self.con.execute(sql)

        # 水温データテーブル
        sql = """
            CREATE TABLE IF NOT EXISTS suion_data (
                '場所' text, '日付' text,
                '0時' text, '1時' text, '2時' text,
                '3時' text, '4時' text, '5時' text,
                '6時' text, '7時' text, '8時' text,
                '9時' text, '10時' text, '11時' text,
                '12時' text, '13時' text, '14時' text,
                '15時' text, '16時' text, '17時' text,
                '18時' text, '19時' text, '20時' text,
                '21時' text, '22時' text, '23時' text,
                '日平均' text, '日最大' text, '日最小' text,
                primary key(場所,日付)
            )
            """
        self.con.execute(sql)

        self.con.commit()

    def df2db(self, df, table):
        '''pd.DataFrameをsqliteのDBに保存'''
        df.to_sql(table, self.con, if_exists='replace')

    def close(self):
        self.c.close()


def main():
    db = MyDB(DATABASE_PATH, DB_NAME)

    # データベース中のテーブル名を取得、期待通りのものかチェック
    # 期待通りでない場合、再構築フラグを立てる
    print('# Checking table name...')
    tables = db.get_tablenames()
    if set(tables)==set(IDEAL_TABELE_NAMES):
        # DBの再構築処理が必要ない場合は、ここで処理終了
        print('########## No need to rebuild the DB! ##########')
        return

    # DBの再構築処理
    print('########## Started to rebuild the DB... ##########')
    # 再構築する新しく作られるDBのオブジェクト
    new_db = MyDB(DATABASE_PATH, 'new_data.db')
    new_db.create_table()

    # NOTE: pandasに入れて処理するのが一番手っ取り早いかな... 要検討
    for table in tables:
        columns = db.get_columnsname(table)

        # テーブル名で処理を分ける
        if table=='data':
            data_df = pd.DataFrame(db.get_all_data(table), columns=columns)
            for c in ['隻数', '本数', '水揚量', '高値', '平均値', '安値']:
                data_df[c] = data_df[c].apply(lambda x: str(x).replace(',', '')) # ',' を取り除く

        if table=='suion_data':
            # 場所と日付をプライマリーキーにして扱いやすいように、時間を行を分けずにまとめる
            data_df = db.edit_time_columns(table)
            data_df['場所'] = data_df['場所'].apply(lambda x: str(x).replace('湾', '')) # '湾' を取り除く
            data_df = data_df.rename(columns=lambda x: str(x).replace(' ', '')) # カラム名から ' ' (半角スペース)を取り除く


        if table=='data': table = 'fishery_data' # NOTE: あまりスマートなコードではないけど面倒なので

        # pd.DataFrameをsqliteのDBに保存
        new_db.df2db(data_df, table)
        # pd.DataFrameを.csvで保存
        data_df.to_csv(os.path.join(DATABASE_PATH, f'{table}.csv'), index=False)

    # クローズ処理
    db.close()
    new_db.close()

    # ファイル名を変換する 古いものをdata{その日の日付}.db 新しいものをdata.dbとする
    os.rename(os.path.join(DATABASE_PATH, 'data.db'), os.path.join(DATABASE_PATH, f'data{date.today()}.db'))
    os.rename(os.path.join(DATABASE_PATH, 'new_data.db'), os.path.join(DATABASE_PATH, 'data.db'))
    print('########## Finished to rebuild the DB! ##########')


if __name__ == "__main__":
    main()