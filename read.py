#!/usr/bin/env python
# _*_coding: utf-8 _*_
# @Time : 2021/5/13 7:31
# @Author : CN-JackZhang
# @File: read.py
'''1.从Item详情中抽取item详情，对推荐结果的评估，
2.得到用户对Item的平均评分，做负采样'''

def get_item_info(input_file):
    '''得到电影详细信息'''
    #放Item详情
    item_dict = {}
    #打开文件
    with open(input_file) as fp:
        num = 0
        for line in fp:
            if num == 0:
                num += 1
                continue
            item = line.strip().split(',')
            if len(item) < 3:
                continue
            if len(item) == 3:
                movieId, title, genres = item[0],item[1],item[2]
            elif len(item) > 3:
                movieId, title, genres = item[0], ','.join(item[1:-1]),item[-1]
            if movieId not in item_dict:
                item_dict[movieId] = [title,genres]
        fp.close()
    return  item_dict


def get_ave_score(input_file):
    '''得到电影平均分'''
    record_dict, score_dict = {}, {}
    # 打开文件
    with open(input_file) as fp:
        num = 0
        for line in fp:
            if num == 0:
                num += 1
                continue
            item = line.strip().split(',')
            if len(item) < 4:
                continue
            userId, movieId, rating = item[0], item[1], item[2]
            if movieId not in record_dict:
                record_dict[movieId] = [0, 0]
            record_dict[movieId][0] += 1
            record_dict[movieId][1] += float(rating)
        fp.close()
    for movieId in record_dict:
        score_dict[movieId] = round(record_dict[movieId][1]/record_dict[movieId][0],3)
    return score_dict

#抽取训练样本函数
def get_train_data(input_file):
    '''提供训练样本'''
    score_dict = get_ave_score(input_file)
    neg_dict, pos_dict, train_data = {}, {}, []
    with open(input_file) as fp:
        num = 0
        for line in fp:
            if num == 0:
                num += 1
                continue
            item = line.strip().split(',')
            if len(item) < 4:
                continue
            userId, movieId, rating = item[0], item[1], float(item[2])
            #得分大于等于4分，为喜欢，小于4分，就是不喜欢
            if userId not in pos_dict:
                pos_dict[userId] = []
            if userId not in neg_dict:
                neg_dict[userId] = []
            if rating >= 4:
                pos_dict[userId].append((movieId, 1))
            else:
                score = score_dict.get(movieId, 0)
                neg_dict[userId].append((movieId, score))
    fp.close()
    for userId in pos_dict:
        data_num = min(len(pos_dict[userId]), len(neg_dict.get(userId, [])))
        if data_num > 0:
            train_data += [(userId, zuhe[0], zuhe[1]) for zuhe in pos_dict[userId]][:data_num]
        else:
            continue
        sorted_neg_list = sorted(neg_dict[userId], key=lambda element:element[1], reverse=True)[:data_num]
        train_data += [(userId, zuhe[0], 0) for zuhe in sorted_neg_list]
        # if userId == '24':
        #     print(len(pos_dict[userId]))
        #     print(len(neg_dict[userId]))
        #     print(sorted_neg_list)
    return train_data

# res = get_item_info('../data/movies.txt')
# score = get_ave_score('../data/ratings.txt')
# print(res,'\n',len(res))
# print(score,'\n',len(score))
# train_data = get_train_data('../data/ratings.txt')
# print('-'*30,len(train_data),train_data[:20])