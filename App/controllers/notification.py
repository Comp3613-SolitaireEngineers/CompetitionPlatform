from flask import Blueprint, jsonify, request
from App.database import db
from App.models import Notification
from datetime import datetime

def get_notifications():
    notifications = Notification.query.all()
    notifications_list = [notification.toDict() for notification in notifications]
    return jsonify({'notifications': notifications_list})

def get_notification(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    return jsonify(notification.toDict())

def create_notification():
    data = request.json
    new_notification = Notification(
        competitor_id=data['competitor_id'],
        message=data['message'],
        timestamp=datetime.utcnow()
    )
    return new_notification
     
def delete_notification(notification_id):
    notification = Notification.query.get(notification_id)
    db.session.delete(notification)
    db.session.commit()
    return jsonify({'message': 'Notification deleted successfully'})
    

