from flask import Flask, request, redirect, render_template, session, flash, url_for
from models import dbConnect
from util.DB import DB
from util.user import User
from datetime import timedelta
import hashlib
import uuid
import re

app = Flask(__name__)
# セッション情報を暗号化するためのキーを設定。キー：16進数文字列のuuid(uuid4()により生成)
app.secret_key = uuid.uuid4().hex
# セッションの有効期間を30日間とする
app.permanent_session_lifetime = timedelta(days=30)

# ユーザー登録画面（メソッド：GET）
@app.route('/signup')
def signup():
    """ ユーザー登録

    ユーザー登録画面を表示
    """
    return render_template('registration/signup.html')

# ユーザー登録画面（メソッド：POST）
@app.route('/signup', methods=['POST'])
def userSignup():
    """ ユーザー登録

    フォームからユーザー名を取得→nameへ代入
    フォームからメールアドレスを取得→emailへ代入
    フォームからパスワード1を取得→password1へ代入
    フォームからパスワード2を取得→password2へ代入

    メールアドレスを正規表現で表す→patternへ代入
    (a-zA-Z0-9_.+-の中から1文字以上)@(a-zA-Z0-9-の中から1文字以上).(a-zA-Z0-9-.の中から1文字以上)

    if ユーザー名、メールアドレス、パスワード1、パスワード2のいずれかに空欄がある場合
        「空のフォームがあるようです」と表示

    elif パスワード1とパスワード2が異なる場合
        「二つのパスワードの値が違っています」と表示

    elif 入力されたメールアドレスがpatternと一致しない場合
        「正しいメールアドレスの形式ではありません」と表示
        *reモジュール:正規表現を扱うモジュール
        match(正規表現, 文字列):文字列が正規表現と一致するかを判定

    else (いずれにも当てはまらない場合)
        uuidを生成→uidに代入
        *uuid:世界で同じ値を持つことがない一意な識別子。バージョン1~5の生成方法がある。
        uuid4():乱数によりuuidを生成
        パスワードをsha256方式でハッシュ化し16進数文字列に変換→passwordに代入
        *sha256():ハッシュ化を施すアルゴリズムの1つ
        hexdigest():16進数形式の文字列に変換して返す
        Userクラスのインスタンスを生成→userに代入
        フォームから取得したメールアドレスに一致するユーザーをデータベースから取得→DBuserに代入

        if DBuserがNoneでない場合=既に同じメールアドレスのユーザーが登録されている場合
            「既に登録されているようです」と表示

        else （同じメールアドレスで登録されているユーザーがいない場合）
            データベースにユーザーを新規登録
            uidをstr型に型変換
            セッション情報にuidを登録(キー:uid, 値:UserId)
            * セッション情報はsessionオブジェクト(辞書型)として操作する
            チャンネル一覧表示画面へリダイレクト

    (最後のelse節以外の場合は)サインアップ画面へリダイレクト
    """
    name = request.form.get('name')
    email = request.form.get('email')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    pattern = '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    if name == '' or email == '' or password1 == '' or password2 == '':
        flash('空のフォームがあるようです')
    elif password1 != password2:
        flash('二つのパスワードの値が違っています')
    elif re.match(pattern, email) is None:
        flash('正しいメールアドレスの形式ではありません')
    else:
        uid = uuid.uuid4()
        password = hashlib.sha256(password1.encode('utf-8')).hexdigest()
        user = User(uid, name, email, password)
        DBuser = dbConnect.getUser(email)

        if DBuser != None:
            flash('既に登録されているようです')
        else:
            dbConnect.createUser(user)
            UserId = str(uid)
            session['uid'] = UserId
            return redirect('/')
    return redirect('/signup')

# ログイン画面(メソッド:GET)
@app.route('/login')
def login():
    """ログイン

    ログイン画面を表示
    """
    return render_template('registration/login.html')

# ログイン画面(メソッド:POST)
@app.route('/login', methods=['POST'])
def userLogin():
    """ログイン

    メールアドレスをフォームから取得→emailに代入
    パスワードをフォームから取得→passwordへ代入

    if emailもしくはpasswordが空白の場合:
        「空のフォームがあるようです」と表示
    else:
        データベースから入力されたemailと一致するユーザーを取得→userへ代入
        if ユーザーが存在しない場合:
            「このユーザーは存在しません」と表示
        else:
            入力されたパスワードをsha256方式でハッシュ化し16進数文字列に変換→hashPasswordに代入
            if hashPasswordとデータベースに登録されているユーザーのpasswordが一致しない場合:
                「パスワードが間違っています」と表示
            else:(hashPasswordがデータベースにある値と一致した場合)
                データベースからuserテーブルのuidをセッション情報の登録
                ホーム(チャンネル一覧)画面にリダイレクト

    その他の場合、ログイン画面へリダイレクト

    """
    email = request.form.get('email')
    password = request.form.get('password')

    if email == '' or password == '':
        flash('空のフォームがあるようです')
    else:
        user = dbConnect.getUser(email)
        if user is None:
            flash('このユーザーは存在しません')
        else:
            hashPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if hashPassword != user['password']:
                flash('パスワードが間違っています')
            else:
                session['uid'] = user['uid']
                return redirect('/')
    return redirect('/login')

# ログアウト機能
@app.route('/logout')
def logout():
    """ ログアウト

    セッション情報をクリア
    ログイン画面へリダイレクト
    """
    session.clear()
    return redirect('/login')

#ホーム画面（チャンネル一覧画面）の作成
@app.route('/')
def index():
    """ ユーザーID

    ユーザーIDをセッションから取得してuidに代入
    ユーザーIDが無ければログインページへリダイレクト
    """
    uid = session.get('uid')
    if uid is None:
        return redirect('/login')

        """チャンネル一覧表示

        データベースから全てのチャンネルを取得→channelsへ代入
        データベースから全てのタグを取得→tagsへ代入
        チャンネル一覧画面を表示
        """
    else:
        channels = dbConnect.getChannelAll()
        tags = dbConnect.getTagsAllByTagId()
    return render_template('index.html', channels=channels, uid=uid, tags=tags)

@app.route('/', methods=['POST'])
def add_channel():
    """ ユーザーID

    ユーザーIDをセッションから取得してuidに代入
    ユーザーIDが無ければログインページへリダイレクト
    """
    uid = session.get('uid')
    if uid is None:
        return redirect('/login')

    """チャンネル名

    フォームからチャンネル名を取得→channel_nameへ代入

    if チャンネル名が入力されていない場合:
        エラーページを表示

    データベースから、入力されたチャンネル名と同じチャンネルを取得→channelへ代入

    if チャンネル名がデータベースに存在しない場合:
        チャンネル説明文をフォームから取得→channel_descriptionへ代入
        フォームからタグIDを取得→tidに代入
        データベースに(ユーザーID, チャンネル名, チャンネル説明文, タグID)を追加
        チャンネル一覧表示画面へリダイレクト
    else: (チャンネル名がデータベースに存在した場合)
        エラーページを表示
    """
    channel_name = request.form.get('channel-title')

    if not channel_name:
        error = 'チャンネル名が入力されていません'
        return render_template('error/error.html', error_message=error)

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
    uid = session.get('uid')
    if uid is None:
        return redirect('/login')

    """ チャンネル編集

    フォームからチャンネルIDを取得→cidに代入
    フォームからチャンネル名を取得→channel_nameに代入

    if チャンネル名が入力されていない場合:
        エラーページを表示

    フォームからチャンネル説明文を取得→channel_descriptionに代入

    データベースの（ユーザーID、チャンネル名、チャンネル説明文、チャンネルID）を更新
    メッセージ一覧画面へリダイレクト
    """

    cid = request.form.get('cid')
    channel_name = request.form.get('channel-title')

    if not channel_name:
        error = 'チャンネル名が入力されていません'
        return render_template('error/error.html', error_message=error)

    channel_description = request.form.get('channel-description')

    dbConnect.updateChannel(uid, channel_name, channel_description, cid)
    return redirect(url_for('detail', cid=cid))

# メッセージ一覧画面
@app.route('/detail/<cid>')
def detail(cid):
    """ ユーザーID

    ユーザーIDをセッションから取得してuidに代入
    ユーザーIDが無ければログインページへリダイレクト
    """
    uid = session.get('uid')
    if uid is None:
        return redirect('/login')

    """ メッセージ一覧画面

    URLよりチャンネルIDを取得→cidに代入
    データベースから該当するcidのチャンネルを取得
    データベースから該当するcidの全てのメッセージを取得
    データベースから該当するcidに紐づいたタグを全て取得→channel_tagsへ代入
    メッセージ一覧画面を表示
    """
    cid = cid
    channel = dbConnect.getChannelById(cid)
    messages = dbConnect.getMessageAll(cid)
    channel_tags = dbConnect.getTagsByChannelId(cid)
    return render_template('detail.html', messages=messages, channel=channel, uid=uid, channel_tags=channel_tags)

# チャンネル削除機能
@app.route('/delete/<cid>')
def delete_channel(cid):
    """ ユーザーID

    ユーザーIDをセッションから取得してuidに代入
    ユーザーIDが無ければログインページへリダイレクト
    """
    uid = session.get('uid')
    if uid is None:
        return redirect('/login')

        """ ユーザーIDがチャンネル作成者と一致しているかの確認

            データベースからURLで指定されたcidに該当するチャンネルを取得

            if データベースから取得したチャンネルのユーザーID(=チャンネルの作成者)が
            現在アクセスしているユーザーIDと異なる場合:
                「チャンネルは作成者のみ削除可能です」と表示
                チャンネル一覧画面へリダイレクト
        """
    else:
        channel = dbConnect.getChannelById(cid)
        if channel['uid'] != uid:
            flash('チャンネルは作成者のみ削除可能です')
            return redirect('/')

            """ チャンネル削除処理
                else:(ユーザーIDが同じ場合)
                    データベースから該当するcidのチャンネルを削除
                    チャンネル一覧画面へリダイレクト
            """
        else:
            dbConnect.deleteChannel(cid)
            dbConnect.deleteTagLinkByChannelId(cid)
            return redirect('/')

# メッセージ作成機能
@app.route('/message', methods=['POST'])
def add_message():
    """ ユーザーID

    ユーザーIDをセッションから取得してuidに代入
    ユーザーIDが無ければログインページへリダイレクト
    """
    uid = session.get('uid')
    if uid is None:
        return redirect('/login')

    """メッセージ

    メッセージをフォームから取得→messageへ代入
    チャンネルIDをフォームから取得(hidden)→channel_idへ代入
    if メッセージが存在する場合:
        データベースに(ユーザーID, チャンネルID, メッセージ)を追加

    メッセージ一覧画面へリダイレクト
    """
    message = request.form.get('message')
    channel_id = request.form.get('channel_id')

    if message:
        dbConnect.createMessage(uid, channel_id, message)

    return redirect(url_for('detail', cid=channel_id))

# メッセージ削除機能
@app.route('/delete_message', methods=['POST'])
def delete_message():
    """ ユーザーID

    ユーザーIDをセッションから取得してuidに代入
    ユーザーIDが無ければログインページへリダイレクト
    """
    uid = session.get('uid')
    if uid is None:
        return redirect('/login')

    """
    メッセージIDをフォームから取得→message_idに代入
    チャンネルIDをフォームから取得→cidに代入
    if メッセージIDが存在したら:
        dbConnectクラスのdeleteMessageメソッドを実行(該当のメッセージを削除)

    チャンネルIDからチャンネルを取得→channelに代入
    チャンネルIDから該当のメッセージを全て取得→messagesに代入
    """
    message_id = request.form.get('message_id')
    cid = request.form.get('channel_id')
    if message_id:
        dbConnect.deleteMessage(message_id)

    return redirect(url_for('detail', cid=cid))

# タグ一覧&タグに紐づいたチャンネル数表示
@app.route('/tags')
def tags():
    """ ユーザーID

    ユーザーIDをセッションから取得してuidに代入
    ユーザーIDが無ければログインページへリダイレクト
    """
    uid = session.get('uid')
    if uid is None:
        return redirect('/login')

        """タグ一覧&タグに紐づいたチャンネル数表示

        データベースから全てのタグを取得→tagsへ代入
        タグ一覧画面を表示
        """
    else:
        tags = dbConnect.getTagsAll()
    return render_template('tags.html', tags=tags, uid=uid)

# 選択されたタグに紐づけられたチャンネルの表示
@app.route('/tag/<tid>')
def tag_channel(tid):
    """ ユーザーID

    ユーザーIDをセッションから取得してuidに代入
    ユーザーIDが無ければログインページへリダイレクト
    """
    uid = session.get('uid')
    if uid is None:
        return redirect('/login')

    """タグに紐づけられたチャンネル表示

    指定されたtidに該当するタグをデーターベースから取得
    取得したタグのname列の値を取り出してtag_nameに代入
    指定されたtidに紐づけられたチャンネルをデーターベースから取得

    if タグに紐づけられたチャンネルが存在する場合
        タグに紐づけられたチャンネル一覧を表示
    else (存在しない場合)
        「まだチャンネルは登録されていません」と表示
        ※redirectでindexに遷移すると、tag_nameの表示が消えてしまうためrender_templateで記述
    """
    tags = []
    tag = dbConnect.getTagById(tid)
    tag_name = tag['name']
    channels = dbConnect.getChannelsByTagId(tid)

    if channels:
        return render_template('index.html',tags=tags, tag_name=tag_name, channels=channels, uid=uid)
    else:
        flash(tag_name + 'のタグにチャンネルは登録されていません')
        return redirect('/tags')


# タグ追加&紐付け
@app.route('/link_tag', methods=['POST'])
def link_tag():
    """ ユーザーID

    ユーザーIDをセッションから取得してuidに代入
    ユーザーIDが無ければログインページへリダイレクト
    """
    uid = session.get('uid')
    if uid is None:
        return redirect('/login')

    """
    フォームからタグ名を取得→tag_nameへ代入
    if タグ名が入力されていない場合:
        エラーページへ遷移
    フォームからチャンネルIDを取得→cidへ代入

    データベースから入力されたタグ名と同じデータを取り出す→tagへ代入

    if タグ存在しない場合:
        データベースにタグを追加
        追加したタグのデータを取得→tagへ代入
        タグのIDを取得→tidへ代入
    else: (タグが存在している場合)
        タグのIDを取得→tidへ代入

    データベースからチャンネルとタグが既に紐付いていないかを検索→countへ代入

    if チャンネルとタグが既に紐付いている場合:
    * COUNT(*)で全ての行をカウントしている
        「追加済みです」と表示
        detail画面へリダイレクト
    else: (チャンネルとタグが紐付いていない場合)
        チャンネルとタグを紐付ける
        detail画面へリダイレクト
    """

    tag_name = request.form.get('tag_name')

    if not tag_name:
        error = 'タグ名が入力されていません'
        return render_template('error/error.html', error_message=error)

    cid = request.form.get('cid')

    tag = dbConnect.getTagByName(tag_name)

    if tag is None:
        dbConnect.addTag(tag_name)
        tag = dbConnect.getTagByName(tag_name)
        tid = tag['id']
    else:
        tid = tag['id']

    count = dbConnect.countExistData(cid, tid)

    if count and count['COUNT(*)'] > 0:
        flash('追加済みです')
        return redirect(url_for('detail', cid=cid))
    else:
        dbConnect.linkChannelTag(cid, tid)
        return redirect(url_for('detail', cid=cid))

# タグの紐付け削除
@app.route('/delete_tag_link', methods=['POST'])
def delete_tag_link():
    """ ユーザーID

    ユーザーIDをセッションから取得してuidに代入
    ユーザーIDが無ければログインページへリダイレクト
    """
    uid = session.get('uid')
    if uid is None:
        return redirect('/login')

    """
    フォームからチャンネルIDを取得→cidへ代入
    フォームからタグIDを取得→tidへ代入
    データベースから同じチャンネルID・タグIDの組み合わせを削除
    チャット画面へリダイレクト
    """

    cid = request.form.get('cid')
    tid = request.form.get('tid')
    dbConnect.deleteTagLink(cid, tid)
    return redirect(url_for('detail', cid=cid))

# 404エラー処理
@app.errorhandler(404)
def show_error404(error):
    """エラー処理
    *errorhandler(例外):引数で指定した例外が発生した際に対応する関数を呼び出すデコレータ
    404エラー発生時に404用のエラー画面を表示
    """
    return render_template('error/404.html')

# 500エラー処理
@app.errorhandler(500)
def show_error500(error):
    """エラー処理
    500エラー発生時に500用のエラー画面を表示
    """
    return render_template('error/500.html')

if __name__ == '__main__':
    app.run(debug=True)
