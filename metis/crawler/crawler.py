import json
import flickrapi
from datetime import datetime, timedelta

api_key = u'd1828ca5f5acd03da5d71aeba5d73f53'
api_secret = u'c1ad721b7fee1f4e'
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

PATH = 'D:/MyCode/buptsseProject/metis/rawdata/'
FILE_EXT = '.json'
USER_NUM = 100
PHOTO_NUM_PER_USER = 100
NUM_PER_PAGE = 150
LAST_DAYS = 2


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

    print('total:' + data['photos']['total'])
    if int(data['photos']['total']) <= 100:
        return []

    photos = data['photos']['photo']
    for photo in photos:
        photo_id = photo['id']
        photo_ids.append(photo_id)
    return photo_ids


def get_photo_info(photo_id):
    data = flickr.photos.getInfo(photo_id=photo_id)

    photo_rm_fields = ['description', 'visibility', 'dates', 'urls', 'editability',
                       'publiceditability', 'usage', 'comments', 'notes', 'people',
                       'views', 'dateuploaded', 'isfavorite', 'license', 'media',
                       'rotation', 'safety_level']
    for rm_field in photo_rm_fields:
        data['photo'].pop(rm_field)

    owner_rm_fields = ['location', 'path_alias']
    for rm_field in owner_rm_fields:
        data['photo']['owner'].pop(rm_field)

    tag_rm_fields = ['author', 'authorname', 'machine_tag']
    for tag in data['photo']['tags']['tag']:
        for rm_field in tag_rm_fields:
            tag.pop(rm_field)

    return data


def expand_list(nested_list):
    """ just a util """
    for item in nested_list:
        if isinstance(item, (list, tuple)):
            for sub_item in expand_list(item):
                yield sub_item
        else:
            yield item


def crawl():
    date_str = (datetime.now() - timedelta(LAST_DAYS)).strftime('%Y-%m-%d')

    owner_ids = []
    owner_ids.append(get_owner_id_list(date=date_str, page=1, per_page=NUM_PER_PAGE))
    owner_ids = sum(owner_ids, [])
    owner_ids = list(set(owner_ids))[:USER_NUM]
    print('owner_ids length: ' + str(len(owner_ids)))
    print(owner_ids)

    for owner_id in owner_ids:
        tmp_photo_ids = get_public_photos(user_id=owner_id, page=1, per_page=NUM_PER_PAGE)
        if not tmp_photo_ids:
            continue

        tmp_photo_ids = list(set(tmp_photo_ids))[:PHOTO_NUM_PER_USER]
        photo_infos = []
        for photo_id in tmp_photo_ids:
            photo_info = get_photo_info(photo_id)
            photo_infos.append(photo_info)
        print(photo_infos)

        file_name = 'photo_' + owner_id
        with open(PATH + file_name + FILE_EXT, 'w') as f:
            json.dump(photo_infos, f)


if __name__ == '__main__':
    crawl()
