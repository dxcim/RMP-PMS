import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, request, abort
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, RadioField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bruh'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

load_dotenv()
twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
twilio_api_key_sid = os.environ.get('TWILIO_API_KEY_SID')
twilio_api_key_secret = os.environ.get('TWILIO_API_KEY_SECRET')
twilio_client = Client(twilio_api_key_sid, twilio_api_key_secret,
                       twilio_account_sid)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    user_type = db.Column(db.String(7), nullable =False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    user_type = RadioField('user_type', choices=[('value', 'Patient'), ('value_two', 'Doctor')])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email address'), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    user_type = RadioField('user_type', choices=[('value', 'Patient'), ('value_two', 'Doctor')])

def get_chatroom(name):
    for conversation in twilio_client.conversations.conversations.list():
        if conversation.friendly_name == name:
            return conversation

    # a conversation with the given name does not exist ==> create a new one
    return twilio_client.conversations.conversations.create(
        friendly_name=name)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return render_template('dashboard.html', type=user.user_type)
            else:
                return 'Incorrect Password!'
        else:
            return 'User does not exist!'
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET','POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_pwd = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_pwd, user_type=form.user_type.data)
        db.session.add(new_user)
        db.session.commit()
        return '<h1>User added</h1>'
        return redirect('/dashboard')
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html', name=current_user.username)

@app.route('/meetings', methods=['GET','POST'])
@login_required
def meetings():
    username = current_user.username
    conversation = get_chatroom('Room')
    try:
        conversation.participants.create(identity=username)
    except TwilioRestException as exc:
        # do not error if the user is already in the conversation
        if exc.status != 409:
            raise
    #conversation.participants.create(identity=username)
    token = AccessToken(twilio_account_sid, twilio_api_key_sid, twilio_api_key_secret, identity=username)
    token.add_grant(VideoGrant(room='My Room'))
    #redirect("/meetings")
    #return {'token': token.to_jwt().decode(), 'conversation_sid': conversation.sid}
    return render_template('video.html', name=current_user.username, token=token.to_jwt().decode(), conversation_sid=conversation.sid)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.username)

if __name__ == '__main__':
    app.run(debug=True)