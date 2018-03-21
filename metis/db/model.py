from peewee import *

database = MySQLDatabase('image_recommender',
                         **{'charset': 'utf8', 'use_unicode': True, 'host': 'localhost', 'port': 3306, 'user': 'root',
                            'passwd': '123456'})


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class User(BaseModel):
    avatar = CharField(null=True)
    create_time = DateTimeField(null=True)
    id = BigAutoField(primary_key=True)
    nickname = CharField(null=True)
    password = CharField(null=True)
    username = CharField(unique=True)

    class Meta:
        table_name = 'user'


class Photo(BaseModel):
    create_time = DateTimeField(null=True)
    id = BigAutoField(primary_key=True)
    owner = ForeignKeyField(column_name='owner_id', field='id', model=User)
    title = CharField(null=True)
    url = CharField(null=True)

    class Meta:
        table_name = 'photo'


class Tag(BaseModel):
    content = CharField(null=True)
    create_time = DateTimeField(null=True)
    id = BigAutoField(primary_key=True)
    raw = CharField(null=True)

    class Meta:
        table_name = 'tag'


class PhotoTag(BaseModel):
    create_time = DateTimeField(null=True)
    id = BigAutoField(primary_key=True)
    photo = ForeignKeyField(column_name='photo_id', field='id', model=Photo)
    tag = ForeignKeyField(column_name='tag_id', field='id', model=Tag)

    class Meta:
        table_name = 'photo_tag'
