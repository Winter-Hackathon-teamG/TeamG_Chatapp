from flask import Flask, request, redirect, render_template, session, flash
from models import dbConnect

app = Flask(__name__)

#ホーム画面（チャンネル一覧画面）の作成
@app.route('/')
def index():
    # # セッション情報からuidキーに対応する値を取り出して変数uidに代入
    # uid = session.get('uid')
    # #uidが空＝セッション情報の中にuid情報が登録されていない＝まだログインしていない場合
    # if uid is None:
    #     #ログイン画面へリダイレクト。
    #     return redirect('/login')

    # #uidが空でない＝セッション情報の中にuid情報が登録されている＝ログイン済みの場合
    # else:
    #     #データベースからチャンネル情報を取得して変数channelsへ代入
    channels = dbConnect.getChannelAll()
    #ホーム画面のWEBページを返す。HTMLファイルで使う変数は引数で渡す。
    return render_template('test_index.html', channels=channels) #! uidを追記

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

# チャンネル編集機能
@app.route('/update_channel', methods=['POST'])
def update_channel():
    """ ユーザーID

    ユーザーIDをセッションから取得してuidに代入
    ユーザーIDが無ければログインページへリダイレクト
    """
    #! ユーザー機能作成までコメントアウト
    # uid = session.get('uid')
    # if uid is None:
    #     return redirect('/login')

    """ チャンネル編集

    フォームからチャンネルIDを取得→cidに代入
    フォームからチャンネル名を取得→channel_nameに代入
    フォームからチャンネル説明文を取得→channel_descriptionに代入

    データベースの（ユーザーID、チャンネル名、チャンネル説明文）を更新
    データベースから改めてチャンネルを取得
    （！コメントアウト データベースから全てのメッセージを取得）
    メッセージ一覧画面を表示
    """

    cid = request.form.get('cid')
    channel_name = request.form.get('channel-title')
    channel_description = request.form.get('channel-description')

    #! 仮uid
    uid = '970af84c-dd40-47ff-af23-282b72b7cca8'
    dbConnect.updateChannel(uid, channel_name, channel_description, cid)
    channel = dbConnect.getChannelById(cid)
    #! メッセージ機能作成までコメントアウト
    # messages = dbConnect.getMessageAll(cid)
    return render_template('test_detail.html', channel=channel, uid=uid) #! messagesを追加

# メッセージ一覧画面（チャンネル編集機能用にチャンネル名とチャンネル概要のみ表示する画面）
@app.route('/detail/<cid>')
def detail(cid):
    """ ユーザーID

    ユーザーIDをセッションから取得してuidに代入
    ユーザーIDが無ければログインページへリダイレクト
    """
    #! ユーザー機能作成までコメントアウト
    # uid = session.get('uid')
    # if uid is None:
    #     return redirect('/login')

    """ メッセージ一覧画面

    URLよりチャンネルIDを取得→cidに代入
    データベースから該当するcidのチャンネルを取得
    （！コメントアウト データベースから全てのメッセージを取得）
    メッセージ一覧画面を表示
    """
    cid = cid
    channel = dbConnect.getChannelById(cid)
    #! メッセージ機能作成までコメントアウト
    # messages = dbConnect.getMessageAll(cid)
    return render_template('test_detail.html', channel=channel) #! messages,uidを追加


# メッセージ作成機能
@app.route('/message', methods=['POST'])
def add_message():
    """ ユーザーID

    ユーザーIDをセッションから取得してuidに代入
    ユーザーIDが無ければログインページへリダイレクト
    """
    #! ユーザー機能作成までコメントアウト
    # uid = session.get('uid')
    # if uid is None:
    #     return redirect('/login')

    """メッセージ

    メッセージをフォームから取得→messageへ代入
    チャンネルIDをフォームから取得(hidden)→channel_idへ代入
    if メッセージが存在する場合:
        データベースに(ユーザーID, チャンネルID, メッセージ)を追加

    同チャンネルのチャンネルIDをDBから取得→channelに代入
    同チャンネルのメッセージをDBから全て取得→messagesに代入

    メッセージ一覧画面を表示(message, channel, uid)
    """
    message = request.form.get('message')
    channel_id = request.form.get('channel_id')

    #! 仮uid
    uid = '970af84c-dd40-47ff-af23-282b72b7cca8'
    if message:
        dbConnect.createMessage(uid, channel_id, message)

    channel = dbConnect.getChannelById(channel_id)
    #! メッセージ一覧表示機能作成までコメントアウト
    # messages = dbConnect.getMessageAll(channel_id)

    return render_template('test_detail.html', channel=channel, uid=uid) #! messages=messages追記

if __name__ == '__main__':
    app.run(debug=True)
