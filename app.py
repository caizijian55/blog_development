from curses import flash
from unicodedata import name
from urllib import request
from flask import *
import database
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if(request.method == 'POST'):
        # submitting details
        # The form gives back EmployeeID and Password
        login_return_data = database.check_login(
            request.form['username'],
            request.form['password']
        )
        
        # If it's null, saying they have incorrect details
        if login_return_data is None:
            # page['bar'] = False
            flash("Incorrect username/password, please try again")
            return redirect(url_for('login'))

        # If there was no error, log them in
        # page['bar'] = True
        flash('You have been logged in successfully')
        session['logged_in'] = True

        # Store the user details for us to use throughout
        global user_details
        user_details = login_return_data[0]
        print(user_details)

        return redirect(url_for('home', name = user_details))
    if(request.method == 'GET'):
        return(render_template('login.html'))


@app.route('/home/<name>', methods=['POST', 'GET']) 
def home(name):
    print(session.get('logged_in'))
    return (render_template('index.html', name = name))


@app.route('/register', methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        register_return_data = database.check_exist_usr(
            request.form['username'],
            request.form['password'],
            request.form['repassword']
        )
        # If it's null, saying they have incorrect details
        if register_return_data == 3:
            flash("these two passwords are not same")
            return redirect(url_for('register'))
            
            
        if register_return_data == 2:
            # page['bar'] = False
            flash("The Username has been used, please use another one")
            return redirect(url_for('register'))

        # If there was no error, log them in
        # page['bar'] = True
        if register_return_data == 1:
            flash('register successfully')
            return redirect(url_for('login'))
        
        else:
            flash('databaseproblem')
            return redirect(url_for('register'))
            
        

        # Store the user details for us to use throughout
        
    

    else:
        return (render_template('register.html'))







if __name__ == '__main__':
    app.run(debug=True)
