from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from dotenv import load_dotenv
import json
from routes import all_users_blueprint, add_user_blueprint, create_notification_blueprint, list_user_notifications_blueprint, delete_notification_blueprint, update_notification_blueprint

#Load the env variables
load_dotenv()
server_port = os.getenv('REST_PORT') 
try:
    debug_mode = json.loads(os.getenv('DEBUG_MODE').lower()) 
except:
    debug_mode = True
    print("Debug mode variable not properly set, Server debug_mode set to True")

#Initialize app
app = Flask(__name__)

#Database config
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)



#Configure tables relationship

#User table Class
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(60), unique=True)
    password = db.Column(db.String(60))
    unique_hash = db.Column(db.String(36), unique=True)
    notifications = db.relationship('Notification', backref='user')

    def __init__(self, user_name, password, unique_hash):
        self.user_name = user_name
        self.password = password
        self.unique_hash = unique_hash

#User Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_name', 'password', 'unique_hash')




#Notification table Class
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    summary = db.Column(db.String(25))
    text = db.Column(db.Text(256))
    priority = db.Column(db.String(1))
    seen = db.Column(db.Boolean())
    owner_hash = db.Column(db.String(36), db.ForeignKey('user.unique_hash'))


    def __init__(self, summary, text, priority, seen, owner_hash):
        self.summary = summary
        self.text = text
        self.priority = priority
        self.seen = seen
        self.owner_hash = owner_hash

#Notification Schema
class NotificationSchema(ma.Schema):
    class Meta:
        fields = ('id', 'summary', 'text', 'priority', 'seen', 'owner_hash')





#Init Schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)
notification_schema = NotificationSchema()
notifications_schema = NotificationSchema(many=True)



#Registering routes
app.register_blueprint(all_users_blueprint) # /users GET
app.register_blueprint(add_user_blueprint) # /add-user POST
app.register_blueprint(create_notification_blueprint) # /create-notif POST 
app.register_blueprint(list_user_notifications_blueprint) # /list-notifs/<unique_hash> GET
app.register_blueprint(delete_notification_blueprint) # /delete-notif/<id>
app.register_blueprint(update_notification_blueprint) # /update-notif/<id>

#Start the server
if __name__ == "__main__":
    app.run(debug=debug_mode, port=server_port)