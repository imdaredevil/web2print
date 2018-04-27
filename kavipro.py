import codecs, os, pymongo
import gridfs
import shutil
import msg
import smtplib
import time
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging,send_file,Response
from pymongo import MongoClient
from functools import wraps
import time
import random
from time import strftime,gmtime,strptime
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from os import listdir
import base64
import bcrypt
app = Flask("web2print")
app.secret_key = 'secretkey'	
MONGO_URL='localhost:27017'
print(MONGO_URL)
client=pymongo.MongoClient(MONGO_URL)
db=client.printt
fs=gridfs.GridFS(db)


def sendmail(msg,email):
	server = smtplib.SMTP("smtp.gmail.com",587);
	server.connect("smtp.gmail.com",587);
	server.ehlo()
	server.starttls()
	server.login("3929jarvis@gmail.com","cibicool");
	#server.ehlo();
	k = server.sendmail("3929jarvis@gmail.com",email,msg);
	return k
	
@app.route('/oorder')
def oorder():
	return render_template('order.html')

@app.route('/images/<kname>')
def functi(kname):
	return send_file(
		"images/" + kname,
		mimetype="application/*")


@app.route('/fonts/<kname>')
def functio(kname):
	return send_file(
		"fonts/" + kname,
		mimetype="application/*")



@app.route('/background/<kname>')
def funct(kname):
	return send_file(
		"background/" + kname,
		mimetype="application/*")

@app.route('/')
def index():
	
	printe = db.printe
	return render_template('home.html')

@app.route('/card')
def card():
	return render_template('card.html')



@app.route('/login')
def login():
    return render_template('order.html')

@app.route("/auth/login",methods=['POST','GET'])
def login_template():
	print(dict(request.form))
	users=db.users
	login_user=users.find_one({'uname':request.form['uname']})
	if login_user :
		if bcrypt.hashpw(request.form['password'].encode('utf-8'),login_user['password']) ==login_user['password'] :
			session['uname']=request.form['uname']
			session['logged_in']=True
			flash('You are now logged in','success')
			return redirect(url_for('dashboard'))
	return render_template('home.html',value='Invalid User Name or Password')		
	
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard', methods=['POST','GET'])
@is_logged_in
def dashboard():
	if request.method == 'POST':
		#return render_template('dashboard.html')
		fil = request.files['file']
		name = request.form['filename']
		st1 = float(request.form['Substrate'].split(' ')[1]);
		fi1 = float(request.form['Finishing'].split(' ')[1]);
		g1 = float(request.form['G'].split(' ')[1]);	
		st = request.form['Substrate'].split(' ')[0];
		fi = request.form['Finishing'].split(' ')[0];
		q = request.form["quantity"];
		msg = request.form["message"];
		g = request.form['G'].split(' ')[0];	
		printe = db.printe
		ki = base64.b64encode(fil.read());
		order = db.order;
		pri = 0
		if(str(ki) == "b''"):
			print("kk")
			fil = open("images/power1.pdf","rb")	
			pri = 50
		order.insert_one({"name":name + " " + session['uname'],"st":st,"fi":fi,"g":g,"price":pri + g1 + st1 + fi1,"quantity":q,"Daddress":msg,"status":"Order placed"});
		print(fil.read())
		fil.seek(0,0)
		a = fs.put(fil,filename=name + " " + session['uname'])
		k = "ponlakshmibalagan@gmail.com"
		msg1 = "\n New order received\n  order details: \n Order name: " + name + " " + session['uname'] + "\nSubstrate type: " + st + "\nFinishing operation: " + fi + "\nQuantity: " + q + "\nGSM" + g + "\nDelivery: " + msg + "\n" 
		BODY = "From: 3929jarvis@gmail.com\n" +  "To: %s\n" % k + "Subject: printing order\n" + "" + msg1 + "\r\n"
		#sendmail(BODY,k);		
		filenames = []
		for f in list(db.fs.files.find()):
			lij = f['filename'].split(' ')		
			if lij[1] == session['uname']:			
				filenames.append(lij[0])
		return render_template("Upload.html",names=filenames)
	filenames = []
	for f in list(db.fs.files.find()):
		lij = f['filename'].split(' ')		
		if lij[1] == session['uname']:			
			filenames.append(lij[0])
	return render_template("Upload.html",names=filenames)

@app.route('/remove/<name>')
def remove(name):
	f = db.fs.files.find_one({'filename':name + ' ' + session['uname']})
	fs.delete(f['_id'])
	db.order.delete_one({'name':name + ' ' + session['uname']})
	return redirect(url_for('dashboard'))

@app.route('/dashboard/<kname>')
@is_logged_in
def display(kname):
	fil = db.fs.files.find_one({"filename":kname + " " + session['uname']})
	print(fil);
	fi = fs.get(fil["_id"])
	#fi.show();
	return send_file(
        fi, 
        mimetype="application/pdf",  
        attachment_filename=kname + "pdf")

@app.route('/register', methods=['POST','GET'])
def regis():
	return render_template('register.html')

@app.route('/auth/images/<kname>')
def functt(kname):
	return send_file(
		"images/" + kname,
		mimetype="application/*")
tempu = {};
un = 'sdsfwf';
OTP = 0;
@app.route('/otp',methods=['POST','GET'])
def otp():
	print(OTP)
	if request.method == 'POST':
		users = db['users']
		if int(request.form['OTP']) == int(session['OTP']):
			db['users'].insert_one({'uname':session['tempu']['uname'],'phone':session['tempu']['phone'],'password':session['tempu']['password']})
			session['uname'] = un
			return render_template('order.html')
		return render_template('home.html',value = "wrong otp")
	return render_template('otp.html');
		
@app.route('/auth/register', methods=['POST','GET'] )
def register_template():
	if request.method =='POST':
		if 'g-recaptcha-response' not in request.form.keys():
			return render_template('register.html')
		users=db['users']
		existing_user=users.find_one({'uname':request.form['uname']})
		if existing_user == None:
			#print(request.form['g-recaptcha-response'])
			hashpass=bcrypt.hashpw(request.form['password'].encode('utf-8'),bcrypt.gensalt())
			session['tempu'] = {'uname':request.form['uname'],'password':hashpass,'phone':request.form['phone']}
			un=request.form['uname']
			q=msg.sms(9486293823,'cibicool')
			OTP = random.randint(99999,1000000)
			session['OTP'] = OTP
			n=q.send(request.form['phone'],str(OTP))
			return render_template('otp.html')
		return render_template('home.html',value="user already registered")


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/order/img')
@is_logged_in
def func():
	return send_file(
        "power1.jpg", 
        mimetype="application/*",
	attachment_filename="file.jpg")

@app.route('/choosetm')
@is_logged_in
def choosetm():
	f = listdir("templates/background")
	print(f)
	return render_template("choosetm.html",fil=f);




@app.route('/getphoto')
def functiono():
	nal = request.args.get("nal")
	nat = request.args.get("nat")
	il = request.args.get("il")
	it = request.args.get("it")
	a1l = request.args.get("a1l")
	a1t = request.args.get("a1t")
	a2l = request.args.get("a2l")
	a2t = request.args.get("a2t")
	a3l = request.args.get("a3l")
	a3t = request.args.get("a3t")
	lol = request.args.get("lol")
	lot = request.args.get("lot")
	phl = request.args.get("phl")
	pht = request.args.get("pht")
	img = Image.open(session["img"])	
	name = session["name"];
	address = session["address"];
	add = session["add"]
	addr = session["addr"];	
	size = request.args.get("tsize");
	size = size.strip("px");
	print(size);
	#fi = session["uname"];
	h = session["color"].strip('#');
	kl = tuple(int(h[i:i+2], 16) for i in (0, 2 ,4))
	im = Image.open(session["logo"])
	v = int(lot) - int(it);
	k = int(lol) - int(il);	
	im.thumbnail((100, 100), Image.ANTIALIAS)
	im.save("temp.jpg",quality=100);
	im = Image.open("temp.jpg")
	img.paste(im,(k,v))
	draw = ImageDraw.Draw(img)
	font = ImageFont.truetype("fonts/"+session["ffa"], int(size))
	v = int(nat) - int(it);
	k = int(nal) - int(il);
	draw.text((k,v),name,kl,font=font)
	v = int(a1t) - int(it);
	k = int(a1l) - int(il);
	draw.text((k,v),address,kl,font=font)
	v = int(a2t) - int(it);
	k = int(a2l) - int(il);
	draw.text((k, v),add,kl,font=font)
	v = int(a3t) - int(it);
	k = int(a3l) - int(il);
	draw.text((k,v),addr,kl,font=font)
	v = int(pht) - int(it);
	k = int(phl) - int(il);
	draw.text((k,v),session["phone1"],kl,font=font)
	img.save('images/power1.jpg',quality=100)	
	img.save('images/power1.pdf',"PDF",resolution=100.0,quality=100)
	return render_template("desresult.html");


k = {}
@app.route('/order',methods=['GET','POST'])
@is_logged_in
def order():
	if request.method == 'POST':
		name = request.form["name"]
		address = request.form["address1"]
		add = request.form["address2"]
		addr = request.form["address3"]
		fi = request.files["logo"];
		fi.save(fi.filename);
		session["phone1"] = "Ph: " + request.form["phone"] 
		session["logo"] = fi.filename;
		session["name"] = name;
		session["address"] = address;
		session["add"] = add;
		session["addr"] = addr;
		ffa = request.form["font-style"];
		session["ffa"] = ffa;
		fi = open(session["logo"],'rb')
		st = (base64.b64encode(fi.read()));
		st = st.replace(b"\n",b"");
		st =str(st)
		print(st)
		st = st[2:-1]
		fon = listdir("fonts");
		col = request.form["color"];
		session["color"] = col;
		return render_template("design1.html",na=name,add1=address,add2=add,add3=addr,fik=st,fil=session["img"],fonts=fon,color=col,filsty=ffa,phone=session["phone1"]);
	session["img"] = request.args.get("img");
	fon = listdir("fonts");
	return render_template("design1.html",fil=session["img"],fonts=fon,filsty="dsfes")


if __name__ == '__main__':
	app.config["CACHE_TYPE"] = "null"
	app.secret_key = 'secretkey'	
	app.run(host='0.0.0.0',debug=True)




