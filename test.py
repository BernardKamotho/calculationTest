from flask import Flask, render_template, request, redirect
import pymysql

app = Flask(__name__)  

def db_connection():
    return pymysql.connect(host='localhost', user='root', password='', database='calculations')

@app.route('/test', methods=['POST', 'GET'])
def test(): 
    if request.method == 'GET':
        return render_template('test.html')
    else:
        valueA = int(request.form['a'])
        valueB = int(request.form['b'])
        valueC = int(request.form['c'])
        valueD = int(request.form['d'])

        calc = (valueA**2 + valueB**2) - (valueC * valueD)

        connection = db_connection()
        sql = "INSERT INTO `tests`(`test_value_A`, `test_value_B`, `test_value_C`, `test_value_D`, `text_Answer`) VALUES (%s, %s, %s, %s, %s)" 

        data = (valueA, valueB, valueC, valueD, calc)

        cursor = connection.cursor()
        cursor.execute(sql, data)
        connection.commit()    

       
       
        return render_template('test.html' , answer = calc)
    

@app.route("/delete/<test_id>", methods=["POST"])
def delete(test_id):
    connection = db_connection()
    cursor = connection.cursor()

    # structure the delete sql 
    sql = "DELETE FROM `tests` WHERE `tests`.`test_id` = %s"
    cursor.execute(sql, test_id)
    connection.commit()

    return redirect("/result")
    
@app.route('/result')
def result():
     # fetching all the details from the test table
    connection = db_connection()
    sql2 = "SELECT * FROM `tests`"
    cursor2 = connection.cursor()
    cursor2.execute(sql2)
    allCalculations = cursor2.fetchall()

    return render_template('result.html', calculations = allCalculations)




app.run(debug=True)  