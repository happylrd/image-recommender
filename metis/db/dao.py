import os
import json
from datetime import datetime
from db.utils import get_photo_url, get_avatar_url
from db.model import User, Photo, Tag, PhotoTag, Favorite, UserPhotoRec, PhotoPhotoRec

PATH = 'D:/MyCode/buptsseProject/metis/predbdata/'
DEFAULT_PASSWORD = '123456'
TAG_MAX_LEN = 30


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
        print('{0} has finished.'.format(file_names[i]))


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

    fav_persons = photo['favpersons']
    for i in range(len(fav_persons)):
        fav_user_inst = add_user(fav_persons[i])
        add_favorite(fav_user_inst, photo_inst)


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
    return User.create(username=username, password=password, nickname=nickname,
                       avatar=avatar, create_time=create_time)


def add_photo(photo, owner):
    """

    :param photo: the json of photo
    :param owner: the instance of owner
    :return:
    """
    title = photo['title']['_content']
    url = get_photo_url(photo['farm'], photo['server'], photo['id'], photo['secret'])
    f_view_num = int(photo['views'])
    f_fav_num = int(photo['faves'])
    f_comment_num = int(photo['comments']['_content'])
    create_time = datetime.now()

    print('title: {0}'.format(title))

    return Photo.create(title=title, url=url, f_view_num=f_view_num,
                        f_fav_num=f_fav_num, f_comment_num=f_comment_num,
                        owner=owner, create_time=create_time)


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


def add_favorite(user, photo):
    """

    :param user: the instance of user
    :param photo: the instance of photo
    :return:
    """
    is_fav = 1
    create_time = datetime.now()
    Favorite.create(user=user, photo=photo, is_fav=is_fav, create_time=create_time)


def add_user_photo_rec(user_id, rec_photo_ids):
    """

    :param user_id: long
    :param rec_photo_ids: str
    :return:
    """
    create_time = datetime.now()

    query = UserPhotoRec.select().where(UserPhotoRec.user_id == user_id)
    if query.exists():
        u_p_r_inst = query.get()
        u_p_r_inst.rec_photo_ids = rec_photo_ids
        u_p_r_inst.save()
        print('user_id: {0} has updated.Result: ({1}, {2}).'
              .format(user_id, u_p_r_inst.user_id, u_p_r_inst.rec_photo_ids))
    else:
        u_p_r_inst = UserPhotoRec.create(user_id=user_id, rec_photo_ids=rec_photo_ids, create_time=create_time)
        print('user_id: {0} has created.Result: ({1}, {2}).'
              .format(user_id, u_p_r_inst.user_id, u_p_r_inst.rec_photo_ids))


def add_photo_photo_rec(photo_id, rec_photo_ids):
    """

    :param photo_id: long
    :param rec_photo_ids: str
    :return:
    """
    create_time = datetime.now()

    query = PhotoPhotoRec.select().where(PhotoPhotoRec.photo_id == photo_id)
    if query.exists():
        p_p_r_inst = query.get()
        p_p_r_inst.rec_photo_ids = rec_photo_ids
        p_p_r_inst.save()
        print('photo_id: {0} has updated.Result: ({1}, {2}).'
              .format(photo_id, p_p_r_inst.photo_id, p_p_r_inst.rec_photo_ids))
    else:
        PhotoPhotoRec.create(photo_id=photo_id, rec_photo_ids=rec_photo_ids, create_time=create_time)


if __name__ == '__main__':
    init_data()
