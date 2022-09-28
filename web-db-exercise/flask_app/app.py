from flask import Flask, render_template,request,redirect
from flask_mysqldb import MySQL

import MySQLdb.cursors
import json

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'dbcontainer'
app.config['MYSQL_USER'] = 'example_users'
app.config['MYSQL_PASSWORD'] = 'mysql'
app.config['MYSQL_DB'] = 'example'
#app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)



   
@app.route('/', methods=['GET'])
def professor_list_json():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM professor')
    data = cursor.fetchall()
    return json.dumps(data)
@app.route("/home") 
def  home(): 
   return render_template("home.html") 

@app.route("/nuevoprof")
def nuevoprof():
    return render_template("agregar_professor.html")
def obtener():
    professors= []
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT id,first_name,last_name,city,address,salary FROM professor')
    professors = cursor.fetchall()
    return professors 
@app.route('/professors')
def professors():
    professors = obtener()
    return render_template("profesores.html", professors=professors)
    

@app.route('/professorlist', methods=['GET'])
def professor_list():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM professor')
    data = cursor.fetchall()
    return render_template('list.html', profesors=data)


@app.route("/guardarprofessor", methods=["POST"])
def guardar_professor():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    city = request.form["city"]
    address = request.form["address"]
    salary = request.form["salary"]
    cursor .execute('INSERT INTO professor VALUES(NULL, % s, % s, % s, % s,%s)',(first_name, last_name,city,address,salary)) 
    mysql.connection.commit()
    return redirect("/professors")



@app.route("/eliminar_profesor", methods=["POST"])
def eliminar_profesor():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    id= request.form["id"]
    cursor.execute("DELETE FROM professor WHERE id = %s", (id,))
    mysql.connection.commit()
    return redirect("/professors")



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=True)
