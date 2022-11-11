#Imports
from random import randint
import firebase_admin
import pyrebase
import json
from uuid import uuid4
from firebase_admin import credentials, auth, db
from flask import Flask, request, render_template, redirect
from forms import AddNewUserForm, RemoveUserForm, CreateNewGroup
from functools import wraps
from twilio.rest import Client
import collections
from collections.abc import MutableMapping

#App configuration
app = Flask(__name__)

app.config['SECRET_KEY'] = '166bd6c8c805a8a3a4e62b55f36219a737f0345dba389cce'

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
tables = ref.child('Tables')

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

#Api route 
@app.route('/')
def admin():
    adduser_form = AddNewUserForm() #make its createuser
    removeuser_form = RemoveUserForm() #make it deleteuser
    tables.child(str(uuid4())).push({'First Name' : adduser_form.first_name.data, 'Last Name' : adduser_form.last_name.data, 'Email' : adduser_form.email.data, 'Phone Number' : adduser_form.phone_number.data})
    #insert code that makes the remove user form functional - take first and last name and delete corresponding child node from channels
    return render_template('admin.html', adduser_form=adduser_form, 
    removeuser_form=removeuser_form)

#Api route to creating a new group
@app.route('/api/creategroup', methods=['GET', 'POST'])
def editgroup():
    adduser_form = AddNewUserForm() #modify to add user to a group - ie add a key/value that connects to group id in question
    removeuser_form = RemoveUserForm() #modify to remove user from a group (either set key value to null or delete child altogether)
    creategroup_form = CreateNewGroup() # actually i think this one is functional? 
    tables.child(str(uuid4())).set({'First Name' : adduser_form.first_name.data, 'Last Name' : adduser_form.last_name.data, 'Email' : adduser_form.email.data, 'Phone Number' : adduser_form.phone_number.data})
    channelgroups.child(str(uuid4())).set({'Group Name' : creategroup_form.group_name.data, 'Group Description' : creategroup_form.group_desc.data})
    return render_template('editgroup.html', adduser_form=adduser_form, 
        removeuser_form=removeuser_form, creategroup_form =creategroup_form)


@app.route('/api/groupgrid', methods=['GET', 'POST'])
def groupgrid():
    groups = channelgroups.get()
    return render_template('groupgrid.html', groups=groups)

if __name__ == '__main__':
    app.run(debug=True)