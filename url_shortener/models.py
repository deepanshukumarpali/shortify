from mongoengine import Document, StringField, DateTimeField, ObjectIdField
from bson import ObjectId 
from datetime import datetime 


class Url(Document): 
    id = ObjectId()
    longUrl = StringField(required = True)
    shortCode = StringField(required = True, unique = True)
    shortUrl = StringField(required = True)
    createdAt = DateTimeField(default = datetime.now())
