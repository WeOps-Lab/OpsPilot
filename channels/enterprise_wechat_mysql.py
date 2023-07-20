"""存放mysql操作相关的函数
"""
import os
import pymysql

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")


def mysql_connect(exist_db=True):
    # 从环境变量载入MYSQL配置
    if not exist_db:
        MYSQL_DATABASE = None
    db = pymysql.connect(
        host=MYSQL_HOST,
        port=int(MYSQL_PORT),
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )
    cursor = db.cursor()
    return db, cursor


def mysql_select(db, cursor, sql):
    """对数据库进行查找操作，返回结果列表"""
    if not db.open:
        _, cursor = mysql_connect()
    cursor.execute(sql)
    results = list(cursor.fetchall())
    return results


def create_mysql_engine():
    conn = create_engine(
        f"mysql+pymysql://{MYSQL_USER}:"
        + MYSQL_PASSWORD
        + f"@{MYSQL_HOST}:{MYSQL_PORT}/"
        + MYSQL_DATABASE
        + "?charset=utf8",
        encoding="utf-8",
    )
    return conn