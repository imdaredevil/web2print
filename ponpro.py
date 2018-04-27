from flask import Flask, render_template, flash, redirect		, url_for, session, request, logging,send_file,Response
import pymongo
from pymongo import MongoClient
import msg
app = Flask("web2print")
app.secret_key = 'secretkey'	
MONGO_URL='localhost:27017'
print(MONGO_URL)
client=pymongo.MongoClient(MONGO_URL)
db=client.printt
ordi = db.order
@app.route("/",methods=["POST","GET"])
def jobtrack():
	if(request.method == "POST"):
		name = request.form["name"];
		status = request.form["status"];
		ordi.update({"name":name},{"status":status});
		user = db.users;
		k = user.find_one({"uname":(name.split())[1]});
		q=msg.sms(9789752663,'pon123')
		q.send(k["phone"],"ur order status is" + status);
	return render_template("job.html");
							

if __name__ == '__main__':
	app.secretkey = 'secretkey'	
	app.run(debug=True)
