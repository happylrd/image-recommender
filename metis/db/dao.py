import os
import json
from datetime import datetime
from crawler.crawler import PATH
from db.utils import get_photo_url, get_avatar_url
from db.model import User, Photo, Tag, PhotoTag

DEFAULT_PASSWORD = '123456'
TAG_MAX_LEN = 10


def init_data():
    """
    load all file into db
    :return:
    """
    path = PATH
    file_names = [fname for fname in os.listdir(path) if os.path.splitext(fname)[1] == '.json']
    file_names_len = len(file_names)
    print('num of json files: {0}'.format(file_names_len))
    for i in range(file_names_len):
        load_data_into_db(path, file_names[i])


def load_data_into_db(path, file_name):
    """
    load one json into db
    :param path:
    :param file_name: filename with ext
    :return:
    """
    with open(path + file_name, 'r') as load_f:
        load_dict = json.load(load_f)
        print('photo num in a json file: {0}'.format(len(load_dict)))
        for i in range(len(load_dict)):
            add_data_by_per_photo(load_dict[i]['photo'])


def add_data_by_per_photo(photo):
    """

    :param photo: the json of photo
    :return:
    """
    owner_inst = add_user(photo['owner'])
    photo_inst = add_photo(photo, owner_inst)

    tags = photo['tags']['tag']
    tags_length = len(tags)
    if not tags_length:
        print('the size of json tags is 0')
    elif tags_length < TAG_MAX_LEN:
        for i in range(tags_length):
            tag_inst = add_tag(tags[i])
            add_photo_tag(photo_inst, tag_inst)
    else:
        for i in range(TAG_MAX_LEN):
            tag_inst = add_tag(tags[i])
            add_photo_tag(photo_inst, tag_inst)


def add_user(owner):
    """

    :param owner: the json of owner
    :return:
    """
    username = owner['username']
    password = DEFAULT_PASSWORD
    nickname = owner['realname']
    avatar = get_avatar_url(owner['iconfarm'], owner['iconserver'], owner['nsid'])
    create_time = datetime.now()

    query = User.select().where(User.username == username)
    if query.exists():
        print('user: {0} has existed'.format(username))
        return query.get()

    print('user: {0} not exist'.format(username))
    return User.create(username=username, password=password, nickname=nickname, avatar=avatar, create_time=create_time)


def add_photo(photo, owner):
    """

    :param photo: the json of photo
    :param owner: the instance of owner
    :return:
    """
    title = photo['title']['_content']
    url = get_photo_url(photo['farm'], photo['server'], photo['id'], photo['secret'])
    create_time = datetime.now()
    return Photo.create(title=title, url=url, owner=owner, create_time=create_time)


def add_tag(tag):
    """

    :param tag: the json of tag
    :return:
    """
    raw = tag['raw']
    content = tag['_content']
    create_time = datetime.now()

    query = Tag.select().where(Tag.content == content)
    if query.exists():
        print('tag: {0} has existed'.format(content))
        return query.get()

    print('tag: {0} not exist'.format(content))
    return Tag.create(raw=raw, content=content, create_time=create_time)


def add_photo_tag(photo, tag):
    """

    :param photo: the instance of photo
    :param tag: the instance of tag
    :return:
    """
    create_time = datetime.now()
    PhotoTag.create(photo=photo, tag=tag, create_time=create_time)


if __name__ == '__main__':
    init_data()
