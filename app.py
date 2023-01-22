from flask import Flask, request, redirect, render_template, session, flash
from models import dbConnect

app = Flask(__name__)

#ホーム画面（チャンネル一覧画面）の作成
@app.route('/')
def index():
    #セッション情報からuidキーに対応する値を取り出して変数uidに代入
    uid = session.get('uid')
    #uidが空＝セッション情報の中にuid情報が登録されていない＝まだログインしていない場合
    if uid == None:
        #ログイン画面へリダイレクト。
        redirect('/login')

    #uidが空でない＝セッション情報の中にuid情報が登録されている＝ログイン済みの場合
    else:
        #データベースからチャンネル情報を取得して変数channelsへ代入
        channels = dbConnect.getChannelAll()
    #ホーム画面のWEBページを返す。HTMLファイルで使う変数は引数で渡す。
    return render_template('index.html', channels=channels, uid=uid)

if __name__ == '__main__':
    app.run(debug=True)
