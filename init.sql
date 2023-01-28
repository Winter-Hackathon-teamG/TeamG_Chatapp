#初期化処理
DROP DATABASE chatapp;
DROP USER 'testuser'@'localhost';

#ユーザーの作成 ユーザー名:testuser パスワード:testuser
CREATE USER 'testuser'@'localhost' IDENTIFIED BY 'testuser';
#データベースの作成
CREATE DATABASE chatapp;

#testuserにchatappデータベースの全テーブルへの権限を付与
USE chatapp;
GRANT ALL PRIVILEGES ON chatapp.* TO 'testuser'@'localhost';

#usersテーブルの作成
  #[uid]ユーザーID:主キー、255字以内
  #[user_name]ユーザー名:255字以内、重複不可、空データ不可
  #[email]メールアドレス:255字以内、重複不可、空データ不可
  #[password]パスワード:255字以内、空データ不可
CREATE TABLE users (
    uid varchar(255) PRIMARY KEY,
    user_name varchar(255) UNIQUE NOT NULL,
    email varchar(255) UNIQUE NOT NULL,
    password varchar(255) NOT NULL
);

#channnelsテーブルの作成
  #[id]チャンネルID:主キー、serial型はオートインクリメントの重複しない整数
  #[uid]ユーザーID:255字以内、userテーブルより参照
  #[name]チャンネル名:255字以内、重複不可、空データ不可
  #[abstract]チャンネル概要:255字以内
CREATE TABLE channels (
    id serial PRIMARY KEY,
    uid varchar(255) REFERENCES users(uid),
    name varchar(255) UNIQUE NOT NULL,
    abstract varchar(255)
);

#動作確認用データの挿入
#テスト1とテスト2のuidとpasswordは最後の1文字だけ変えています。
INSERT INTO users(uid, user_name, email, password)VALUES('970af84c-dd40-47ff-af23-282b72b7cca8','テスト1','test1@gmail.com','37268335dd6931045bdcdf92623ff819a64244b53d0e746d438797349d4da578');
INSERT INTO channels(id, uid, name, abstract)VALUES(1, '970af84c-dd40-47ff-af23-282b72b7cca8','ぼっち部屋','テストさんの孤独な部屋です');

INSERT INTO users(uid, user_name, email, password)VALUES('970af84c-dd40-47ff-af23-282b72b7cca9','テスト2','test2@gmail.com','37268335dd6931045bdcdf92623ff819a64244b53d0e746d438797349d4da579');
INSERT INTO channels(id, uid, name, abstract)VALUES(2, '970af84c-dd40-47ff-af23-282b72b7cca9','リア充部屋','テスト2さんのパーティルームです');
