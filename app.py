from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL, MySQLdb
from flask_cors import CORS
import bcrypt, os


app = Flask(__name__)
cors = CORS(app, resource={r"/*":{"origins": "*"}})
app.secret_key = "^A%DJAJU^JJ123"


app.config['MYSQL_HOST'] = 'sql10.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql10325576'
app.config['MYSQL_PASSWORD'] = 'Dqm26RMtFv'
app.config['MYSQL_DB'] = 'sql10325576'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


@app.route('/')
def home():
    return render_template("home.html")


def main():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM users WHERE email=%s",(email,))
        user = cur.fetchone()
        cur.close()

        if len(user) > 0:
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                session['name'] = user['name']
                session['email'] = user['email']
                return render_template("home.html")
            else:
                return "Error, senha e email errados !"
        else:
            return "Error, usuário não encontrado"
    else:
        return render_template("login.html")


@app.route('/logout')
def logout():
    session.clear()
    return render_template("home.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, password) VALUES (%s,%s,%s)", (name,email,hash_password,))
        mysql.connection.commit()
        session['name'] = request.form['name']
        session['email'] = request.form['email']
        return redirect(url_for('home'))


if __name__ == '__main__':
    main()
