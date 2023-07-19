"""此文件目的：
    1.创建用于存放企微人员通讯录的mysql数据库和数据表，并将企微后台导出的通讯录文件写入
    2.存放mysql操作相关的函数
"""

import os
import pymysql
from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
import sqlalchemy


def init_db_table():
    """根据企微后台通讯录应用导出的excel，将其中用于一键拉群的字段写入mysql；
    函数包括建库、建表、导入三部分
    """
    # 数据库连接
    db = pymysql.connect(
        host=MYSQL_HOST, port=int(MYSQL_PORT), user=MYSQL_USER, password=MYSQL_PASSWORD
    )
    # 建立数据库
    cursor = db.cursor()
    create_db_sql = """CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci;""".format(
        MYSQL_DATABASE
    )
    try:
        cursor.execute(create_db_sql)
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()
    # 关闭数据库连接
    db.close()

    # 建立数据表
    db, cursor = mysql_connect()
    create_table_sql = """CREATE TABLE `qywx_contacts` (
        `id` smallint(5) unsigned NOT NULL AUTO_INCREMENT COMMENT '默认主键',
        `user_id` varchar(20) NOT NULL DEFAULT '' COMMENT '帐号',
        `name` varchar(16) NOT NULL DEFAULT '' COMMENT '姓名',
        `sex` char(2) DEFAULT '' COMMENT '性别',
        `department` varchar(100) DEFAULT '' COMMENT '部门',
        `phone_number` varchar(20) DEFAULT '' COMMENT '手机',
        `email` varchar(50) DEFAULT '' COMMENT '企业邮箱',
        
        PRIMARY KEY (`id`),
        KEY `k_name` (`name`)
        ) CHARSET=utf8 COMMENT='企微通讯录';""".format(
        MYSQL_DATABASE
    )
    try:
        cursor.execute(create_table_sql)
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()
    # 关闭数据库连接
    db.close()


def contacts_to_mysql():
    """将通讯录相关字段写入Mysql"""
    contacts_path = "D:\常用文件夹\下载\嘉为公司通讯录.xlsx"
    conn = create_engine(
        f"mysql+pymysql://{MYSQL_USER}:"
        + MYSQL_PASSWORD
        + f"@{MYSQL_HOST}:{MYSQL_PORT}/"
        + MYSQL_DATABASE
        + "?charset=utf8",
        encoding="utf-8",
    )
    contacts_df = pd.read_excel(
        contacts_path,
        engine="openpyxl",
        header=9,
        usecols=["帐号", "姓名", "性别", "部门", "手机", "企业邮箱"],
        index_col=None
    )
    contacts_df = contacts_df.reset_index(drop=True)
    # contacts_df = contacts_df.drop(columns=['index'])
    contacts_df = contacts_df.rename(columns={"帐号":"user_id", "姓名":"name", "性别":"sex", "部门":"department", "手机":"phone_number", "企业邮箱":"email"})
    contacts_df.to_sql(
        "qywx_contacts",
        con=conn,
        if_exists="append",
        dtype={
            "user_id": sqlalchemy.VARCHAR(length=30),
            "name": sqlalchemy.VARCHAR(length=16),
            "sex": sqlalchemy.CHAR(length=2),
            "department": sqlalchemy.VARCHAR(length=100),
            "phone_number": sqlalchemy.VARCHAR(length=20),
            "email": sqlalchemy.VARCHAR(length=50)
        },
        index=False
    )


def mysql_connect():
    # 从环境变量载入MYSQL配置
    load_dotenv()
    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_PORT = os.getenv("MYSQL_PORT")
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

    db = pymysql.connect(
        host=MYSQL_HOST,
        port=int(MYSQL_PORT),
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
    )
    cursor = db.cursor()
    return db, cursor


def mysql_select(db, cursor, sql):
    """对数据库进行查找操作，返回结果列表"""
    if db.open:
        cursor.execute(sql)
        results = list(cursor.fetchall())
    else:
        db, cursor = mysql_connect()
        cursor.execute(sql)
        results = list(cursor.fetchall())
    return results


if __name__ == "__main__":
    # 载入MYSQL配置
    load_dotenv()
    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_PORT = os.getenv("MYSQL_PORT")
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

    init_db_table()
    contacts_to_mysql()

    print("load contacts success")
