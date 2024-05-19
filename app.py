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
    return render_template("index.html")

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
                upit="SELECT * FROM customer WHERE Name=%s"
                vrednost = (forma["Name"],)
                kursor.execute(upit, vrednost)
                user=kursor.fetchone()
                
                if user !=None:
                        #if user["Password"]==forma["Password"]:#za ne hash lozinke
                        if check_password_hash(user["Password"], forma["Password"]):#za hash lozinke
                        
                                session["ulogovani_user"]=user["ID"]
                                session["rola_user"]=str(user)  

                                #render_template("contact.html")                                      
                                return redirect(url_for("render_index"))
                        else:
                                        
                                        return render_template("login.html")
                else:
                        return render_template("login.html")    

@app.route("/new_user",methods=["GET","POST"])#za registraciju novih korisnika
def new_user():
        if ulogovan():
                if request.method=="GET":
                        return render_template("idex.html")

                elif request.method=="POST":
                        forma=request.form
                        hesovana_lozinka=generate_password_hash(forma["Password"])#generise hash lozinku
                        vrednosti=(
                                forma["Name"],
                                forma["Email"],
                                hesovana_lozinka,
                                #forma["Password"],
                        )
                        upit=""" INSERT INTO
                                customer(Name,Email,Password)
                                VALUES(%s,%s,%s)        
                        """
                
                        #unosi vrednosti u bazu
                        kursor.execute(upit, vrednosti)
                        
                       ## upitUserID="select ID from customer where Name=%s and Surname=%s and Password=%s"
                       # kursor.execute(upitUserID,vrednosti)
                        
                        

                        konekcija.commit()



                        
                        return redirect(url_for("login"))
                else:
                        return redirect(url_for("login"))
        
@app.route('/meni',methods=["GET","POST"])
def meni():
     #  if request.method=="GET":
              upit= "select * from meni where ID=1"
              kursor.execute(upit)
              meni=kursor.fetchall()
              konekcija.commit()
              
              return render_template("meni.html",meni=meni)

        
@app.route('/menu',methods=["GET","POST"])
def menu():
              upit= "select * from meni"
              kursor.execute(upit)
              menu=kursor.fetchall()
              konekcija.commit()
              print(menu)
    
              
              return render_template("menu.html",menu=menu)
        

app.run(debug=True)