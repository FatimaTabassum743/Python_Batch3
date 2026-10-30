from flask import Flask,render_template,redirect,request
import sqlite3

app=Flask(__name__)
def get_db(): 
  conn = sqlite3.connect("users.db") 
  conn.row_factory = sqlite3.Row 
  return conn
# create table (run once) 
def create_table(): 
   conn = get_db() 
   conn.execute(""" 
CREATE TABLE IF NOT EXISTS users ( 
id INTEGER PRIMARY KEY AUTOINCREMENT, 
name TEXT, 
role TEXT 
) 
""") 
   conn.commit() 
   conn.close() 
create_table() 

@app.route("/" , methods=["GET"])
def index():
   conn=get_db()
   users=conn.execute("SELECT * FROM users").fetchall()
   return render_template("index.html",users=users)
@app.route("/add", methods=["GET","POST"])
def add():
   if request.method=="POST":
      name=request.form["name"]
      role=request.form["role"]
      conn = get_db() 
      conn.execute("INSERT INTO users (name, role) VALUES (?, ?)", (name, role)) 
      conn.commit() 
      conn.close() 
      return redirect("/")
   return render_template("add.html") 
@app.route("/delete/<int:id>") 
def delete(id):
   conn=get_db()
   conn.execute("DELETE FROM users WHERE id=?", (id,)) 
   conn.commit()
   conn.close()
   return redirect("/")
if __name__=="__main__":
   app.run(debug=True) 
   