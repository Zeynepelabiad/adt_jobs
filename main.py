from flask import Flask, render_template, request, redirect, url_for, flash
from flask import Flask, render_template, session
from flask_mysqldb import MySQL
import MySQLdb
from flaskext.mysql import MySQL
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, render_template
from io import BytesIO
import base64




app = Flask(__name__)
app.secret_key="super secret key"

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
app.config['MYSQL_DATABASE_PORT'] = 8889
app.config['MYSQL_DATABASE_DB'] = 'adt_jobs'

mysql = MySQL(app)


jobs=pd.read_csv("Export.csv")
jobs_groupby=jobs.groupby(['state']).agg({'company_score':['mean']})
jobs_groupby=jobs_groupby.reset_index()
states=jobs_groupby.melt(id_vars="state")


@app.route('/')
def home():
    return render_template('home.html')



@app.route('/login',methods=['GET','POST'])
def login():
    msg=''
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        cur= mysql.get_db().cursor()
        cur.execute('''SELECT * from users where username=%s and password=%s''',(username,password))
        record=cur.fetchone()
        if record:
            session['loggedin']=True
            session['username']=record[1]
            return redirect(url_for('admin'))
        else:
            msg='Incorrect username/password. Try again!'
    return render_template('home.html',msg=msg)


@app.route('/plots.html', methods=['GET','POST'])
def plots():

    plt.bar(states['state'], states['value'])
    plt.grid(color='g', linestyle='-.', linewidth=0.8)
    plt.title('Average company score by state')
    plt.savefig('static/images/plot.png')
    
    return render_template('plots.html', plot_url='/static/images/plot.png')

@app.route('/jobs.html', methods=['GET','POST'])
def jobs(): 
    selection=request.form.get('joblist', None)
    cur= mysql.get_db().cursor()
    cur.execute('''SELECT * from jobs
WHERE state=%s order by id desc''',(selection))    
    job = cur.fetchall()
    return render_template('jobs.html',job=job)



@app.route('/admin')
def admin():
    cur= mysql.get_db().cursor()
    cur.execute('''SELECT id, pdate, job_title, company, company_score, city, state, est_wage from jobs order by id DESC;''')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', data=data ,username=session['username'])

@app.route('/insert', methods = ['POST'])
def insert():

    if request.method=="POST":
        flash("Inserted Successfully")
        pdate= request.form['pdate']
        job_title= request.form['job_title']
        company= request.form['company']
        company_score= request.form['company_score']
        city= request.form['city']
        state= request.form['state']
        est_wage= request.form['est_wage'] 

        cur= mysql.get_db().cursor()
        cur.execute('''INSERT INTO jobs (pdate, job_title, company, company_score, city, state, est_wage) VALUES (%s,%s,%s,%s,%s,%s,%s);''', (pdate, job_title, company, company_score, city, state, est_wage))
        cur.connection.commit()
        return redirect(url_for('admin'))

@app.route('/update', methods = ['POST'])
def update():

    if request.method=="POST":

        pdate= request.form['pdate']
        job_title= request.form['job_title']
        company= request.form['company']
        company_score= request.form['company_score']
        city= request.form['city']
        state= request.form['state']
        est_wage= request.form['est_wage'] 
        id=request.form['id']

        cur= mysql.get_db().cursor()
        cur.execute('''UPDATE jobs set pdate=%s, job_title=%s, company=%s, company_score=%s, city=%s, state=%s, est_wage=%s where id=%s''',(pdate, job_title, company, company_score, city, state, est_wage,id))
        flash("Updated Successfully")
        cur.connection.commit()
        return redirect(url_for('admin'))


@app.route('/delete/<string:id>', methods = ['GET'])
def delete(id):
    flash("Deleted Successfully")
    cur= mysql.get_db().cursor()
    cur.execute("DELETE FROM jobs WHERE id=%s", (id,))
    cur.connection.commit()
    return redirect(url_for('admin'))





if __name__ == "__main__":
    app.run(debug = True)
