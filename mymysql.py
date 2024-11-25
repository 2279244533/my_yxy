import mysql.connector
from mysql.connector import Error
import json
import os

# 导入配置文件
from conf import DB_CONFIG
def reset_count_for_qq(qq):
    try:
        # 获取数据库连接
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor()

            # 检查 qq 是否已存在
            cursor.execute("SELECT count FROM proxy WHERE qq = %s", (qq,))
            result = cursor.fetchone()

            if result:
                # 如果存在，设置 count 为 0
                cursor.execute("UPDATE proxy SET count = 0 WHERE qq = %s", (qq,))
                print(f"Reset count to 0 for QQ {qq}.")
            else:
                # 如果不存在，插入新记录，并将 count 设置为 0
                cursor.execute("INSERT INTO proxy (qq, count) VALUES (%s, 0)", (qq,))
                print(f"Inserted new record with count 0 for QQ {qq}.")

            # 提交更改并关闭连接
            connection.commit()
            cursor.close()
            connection.close()
    except Error as e:
        print(f"Error: {e}")
def connect_to_database():
    try:
        # 使用 conf.py 中的 DB_CONFIG 配置来连接数据库
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],        # 数据库主机
            user=DB_CONFIG['user'],        # 数据库用户名
            password=DB_CONFIG['password'],  # 数据库密码
            database=DB_CONFIG['database']  # 数据库名称
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def create_proxy_table():
    try:
        # 获取数据库连接
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor()

            # 创建 proxy 表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS proxy (
                    qq VARCHAR(20) PRIMARY KEY,
                    count INT DEFAULT 0
                );
            """)

            # 提交更改并关闭连接
            connection.commit()
            cursor.close()
            connection.close()
            print("Proxy table created or already exists.")
    except Error as e:
        print(f"Error: {e}")

def get_count_for_qq(qq):
    try:
        # 获取数据库连接
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor()

            # 查找指定 qq 的 count 值
            cursor.execute("SELECT count FROM proxy WHERE qq = %s", (qq,))
            result = cursor.fetchone()

            # 关闭连接
            cursor.close()
            connection.close()

            # 如果没有找到，返回 None
            if result:
                return result[0]
            else:
                return None
    except Error as e:
        print(f"Error: {e}")
        return None

def update_count_for_qq(qq):
    try:
        # 获取数据库连接
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor()

            # 检查 qq 是否已存在
            cursor.execute("SELECT count FROM proxy WHERE qq = %s", (qq,))
            result = cursor.fetchone()

            if result:
                # 如果存在，增加 count 值
                cursor.execute("UPDATE proxy SET count = count + 1 WHERE qq = %s", (qq,))
                print(f"Updated count for QQ {qq}.")
            else:
                # 如果不存在，插入新记录
                cursor.execute("INSERT INTO proxy (qq, count) VALUES (%s, 1)", (qq,))
                print(f"Inserted new record for QQ {qq}.")

            # 提交更改并关闭连接
            connection.commit()
            cursor.close()
            connection.close()
    except Error as e:
        print(f"Error: {e}")