from flask import *
app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

import mysql.connector
mydb=mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678",
        database="tourist_data"
    )
my_cursor=mydb.cursor()

# 求資料長度
my_cursor.execute("SELECT COUNT(*) FROM `sub_data`")
data_count=my_cursor.fetchone()[0] # 資料長度
data_count_for_page=data_count//12 # 每頁裝 12 筆，共有 (data_count_for_page)+1 頁


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
def attractions():
	# 兩個變數 page 和 keyword
	keyword=request.args.get("keyword")
	page=request.args.get("page")
	page=int(page)

	# step1-1. 有 keyword
	if keyword!=None:
		if page<data_count_for_page:
			nextPage=page+1
		else: nextPage=None
		sql_keyword="SELECT `id` FROM `sub_data` WHERE `name` LIKE '%"+keyword+"%'"
		# 取得有 keyword 的 id
		my_cursor.execute(sql_keyword)
		keyword_result=my_cursor.fetchall() #step2. 把 keyword 放進資料庫搜尋 
		# step2-1. 有搜尋到資料
		print(keyword_result)
		if keyword_result != []:
			for i in range(len(keyword_result)):
				keyword_result[i]=keyword_result[i][0]

			data_count_for_keyword=len(keyword_result)//12 # 每頁裝 12 筆，共有 (data_count_for_keyword)+1 頁
			# 處理 nextPage
			if page<data_count_for_keyword:
				nextPage=page+1
			else: nextPage=None
			#======================
			if page<=data_count_for_keyword: # stpe3-1. 頁數在規定內
				show_keyword0_to_full=[] # 所有符合 keyword 的詳細資料
				if page*12+12<=len(keyword_result):
					for k in range(page*12,page*12+12):
						# if keyword_result[k] != None:
							keyword_parameter=keyword_result[k]
							my_cursor.execute("SELECT * FROM `sub_data` WHERE `id`=%s" %keyword_parameter)
							keyword_data=my_cursor.fetchone() # 每筆符合 keyword 的詳細資料
							# if keyword_data != None:
							keyword_data9=keyword_data[9].split(" ",-1)

							keyword_show={
								"id": keyword_data[0],
								"name": keyword_data[1],
								"category": keyword_data[2],
								"description": keyword_data[3],
								"address": keyword_data[4],
								"transport": keyword_data[5],
								"mrt": keyword_data[6],
								"latitude": keyword_data[7],
								"longitude": keyword_data[8],
								"images": keyword_data9
							}
							show_keyword0_to_full.append(keyword_show.copy())
					return jsonify({"nextPage":nextPage,"data":show_keyword0_to_full}) # 尚未有nextPage
				else:
					for k in range(page*12,len(keyword_result)):
						# if keyword_result[k] != None:
							keyword_parameter=keyword_result[k]
							my_cursor.execute("SELECT * FROM `sub_data` WHERE `id`=%s" %keyword_parameter)
							keyword_data=my_cursor.fetchone() # 每筆符合 keyword 的詳細資料
							# if keyword_data != None:
							keyword_data9=keyword_data[9].split(" ",-1)

							keyword_show={
								"id": keyword_data[0],
								"name": keyword_data[1],
								"category": keyword_data[2],
								"description": keyword_data[3],
								"address": keyword_data[4],
								"transport": keyword_data[5],
								"mrt": keyword_data[6],
								"latitude": keyword_data[7],
								"longitude": keyword_data[8],
								"images": keyword_data9
							}
							show_keyword0_to_full.append(keyword_show.copy())
					return jsonify({"nextPage":nextPage,"data":show_keyword0_to_full}) # 尚未有nextPage
			else: # stpe3-2. 頁數沒在規定內
				return jsonify({"error": True,"message": "超過分頁"})
		# step2-2. 沒有搜尋到資料
		else:
			return jsonify({"error": True,"message": "沒有此關鍵字的資料"})
	
	# step1-2. 沒有 keyword，只有 page
	else:
		# page 在 4 之內
		if page<=data_count_for_page:
			# 處理 nextPage
			if page<data_count_for_page:
				nextPage=page+1
			else: nextPage=None


			# 用page把資料抓下來
			show_page0_to_full=[] # 所有符合 page 的資料
			for j in range(page*12,page*12+12):
				j=j+1
				my_cursor.execute("SELECT * FROM `sub_data` WHERE `id`=%s" %j)
				page_data=my_cursor.fetchone()
				if page_data != None:
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
					show_page0_to_full.append(page_show.copy())
			return jsonify({"nextPage":nextPage,"data":show_page0_to_full})
		# page 不在 4 之內
		else:
			return jsonify({"error": True,"message": "超過分頁"})

@app.route("/api/attraction/<attractionId>")
def api_attraction_id(attractionId):
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
	



app.run(host="0.0.0.0",port=3000)
