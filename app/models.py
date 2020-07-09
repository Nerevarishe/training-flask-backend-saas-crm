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
    email = fl.EmailField()
    avatar = fl.URLField()
    
    
class TaskCard(BaseDocument):
    task_due_date = fl.DateField(default=datetime.utcnow)
    task_type = fl.StringField(max_length=10, choices=['Reminder', 'Call', 'Event'])
    task_status = fl.StringField(max_length=10, choices=['Active', 'Completed', 'Ended'])
    # TODO: set max_length
    task_body = fl.StringField()

    
class Deal(BaseDocument):
    deal_date = fl.DateTimeField(default=datetime.utcnow)
