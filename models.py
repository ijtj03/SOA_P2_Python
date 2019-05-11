from datetime import datetime
from mongoengine import Document
from mongoengine.fields import (
    IntField, StringField,
)


class Catalog(Document):
    meta = {'collection': 'catalog'}
    name = StringField(required=True)
    description = StringField(required=True)
    stock = IntField(required=True)
