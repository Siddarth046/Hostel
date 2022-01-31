import MySQLdb
import flask
from flask import Flask,render_template,request,redirect,url_for,session
from flask import app
from MySQLdb import cursors
from MySQLdb.cursors import Cursor
from flask_mysqldb import MySQL
app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'GDSiddu@3858'
app.config['MYSQL_DB'] = 'hostel'
mysql = MySQL(app)

@app.route("/",methods=['GET','POST'])
def home():
    return render_template('home.html')

@app.route("/login",methods=['GET','POST'])
def login():
    msg=''
    if request.method=='POST' and 'username' in request.form and 'password' in request.form:
        username=request.form['username']
        password=request.form['password']
        cursor=mysql.connection.cursor()
        cursor.execute('select * from user where username=%s and password=%s',(username,password,))
        check=cursor.fetchall()
        if check:
            return redirect('/')
        else:
            msg="Incorrect username/password"
            return render_template('login.html',msg=msg)
    return render_template('login.html')

@app.route("/Admin-login",methods=['POST','GET'])
def Adm_login():
    msg=''
    if request.method=='POST' and 'username' in request.form and 'password' in request.form:
        username=request.form['username']
        password=request.form['password']
        return redirect('/add-data')
        # if username=="asd" and password=="asd":
        #     return redirect('/add-data')
        # if username=="asd" and password!="asd":
        #     msg="Incorrect Password!"
        #     return render_template('admin_login.html',msg=msg) 
        # if username!="asd" and password=="asd":
        #     msg="Incorrect Username!"
        #     return render_template('admin_login.html',msg=msg)
        # else:
        #     msg="Incorrect Username/Password!"
        #     return render_template('admin_login.html',msg=msg)
    return render_template('admin_login.html')

@app.route('/st-details',methods=['GET','POST'])
def ditails():
    cursor=mysql.connection.cursor()
    if request.method=='POST':
        # sid=request.form['sid']
        # cursor.execute("select * from student where sid=%s",(sid,))
        fname=request.form['Fname']
        lname=request.form['Lname']
        cursor.execute("select * from student where fname=%s and lname=%s",(fname,lname,))
        studentd=cursor.fetchall()
        if studentd:
            return render_template('details.html',studentd=studentd)
    else:
        # query=("select * from student")
        cursor.execute("select * from student")
        students=cursor.fetchall()
        return render_template('search.html',students=students)

@app.route("/add-data",methods=['GET','POST'])
def add_data():
    msg=''
    if request.method=='POST':
        fname=request.form['fname']
        lname=request.form['lname']
        room=request.form['Room']
        dept=request.form['Dept']
        year=request.form['Year']
        cursor=mysql.connection.cursor()
        cursor.execute(
            "insert into student(fname,lname,room_no,department,year) values(%s,%s,%s,%s,%s)",(fname,lname,room,dept,year)
        )
        msg="One Data Added...!"
        mysql.connection.commit()
        cursor.close()
        return render_template('add_data.html',msg=msg)
    return render_template('add_data.html')

@app.route("/remove",methods=['GET','POST'])
def remove():
    msg=''
    if request.method=='POST':
        fname=request.form['fname']
        lname=request.form['lname']
        cursor=mysql.connection.cursor()
        if fname and lname:
            cursor.execute(
                "delete from student where fname=%s and lname=%s",(fname,lname)
            )
            msg='One Data Removed....!'
        else:
            msg='Enter Data!'
        mysql.connection.commit()
        cursor.close()
        return render_template('/remove.html',msg=msg)
    return render_template('/remove.html')

@app.route("/update",methods=['GET','POST'])
def update():
    msg=''
    if request.method=='POST':
        fname=request.form['fname']
        lname=request.form['lname']
        newfname=request.form['newfname']
        newlname=request.form['newlname']
        room=request.form['Room']
        dept=request.form['Dept']
        year=request.form['Year']
        cursor=mysql.connection.cursor()
        if newfname or newlname or room or dept or year:
            if newfname:
                cursor.execute(
                    "update student set fname=%s where fname=%s and lname=%s",(newfname,fname,lname,)
                )
            if newlname:
                cursor.execute(
                    "update student set lname=%s where fname=%s and lname=%s",(newlname,fname,lname,)
                )
            if room:
                cursor.execute(
                    "update student set room_no=%s where fname=%s and lname=%s",(room,fname,lname,)
                )
            if dept:
                cursor.execute(
                    "update student set department=%s where fname=%s and lname=%s",(dept,fname,lname,)
                )
            if year:
                cursor.execute(
                    "update student set year=%s where fname=%s and lname=%s",(year,fname,lname,)
                )
            msg='Updated Successfully you can check in students details..!'
        else:
            msg="Enter data to be modified..!"
        mysql.connection.commit()
        cursor.close()
        return render_template('/update.html',msg=msg)
    return render_template('/update.html')

@app.route('/contact-us')
def contact_us():
    return render_template('Contact_Us.html')

app.run(debug=True)