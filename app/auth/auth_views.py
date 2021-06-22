from app.auth.auth_forms import RegistrationForm, LoginForm
from app.auth import auth
from flask import render_template, url_for, redirect, request, flash
from app.models import User, db
from werkzeug.security import check_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from .auth_utils import token_generator, token_confirmation
from app.email import send_email

# import password encryption tool
from werkzeug.security import generate_password_hash


@auth.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    # validate the form data before submitting
    if form.validate_on_submit():
        encrypted_password = generate_password_hash(form.password.data, method='pbkdf2:sha1', salt_length=8)

        # add the user data to db
        new_user = User(username=form.username.data, email=form.email.data, password_enc = encrypted_password)
        db.session.add(new_user)
        db.session.commit()
        print(new_user.id)

        # new user confirmation key
        confirmation_key = token_generator(new_user)

        # send email
        send_email(new_user.email, 'Confirm your account', 'auth/email/confirm.html', new_user=new_user,
                   confirmation_key=confirmation_key)
        flash('A confirmation email has been sen to ' + new_user.email)
        return redirect(url_for('main.index'))

    return render_template('auth/register.html', form=form)


@auth.route('/login', methods=["GET", "POST"])
def login():

    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if form.validate_on_submit():
        # query the db to get the user row with the matching email address in the form
        user = User.query.filter_by(email=form.email.data).first()
        print(user)
        print(form.password.data)
        print(user.password_enc)

        if user is not None and check_password_hash(user.password_enc, form.password.data):
            login_user(user, form.remember_me.data)
            flash('Login successful', 'success')
            return redirect(url_for('main.index'))

        else:
            flash("Invalid Email or Password", "warning")

    return render_template('auth/login.html', form=form)


@auth.route("/sign_out")
@login_required
def sign_out():
    logout_user()
    return redirect(url_for('main.index'))

