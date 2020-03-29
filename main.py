import os, os.path, random, hashlib, sys, json
from flask import Flask, flash, render_template, redirect, request, url_for, jsonify, session, Response
from login import signup_f, login_f
from aid import *

app = Flask(__name__)
app.secret_key = '9je0jaj09jk9dkakdwjnjq'

@app.route('/')
def main():
    if 'username' in session:
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))

@app.route('/index')
def index():
    if 'username' in session:
        return render_template('index.html', username = session.get('username'))
    else:
        return redirect(url_for('login'))

@app.route('/info')
def info():
    if 'username' in session:
        return render_template('info.html', username = session.get('username'), events=get_info(session.get('username')))
    else:
        return redirect(url_for('login'))

@app.route('/handle_aid', methods=['GET','POST'])
def handle_aid():
    title = request.form['title']
    description = request.form['description']
    user = session.get('username')
    create_aid(user,title,description)
    return redirect(url_for('requestaid'))

@app.route('/handle_info', methods=['GET','POST'])
def handle_info():
    title = request.form['title']
    description = request.form['description']
    user = session.get('username')
    create_info(user,title,description)
    return redirect(url_for('info'))

@app.route('/requestaid')
def requestaid():
    if 'username' in session:
        return render_template('requestaid.html', username = session.get('username'))
    else:
        return redirect(url_for('login'))

@app.route('/sendaid')
def sendaid():
    if 'username' in session:
        return render_template('sendaid.html', events=get_aid(session.get('username')), username=session.get('username'))
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['password']
        if login_f(username, password):
            session['username'] = username
            session['password'] = password
            return redirect(url_for('main'))
        else:
        	#zły login lub hasło
            return render_template('login.html', info="Bad login or password!")

    return render_template('login.html', info = "")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'username' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['password']
        description = request.form['description']
        mail = request.form['mail']
        phone = request.form['phone']
        country = request.form['country']
        city = request.form['city']
        if signup_f(username, password, description, mail, phone, country, city):
            return redirect(url_for('main'))
        else:
        	#zły login lub hasło
            return render_template('signup.html')
    return render_template('signup.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    del session['username']
    del session['password']
    return redirect('/')

if __name__=='__main__':
    app.run(debug=True)
