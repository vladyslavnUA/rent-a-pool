from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/pools')
client = MongoClient(host=host)
db = client.get_default_database()
pools = db.pools

app = Flask(__name__)

# @app.route("/login")
# def login:
# 	auth = request.authorization
# 	return " "

@app.route("/")
def pools_index():
	#this will show the type of pools we have
		#this will show the type of pants we have
	return render_template("base.html", pools=pools.find())
	#return render_template("pools_index.html", pools=pools.find())

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/pools/reserve", methods=["POST"])
def pools_submit():
	pool = {
		"pool_name": request.form.get("pool_name"),
		"description": request.form.get("description"),
		"price": request.form.get("price")
	}
	pool_id = pools.insert_one(pool).inserted_id
	print(pool_id)
	return redirect(url_for("pools_show", pool_id = pool_id))

@app.route("/reserve/<pool_id>")
def pools_show(pool_id):
	pool = pools.find_one({'_id' : ObjectId(pool_id)})
	return render_template("pools_show.html", pool = pool)

@app.route("/pools/login")
def login():
	return render_template("login.html")

@app.route("/pools/new")
def pools_new():
	return render_template("pools_new.html", pool={})

@app.route("/pools/reserve")
def pools_reserve():
	return render_template("pools_reserve.html", pool={})

@app.route("/pools/<pool_id>/edit")
def pools_edit(pool_id):
	pool = pools.find_one({"_id" : ObjectId(pool_id)})
	return render_template("pools_edit.html", pool = pool)

@app.route("/pools/<pool_id>", methods = ['POST'])
def pools_update(pool_id):
	updated_pool = {
		"pool_name": request.form.get("pool_name"),
		"description": request.form.get("description"),
		"price": request.form.get("price"),
        	"picture": request.form.get("picture")
	}

	pools.update_one( {"_id" : ObjectId(pool_id)}, {"$set" : updated_pool})
	return redirect(url_for("pools_show", pool_id = pool_id))

@app.route("/pools/<pool_id>/delete", methods=["POST"])
def pools_delete(pool_id):
	pools.delete_one({"_id" : ObjectId(pool_id)})
	return redirect(url_for("pools_index"))

app.config['DROPZONE_UPLOAD_MULTIPLE'] = True
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*'
app.config['DROPZONE_REDIRECT_VIEW'] = 'results'

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
