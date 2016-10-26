#coding:utf-8
#服务器使用的是Python2，代码里含有中文时需要指明程序文件的编码
from flask import Flask
from flask import render_template
from flask import request

#注意dbconfig没有加入版本管理，本地的dbconfig只有一句 test = True
#服务器端的dbconfig除了有test = False，还有数据库的凭证
import dbconfig
if dbconfig.test:
	from mockdbhelper import MockDBHelper as DBHelper
else:
	from dbhelper import DBHelper


app = Flask(__name__)
DB = DBHelper()

@app.route("/")
def home():
	try:
		data = DB.get_all_inputs()
	except Exception as e:
		print(e)
		data = None
	return render_template("home_google.html", data=data)
	#前端显示地图可以选择谷歌地图或者百度地图home_google或者home_baidu

@app.route("/submitrecord", methods=['POST'])
def submitrecord():
	category = request.form.get("category")
	date = request.form.get("date")
	latitude = float(request.form.get("latitude"))
	longitude = float(request.form.get("longitude"))
	description = request.form.get("description")
	DB.add_record(category, date, latitude, longitude, description)
	return home()

@app.route("/add", methods=["POST"])
def add():
	try:
		data = request.form.get("userinput")
		DB.add_input(data)
	except Exception as e:
		print(e)
	return home()

@app.route("/clear")
def clear():
	try:
		DB.clear_all()
	except Exception as e:
		print(e)
	return home()


if __name__ == '__main__':
	app.run(port=5000, debug=True)

