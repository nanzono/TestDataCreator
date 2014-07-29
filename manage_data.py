# coding:utf-8

import time
import MySQLdb
import os



def connect():
    host = os.environ["RDS_host"]
    port = os.environ["RDS_port"]
    db = os.environ["RDS_db"]
    user = os.environ["RDS_user"]
    passwd = os.environ["RDS_passwd"]
    connector = MySQLdb.connect(host=host, port=int(port), db=db, user=user, passwd=passwd, charset="utf8")
    return connector

def insert_1(cur, table_name):
    tmp_sql = """
    INSERT INTO %(table_name)s (id,name,comment,created_at) 
    SELECT IFNULL(MAX(id),0)+1,'name insert 1','comment insert 1', now() FROM %(table_name)s;
    """
    sql = tmp_sql % {'table_name': table_name}
    cur.execute(sql)
    print "INSERT_1", table_name

def insert_2(cur,table_name):
    tmp_sql = """
    INSERT INTO %(table_name)s (id,name,comment,user,created_at) 
    SELECT IFNULL(MAX(id),0)+1,'name insert 2','comment insert 2','user insert 2', now() FROM %(table_name)s;
    """
    sql = tmp_sql % {'table_name': table_name}
    sql = tmp_sql % {'table_name': table_name}
    cur.execute(sql)
    print "INSERT_2", table_name

def alter_table(cur,table_name):
    tmp_sql = "ALTER TABLE %(table_name)s ADD COLUMN user VARCHAR(32);"
    sql = tmp_sql % {'table_name': table_name}
    cur.execute(sql)
    print "ADD COLUMN", table_name


def commit(connection):
    connection.commit()
    print "commit"
    # do commit

def add_data():
    connection = connect()
    cur = connection.cursor()
    for i in range(20):
        insert_1(cur, "table_01")
        insert_1(cur, "table_02")
        insert_1(cur, "table_03")
        commit(connection)
        print "phase 1 -", i
        time.sleep(0.5)
    alter_table(cur, "table_01")
    while 0 < 1:
    	i = i +1
        insert_2(cur, "table_01")
        insert_1(cur, "table_02")
        insert_1(cur, "table_03")
        commit(connection)
        print "phase 2 -", i
        time.sleep(0.5)

def create_table(cur, table_name):
    tmp_sql = """
	CREATE TABLE %(table_name)s (
	  id INTEGER
	  , name VARCHAR(64)
	  , comment VARCHAR(256)
	  , created_at DATETIME
	  , PRIMARY KEY (id)
	);
    """
    sql = tmp_sql % {'table_name': table_name}
    cur.execute(sql)
    print sql

def drop_table(cur, table_name):
    tmp_sql = """
    DROP TABLE IF EXISTS %(table_name)s;
    """
    sql = tmp_sql % {'table_name': table_name}
    cur.execute(sql)
    print sql


def initialize():
    connection = connect()
    cur = connection.cursor()
    drop_table(cur, "table_01")
    drop_table(cur, "table_02")
    drop_table(cur, "table_03")
    create_table(cur, "table_01")
    create_table(cur, "table_02")
    create_table(cur, "table_03")
    commit(connection)

def connection_test():
    connection = connect()
    connection.close()
    print "success"


if __name__ == '__main__':
    connection_test()
    initialize()
    add_data()

