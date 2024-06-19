from flask import Flask, render_template, url_for, request, redirect, session
import mariadb
import mysql.connector
from werkzeug.security import generate_password_hash,check_password_hash
import ast
from flask_mail import Mail, Message
app=Flask(__name__)
app.secret_key="tajni_kljuc_aplikacije"

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'pythonprimavera@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_email_password'
app.config['MAIL_DEFAULT_SENDER'] = 'pythonprimavera@gmail.com'


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
        
def name():
        upit="select Name from customer where id=%s"
        vrednostUlogovanog=(session.get("ulogovani_user"),)
        kursor.execute(upit,vrednostUlogovanog)
        ime=kursor.fetchall()
        konekcija.commit()
        return (ime)
        
   
@app.route('/',methods=["GET","POST"])

def render_index():
        
        
        return render_template("index.html",ime=name())


@app.route('/contact',methods=["GET","POST"])
def render_contact():
        
        print(name())
        return render_template("contact.html",ime=name())

@app.route('/send_email', methods=["GET","POST"])
def send_email():
                forma = request.form
                user_name = forma['name']
                user_email = forma['email']
                user_message = forma['message']
                print(user_name,user_email,user_message)
                
                subject = f"New contact form submission from {user_name}"
                recipient = 'pythonprimavera@gmail.com'  # Tvoj email gde želiš da primaš poruke
                body = f"Name: {user_name}\nEmail: {user_email}\n\nMessage:\n{user_message}"
                print(body)
                msg = Message(subject, recipients=[recipient])
                msg.body = body

                with app.app_context():
                        mail.send(msg)
                
                return "Email sent successfully!"

@app.route("/logout")
def logout():
       session["ulogovani_user"]=None
       return redirect(url_for("render_index"))

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
        #if ulogovan():
                if request.method=="GET":
                        return render_template("idex.html")

                elif request.method=="POST":
                        forma=request.form
                        hesovana_lozinka=generate_password_hash(forma["Password"])#generise hash lozinku
                        vrednosti=(
                                forma["Name"],
                                forma["Surname"],
                                forma["Email"],
                                hesovana_lozinka,
                                #forma["Password"],
                                forma["Address"]
                               # forma["Number"],
                        )
                        upit=""" INSERT INTO
                                customer(Name,Surname,Email,Password,Address)
                                VALUES(%s,%s,%s,%s,%s)        
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
     
              
            
    categories = ['pizza', 'pasta', 'salad', 'dessert']
    if request.method == 'POST':
        selected_categories = request.form.getlist('category')
        if selected_categories:
            menu_items = MenuItem.query.filter(MenuItem.category.in_(selected_categories)).all()
        else:
            menu_items = MenuItem.query.all()
    else:
        menu_items = MenuItem.query.all()
    
    return render_template('index.html', categories=categories, menu_items=menu_items)

        
@app.route('/menu',methods=["GET","POST"])
def menu():
              if request.method=="GET":
                forma=request.form
                upit= "select * from meni"
                
                kursor.execute(upit)
                menu=kursor.fetchall()
                konekcija.commit()
                #print(menu)

                upit2="select * from meni where Kategorija=%s"\
                #kategorija=forma()
        
                
                return render_template("menu.html",menu=menu, ime=name())
              elif request.method=="POST":
                forma=request.form
                print(forma)

                kategorije=forma.getlist('Kategorija')
                print(kategorije)

                categories = ['']
                query = f"SELECT * FROM meni WHERE Kategorija IN ({','.join(['%s'] * len(kategorije))})"
                kursor.execute(query, kategorije)
                

                #upit= "select * from meni where Kategorija=%s and Cena<=%s"
                #upit= "select * from meni where Cena<=%s"
               # kat=forma["Kategorija"]
                
                #print(kat)
               # vrednost=(kat,forma["Cena"])
               # print(vrednost)
               # kursor.execute(upit, vrednost)
                
                menu=kursor.fetchall()
                konekcija.commit()
        
                

                
                return render_template("menu.html",menu=menu,ime=name())
        
              
                
                
        

app.run(debug=True)