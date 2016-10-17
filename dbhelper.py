#coding: utf-8
import pymysql
import dbconfig

#所有的数据操作都放在try-finally里面，以便数据库最终都能顺利关闭连接
class DBHelper:

	def connect(self, database="crimemap"):
		return pymysql.connect(host='localhost',
		user=dbconfig.db_user,
		passwd=dbconfig.db_password,
		db=database)

	#Reading data
	def get_all_inputs(self):
		connection = self.connect() #每次操作之前都要先和数据库建立连接
		try:
			query = "SELECT description FROM crimes;" #从crimes数据库选择description数据，注意最后有分号，应该是SQL的语法
			with connection.cursor() as cursor: #使用with-as
				cursor.execute(query) #指针执行这个请求之后，cursor就指向所需数据了。
			return cursor.fetchall() #使用fetchall方法把指向的数据变成Python能处理的列表数据
		finally:
			connection.close()

	#Inserting data
	def add_input(self, data):
		connection = self.connect()
		try:
			# small fix to SQL injection
			query = "INSERT INTO crimes (description) VALUES (%s);"
			with connection.cursor() as cursor:
				cursor.execute(query, data) #执行请求操作
				connection.commit() #不同于读取数据，插入数据对数据库修改了所以要提交修改才能生效
		finally:
			connection.close()

	def clear_all(self):
		connection = self.connect()
		try:
			query = "DELETE FROM crimes;" #删除crimes数据库的所有内容
			with connection.cursor() as cursor:
				cursor.execute(query) #执行请求操作
				connection.commit() #删除数据对数据库修改了所以要提交修改才能生效
		finally:
			connection.close()

