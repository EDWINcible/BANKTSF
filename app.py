from flask import Flask, flash,render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

import MySQLdb.cursors

app = Flask(__name__)

app.secret_key = 'TIGER'

app.config['MYSQL_HOST'] = 'sql6.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql6399998'
app.config['MYSQL_PASSWORD'] = '8sf2YbwRpb'
app.config['MYSQL_DB'] = 'sql6399998'

mysql = MySQL(app)

@app.route("/bankhome")
def home():
    return render_template('index.html')

@app.route("/customer")
def cust():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM customers")
    cdata=cursor.fetchall()
    return render_template('customer.html', data=cdata)

@app.route("/profile", methods=['GET', 'POST'])
def prof():
    if request.method == 'POST' and 'cid'in request.form and 'cname' in request.form  and 'cemail' in request.form  and 'cbal' in request.form:
        user=request.form['cname']
        id=request.form['cid']
        email=request.form['cemail']
        bal=request.form['cbal']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT name,id FROM customers WHERE id=%s",(id,))
        pid=cursor.fetchall()
        return render_template('profile1.html',value=pid,value1=user,value2=id,value3=email,value4=bal)

  
@app.route("/transactions", methods=['GET', 'POST'])
def transact():
    if request.method == 'POST' and 'reciever'in request.form and 'amount' in request.form and 'pname' in request.form and 'pbal' in request.form:
        reciever=request.form['reciever']
        amount=float(request.form['amount'])
        amount1=float(request.form['amount'])
        sender=request.form['pname']
        scurrbal=float(request.form['pbal'])
        cursor = mysql.connection.cursor()
        sbal=scurrbal-amount
        cursor.execute("SELECT curr_bal FROM customers WHERE name=%s",(reciever,))
        rcurr_bal=cursor.fetchone()
        rcurrbal=float(rcurr_bal[0])
        rbal=rcurrbal+amount1
        print(rcurrbal)
        print(rbal)
        cursor.execute("SELECT * FROM transactions WHERE sname=%s",(sender,))
        
        tid=cursor.fetchall()
        if scurrbal>=amount:
            cursor.execute("UPDATE customers SET curr_bal=%s where name=%s", (rbal, reciever,))
            cursor.execute("UPDATE customers SET curr_bal=%s where name=%s", (sbal, sender,))           
            cursor.execute("INSERT INTO transactions(sname,rname,amount) VALUES ( %s, %s,%s)", (sender, reciever, amount,))
            mysql.connection.commit()
        else:
            return "Insufficient Funds!"  
        return redirect(url_for('transact2'))
        #return render_template('transact.html',value=tid)

@app.route("/transactfinal",methods=['GET', 'POST'])
def transact2():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM transactions ORDER BY time desc")
    cdata=cursor.fetchall()
    return render_template('transact.html', value=cdata)  
  

'''
@app.route("/transactions", methods=['GET', 'POST'])
def transact():
    if request.method == 'POST' and 'reciever'in request.form and 'amount' in request.form and 'pname' in request.form and 'pbal' in request.form:
        reciever=request.form['reciever']
        amount=float(request.form['amount'])
        sender=request.form['pname']
        scurrbal=float(request.form['pbal'])
        cursor = mysql.connection.cursor()
        sbal=scurrbal-amount
        cursor.execute("SELECT curr_bal FROM customers WHERE name=%s",(reciever,))
        rcurr_bal=cursor.fetchone()
        rcurrbal=float(rcurr_bal[0])
       # rbal=rcurrbal+amount
        
        print(rcurrbal)
        print(scurrbal)
        print(sender)
        print(reciever)
        #print(rbal)


        cursor.execute("SELECT * FROM transactions WHERE sname=%s",(sender,))
        
        tid=cursor.fetchall()
        if scurrbal>=amount:
            #tbal=rbal
            cursor.execute("UPDATE customers SET curr_bal=%s where name=%s", (rcurrbal+amount, reciever,))
            cursor.execute("UPDATE customers SET curr_bal=%s where name=%s", (sbal, sender,))           
            cursor.execute("INSERT INTO transactions(sname,rname,amount) VALUES ( %s, %s,%s)", (sender, reciever, amount,))
            mysql.connection.commit()
        else:
            return "Insufficient Funds!"  
        return redirect(url_for('tp')) 
    #return render_template('transact.html',value=tid)

@app.route("/transfer")
def tp():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM transactions")
    cdata=cursor.fetchall()
    print(value)
    return render_template('transact.html', value=cdata)    
'''

if __name__=="__main__":
    app.run(debug=True);  

 
