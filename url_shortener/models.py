from mongoengine import Document, StringField, DateTimeField
from datetime import datetime 


class Url(Document): 
    longUrl = StringField(required = True)
    shortCode = StringField(required = True, unique = True)
    shortUrl = StringField(required = True)
    createdAt = DateTimeField(default = datetime.now())
