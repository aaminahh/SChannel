#Imports
from random import randint
import firebase_admin
import pyrebase
import json
from uuid import uuid4
from firebase_admin import credentials, auth, db
from flask import Flask, request, render_template, redirect
from forms import CreateUserForm, DeleteUserForm, AddUserForm, RemoveUserForm, CreateGroup
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
tables = ref.child('Tables')
channels = tables.child('Channels')
channelgroups = tables.child('ChannelGroups')
workflow = tables.child('Workflows')

channelsCount=0
channelGroupCount=0
workflowCount=0

channelName = channels.child("Name").get()
channelEmail = channels.child("Email").get()
channelPhone = channels.child("Phone Number").get()
channelItems = channels.child("Items Bought").get()

channelGroupID = channelgroups.child("GroupID").get()
channelGroupEmail = channelgroups.child("Email Addresses").get()
channelGroupWhatsapp = channelgroups.child("Whatsapp Numbers").get()
channelGroupSMS = channelgroups.child("SMS Numbers").get()

workflowID = workflow.child("ID").get()
workflowEmailTemp = workflow.child("Email template").get()
workflowWhatsappTemp = workflow.child("Whatsapp template").get()
workflowSMSTemp = workflow.child("SMS template").get()

#Api route 
@app.route('/api/admin', methods=['GET', 'POST'])
def admin():
    u_id = str(channelsCount + 1)
    createuser_form = CreateUserForm()
    deleteuser_form = DeleteUserForm()
    channels.child(u_id).push({
        'First Name' : createuser_form.first_name.data, 
        'Last Name' : createuser_form.last_name.data, 
        'Email' : createuser_form.email.data, 
        'Phone Number' : createuser_form.phone_number.data
        })
    #maybe if statement to work on adding the group. like if createuser_form.group.data: for group in groups: table.ladkflkjsdjfs.push('Channel Groups': group.id IDK)
    #insert code that makes the remove user form functional - take first and last name and delete corresponding child node from channels
    return render_template('admin.html', createuser_form=createuser_form, 
    deleteuser_form=deleteuser_form)

#Api route to creating a new group
@app.route('/api/creategroup', methods=['GET', 'POST'])
def editgroup():
    adduser_form = AddUserForm() #modify to add user to a group - ie add a key/value that connects to group id in question
    removeuser_form = RemoveUserForm() #modify to remove user from a group (either set key value to null or delete child altogether)
    creategroup_form = CreateGroup() # actually i think this one is functional? 
    
    #set the user indicated by adduser_form (OR PICK FROM DROP DOWN, IM GENIUS) and modify channelgroup key to add cgID, true
    #delete channel group ID from user indicated by removeuser_form.first_name/last_name.data
    return render_template('editgroup.html', adduser_form=adduser_form, 
        removeuser_form=removeuser_form, creategroup_form =creategroup_form)


@app.route('/api/groupgrid', methods=['GET', 'POST'])
def groupgrid():
    groups = channelgroups.get()
    return render_template('groupgrid.html', groups=groups)

if __name__ == '__main__':
    app.run(debug=True)