# app.py
from myproject import app, db
from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user, login_required, logout_user
from myproject.models import User
from myproject.forms import LoginForm, Registration

@app.route('/')
def home():
    return render_template('home.html')

# The 2nd decorator, requries the user to be logged in to be able to see the view.
# If you're not logged in, you'll be redirected to the login page.
@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome_user.html')


@app.route('/logout')
@login_required
def logout():
    # This function is from the imported library
    logout_user()
    flash("You're logged out now")
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        # We 'get' from the database the user that the customer provided.
        # Thats why we use query here. We won't be using query in the registration view... (*)
        user = User.query.filter_by(email=form.email.data).first()
        
        # check_password() is the function from our User model from our models.py file
        # the condition before "and" checks if the password is valid.
        # the condition after checks if the user was provided. Basically checking if
        # a user is registered.
        if user.check_password(form.password.data) and user is not None:
            # This login_user() function is frm the "flask_login" import
            login_user(user)
            flash('Logged in Successfully')

            # this next thing:
            # If a user tries to access a page that requires them to be logged in,
            # but they're currently not logged in then flask can
            # save the page they were requesting as their 'next' request.
            next = request.args.get('next')

            # If next is none, then just go to the welcome page
            if next == None or not next[0]=='/':
                next = url_for('welcome_user')
            
            # If that oesnt happen, and they DID request something before logging in then...
            # Once they log in, they will be redirected to the page they orginally requested.
            return redirect(next)
        
    # The default view when a person tries to login. I.e: the login page
    # This return statement should be on the top most level of this function. (lined with the first if)
    return render_template('login.html', form=form)
            
             
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = Registration()

    if form.validate_on_submit():
        # (*) Because we are 'ADDING' to the database a new 'User' object, with the information 
        # provided in the form.
        user = User(email=form.email.data,
                    username=form.username.data,
                    mypassword=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Successfully Registered')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)



if __name__ == '__main__':
    app.run(debug=True)


















