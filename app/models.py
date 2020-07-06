from datetime import datetime
from flask_mongoengine import Document
from mongoengine import fields as fl


class BaseDocument(Document):
    
    meta = {
        'abstract': True
    }
    
    date_created = fl.DateTimeField(default=datetime.utcnow)
    date_edited = fl.DateTimeField(default=datetime.utcnow)      

    
class User(BaseDocument):
    username = fl.StringField(max_length=30)
    email = fl.EmailField
    
    
class TaskCard(BaseDocument):
    task_gtdue_date = fl.DateTimeField(default=datetime.utcnow)
    task_type = fl.StringField(max_length=100, choices=['Reminder', 'Call', 'Event'])
    task_status = fl.StringField(max_length=100, choices=['Active', 'Completed', 'Ended'])
    task_body = fl.StringField(max_length=100)
