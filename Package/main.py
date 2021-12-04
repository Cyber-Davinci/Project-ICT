from logging import log
from flask import Flask, render_template,redirect,url_for, request,g,session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "justusoursecret"
#config databse
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFIFCATIONS'] = False



db = SQLAlchemy(app)

class Member(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    clas = db.Column(db.String(6), nullable=False)
    gr_no = db.Column(db.String(6), nullable=False)
    phone = db.Column(db.String(7), nullable=False)

    question_1 = db.Column(db.String(400),nullable=False)
    question_2 = db.Column(db.String(400),nullable=False)
    question_3 = db.Column(db.String(400),nullable=False)

    level = db.Column(db.String(), nullable=False)

class Admin:
    def __init__(self, username,password):
        self.username = username
        self.password = password


president = Admin("user","password")
username = president.username


logged_in = False

#home route =================================================
@app.route("/")
@app.route("/home")
def home():
    return render_template('main.html')

#member form route ============================================
@app.route("/join", methods=["GET", "POST"])
def join():
    # fetching form inputs from our join site
    if request.method=="POST":
        name = request.form.get("Name")
        email = request.form.get("Email")
        clas = request.form.get("Class")
        gr_no = request.form.get("GrNo.")
        phone = request.form.get("PhoneNumber")

        question_1 = request.form.get("Why Do You Want to Join The Club?")
        question_2 = request.form.get("How are You Going to Benefit The Club?")
        question_3 = request.form.get("What are You Aspiring to Achieve from The Club?")

        level = request.form.get("What is Your level of IT Knowledge?")


        new_member = Member(name=name, email=email, clas=clas,gr_no=gr_no, phone=phone, question_1=question_1, question_2=question_2, question_3=question_3, level=level)

        db.session.add(new_member)
        db.session.commit()

        return redirect(url_for("home"))
    return render_template('join.html', title="Join Page")

#admin login route ===========================================
@app.route("/admin", methods=["GET","POST"])
def admin():
    if request.method == "POST":
        user = request.form.get("username")
        password = request.form.get("password")
        next_url = request.form.get("next")

        if username == user and president.password == password:
            global logged_in
            logged_in = True
            session["username"] = user
            return redirect(next_url)
            #return redirect(url_for("home"))
    return render_template('admin_login.html', title="Admin Login")

#members route======================================
@app.route("/members_info", methods=["POST", "GET"])
def members_info():
    global logged_in
    if logged_in == False:
        return redirect(url_for("admin"))
    else:
        # fetching all the registered members from our db       
        new_member = Member.query.all()
        logged_in = not logged_in
        return render_template("members.html", new_member=new_member)

#delete route ==============================================
@app.route("/delete/<int:member_id>")
def delete(member_id):
    # fetching member through its unique id and using that to delete member
    member = Member.query.filter_by(id=member_id).first()
    db.session.delete(member)
    db.session.commit()

    return redirect(url_for("members_info"))



if __name__ == "__main__":
    app.run(debug=True)