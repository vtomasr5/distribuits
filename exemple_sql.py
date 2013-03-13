#!/usr/bin/env python
# coding: utf8

import MySQLdb as mysqldb
import logging
import sys
from mysql import MySQL
from carrega import Carrega

# Uncomment for disable logging
#logging.disable(logging.DEBUG)

# constants
HOST='localhost'
USER='root'
PASS=''
DB='test'


def main():
	m = MySQL(HOST, USER, PASS, DB)
	conn = m.get_connection()
	cursor = m.get_cursor(conn)
	# sql test
	sql = "INSERT INTO links VALUES (NULL, 'algo')"
	m.exec_sql(conn, cursor, sql)
	m.disconnect(conn)

if __name__ == "__main__":
	main()
