#Imports
import firebase_admin
import pyrebase
import json
from firebase_admin import credentials, auth, db
from flask import Flask, request, render_template, redirect
from forms import AddUserForm, RemoveUserForm
from functools import wraps
from twilio.rest import Client
import collections
from collections.abc import MutableMapping

#App configuration
app = Flask(__name__)

app.config['SECRET_KEY'] = 'any secret string'

#Connect to firebase
cred = credentials.Certificate('schannel-538d4-firebase-adminsdk-fp41y-f2a6a4646d.json')
firebase = firebase_admin.initialize_app(cred, {
	'databaseURL': 'https://schannel-538d4-default-rtdb.firebaseio.com/'	
})
pb = pyrebase.initialize_app(json.load(open('sChannelconfig.json')))

#Initialize messaging information
account_sid = 'AC91c5afebf10d075eb56a120c957845ee' 
auth_token = '6b6b5ed94e20a62803d7d704952c996a'
client = Client(account_sid, auth_token) 

#Creating variables from DB
ref = db.reference('SChannel')
channels = ref.child('Channels')
channelgroups = ref.child('ChannelGroups')
workflow = ref.child('Workflows')

channelName = ref.child("Tables").child("Channels").child("Name").get()
channelEmail = ref.child("Tables").child("Channels").child("Email").get()
channelPhone = ref.child("Tables").child("Channels").child("Phone Number").get()
channelItems = ref.child("Tables").child("Channels").child("Items Bought").get()

channelGroupID = ref.child("Tables").child("Channel Groups").child("GroupID").get()
channelGroupEmail = ref.child("Tables").child("Channel Groups").child("Email Addresses").get()
channelGroupWhatsapp = ref.child("Tables").child("Channel Groups").child("Whatsapp Numbers").get()
channelGroupSMS = ref.child("Tables").child("Channel Groups").child("SMS Numbers").get()

workflowID = ref.child("Tables").child("Workflow").child("ID").get()
workflowEmailTemp = ref.child("Tables").child("Workflow").child("Email template").get()
workflowWhatsappTemp = ref.child("Tables").child("Workflow").child("Whatsapp template").get()
workflowSMSTemp = ref.child("Tables").child("Workflow").child("SMS template").get()

#Additional test data source
users = [{'uid': 1, 'name': 'Aaminah Halipoto'}]

#Function to authorize user token
def check_token(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if not request.headers.get('authorization'):
            return {'message': 'No token provided'},400
        try:
            user = auth.verify_id_token(request.headers['authorization'])
            request.user = user
        except:
            return {'message':'Invalid token provided.'},400
        return f(*args, **kwargs)
    return wrap

#Api route to get users
@app.route('/api/userinfo')
#@check_token
def userinfo():
    return {'data': users}, 200

#Api route to sign up a new user
@app.route('/api/signup')
def signup():
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or password is None:
        return {'message': 'Error missing email or password'},400
    try:
        user = auth.create_user(
               email=email,
               password=password
        )
        return {'message': f'Successfully created user {user.uid}'},200
    except:
        return {'message': 'Error creating user'},400
        
#Api route to get a new token for a valid user
@app.route('/api/token')
def token():
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = pb.auth().sign_in_with_email_and_password(email, password)
        jwt = user['idToken']
        return {'token': jwt}, 200
    except:
        return {'message': 'There was an error logging in'},400

#Api route to test fetching from firebase data
@app.route('/api/attempt')
def attempt():
    info=channelEmail
    return render_template('attempt.html', info=info), 200

#Api route to basic, untouched bootstrap modal
@app.route('/api/addusercopy')
def addusercopy():
    return render_template('userinfocopy.html'), 200

#Api route to bootstrap modal newly integrated to html
@app.route('/api/adduser', methods=['GET', 'POST'])
def adduser():
    return render_template('userinfo.html')

#Api route to bootstrap modal with integrated python forms
@app.route('/api/action', methods=['GET', 'POST'])
def register():
    adduser_form = AddUserForm()
    removeuser_form = RemoveUserForm()
    return render_template(
        'action.html', 
        adduser_form=adduser_form, 
        removeuser_form=removeuser_form)

if __name__ == '__main__':
    app.run(debug=True)