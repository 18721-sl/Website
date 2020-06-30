from flask import Flask,g,render_template,request,redirect

import sqlite3

app = Flask(__name__)

DATABASE = 'database.db'

def get_db():
    db= getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database' , None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    cursor = get_db().cursor()
    sql = 'SELECT * FROM Video'
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("Garage Rock Public Library.html" , results=results)

@app.route('/add', methods=['GET','POST'])
def add():
    if request.method == 'POST':
        cursor = get_db().cursor()
        new_Video = request.form['item_Video']
        new_comment = request.form['item_comment']
        sql = 'INSERT INTO comment(video,comment) VALUES (?,?)'
        cursor.execute(sql,(new_Video,new_comment))
        get_db().commit()
    return redirect('/')

@app.route('/delete', methods=['GET','POST'])
def delete():
    if request.method =='POST':
        cursor = get_db().cursor()
        id = int(request.form['item_Video'])
        sql = 'DELETE FROM Video WHERE id=?'
        cursor.execute(sql,(id,))
        get_db().commit()
    return redirect('/')

if __name__ ==   '__main__':
    app.run(debug=True)
