#coding: utf-8
import pymysql
import dbconfig
import datetime

#所有的数据操作都放在try-finally里面，以便数据库最终都能顺利关闭连接
class DBHelper:

	#数据库连接，每次操作数据表格前都要连接，末尾指定编码
	def connect(self, database="crimemap"):
		return pymysql.connect(host='localhost',
		user=dbconfig.db_user,
		passwd=dbconfig.db_password,
		db=database,
        charset = 'utf8')

	#之前测试实验从crimes获取description数据
	def get_all_inputs(self):
		connection = self.connect() #每次操作之前都要先和数据库建立连接
		try:
			query = "SELECT description FROM crimes;" #从crimes数据库选择description数据，注意最后有分号，应该是SQL的语法
			with connection.cursor() as cursor: #使用with-as
				cursor.execute(query) #指针执行这个请求之后，cursor就指向所需数据了。
			return cursor.fetchall() #使用fetchall方法把指向的数据变成Python能处理的列表数据
		finally:
			connection.close()

	#之前测试实验向crimes插入description数据
	def add_input(self, data):
		connection = self.connect()
		try:
			# small fix to SQL injection
			query = "INSERT INTO crimes (description) VALUES (%s);" #作为测试用只插入一个description数据
			with connection.cursor() as cursor:
				cursor.execute(query, data) #执行请求操作
				connection.commit() #不同于读取数据，插入数据对数据库修改了所以要提交修改才能生效
		finally:
			connection.close()

	#删除crimes表格的所有数据
	def clear_all(self):
		connection = self.connect()
		try:
			query = "DELETE FROM crimes;" #删除crimes数据库的所有内容
			with connection.cursor() as cursor:
				cursor.execute(query) #执行请求操作
				connection.commit() #删除数据对数据库修改了所以要提交修改才能生效
		finally:
			connection.close()

	def add_record(self, category, date, latitude, longitude, description):
		connection = self.connect()
		try:
			query = "INSERT INTO crimes (category, date, latitude, longitude, description) VALUES (%s, %s, %s, %s, %s);"
			with connection.cursor() as cursor:
				cursor.execute(query, (category, date, latitude, longitude, description))
				connection.commit()
		except Exception as e:
			print(e)
		finally:
			connection.close()
	
	def get_all_records(self):
		connection = self.connect()
		try:
			query = "SELECT latitude, longitude, date, category, description FROM crimes;"
			with connection.cursor() as cursor:
				cursor.execute(query)
			named_crimes = []
			#从cursor提取元组数据转换为JSON数据保存到列表，方便后面在JavaScript处理
			for crime in cursor:
				named_crime = {
					'latitude': crime[0],
					'longitude': crime[1],
					'date': datetime.datetime.strftime(crime[2], '%Y-%m-%d'),
					'category': crime[3],
					'description': crime[4]
				}
				named_crimes.append(named_crime)
			return named_crimes
		finally:
			connection.close()
