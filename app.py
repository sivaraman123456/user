
from flask import Flask,render_template,url_for,request,flash,redirect
import sqlite3

app=Flask(__name__)
app.secret_key="123"
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=="POST":
        name=request.form['user']
        email=request.form['email']
        con=sqlite3.connect('data2.db')
        cur=con.cursor()
        cur.execute("select * from user where Name=? and email=?",(name,email))
        data=cur.fetchone()
        if data:
            return redirect(url_for("view"))
        else:
            flash("username and password invalid","danger")
    return render_template("home.html")
        
@app.route('/view')
def view():
    con=sqlite3.connect('data2.db')
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute("select * from user")
    data=cur.fetchall()

    return render_template("view.html",data=data)


@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        try:
            name=request.form['user']
            email=request.form['email']
            dob=request.form['dob']
            phone=request.form['phone']
            address=request.form['address']
            con=sqlite3.connect("data2.db")
            cur=con.cursor()
            cur.execute(''' create table if not exists user(pid Integer primary key,Name text,
                        DOB date,phone_no integer,email text,address text)''')
            cur.execute('''insert into user(Name,DOB,phone_no,email,address)
                        values(?,?,?,?,?)''',(name,dob,phone,email,address))
            con.commit()
            flash("Register successfully","success")
        except:
            flash("Register unsuccessfull ","danger")
        finally:
            return redirect(url_for('home'))
            con.close()
    return render_template("register.html")

if __name__=='__main__':
    app.run(debug=True)