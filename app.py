from curses import flash
from re import template
from unicodedata import name
from urllib import request
from flask import *
import database
import os
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_mail import Message
import verify


msg = Message(subject="Hello World!",
              sender="from@qq.com",
              recipients=["to@example.com"])

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)  

# 来自掘金https://juejin.cn/post/6844903481506004999
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = '1115789295@qq.com'
app.config['MAIL_PASSWORD'] = 'evbmiisgdpsmgdfg'

mail = Mail(app)









@app.route('/login', methods=['POST', 'GET'])
def login():
    if(request.method == 'POST'):
        # submitting details
        # The form gives back EmployeeID and Password
        login_return_data = database.check_login(
            request.form['username'],
            request.form['password'],
            request.form['email']
        )
        
        # If it's null, saying they have incorrect details
        if login_return_data is None:
            # page['bar'] = False
            flash("Incorrect username/password/email, please try again")
            return redirect(url_for('login'))

        # If there was no error, log them in
        # page['bar'] = True
        flash('You have been logged in successfully')
        session['logged_in'] = True
        

        # Store the user details for us to use throughout
        global user_details
        user_details = login_return_data[0]
        session['username'] = user_details
        print(user_details)

        return redirect(url_for('home', name = user_details))
    if(request.method == 'GET'):
        return(render_template('login.html'))


@app.route('/home/<name>', methods=['POST', 'GET']) 
def home(name):
    if session.get('logged_in') == True:
        return (render_template('home.html', name = name))
    else:
        return (render_template('login.html'))
        



@app.route('/register', methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        register_return_data = database.check_exist_usr(
            request.form['username'],
            request.form['password'],
            request.form['repassword'],
            request.form['email']
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
    

@app.route('/logout', methods = ['POST', 'GET'])
def logout():
    session['logged_in'] = False
    session['username'] = None
    return (render_template('logout.html'))



@app.route('/send_email', methods = ['POST', 'GET'])
def send_email():
    if request.method == 'GET':
        return (render_template('send_email.html'))
    if request.method == 'POST':
        reset_ps_return_data = database.check_valid_email(
            request.form['name'],
            request.form['email']
        )
        
        if reset_ps_return_data == 1:
            flash("你输入的账户不存在,请重新输入")
            return redirect(url_for('send_email'))
        
        elif reset_ps_return_data == 2:
            token = verify.get_reset_token(request.form['name'])
            recipient = []
            recipient.append(request.form['email'])
            flash("请注意查收邮件信息")
            msg = Message(subject="Message!",
            sender=app.config.get('MAIL_USERNAME'),
            recipients=recipient)
            msg.html = render_template('email_link.html', token = token)
            mail.send(msg)
            return redirect(url_for('send_email'))
        
        
        elif reset_ps_return_data == 3:
            flash("你输入的邮箱与账户邮箱不匹配请重新输入正确邮箱")
            return redirect(url_for('send_email'))
        
               

@app.route('/password_reset_verified/<token>', methods=['GET', 'POST'])
def reset_verified(token):
    user = verify.verify_reset_token(token)
    if not user:
        print('no user found')
        return redirect(url_for('login'))
    
    if request.method == 'GET':
        return render_template('reset_password.html')
    
    if request.method == 'POST':
        password = request.form.get('new_password')
        if password:
            result = database.set_password(password, user)
            if result == False:
                print(1)
            if result == True:
                flash('密码修改成功请重新尝试')
                return redirect(url_for('login'))
        flash('你必须填写新密码')
        return render_template('reset_password.html')











@app.route('/', methods = ['POST', 'GET'])
def root():
    return render_template('root.html')
    



if __name__ == '__main__':
    app.run(debug=True)
