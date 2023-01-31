import pymysql
from util.DB import DB

class dbConnect:
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

        #最終処理 カーソルを閉じる
        finally:
            cur.close()

    # チャンネル名取得
    def getChannelByName(channel_name):
        """
        MySQLにDBクラスで定義した接続用メソッドを使用して接続
        カーソルを作成→curへ代入
        * カーソルとは - 検索結果からデータを１件ずつ取得する仕組みまたその目印のこと
        channelsテーブルから該当のテーブル名を取得する処理そのもの→sqlへ代入
        channelsテーブルから引数で渡ってきたchannel_nameという値を検索し、抜き取る
        * executeとは - SQL文を渡すと実行してくれる関数
        fetchoneでchannel名が一致する1行のみデータを取得→channelに代入
        channelを返す
        """

        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = 'SELECT * FROM channels WHERE name=%s;'
            cur.execute(sql, (channel_name))
            channel = cur.fetchone()
            return channel

        # 例外処理
        except Exception as e:
            print(e + 'が発生しています')
            return None

        # 最終処理:カーソルを閉じる
        finally:
            cur.close()

    # チャンネル追加(ユーザーID, チャンネル名, チャンネル概要)
    def addChannel(newChannelName, newChannelDescription): #! uidを追加
        """
        MySQLにDBクラスで定義した接続用メソッドを使用して接続
        カーソルを作成→curへ代入
        sqlにSQL文を代入
        execute文でsqlを実行(channelテーブルにユーザーID,チャンネル名,チャンネル概要を追加)
        commitで変更を確定
        * commitとは - トランザクションの結果を確定する(変更を確定する)
        """

        try:
            #! 仮uid
            uid = '970af84c-dd40-47ff-af23-282b72b7cca8'
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = 'INSERT INTO channels (uid, name, abstract) VALUES (%s, %s, %s);'
            cur.execute(sql, (uid, newChannelName, newChannelDescription))
            conn.commit()

        # 例外処理
        except Exception as e:
            print(e + 'が発生しています')
            return None

        # 最終処理:カーソルを閉じる
        finally:
            cur.close()

    # 引数で渡したチャンネルIDに該当するチャンネルを取得
    def getChannelById(cid):
        """
        MySQLにDBクラスで定義した接続用メソッドを使用して接続
        カーソルを作成→curへ代入
        channelsテーブルから該当のcidのチャンネルを取得するSQL文→sqlへ代入
        channelsテーブルから引数で渡ってきたcidの値を検索し、抜き取る
        fetchoneでcidが一致する1行のみデータを取得→channelに代入
        channelを返す
        """

        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM channels WHERE id=%s;"
            cur.execute(sql, (cid))
            channel = cur.fetchone()
            return channel

        # 例外処理
        except Exception as e:
            print(e + 'が発生しています')
            return None

        # 最終処理:カーソルを閉じる
        finally:
            cur.close()

    # チャンネル更新(ユーザーID, チャンネル名, チャンネル概要)
    def updateChannel(uid, newChannelName, newChannelDescription, cid):
        """
        MySQLにDBクラスで定義した接続用メソッドを使用して接続
        カーソルを作成→curへ代入
        channelsテーブルで該当するcidの（ユーザーID,チャンネル名,チャンネル概要）を更新するSQL文→sqlへ代入
        execute文にsqlと更新する値の入った各変数を渡して実行
        commitで変更を確定
        カーソルを閉じる
        """

        conn = DB.getConnection()
        cur = conn.cursor()
        sql = "UPDATE channels SET uid=%s, name=%s, abstract=%s WHERE id=%s;"
        cur.execute(sql, (uid, newChannelName, newChannelDescription, cid))
        conn.commit()
        cur.close()

    # メッセージ作成(ユーザーID, チャンネルID, メッセージ)
    def createMessage(uid, cid, message):
        """
        MySQLにDBクラスで定義した接続用メソッドを使用して接続
        カーソルを作成→curへ代入
        sqlにSQL文を代入
        * 「INSERT INTO テーブル名(列名1,列名2,...)VALUES(値1,値2,...);」
        execute文でsqlを実行(messagesテーブル(ユーザーID, チャンネルID, メッセージ)列にそれぞれ登録)
        commitで変更を確定
        """

        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = 'INSERT INTO messages(uid, cid, message) VALUES(%s, %s, %s)'
            cur.execute(sql, (uid, cid, message))
            conn.commit()

        # 例外処理
        except Exception as e:
            print(e + 'が発生しています')
            return None

        # 最終処理:カーソルを閉じる
        finally:
            cur.close()
