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
    def addChannel(uid, newChannelName, newChannelDescription): #! uidを追加
        """
        MySQLにDBクラスで定義した接続用メソッドを使用して接続
        カーソルを作成→curへ代入
        sqlにSQL文を代入
        execute文でsqlを実行(channelテーブルにユーザーID,チャンネル名,チャンネル概要を追加)
        commitで変更を確定
        * commitとは - トランザクションの結果を確定する(変更を確定する)
        """

        try:
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

    # チャンネル削除
    def deleteChannel(cid):
        """
        MySQLにDBクラスで定義した接続用メソッドを使用して接続
        カーソルを作成→curへ代入
        channelsテーブルから該当するcidのチャンネルデータを削除するSQL文→sqlへ代入
        execute文にsqlと削除するチャンネルのcidを渡して実行
        commitで変更を確定
        """

        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "DELETE FROM channels WHERE id=%s;"
            cur.execute(sql, (cid))
            conn.commit()

        # 例外処理
        except Exception as e:
            print(e + 'が発生しています')
            return None

        # 最終処理：カーソルを閉じる
        finally:
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

        # 最終処理：カーソルを閉じる
        finally:
            cur.close()

    # メッセージ全取得(チャンネルID)
    def getMessageAll(cid):
        """
        MySQLにDBクラスで定義した接続用メソッドを使用して接続
        カーソルを作成→curへ代入
        sqlにSQL文を代入:「uid列を軸としてmessagesテーブルとusersテーブルを結合させる。
        その上で、該当するcidの行から(メッセージID、ユーザーID、ユーザー名、メッセージ)を取得する」
        * 内部結合の構文(
            SELECT <カラム名>
            FROM <結合元テーブル名> AS 略称
            INNER JOIN <結合先テーブル名> AS 略称
            ON <結合元テーブルのカラム名> = <結合先テーブルのカラム名>
            WHERE 条件;
            )
        cidを指定してexecute文でsqlを実行
        取得したデータを全て取り出す→messagesに代入
        messagesを返す
        """
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT m.id, u.uid, u.user_name, m.message FROM messages AS m INNER JOIN users AS u ON m.uid = u.uid WHERE cid = %s;"
            cur.execute(sql, (cid))
            messages = cur.fetchall()
            return messages

        # 例外処理
        except Exception as e:
            print(e + 'が発生しています')
            return None

        # 最終処理：カーソルを閉じる
        finally:
            cur.close()

    # メッセージ削除(メッセージID)
    def deleteMessage(message_id):
        """
        DBクラスに定義した接続用メソッドを使用してDBに接続→connへ代入
        カーソルを作成→curへ代入
        sqlにSQL文を代入
        execute関数でsql文を実行(messagesテーブルからメッセージのidが一致するデータを削除)
        commitで変更を確定
        """

        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = 'DELETE FROM messages WHERE id=%s'
            cur.execute(sql, (message_id))
            conn.commit()

        # 例外処理
        except Exception as e:
            print(e + '発生しています')
            return None

        # 最終処理:カーソルを閉じる
        finally:
            cur.close()
