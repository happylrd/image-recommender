def get_photo_url(farm_id, server_id, photo_id, secret):
    return 'https://farm{0}.staticflickr.com/{1}/{2}_{3}_m.jpg'.format(farm_id, server_id, photo_id, secret)


def get_avatar_url(iconfarm, iconserver, nsid):
    return 'http://farm{0}.staticflickr.com/{1}/buddyicons/{2}.jpg'.format(iconfarm, iconserver, nsid)


def test():
    print(get_photo_url(1, 796, 40856221691, '7c74fea97b'))
    print(get_photo_url('1', '796', '40856221691', '7c74fea97b'))
    print(get_avatar_url(5, 4206, '86832534@N03'))
    print(get_avatar_url('5', '4206', '86832534@N03'))


if __name__ == '__main__':
    test()
