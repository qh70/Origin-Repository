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
# data_count=my_cursor.execute("SELECT COUNT(*) FROM `sub_data`")data的長度還沒解決



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
	page=request.args.get("page")
	show_0_to_full=[]
	for i in range(int(page)*12,int(page)*12+12):
		i=i+1
		my_cursor.execute("SELECT * FROM `sub_data` WHERE `id`=%s" %i)
		data=my_cursor.fetchone()
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
	return {"data":show_0_to_full}

	



app.run(port=3000)