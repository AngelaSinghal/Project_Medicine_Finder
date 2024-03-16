from flask import Flask,render_template,request,redirect,url_for,session
import pymysql
import time
import os

from werkzeug.utils import secure_filename

from mylib import *



app=Flask(__name__)

app.config['UPLOAD_FOLDER'] = './static/photos'
app.secret_key="super secret key"

@app.route("/",methods=["GET","POST"])
def welcome():
    if(request.method=="POST"):
        med_name=request.form["T1"]
        cur=db_connection()
        s="select * from medicine_medical where med_name like '%"+med_name+"%'"
        cur.execute(s)
        a=cur.rowcount
        if(a>0):
            data=cur.fetchall()
            return render_template("home.html",data=data,nm=med_name)
        else:
            return render_template("home.html",msg="no data found")
    else:
        return render_template("home.html")




@app.route("/admin_reg",methods=["GET","POST"])
def admin_reg():
    if ("usertype" in session):
        ut = session["usertype"]
        if (ut == "admin"):
            if (request.method == "GET"):
                return render_template("admin_reg.html")
            else:  # post
                # grab the data from form
                c = request.form["A1"]
                d = request.form["A2"]
                e = request.form["A3"]
                f = request.form["A4"]
                g = request.form["A5"]
                h = request.form["A6"]
                usertype = "admin"
                msg = ""
                if (g != h):
                    x = "password not matched"
                else:
                    pl = pymysql.connect(host="localhost", user="root", passwd="", port=3306, db="aarav",
                                         autocommit=True)
                    rac = pl.cursor()
                    t1 = "insert into admindata values ('" + c + "','" + d + "','" + e + "','" + f + "')"
                    t2 = "insert into logindata values ('" + f + "','" + g + "','" + usertype + "')"
                    rac.execute(t1)
                    m1 = rac.rowcount
                    rac.execute(t2)
                    m2 = rac.rowcount
                    if (m1 == 1 and m2 == 1):
                        msg = "Data saved and login created"
                    elif (m1 == 1):
                        msg = "Error : Only data is saved"
                    elif (m2 == 1):
                        msg = "Error : Only login is created"
                    else:
                        msg = "Error : No data is saved and no login is created"
                return render_template("admin_reg.html", x=msg)
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/show_admin")
def show_admin():
    if ("usertype" in session):
        ut = session["usertype"]
        if (ut == "admin"):
            con = pymysql.connect(host="localhost", user="root", port=3306, passwd="", db="aarav", autocommit=True)
            cur = con.cursor()
            s4 = "select * from admindata"
            cur.execute(s4)
            a = cur.rowcount

            if (a > 0):
                data = cur.fetchall()

                return render_template("show_admin.html", vgt=data)
            else:
                return render_template("show_admin.html", msg="NO DATA FOUND")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


@app.route("/medical_reg", methods=["POST","GET"])
def medical_reg():
    if ("usertype" in session):
        ut = session["usertype"]
        if (ut == "admin"):
            if (request.method == "GET"):
                return render_template("medical_reg.html")
            else:  # post
                # grab the data
                nm = request.form["T1"]
                ow = request.form["T2"]
                ln = request.form["T3"]
                ad = request.form["T4"]
                lm = request.form["T5"]
                contact = request.form["T6"]
                email = request.form["T7"]
                p = request.form["T8"]
                con = request.form["T9"]
                usertype = "medical"
                msg = ""
                if (p != con):
                    msg = "password not matched"
                else:
                    cn = pymysql.connect(host="localhost", user="root", port=3306, passwd="", db="aarav",
                                         autocommit=True)
                    cur = cn.cursor()
                    s1 = "insert into medical_data values('" + nm + "','" + ow + "','" + ln + "','" + ad + "','" + lm + "','" + contact + "','" + email + "')"
                    s2 = "insert into logindata values('" + email + "','" + p + "','" + usertype + "')"
                    cur.execute(s1)
                    a = cur.rowcount
                    cur.execute(s2)
                    b = cur.rowcount
                    if (a == 1 and b == 1):
                        msg = "data saved and login created successfully"
                    elif (a == 1):
                        msg = "error:no login values inserted"
                    elif (b == 1):
                        msg = "error:no medical data values inserted"
                return render_template("medical_reg.html", angela=msg)
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


@app.route("/show_medical")
def show_medical():
    if ("usertype" in session):
        ut = session["usertype"]
        if (ut == "admin"):
            con = pymysql.connect(host="localhost", user="root", port=3306, passwd="", db="aarav", autocommit=True)
            cur = con.cursor()
            s2 = "select * from medical_data"
            cur.execute(s2)
            a = cur.rowcount
            if (a > 0):
                data = cur.fetchall()
                return render_template("show_medical.html", vgt=data)
            else:
                return render_template("show_medical.html", msg="NO DATA FOUND")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))




@app.route("/edit_medical",methods=["POST","GET"])
def edit_medical():
    if ("usertype" in session):
        ut = session["usertype"]
        if (ut == "admin"):
            if (request.method == "POST"):
                email = request.form["H1"]
                con = pymysql.connect(host="localhost", user="root", port=3306, passwd="", db="aarav", autocommit=True)
                cur = con.cursor()
                s3 = " select * from medical_data where email ='" + email + "'"
                cur.execute(s3)
                a = cur.rowcount
                if (a == 1):
                    data = cur.fetchone()
                    return render_template("edit_medical.html", vgt=data)
                else:
                    return render_template("edit_medical.html", msg="NO DATA FOUND")
            else:
                return redirect(url_for("show_medical"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/edit_medical1",methods=["GET","POST"])
def edit_medical1():
    if ("usertype" in session):
        ut = session["usertype"]
        if (ut == "admin"):
            if (request.method == "POST"):
                nm = request.form["T1"]
                ow = request.form["T2"]
                ln = request.form["T3"]
                ad = request.form["T4"]
                lm = request.form["T5"]
                contact = request.form["T6"]
                email = request.form["T7"]
                con = pymysql.connect(host="localhost", user="root", port=3306, passwd="", db="aarav", autocommit=True)
                cur = con.cursor()
                s4 = "update medical_data  set name='" + nm + "' ,owner='" + ow + "',lno='" + ln + "' ,address='" + ad + "',landmark='" + lm + "',contact='" + contact + "' where email='" + email + "'"
                cur.execute(s4)
                a = cur.rowcount
                if (a == 1):
                    return render_template("show_medical1.html", msg="data saved succesfully")
                else:
                    return render_template("show_medical1.html", msg="error")
            else:
                return redirect(url_for("show_medical"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


@app.route("/delete_medical",methods=["POST","GET"])
def delete_medical():
    if ("usertype" in session):
        ut = session["usertype"]
        if (ut == "admin"):
            if (request.method == "POST"):
                email = request.form["H1"]
                con = pymysql.connect(host="localhost", user="root", port=3306, passwd="", db="aarav", autocommit=True)
                cur = con.cursor()
                sql = "select * from medical_data where email='" + email + "'"
                cur.execute(sql)
                a = cur.rowcount
                if (a == 1):
                    data = cur.fetchone()
                    return render_template("delete_medical.html", vgt=data)
            else:
                return redirect(url_for("show_medical"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


@app.route("/delete_medical1",methods=["POST","GET"])
def delete_medical1():
    if ("usertype" in session):
        ut = session["usertype"]
        if (ut == "admin"):
            if (request.method == "POST"):
                email = request.form["T7"]
                con = pymysql.connect(host="localhost", user="root", port=3306, passwd="", db="aarav", autocommit=True)
                cur = con.cursor()
                sql = "delete * from medical_data where email='" + email + "'"
                cur.execute(sql)
                a = cur.rowcount
                if (a == 1):
                    return render_template("delete_medical1.html", msg="data deleted")
            else:
                return redirect(url_for("show_medical"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


@app.route("/login",methods=["GET","POST"])
def login():
    if(request.method=="POST"):
        e1=request.form["T1"]
        password=request.form["T2"]
        con = pymysql.connect(host="localhost", user="root", port=3306, passwd="", db="aarav", autocommit=True)
        cur = con.cursor()

        s="select  * from logindata where user_id='"+e1+"' and password='"+password+"'"
        cur.execute(s)
        c=cur.rowcount
        if(c==1):
            data=cur.fetchone()
            kt=data[2] #fetch user type from result
            #create session
            session["email"]=e1
            session["usertype"]=kt
            #send to page
            if(kt=="admin"):
                return redirect(url_for("admin_home"))
            elif(kt=="medical"):
                return redirect(url_for("medical_home"))
            else:
                return render_template("login.html",msg="contact to admin")
        else:
            return render_template("login.html",msg="either email or password is incorrect")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    #check session
    if("email" in session):
        session.pop("email",None)
        session.pop("usertype",None)
        return redirect(url_for("welcome"))
    else:
        return redirect(url_for("welcome"))

@app.route("/auth_error")
def auth_error():
    return render_template("auth_error.html")

@app.route("/admin_home")
def admin_home():
    #check session
    if("usertype" in session):
        ut=session["usertype"]
        e1=session["email"]
        if(ut=="admin"):
            photo=check_photo(e1)
            return render_template("admin_home.html",e1=e1,photo=photo)
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/medical_home")
def medical_home():
    #check session
    if("usertype" in session):
        ut=session["usertype"]
        e1 = session["email"]
        if(ut=="medical"):
            photo = check_photo(e1)
            return render_template("medical_home.html",e1=e1,photo=photo)
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


@app.route("/change_pass" ,methods=["GET","POST"])
def change_pass():
    if("usertype" in session):
        ut=session["usertype"]
        e1=session["email"]
        if(ut=="medical"):
            if(request.method=="POST"):
                old_pass=request.form["A"]
                new_pass = request.form["B"]
                con_pass = request.form["C"]
                msg=""
                if(new_pass!=con_pass):
                    return render_template("medical_change_pass.html",msg="password does not match")
                else:
                    con = pymysql.connect(host="localhost", user="root", port=3306, passwd="", db="aarav",
                                          autocommit=True)
                    cur = con.cursor()
                    s="update logindata set password='"+new_pass+"' where user_id='"+e1+"' and password ='"+old_pass+"'"
                    cur.execute(s)
                    a=cur.rowcount
                    if(a==1):
                        data="password saved successfully"
                        return render_template("medical_change_pass.html",msg=data)
                    else:
                        return render_template("medical_change_pass.html",msg="invalid old password")
            else:
                return render_template("medical_change_pass.html")

        else:
            return redirect(url_for("auth_error"))

    else:
        return redirect(url_for("auth_error"))

@app.route("/change_pass_a" ,methods=["GET","POST"])
def change_pass_a():
    if ("usertype" in session):
        ut = session["usertype"]
        e1 = session["email"]
        if (ut == "admin"):
            if (request.method == "POST"):
                old_pass = request.form["A"]
                new_pass = request.form["B"]
                con_pass = request.form["C"]
                msg = ""
                if (new_pass != con_pass):
                    return render_template("admin_change_pass.html", msg="password does not match")
                else:
                    con = pymysql.connect(host="localhost", user="root", port=3306, passwd="", db="aarav",
                                          autocommit=True)
                    cur = con.cursor()
                    s = "update logindata set password='" + new_pass + "' where user_id='" + e1 + "' and password ='" + old_pass + "'"
                    cur.execute(s)
                    a = cur.rowcount
                    if (a == 1):
                        data = "password saved successfully"
                        return render_template("admin_change_pass.html", msg=data)
                    else:
                        return render_template("admin_change_pass.html", msg="invalid old password")
            else:
                return render_template("admin_change_pass.html")

        else:
            return redirect(url_for("auth_error"))

    else:
        return redirect(url_for("auth_error"))

@app.route("/medical_profile",methods=["GET","POST"])
def medical_profile():
    if("usertype" in session):
        ut=session["usertype"]
        e1=session["email"]
        if(ut=="medical"):
            con = pymysql.connect(host="localhost", user="root", port=3306, passwd="", db="aarav",
                                  autocommit=True)

            if(request.method=="POST"):
                nm=request.form["T1"]
                ow = request.form["T2"]
                lno = request.form["T3"]
                add = request.form["T4"]
                land = request.form["T5"]
                contact = request.form["T6"]


                cur=con.cursor()
                s1="update medical_data set name='"+nm+"',owner='"+ow+"',lno='"+lno+"',address='"+add+"',landmark='"+land+"',contact='"+contact+"' where email='"+e1+"'"
                cur.execute(s1)
                a=cur.rowcount
                if(a>0):
                    return render_template("medical_profile.html",msg="data changes are saved")
                else:
                    return render_template("medical_profile.html", msg="data changes are not  saved")

            else:
                cur=con.cursor()
                sql="select * from medical_data where email='"+e1+"'"
                cur.execute(sql)
                a=cur.rowcount
                if(a==1):
                    data=cur.fetchone()
                    return render_template("medical_profile.html",data=data)
                else:
                    return render_template("medical_profile.html", data="no data")

        else:
            return redirect(url_for("auth_error"))

    else:
        return redirect(url_for("auth_error"))





@app.route("/admin_profile",methods=["GET","POST"])
def admin_profile():
    if ("usertype" in session):
        ut = session["usertype"]
        e1 = session["email"]
        if (ut == "admin"):
            con = pymysql.connect(host="localhost", user="root", port=3306, passwd="", db="aarav",
                                  autocommit=True)
            if (request.method == "POST"):
                nm=request.form["T1"]
                add=request.form["T2"]
                contact=request.form["T3"]
                s1="update admindata set admin_name='"+nm+"',address='"+add+"' ,contact='"+contact+"' where email='"+e1+"'"
                cur=con.cursor()
                cur.execute(s1)
                a=cur.rowcount
                if(a>0):
                    return render_template("admin_profile.html",msg="data changes are saved")
                else:
                    return render_template("admin_profile.html",msg="data changes are not saved")

            else:
                s2="select * from admindata where email='"+e1+"' "
                cur=con.cursor()
                cur.execute(s2)
                a=cur.rowcount
                if(a==1):
                    data=cur.fetchone()
                    return render_template("admin_profile.html",data=data)
                else:
                    return render_template("admin_profile.html", data="NO DATA FOUND")

        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


@app.route("/medicine_reg" ,methods=["GET","POST"])
def medicine_reg():
    if ("usertype" in session):
        ut = session["usertype"]
        if (ut == "medical"):
            if (request.method == "GET"):
                return render_template("medicine_reg.html")
            else:  # post
                # grab the data from form
                c = request.form["T1"]
                d = request.form["T2"]
                e = request.form["T3"]
                f = request.form["T4"]
                g = request.form["T5"]
                h = request.form["T6"]
                i = request.form["T7"]
                msg = ""

                pl = pymysql.connect(host="localhost", user="root", passwd="", port=3306, db="aarav", autocommit=True)
                rac = pl.cursor()
                t1 = "insert into medicine_data values ('" + c + "','" + d + "','" + e + "','" + f + "','" + g + "','" + h + "','" + i + "')"

                rac.execute(t1)
                m1 = rac.rowcount

                if (m1 == 1):
                    msg = "Data saved "
                else:
                    msg = "Error :  data is not  saved"

                return render_template("medicine_reg.html", msg=msg)

        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


@app.route("/show_medicine")
def show_medicine():
    if ("usertype" in session):
        ut = session["usertype"]
        if (ut == "medical"):
            if ("usertype" in session):
                ut = session["usertype"]
                e1 = session["email"]
                if (ut == "medical"):
                    con = pymysql.connect(host="localhost", user="root", port=3306, passwd="", db="aarav",
                                          autocommit=True)
                    cur = con.cursor()
                    s2 = "select * from medicine_data where email_medical='" + e1 + "'"
                    cur.execute(s2)
                    a = cur.rowcount
                    if (a > 0):
                        data = cur.fetchall()
                        return render_template("show_medicine.html", vgt=data)
                    else:
                        return render_template("show_medicine.html", msg="NO DATA FOUND")
                else:
                    return redirect(url_for("auth_error"))
            else:
                return redirect(url_for("auth_error"))

        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))




@app.route("/edit_medicine",methods=["POST","GET"])
def edit_medicine():
    if ("usertype" in session):
        ut = session["usertype"]
        if (ut == "medical"):
            if (request.method == "POST"):
                med_id = request.form["H1"]
                con = pymysql.connect(host="localhost", user="root", port=3306, passwd="", db="aarav", autocommit=True)
                cur = con.cursor()
                s3 = " select * from medicine_data where med_id ='" + med_id + "'"
                cur.execute(s3)
                a = cur.rowcount
                if (a == 1):
                    data = cur.fetchone()
                    return render_template("edit_medicine.html", vgt=data)
                else:
                    return render_template("edit_medicine.html", msg="NO DATA FOUND")
            else:
                return redirect(url_for("show_medicine"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/edit_medicine1",methods=["GET","POST"])
def edit_medicine1():
    if ("usertype" in session):
        ut = session["usertype"]
        if (ut == "medical"):
            if (request.method == "POST"):
                med_id = request.form["T1"]
                med_name = request.form["T2"]
                comp = request.form["T3"]
                lno = request.form["T4"]
                p = request.form["T5"]
                d = request.form["T6"]
                con = pymysql.connect(host="localhost", user="root", port=3306, passwd="", db="aarav", autocommit=True)
                cur = con.cursor()
                s4 = "update medicine_data  set med_name='" + med_name + "' ,company='" + comp + "',l_no='" + lno + "' ,price='" + p + "',details='" + d + "' where med_id='" + med_id + "'"
                cur.execute(s4)
                a = cur.rowcount
                if (a == 1):
                    return render_template("show_medicine.html", msg="data saved succesfully")
                else:
                    return render_template("show_medicine.html", msg="error")
            else:
                return redirect(url_for("show_medicine"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


@app.route("/delete_medicine",methods=["POST","GET"])
def delete_medicine():
    if ("usertype" in session):
        ut = session["usertype"]
        if (ut == "medical"):
            if ("usertype" in session):
                ut = session["usertype"]
                if (ut == "medical"):
                    if (request.method == "POST"):
                        mi = request.form["H1"]
                        con = pymysql.connect(host="localhost", user="root", port=3306, passwd="", db="aarav",
                                              autocommit=True)
                        cur = con.cursor()
                        sql = "select * from medicine_data where med_id='" + mi + "'"
                        cur.execute(sql)
                        a = cur.rowcount
                        if (a == 1):
                            data = cur.fetchone()
                            return render_template("delete_medicine.html", vgt=data)
                    else:
                        return redirect(url_for("show_medicine"))
                else:
                    return redirect(url_for("auth_error"))
            else:
                return redirect(url_for("auth_error"))


        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))



@app.route("/delete_medicine1",methods=["POST","GET"])
def delete_medicine1():
    if ("usertype" in session):
        ut = session["usertype"]
        if (ut == "medical"):
            if ("usertype" in session):
                ut = session["usertype"]
                if (ut == "medical"):
                    if (request.method == "POST"):
                        mi = request.form["T1"]
                        con = pymysql.connect(host="localhost", user="root", port=3306, passwd="", db="aarav",
                                              autocommit=True)
                        cur = con.cursor()
                        sql = "delete  from medicine_data where med_id='" + mi + "'"
                        cur.execute(sql)
                        a = cur.rowcount
                        if (a == 1):
                            return render_template("delete_medicine1.html", msg="data deleted")
                    else:
                        return redirect(url_for("show_medicine"))
                else:
                    return redirect(url_for("auth_error"))
            else:
                return redirect(url_for("auth_error"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/show_medical_user")
def show_medical_user():

            con = pymysql.connect(host="localhost", user="root", port=3306, passwd="", db="aarav", autocommit=True)
            cur = con.cursor()
            s2 = "select * from medical_data"
            cur.execute(s2)
            a = cur.rowcount
            if (a > 0):
                data = cur.fetchall()
                return render_template("show_medical_user.html", vgt=data)
            else:
                return render_template("show_medical_user.html", msg="NO DATA FOUND")

@app.route("/adminphoto")
def adminphoto():
    return render_template("photoupload_admin.html")


@app.route("/adminphoto1",methods=["GET","POST"])
def adminphoto1():
    if('usertype' in session):
        ut=session["usertype"]
        e1=session["email"]
        if(ut=='admin'):
            if(request.method=="POST"):
                file=request.files['F1']
                if (file):
                    path=os.path.basename(file.filename)
                    file_ext=os.path.splitext(path)[1][1:]
                    filename=str(int(time.time()))+'.' +file_ext
                    filename=secure_filename(filename)
                    con = pymysql.connect(host="localhost", user="root", passwd="", port=3306, db="aarav",
                                          autocommit=True)
                    cur = con.cursor()
                    sql="insert into photodata values ('"+e1+"','"+filename+"')"
                    try:
                        cur.execute(sql)
                        n=cur.rowcount
                        if(n==1):
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                            return render_template('photoupload_admin1.html',result="success")
                        else:
                            return render_template('photoupload_admin1.html', result="failure")

                    except:
                        return render_template("photoupload_admin1.html",result="duplicate")

                else:
                    return render_template('photoupload_admin.html')
            else:
                return redirect(url_for("adminphoto"))
        else:
            return redirect(url_for("auth_error"))

    else:
        return redirect(url_for("auth_error"))

@app.route("/medicalphoto")
def medicalphoto():
    return render_template("photoupload_medical.html")

@app.route("/medicalphoto1",methods=["GET","POST"])
def medicalphoto1():
    if('usertype' in session):
        ut=session["usertype"]
        e1=session["email"]
        if(ut=='medical'):
            if(request.method=="POST"):
                file = request.files['F1']
                if (file):
                    path=os.path.basename(file.filename)
                    file_ext=os.path.splitext(path)[1][1:]
                    filename=str(int(time.time()))+'.' +file_ext
                    filename=secure_filename(filename)
                    con = pymysql.connect(host="localhost", user="root", passwd="", port=3306, db="aarav",
                                          autocommit=True)
                    cur = con.cursor()
                    sql="insert into photodata values ('"+e1+"','"+filename+"')"
                    try:
                        cur.execute(sql)
                        n=cur.rowcount
                        if(n==1):
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                            return render_template('photoupload_medical1.html',result="success")
                        else:
                            return render_template('photoupload_medical1.html', result="failure")

                    except:
                        return render_template("photoupload_medical1.html",result="duplicate")

                else:
                    return render_template('photoupload_medical.html')
            else:
                return redirect(url_for("medicalphoto"))
        else:
            return redirect(url_for("auth_error"))

    else:
        return redirect(url_for("auth_error"))


@app.route("/admin_change_photo")
def admin_change_photo():
    if('usertype' in session):
        ut=session["usertype"]
        e1=session["email"]
        if(ut=='admin'):
            photo=check_photo(e1)
            con = pymysql.connect(host="localhost", user="root", passwd="", port=3306, db="aarav",
                                  autocommit=True)
            cur = con.cursor()
            s1 = "delete from photodata where email='"+e1+"'"
            cur.execute(s1)
            n = cur.rowcount
            if(n>0):
                os.remove("./static/photos/"+ photo)
                return render_template("admin_change_photo.html",data="success")
            else:
                return render_template("admin_change_photo.html", data="failure")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route("/medical_change_photo")
def medical_change_photo():
    if('usertype' in session):
        ut=session["usertype"]
        e1=session["email"]
        if(ut=='medical'):
            photo=check_photo(e1)
            con = pymysql.connect(host="localhost", user="root", passwd="", port=3306, db="aarav",
                                  autocommit=True)
            cur = con.cursor()
            s1 = "delete from photodata where email='"+e1+"'"
            cur.execute(s1)
            n = cur.rowcount
            if(n>0):
                os.remove("./static/photos/"+ photo)
                return render_template("medical_change_photo.html",data="success")
            else:
                return render_template("medical_change_photo.html", data="failure")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))






if(__name__=="__main__"):
    app.run(debug=True)
