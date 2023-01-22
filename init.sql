#初期化処理
DROP DATABASE chatapp;
DROP USER 'testuser'@'localhost';

#ユーザーの作成　ユーザー名:testuser パスワード:testuser
CREATE USER 'testuser'@'localhost' IDENTIFIED BY 'testuser'; 
#データベースの作成
CREATE DATABASE chatapp; 

#testuserにchatappデータベースの全テーブルへの権限を付与
USE chatapp;
GRANT ALL PRIVILEGES ON chatapp.* TO 'testuser'@'localhost'

#usersテーブルの作成
 #[uid]ユーザーID:主キー、255字以内
 #カラムは取り合えずチャンネル表示で必要なuidのみにしています。
CREATE TABLE users(
    uid varchar(255) PRIMARY KEY,
)

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

