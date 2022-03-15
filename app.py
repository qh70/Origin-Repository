from flask import *
from flask_cors import CORS

app=Flask(__name__)
CORS(app)

app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

import mysql.connector

# connection pool
from mysql.connector import Error, pooling
pool=pooling.MySQLConnectionPool(
	host="localhost",
	user="jerry",
	password="12345678",
	database="tourist_data",
	pool_name="mypool",
	pool_size=3,
)


# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

@app.route("/api/attractions")
def api_attractions():
	db_connection_mydb=pool.get_connection()
	my_cursor=db_connection_mydb.cursor()

	# 求資料長度
	my_cursor.execute("SELECT COUNT(*) FROM `sub_data`")
	data_count=my_cursor.fetchone()[0] # 資料長度
	data_count_for_page=data_count//12 # 每頁裝 12 筆，共有 (data_count_for_page)+1 頁

	# 兩個變數 page 和 keyword
	keyword=request.args.get("keyword")
	page_str=request.args.get("page")

	# 當 page 是大於等於0的整數:
	if page_str.isnumeric():
		page=int(page_str)
		# step1-1. 有 keyword
		if keyword!=None:
			if page<data_count_for_page:
				nextPage=page+1
			else: nextPage=None
			page12=str(page*12)
			my_cursor.execute("SELECT * FROM `sub_data` WHERE `name` LIKE '%"+keyword+"%' LIMIT "+page12+",13")
			keyword_result=my_cursor.fetchall()# 用 keyword 搜尋到的資料集合
			# step 2-1. 搜尋到的資料集合有東西
			if keyword_result != []:
				# 如果不到 12 筆
				show_keyword0_to_full=[]
				if len(keyword_result)<12:
					for k in range(len(keyword_result)):
						keyword_data_k_9=keyword_result[k][9].split(" ",-1)

						keyword_show={
							"id": keyword_result[k][0],
							"name": keyword_result[k][1],
							"category": keyword_result[k][2],
							"description": keyword_result[k][3],
							"address": keyword_result[k][4],
							"transport": keyword_result[k][5],
							"mrt": keyword_result[k][6],
							"latitude": keyword_result[k][7],
							"longitude": keyword_result[k][8],
							"images": keyword_data_k_9
						}
						show_keyword0_to_full.append(keyword_show.copy())
					return jsonify({"nextPage":None,"data":show_keyword0_to_full}) # 沒有nextPage
				# 有到 12 筆
				else:
					for k in range(12):
						keyword_data_k_9=keyword_result[k][9].split(" ",-1)

						keyword_show={
							"id": keyword_result[k][0],
							"name": keyword_result[k][1],
							"category": keyword_result[k][2],
							"description": keyword_result[k][3],
							"address": keyword_result[k][4],
							"transport": keyword_result[k][5],
							"mrt": keyword_result[k][6],
							"latitude": keyword_result[k][7],
							"longitude": keyword_result[k][8],
							"images": keyword_data_k_9
						}
						show_keyword0_to_full.append(keyword_show.copy())
					if len(keyword_result)==12:
						return jsonify({"nextPage":None,"data":show_keyword0_to_full})# 沒有nextPage
					else:
						return jsonify({"nextPage":nextPage,"data":show_keyword0_to_full})
			# step 2-1. 搜尋到的資料集合沒有東西
			else:
				return jsonify({"error": True,"message": "沒有此關鍵字的資料"})
		
		# step1-2. 沒有 keyword，只有 page
		else:
			# 當 page 是數字
			page_is_N=page_str.isnumeric()
			if page_is_N:
				# page 在 4 之內
				if page<=data_count_for_page:
					# 處理 nextPage
					if page<data_count_for_page:
						nextPage=page+1
					else: nextPage=None

					# 用page把資料抓下來
					page12=str(page*12)
					my_cursor.execute("SELECT * FROM `sub_data` LIMIT "+page12+",12")
					page_data=my_cursor.fetchall()
					show_page0_to_full=[] # 所有符合 page 的資料
					for j in range(12):
						if j+1<=len(page_data):
							page_data_j_9=page_data[j][9].split(" ",-1)

							page_show={
								"id": page_data[j][0],
								"name": page_data[j][1],
								"category": page_data[j][2],
								"description": page_data[j][3],
								"address": page_data[j][4],
								"transport": page_data[j][5],
								"mrt": page_data[j][6],
								"latitude": page_data[j][7],
								"longitude": page_data[j][8],
								"images": page_data_j_9
							}
							show_page0_to_full.append(page_show.copy())
					return jsonify({"nextPage":nextPage,"data":show_page0_to_full})
					
				# page 不在 4 之內
				else:
					return jsonify({"error": True,"message": "超過分頁"})
	# 當 page 不是大於等於0的整數:
	else:
		return jsonify({"error": True,"message": "請輸入大於等於 0 的整數"})

	db_connection_mydb.close()

@app.route("/api/attraction/<attractionId>")
def api_attraction_id(attractionId):
	db_connection_mydb=pool.get_connection()
	my_cursor=db_connection_mydb.cursor()
	# 求資料長度
	my_cursor.execute("SELECT COUNT(*) FROM `sub_data`")
	data_count=my_cursor.fetchone()[0] # 資料長度

	# 當 attractionId 是數字
	attractionid_is_N=attractionId.isnumeric()
	if attractionid_is_N:
		attractionId=int(attractionId)
		if attractionId>data_count:
			return jsonify({"error": True,"message": "景點編號太大"})
		elif attractionId<1:
			return jsonify({"error": True,"message": "景點編號太小"})
		else:
			my_cursor.execute("SELECT * FROM `sub_data` WHERE `id`=%s" %attractionId)
			page_data=my_cursor.fetchone()
			page_data9=page_data[9].split(" ",-1)

			page_show={
				"id": page_data[0],
				"name": page_data[1],
				"category": page_data[2],
				"description": page_data[3],
				"address": page_data[4],
				"transport": page_data[5],
				"mrt": page_data[6],
				"latitude": page_data[7],
				"longitude": page_data[8],
				"images": page_data9
			}
			return jsonify({"data":page_show})
	else:
		return jsonify({"error": True,"message": "請輸入正整數"})

	db_connection_mydb.close()





app.run(host="0.0.0.0",port=3000)