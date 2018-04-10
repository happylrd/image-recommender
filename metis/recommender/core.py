import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from db.dao import add_user_photo_rec, add_photo_photo_rec
from pprint import pprint

USER_NUMBER = 23259
PHOTO_NUMBER = 8837
TOP_K_NUM = 10


def get_recommend_list_by_itemcf():
    header = ['user_id', 'photo_id', 'is_fav']
    df = pd.read_csv('../scidata/user_photo_fav.csv', names=header)

    fav_matrix = np.zeros((USER_NUMBER, PHOTO_NUMBER))
    for row in df.itertuples():
        user_id = row[1] - 1  # real user id need + 1
        photo_id = row[2] - 1
        is_fav = row[3]
        fav_matrix[user_id, photo_id] = is_fav

    item_similarity = cosine_similarity(fav_matrix.T)
    rec_result = fav_matrix.dot(item_similarity)
    # 归一化
    rec_result = rec_result / np.array([np.abs(item_similarity).sum(axis=1)])

    rec_list = []
    for user_id in range(rec_result.shape[0]):
        rec_item_per_user = rec_result[user_id].argsort()[-TOP_K_NUM:][::-1].tolist()
        rec_list.append(rec_item_per_user)
    return rec_list


def do_recommend_for_user():
    """
    load recommend data for user into database
    :return:
    """
    rec_list = get_recommend_list_by_itemcf()
    user_num = len(rec_list)
    rec_photo_num = len(rec_list[0])
    print('rec_list shape: ({0}, {1})'.format(user_num, rec_photo_num))

    for i in range(user_num):
        user_id = i + 1
        rec_photo_ids = ','.join(str(photo_id + 1) for photo_id in rec_list[i])
        pprint(rec_photo_ids)
        add_user_photo_rec(user_id, rec_photo_ids)


def get_recommend_list_by_tag_based():
    header = ['photo_id', 'tag_id']
    df = pd.read_csv('../scidata/photo_tag.csv', names=header)
    photo_num = df.photo_id.unique().shape[0]
    tag_num = df.tag_id.unique().shape[0]

    photo_tag_matrix = np.zeros((photo_num, tag_num))
    for row in df.itertuples():
        photo_id = row[1] - 1  # real photo id need + 1
        tag_id = row[2] - 1
        photo_tag_matrix[photo_id, tag_id] = 1

    photo_similarity = cosine_similarity(photo_tag_matrix)
    np.fill_diagonal(photo_similarity, 0)
    rec_result = photo_similarity

    rec_list = []
    for photo_id in range(rec_result.shape[0]):
        rec_item_per_photo = rec_result[photo_id].argsort()[-TOP_K_NUM:][::-1].tolist()
        rec_list.append(rec_item_per_photo)
    return rec_list


def do_recommend_for_photo():
    """
    load recommend data for photo into database
    :return:
    """
    rec_list = get_recommend_list_by_tag_based()
    photo_num = len(rec_list)
    rec_photo_num = len(rec_list[0])
    print('rec_list shape: ({0}, {1})'.format(photo_num, rec_photo_num))

    for i in range(photo_num):
        photo_id = i + 1
        rec_photo_ids = ','.join(str(e + 1) for e in rec_list[i])
        add_photo_photo_rec(photo_id, rec_photo_ids)


if __name__ == '__main__':
    # do_recommend_for_user()
    do_recommend_for_photo()
