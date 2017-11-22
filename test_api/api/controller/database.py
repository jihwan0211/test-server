from datetime import datetime, timezone

import json

#from endpoint import parse_time
from aniso8601 import parse_time

from flask import Flask, session
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
import pytz
import pdb

APP = Flask(__name__)
APP.config['MYSQL_DATABASE_USER'] = 'hawayou'
APP.config['MYSQL_DATABASE_PASSWORD'] = 'HaaWAAYOU'
APP.config['MYSQL_DATABASE_DB'] = 'test_db'
APP.config['MYSQL_DATABASE_HOST'] = 'hawayou-mysql-instance.cji2aeewmf6q.ap-northeast-2.rds.amazonaws.com'
APP.config['MYSQL_DATABASE_PORT'] = 3306
APP.config['MYSQL_CURSORCLASS'] = 'DictCursor'

SQL = MySQL(cursorclass=DictCursor)
SQL.init_app(APP)

class DatabaseConnector():
    connection = None

    def __init__(self):
        self.connection = SQL.connect()
        self.connection.autocommit(True)

    def __del__(self):
        self.connection.close()

    # query 함수
    def get_news_data(self, page, length):
        """뉴스 데이터 가져오기"""
        start_index = length*(page-1)

        cursor = self.connection.cursor()
        cursor.execute("SELECT * from news WHERE delete_check=0 ORDER BY timestamp DESC limit %s, %s", (start_index, length))
        rows = cursor.fetchall()
        cursor.close()

        if rows is None:
            return None

        result=[]
        for row in rows:
            row['timestamp'] = str(row['timestamp'])
            row.pop('delete_check')

        return rows

    def post_news_data(self, title, contents, url):
        """뉴스 데이터 작성"""
        query = "INSERT INTO news (title, contents, url, timestamp) VALUES (%s, %s, %s, (NOW() + interval 9 hour))"
        data = (title, contents, url)
        cursor = self.connection.cursor()
        cursor.execute(query, data)
        result = cursor.lastrowid
        cursor.close()
        
        return result

    def update_news_data(self, nid, title, contents, url):
        """뉴스 데이터 수정"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*) as COUNT from news WHERE nid=%s", (nid))
        rows = cursor.fetchall()
        data_exist_flag = bool(rows[0]['COUNT'])

        if data_exist_flag is True:
            cursor.execute("UPDATE news SET title=%s, contents=%s, url=%s, timestamp=(NOW() + interval 9 hour) WHERE nid=%s", (title, contents, url, nid))
            cursor.close()
            result = True
        else:
            result = False
        cursor.close()
        return result

    def remove_news_data(self, nid):
        """뉴스 데이터 삭제"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*) as COUNT from news WHERE nid=%s",(nid))
        rows = cursor.fetchall()
        data_exist_flag = bool(rows[0]['COUNT'])

        if data_exist_flag is True:
            cursor.execute("UPDATE news SET delete_check = 1 WHERE nid=%s", (nid))
            cursor.close()
            result = True
        else:
            result = False
        cursor.close()
        return result

        
        