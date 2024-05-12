from flask import Flask, render_template, url_for, request, redirect, session
import mariadb
import mysql.connector
from werkzeug.security import generate_password_hash,check_password_hash
import ast

app=Flask(__name__)
app.secret_key="tajni_kljuc_aplikacije"

konekcija=mysql.connector.connect(
    passwd="",
    user="root",
    database="restoran",
    port=3306,
    #pauto_plugin="mysq_narative_password"
)

kursor=konekcija.cursor(dictionary=True)
def ulogovan():
    if "ulogovani_user" in session:
        return True
    else:
        return False
    
#Ova funkcija za role
def rola():
        if ulogovan():
                return ast.literal_eval(session["rola_user"]).pop("rola")
   
@app.route('/',methods=["GET","POST"])

def render_index():
    return render_template("idex.html")

@app.route('/contact',methods=["GET","POST"])
def render_contact():
     return render_template("contact.html")

@app.route("/logout")
def logout():
       session["ulogovani_user"]=None
       return redirect(url_for("login"))

@app.route('/login',methods=["GET","POST"])

def login():
        
        if request.method=="GET":
                
                return render_template("login.html")

        elif request.method=="POST":
                
                forma = request.form
                upit="SELECT * FROM user WHERE ime=%s"
                vrednost = (forma["ime"],)
                kursor.execute(upit, vrednost)
                user=kursor.fetchone()
                
                if user !=None:
                        #if user["lozinka"]==forma["lozinka"]:#za ne hash lozinke
                        if check_password_hash(user["lozinka"], forma["lozinka"]):#za hash lozinke
                        
                                session["ulogovani_user"]=user["id"]
                                session["rola_user"]=str(user)                                     
                                return redirect(url_for("render_index",id=1,idp=1))
                        else:
                                        
                                        return render_template("login.html")
                else:
                        return render_template("login.html")    


app.run(debug=True)