from flask import Flask, request, redirect, render_template, session, flash
from models import dbConnect

app = Flask(__name__)

#ホーム画面（チャンネル一覧画面）の作成
@app.route('/')
def index():
    # セッション情報からuidキーに対応する値を取り出して変数uidに代入
    uid = session.get('uid')
    #uidが空＝セッション情報の中にuid情報が登録されていない＝まだログインしていない場合
    if uid is None:
        #ログイン画面へリダイレクト。
        return redirect('/login')

    #uidが空でない＝セッション情報の中にuid情報が登録されている＝ログイン済みの場合
    else:
        #データベースからチャンネル情報を取得して変数channelsへ代入
        channels = dbConnect.getChannelAll()
    #ホーム画面のWEBページを返す。HTMLファイルで使う変数は引数で渡す。
    return render_template('index.html', uid=uid, channels=channels)

@app.route('/', methods=['POST'])
def add_channel():
    """ ユーザーID

    ユーザーIDをセッションから取得してuidに代入
    ユーザーIDが無ければログインページへリダイレクト
    """
    #! ユーザー機能作成までコメントアウト
    # uid = session.get('uid')
    # if uid is None:
    #     return redirect('/login')

    """チャンネル名

    フォームからチャンネル名を取得→channel_nameへ代入
    データベースから、入力されたチャンネル名と同じチャンネルを取得→channelへ代入

    if チャンネル名がデータベースに存在しない場合:
        チャンネル説明文をフォームから取得→channel_descriptionへ代入
        データベースに(ユーザーID, チャンネル名, チャンネル説明文)を追加
        チャンネル一覧表示画面へリダイレクト
    else: (チャンネル名がデータベースに存在した場合)
        エラーページを表示
    """
    channel_name = request.form.get('channel-title')
    channel = dbConnect.getChannelByName(channel_name)
    if channel == None:
        channel_description = request.form.get('channel-description')
        dbConnect.addChannel(channel_name, channel_description) #! uidを追加
        return redirect('/')
    else:
        error = '既に同じチャンネルが存在しています'
        return render_template('error/error.html', error_message=error)

if __name__ == '__main__':
    app.run(debug=True)
