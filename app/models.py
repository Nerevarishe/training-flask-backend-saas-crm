from datetime import datetime
from flask_mongoengine import Document
from mongoengine import fields as fl


class BaseDocument(Document):
    
    meta = {
        'abstract': True
    }
    
    date_created = fl.DateTimeField(default=datetime.utcnow)
    date_edited = fl.DateTimeField(default=datetime.utcnow)      
