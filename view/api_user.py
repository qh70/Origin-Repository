from flask import *

api_User = Blueprint('api_User', __name__,static_url_path="/")

# @api_user.route('/api/user')
# def show(page):
#         return "Hello Blueprint app2"

from mysql.connector import pooling
pool=pooling.MySQLConnectionPool(
	host="localhost",
	user="jerry",
	password="12345678",
	database="tourist_data",
	pool_name="mypool",
	pool_size=3,
)


@api_User.route("/api/user")
def api_user_get():
	print(session)
	if session!={}:
		print(session["email"])
		if session["email"]!="logout":
			try:
				db_connection_mydb=pool.get_connection()
				my_cursor=db_connection_mydb.cursor()
				my_cursor.execute("SELECT `id`,`name` FROM `user` WHERE email='%s'" %session["email"])
				result=my_cursor.fetchone()
				return jsonify({
					"data":{
						"id":result[0],
						"name":result[1],
						"email":session["email"]
					}
				})
			except:
				return jsonify({"error":True}), 500
			finally:
				db_connection_mydb.close()
		else:
			return jsonify({"data":None})
	else:
		return jsonify({"data":None})
	
@api_User.route("/api/user", methods=["POST",])
def api_user():
	name_signup=request.json["name_signup"]
	email_signup=request.json["email_signup"]
	password_signup=request.json["password_signup"]
	try:
		db_connection_mydb=pool.get_connection()
		my_cursor=db_connection_mydb.cursor()
		my_cursor.execute("SELECT `name`,`email`,`password` FROM `user` WHERE email='%s'" %email_signup)
		result=my_cursor.fetchone()
		if result!=None:
			return jsonify({"error":True,"message":"Email 已經被註冊"})
		else:
			my_cursor.execute("INSERT INTO user (name, email, password) VALUES (%s, %s, %s);", (name_signup, email_signup, password_signup))
			db_connection_mydb.commit()
			return jsonify({"ok":True}), 200
	except:
		return jsonify({"error":True}), 500
	finally:
		db_connection_mydb.close()

@api_User.route("/api/user", methods=["PATCH"])
def api_user_patch():
	email_login=request.json["email_login"]
	password_login=request.json["password_login"]
	try:
		db_connection_mydb=pool.get_connection()
		my_cursor=db_connection_mydb.cursor()
		my_cursor.execute("SELECT `name`,`email`,`password` FROM `user` WHERE email='%s'" %email_login)
		result=my_cursor.fetchone()
		if result!=None:
			# 登入成功
			if password_login==result[2]:
				session["email"]=result[1]
				return jsonify({"ok":True}), 200
			# 密碼錯誤
			else:
				return jsonify({"error":True,"message":"密碼錯誤"}), 400
		# 此Email 未註冊帳號
		else:
			return jsonify({"error":True,"message":"此Email 未註冊帳號"}), 400
	except:
		return jsonify({"error":True}), 500
	finally:
		db_connection_mydb.close()

@api_User.route("/api/user", methods=["DELETE"])
def api_user_delete():
	session["email"]="logout"
	return jsonify({"ok":True}), 200

# export FLASK_APP=app.py
# flask run