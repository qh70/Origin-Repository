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
data_count=my_cursor.fetchone()[0]
data_count=data_count//12


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
	if page<4:
		nextPage=page+1
	else: nextPage=None

	# 用page把資料抓下來
	show_0_to_full=[]
	for i in range(page*12,page*12+12):
		i=i+1
		my_cursor.execute("SELECT * FROM `sub_data` WHERE `id`=%s" %i)
		data=my_cursor.fetchone()
		if data != None:
			data9=data[9].split(" ",-1)

			show={
				"id": data[0],
				"name": data[1],
				"category": data[2],
				"description": data[3],
				"address": data[4],
				"transport": data[5],
				"mrt": data[6],
				"latitude": data[7],
				"longitude": data[8],
				"images": data9
			}
			show_0_to_full.append(show.copy())
	return jsonify({"nextPage":nextPage,"data":show_0_to_full})

app.run(port=3000)