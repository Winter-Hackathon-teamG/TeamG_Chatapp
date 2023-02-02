from flask import Flask, request, redirect, render_template, session, flash
from models import dbConnect
import uuid

app = Flask(__name__)
app.secret_key = uuid.uuid4().hex


#ホーム画面（チャンネル一覧画面）の作成
@app.route('/')
def index():
    """ ユーザーID

    ユーザーIDをセッションから取得してuidに代入
    ユーザーIDが無ければログインページへリダイレクト
    """
    #! ユーザー機能作成までコメントアウト
    # uid = session.get('uid')
    # if uid is None:
    #     return redirect('/login')
    # else:

    """チャンネル一覧表示

    データベースから全てのチャンネルを取得→channelsへ代入
    チャンネル一覧画面を表示
    """
    channels = dbConnect.getChannelAll() #! インデント必要
    return render_template('test_index.html', channels=channels) #! uidを追加

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
    #! 仮uid
    uid = '970af84c-dd40-47ff-af23-282b72b7cca8'
    channel_name = request.form.get('channel-title')
    channel = dbConnect.getChannelByName(channel_name)
    if channel == None:
        channel_description = request.form.get('channel-description')
        dbConnect.addChannel(uid, channel_name, channel_description)
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
    messages = dbConnect.getMessageAll(cid)
    return render_template('test_detail.html', messages=messages, channel=channel, uid=uid)

# メッセージ一覧画面
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
    データベースから該当するcidの全てのメッセージを取得
    メッセージ一覧画面を表示
    """
    cid = cid
    channel = dbConnect.getChannelById(cid)
    messages = dbConnect.getMessageAll(cid)
    return render_template('test_detail.html', messages=messages, channel=channel) #! uidを追加

# チャンネル削除機能
@app.route('/delete/<cid>')
def delete_channel(cid):
    """ ユーザーID

    ユーザーIDをセッションから取得してuidに代入
    ユーザーIDが無ければログインページへリダイレクト
    """
    #! ユーザー機能作成までコメントアウト
    # uid = session.get('uid')
    # if uid is None:
    #     return redirect('/login')
    # else:

    """ ユーザーIDがチャンネル作成者と一致しているかの確認

        データベースからURLで指定されたcidに該当するチャンネルを取得

        if データベースから取得したチャンネルのユーザーID(=チャンネルの作成者)が
        現在アクセスしているユーザーIDと異なる場合:
            「チャンネルは作成者のみ削除可能です」と表示
            チャンネル一覧画面へリダイレクト
    """
    #!    ユーザー機能作成までコメントアウト
    #     channel = dbConnect.getChannelById(cid)
    #     if channel['uid'] != uid:
    #         flash('チャンネルは作成者のみ削除可能です')
    #         return redirect('/')
    #     else:

    """ チャンネル削除処理
        else:(ユーザーIDが同じ場合)
            データベースから該当するcidのチャンネルを削除
            データベースから登録されている全てのチャンネルを取得
            チャンネル一覧画面を表示
    """
    #! 下記3行はインデント必要
    dbConnect.deleteChannel(cid)
    channels = dbConnect.getChannelAll()
    return render_template('test_index.html', channels=channels) #! uidを追加

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
    messages = dbConnect.getMessageAll(channel_id)

    return render_template('test_detail.html', messages=messages, channel=channel, uid=uid)

# メッセージ削除機能
@app.route('/delete_message', methods=['POST'])
def delete_message():
    """ ユーザーID

    ユーザーIDをセッションから取得してuidに代入
    ユーザーIDが無ければログインページへリダイレクト
    """
    #! ユーザー機能作成までコメントアウト
    # uid = session.get('uid')
    # if uid is None:
    #     return redirect('/login')

    """
    メッセージIDをフォームから取得→message_idに代入
    チャンネルIDをフォームから取得→cidに代入
    if メッセージIDが存在したら:
        dbConnectクラスのdeleteMessageメソッドを実行(該当のメッセージを削除)

    チャンネルIDからチャンネルを取得→channelに代入
    チャンネルIDから該当のメッセージを全て取得→messagesに代入
    """

    #! 仮uid
    uid = '970af84c-dd40-47ff-af23-282b72b7cca8'
    message_id = request.form.get('message_id')
    cid = request.form.get('channel_id')
    if message_id:
        dbConnect.deleteMessage(message_id)

    channel = dbConnect.getChannelById(cid)
    messages = dbConnect.getMessageAll(cid)

    return render_template('test_detail.html', messages=messages, channel=channel, uid=uid)

if __name__ == '__main__':
    app.run(debug=True)
