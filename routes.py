from flask import Blueprint, jsonify, request
import uuid


#Get All Users 
all_users_blueprint = Blueprint('all_users_blueprint', __name__)
@all_users_blueprint.route('/users', methods=['GET'])
def get_users():
    from pythonRest import User, users_schema
    all_users = User.query.all()
    print(users_schema.dump(all_users))

    return jsonify(users_schema.dump(all_users))



#Get User Login
user_login_blueprint = Blueprint('user_login_blueprint', __name__)
@user_login_blueprint.route('/users/<user_name>', methods=['GET'])
def get_users(user_name):
    from pythonRest import User, user_schema
    user = User.query.filter_by(user_name=user_name).first()
    print(user_schema.dump(user))

    return jsonify(user_schema.dump(user))



#Adds a User
add_user_blueprint = Blueprint('add_user_blueprint', __name__)
@add_user_blueprint.route('/add-user', methods=['POST'])
def add_user():
    from pythonRest import User, db, user_schema
    user_name = request.json['user_name']
    password = request.json['password']
    id = uuid.uuid1()
    unique_hash = id.hex
    new_user = User(user_name, password, unique_hash)
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

#Create a new notification
create_notification_blueprint = Blueprint('create_notification_blueprint', __name__)
@create_notification_blueprint.route('/create-notif', methods=['POST'])
def create_notif():
    from pythonRest import Notification, db, notification_schema
    summary = request.json['summary']
    text = request.json['text']
    priority = request.json['priority'].lower()
    seen = request.json['seen']
    owner_hash = request.json['owner_hash']

    if (priority == "h" or priority == "m" or priority == "l"):
        print("valid priority")
    else:
        priority = "l"
        print("invalid priority, setting to l")

    create_notification = Notification(summary, text, priority, seen, owner_hash)
    db.session.add(create_notification)
    db.session.commit()

    return notification_schema.jsonify(create_notification)

#List all User notifications
list_user_notifications_blueprint = Blueprint('list_user_notifications_blueprint', __name__)
@list_user_notifications_blueprint.route('/list-notifs/<unique_hash>', methods=['GET'])
def list_notifs(unique_hash):
    from pythonRest import User, Notification, notifications_schema
    list = []
    user = User.query.filter_by(unique_hash=unique_hash).first()
    list.append(notifications_schema.dump(user.notifications))
    everyone_notifs = Notification.query.filter_by(owner_hash='everyone').all()
    list.append(notifications_schema.dump(everyone_notifs))

    return list

#Delete notification
delete_notification_blueprint = Blueprint('delete_notification_blueprint', __name__)
@delete_notification_blueprint.route('/delete-notif/<id>', methods=['DELETE'])
def delete_notif(id):
    from pythonRest import User, Notification, db, notification_schema
    notification = Notification.query.get(id)
    db.session.delete(notification)
    db.session.commit()

    return notification_schema.jsonify(notification)

#Update notification
update_notification_blueprint = Blueprint('update_notification_blueprint', __name__)
@update_notification_blueprint.route('/update-notif/<id>', methods=['PUT'])
def update_notif(id):
    from pythonRest import Notification, db, notification_schema
    notification = Notification.query.get(id)
    summary = request.json['summary']
    text = request.json['text']
    seen = request.json['seen']
    priority = request.json['priority']
    notification.summary = summary
    notification.text = text
    notification.seen = seen
    notification.priority = priority
    db.session.commit()

    return notification_schema.jsonify(notification)