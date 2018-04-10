import json
import time
import flickrapi
from datetime import datetime, timedelta
from pprint import pprint

api_key = u'd1828ca5f5acd03da5d71aeba5d73f53'
api_secret = u'c1ad721b7fee1f4e'
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

PATH = 'D:/MyCode/buptsseProject/metis/rawdata/'
# PATH = 'D:/MyCode/buptsseProject/metis/testdata/'
OWNER_IDS_FILE_NAME = 'owner_ids.json'
FILE_EXT = '.json'
USER_NUM_PER_PAGE = 300
USER_NUM = 250  # a greater value than a real value
PHOTO_NUM_PER_PAGE = 200
PHOTO_NUM_PER_USER = 150
LAST_DAYS = 12  # 2018.3.17

MIN_TAG_NUM = 1
MIN_FAV_TOTAL_NUM = 10
FAV_PERSON_PER_PHOTO = 10
MIN_VIEWS = 1000
MIN_COMMENTS = 1

SLEEP_SECOND = 1


def get_owner_id_list(date, page=1, per_page=100):
    """get owner id list by interesting photos"""
    owner_ids = []
    data = flickr.interestingness.getList(date=date, page=page, per_page=per_page)
    photos = data['photos']['photo']
    for photo in photos:
        owner_id = photo['owner']
        owner_ids.append(owner_id)
    return owner_ids


def get_public_photos(user_id, page=1, per_page=100):
    """ get photo id list by user_id """
    photo_ids = []
    data = flickr.people.getPublicPhotos(user_id=user_id, page=page, per_page=per_page)

    print('owner: {0} photo num: {1}'.format(user_id, data['photos']['total']))
    if int(data['photos']['total']) <= 100:
        return []

    photos = data['photos']['photo']
    for photo in photos:
        photo_id = photo['id']
        photo_ids.append(photo_id)
    return photo_ids


def get_photo_info(photo_id):
    data = flickr.photos.getInfo(photo_id=photo_id)

    tag_num = len(data['photo']['tags']['tag'])
    print('photo: {0},tag num: {1},views:{2},comments:{3}'
          .format(photo_id, tag_num, data['photo']['views'], data['photo']['comments']['_content']))
    if tag_num < MIN_TAG_NUM:
        return {}
    elif int(data['photo']['views']) < MIN_VIEWS:
        return {}
    elif int(data['photo']['comments']['_content']) < MIN_COMMENTS:
        return {}

    fav_data = flickr.photos.getFavorites(photo_id=photo_id, page=1, per_page=10)
    fav_total_num = int(fav_data['photo']['total'])
    if fav_total_num < MIN_FAV_TOTAL_NUM:
        print('fav_total_num: {0}'.format(fav_total_num))
        return {}
    data['photo']['favpersons'] = fav_data['photo']['person'][:FAV_PERSON_PER_PHOTO]
    data['photo']['faves'] = fav_total_num

    # data['photo']['favpersons'] = get_fav_persons(photo_id)
    # if not data['photo']['favpersons']:
    #     return {}

    photo_rm_fields = ['description', 'visibility', 'dates', 'urls', 'editability',
                       'publiceditability', 'usage', 'notes', 'people', 'dateuploaded',
                       'isfavorite', 'license', 'media', 'rotation', 'safety_level',
                       'location', 'geoperms', 'originalsecret', 'originalformat']
    for rm_field in photo_rm_fields:
        data['photo'].pop(rm_field, None)

    owner_rm_fields = ['location', 'path_alias']
    for rm_field in owner_rm_fields:
        data['photo']['owner'].pop(rm_field)

    tag_rm_fields = ['author', 'authorname', 'machine_tag']
    for tag in data['photo']['tags']['tag']:
        for rm_field in tag_rm_fields:
            tag.pop(rm_field)

    return data


def get_fav_persons(photo_id, page=1, per_page=10):
    """ Deprecated. get fav persons by photo id """
    fav_data = flickr.photos.getFavorites(photo_id=photo_id, page=page, per_page=per_page)
    fav_total_num = int(fav_data['photo']['total'])
    if fav_total_num < MIN_FAV_TOTAL_NUM:
        print('fav_total_num: {0}'.format(fav_total_num))
        return []
    return fav_data['photo']['person'][:FAV_PERSON_PER_PHOTO]


def expand_list(nested_list):
    """ just a util """
    for item in nested_list:
        if isinstance(item, (list, tuple)):
            for sub_item in expand_list(item):
                yield sub_item
        else:
            yield item


def write_owner_ids_ext():
    """ get owner ids and write them into file with ext, just invoke once at first """
    date_str = (datetime.now() - timedelta(LAST_DAYS)).strftime('%Y-%m-%d')

    owner_ids = []
    owner_ids.append(get_owner_id_list(date=date_str, page=1, per_page=USER_NUM_PER_PAGE))
    owner_ids = sum(owner_ids, [])
    owner_ids = list(set(owner_ids))[:USER_NUM]

    owner_ids_ext = []
    for id in owner_ids:
        owner_id_ext = {'owner': id, 'finished': False}
        owner_ids_ext.append(owner_id_ext)

    with open(PATH + OWNER_IDS_FILE_NAME, 'w') as f:
        json.dump(owner_ids_ext, f)

    print('write finished. filename: {0} owner_ids length: {1}, owner_ids: {2}'
          .format(OWNER_IDS_FILE_NAME, len(owner_ids_ext), owner_ids_ext))


def get_owner_ids_ext():
    with open(PATH + OWNER_IDS_FILE_NAME, 'r') as load_f:
        owner_ids_ext = json.load(load_f)
        return owner_ids_ext


def crawl():
    owner_ids_ext = get_owner_ids_ext()
    print('owner_ids length: {0}, owner_ids: {1}'.format(len(owner_ids_ext), owner_ids_ext))
    for owner_id_ext in owner_ids_ext:
        owner_id = owner_id_ext['owner']
        finished = owner_id_ext['finished']
        if finished:
            print('owner_id: {0} has finished'.format(owner_id))
            continue

        tmp_photo_ids = get_public_photos(user_id=owner_id, page=1, per_page=PHOTO_NUM_PER_PAGE)
        if not tmp_photo_ids:
            continue

        tmp_photo_ids = list(set(tmp_photo_ids))[:PHOTO_NUM_PER_USER]
        photo_infos = []
        for photo_id in tmp_photo_ids:
            print('time sleep start...')
            time.sleep(SLEEP_SECOND)
            print('time sleep end...')
            photo_info = get_photo_info(photo_id)
            if not photo_info:
                continue
            photo_infos.append(photo_info)
        print(photo_infos)

        owner_id_ext['finished'] = True

        with open(PATH + OWNER_IDS_FILE_NAME, 'w') as dump_f:
            json.dump(owner_ids_ext, dump_f)
            print('{0} has changed'.format(OWNER_IDS_FILE_NAME))

        file_name = 'photo_' + owner_id
        with open(PATH + file_name + FILE_EXT, 'w') as f:
            json.dump(photo_infos, f)
            print('{0} has finished'.format(file_name + FILE_EXT))


if __name__ == '__main__':
    # write_owner_ids_ext()
    crawl()
