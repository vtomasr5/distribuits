#!/usr/bin/env python
# coding: utf8

import MySQLdb as mysqldb
import logging
import sys

logging.basicConfig(filename='debug.log', filemode='w', level=logging.DEBUG)

class MySQL:
	def __init__(self, host, user, passwd, db):
		self.host = host
		self.user = user
		self.passwd = passwd
		self.db = db
	
	def get_connection(self):
		try:
			conn = mysqldb.connect(self.host, self.user, self.passwd, self.db)
			if conn:
				logging.debug("Connected to db");
				return conn
		except mysqldb.Error, e:
				logging.debug("ERROR %d: %s", e.args[0], e.args[1])
				sys.exit(-1)

	def get_cursor(self, conn):
		cursor = conn.cursor()
		if cursor:
			logging.debug("Cursor got OK")
			return cursor
		else:
			if conn:
				conn.close()
				logging.debug("ERROR getting cursor. Disconnecting")

	def exec_sql(self, conn, cursor, sql):
		try:
			cursor.execute(sql)
			conn.commit()
			logging.debug("SQL executed OK")
		except mysqldb.Error, e:
			logging.debug("ERROR executing SQL")
			conn.rollback()

	def disconnect(self, conn):
		if conn:
			conn.close()
			logging.debug("Connection closed")