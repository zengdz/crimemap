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
	return render_template("home.html", data=data)

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

