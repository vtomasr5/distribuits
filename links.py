#!/usr/bin/env python
# coding: utf8

import MySQLdb as mysqldb
import logging

logging.basicConfig(filename='debug.log', filemode='w', level=logging.DEBUG)
# Uncomment for disable logging
#logging.disable(logging.DEBUG)

# constants
HOST='localhost'
USER='root'
PASS=''
DB='test'

class Carrega:
	def __init__(self, host, user, passwd, db):
		self.host = host
		self.user = user
		self.passwd = passwd
		self.db = db
	
	def get_connection(self):
		conn = mysqldb.connect(self.host, self.user, self.passwd, self.db)
		if conn:
			logging.debug("Connected to db");
			return conn
		else:
			logging.debug("Error connecting to db")

	def get_cursor(self, conn):
		cursor = conn.cursor()
		if cursor:
			logging.debug("Cursor got OK")
			return cursor
		else:
			conn.close()
			logging.debug("Error getting cursor. Disconnecting")

	def exec_sql(self, conn, cursor, sql):
		try:
			cursor.execute(sql)
			conn.commit()
			logging.debug("SQL executed OK")
		except:
			logging.debug("Error executing SQL")
			conn.rollback()
			conn.close()

	def disconnect(self, conn):
		conn.close()
		logging.debug("Connection closed")


def main():
	c = Carrega(HOST, USER, PASS, DB)
	conn = c.get_connection()
	cursor = c.get_cursor(conn)
	# sql test
	sql = "INSERT INTO links VALUES (NULL, 'algo2')"
	c.exec_sql(conn, cursor, sql)
	c.disconnect(conn)

if __name__ == "__main__":
	main()
