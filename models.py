import pymysql
from util.DB import DB 

#チャンネル一覧取得機能
def getChannelAll():
    try:
        #MySQLに接続(DBクラスで定義した接続用メソッドを使用)
        conn = DB.getConnection()
        #カーソルを作成し、変数curへ代入
        cur = conn.cursor()
        #カーソルに対してchannelsテーブルの全カラムの値を取得するSQL文を実行
        sql = 'SELECT * FROM channels;'
        cur.execute(sql)
        #実行結果を全て取り出し変数channelsに入れて返す
        channels = cur.fetchall()
        return channels

    #例外処理　
    except Exception as e:
        print(e + 'が発生しています')
        return None
    
    #最終処理　カーソルを閉じる
    finally:
        cur.close()
