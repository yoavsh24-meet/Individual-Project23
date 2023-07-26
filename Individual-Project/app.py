from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
import os
config = {  "apiKey": "AIzaSyDECMaXsfGEux5NWhONXeZmHgRJ66RyK0A",
  "authDomain": "misinfo-90919.firebaseapp.com",
  "projectId": "misinfo-90919",
  "storageBucket": "misinfo-90919.appspot.com",
  "messagingSenderId": "380051167038",
  "appId": "1:380051167038:web:72e0449ba18f273914be6f",
  "measurementId": "G-EB3EZT4HTC",
"databaseURL": "https://misinfo-90919-default-rtdb.europe-west1.firebasedatabase.app/"}
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
error = ""
db = firebase.database()
#UPLOAD_FOLDER = "/home/student/Documents/GitHub/Individual-Project23/Individual-Project"
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        username = request.form["username"]
        #try:
        login_session['user'] = auth.create_user_with_email_and_password(email, password)
        UID = login_session['user']['localId']
        user = {'email': email, "password": password,  'username': username}
        db.child("Users").child(UID).set(user)
        return redirect(url_for("new_article"))
        #except:
        error = "auth failed :(c"
        return render_template('signup.html')

    return render_template("signup.html")
@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('new_article'))
        except:
            error = 'sign in failed'
    return render_template("signin.html")

@app.route('/new_article', methods=['GET', 'POST'])
def new_article():
    if request.method == 'POST':
        headline = request.form['headline']
        text = request.form['text']
        #file = request.files['file']
        #filename = file.filename
        #file_name = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        #file.save(file_name)
        article = {"headline": headline, "text": text}
        db.child('articles').push(article)
        try:
            UID = login_session['user']["localId"]


            return redirect(url_for('articles'))
        except:
            error = "article failed"
            return redirect(url_for('articles'))
    return render_template("new_article.html")
@app.route('/homepage', methods=['GET', 'POST'])
def articles():
    articles = db.child("articles").get().val()
    return render_template("homepage.html", articles=articles)



if __name__ == '__main__':
  app.run(debug=True)