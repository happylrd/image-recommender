import re


def get_photo_url(farm_id, server_id, photo_id, secret):
    return 'https://farm{0}.staticflickr.com/{1}/{2}_{3}_m.jpg'.format(farm_id, server_id, photo_id, secret)


def get_avatar_url(iconfarm, iconserver, nsid):
    return 'http://farm{0}.staticflickr.com/{1}/buddyicons/{2}.jpg'.format(iconfarm, iconserver, nsid)


def remove_emoji(text):
    # Narrow UCS-2 build
    myre = re.compile(u'('
                      u'\ud83c[\udf00-\udfff]|'
                      u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'
                      u'[\u2600-\u26FF\u2700-\u27BF])+',
                      re.UNICODE)
    return myre.sub('', text)


def remove_emoji_ucs4(text):
    # Wide UCS-4 build
    myre = re.compile(u'['
                      u'\U0001F300-\U0001F64F'
                      u'\U0001F680-\U0001F6FF'
                      u'\u2600-\u26FF\u2700-\u27BF]+',
                      re.UNICODE)
    return myre.sub('', text)


def test():
    emoji = 'britishcars🚗'
    print(remove_emoji_ucs4(emoji))


if __name__ == '__main__':
    test()
