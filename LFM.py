#!/usr/bin/env python
# _*_coding: utf-8 _*_
# @Time : 2021/5/14 18:39
# @Author : CN-JackZhang
# @File: LFM.py
import numpy as np
import utility.read as read
import operator

def init_model(vec_len):
    '''
    :param vec_len:向量的长度
    :return: a ndarray
    '''
    return np.random.randn(vec_len)


def moodel_predict(user_vec,movie_vec):
    '''
    :param user_vec: 模型产出表示用户的向量
    :param movie_vec:模型产出表示电影的向量
    :return:数字，表示user_vec和movie_vec之间距离的远近，也就是模型认为推荐的强度
    '''
    #用cos计算距离
    res = np.dot(user_vec, movie_vec)/(np.linalg.norm(user_vec)*np.linalg.norm(movie_vec))
    return res

def lfm_train(train_data,F,alpha,beta,step):
    '''
    通过lfm得到用户向量和电影向量
    :param train_data:训练样本
    :param F: 用户向量长度，电影向量长度
    :param alpha:正则化参数
    :param beta:学习率
    :param step:迭代次数
    :return:两个字典，key movieid, value np.ndarray
                    key userid,  value np.ndarray
    '''
    user_vec = {}
    movie_vec = {}
    for step_index in range(step):
        for data_instance in train_data:
            userid,movieid,label = data_instance
            if userid not in user_vec:
                user_vec[userid] = init_model(F)
            if movieid not in movie_vec:
                movie_vec[movieid] = init_model(F)
        delta = label - moodel_predict(user_vec[userid], movie_vec[movieid])
        for index in range(F):
            user_vec[userid][index] += beta*(delta*movie_vec[movieid][index]-alpha*user_vec[userid][index])
            movie_vec[movieid][index] += beta*(delta*user_vec[userid][index]-alpha*movie_vec[movieid][index])
        beta = beta*0.9
    return user_vec, movie_vec


def give_recom_result(user_vec,movie_vec,userid):
    '''
    得到推荐结果
    :param user_vec:模型得到的结果
    :param movie_vec: 模型得到的结果
    :param userid:想得到某个用户的推荐结果
    :return: 一个列表，每个元素是一个元组，分别是Itemid和推荐的得分
    '''
    fix_num = 10
    if userid not in user_vec:
        return []
    record = {}
    recom_list = []
    user_vector = user_vec[userid]
    for movieid in movie_vec:
        movie_vecor = movie_vec[movieid]
        res = np.dot(user_vector, movie_vecor)/(np.linalg.norm(user_vector)*np.linalg.norm(movie_vecor))
        record[movieid] = res
    for zuhe in sorted(record.items(),key=operator.itemgetter(1), reverse=True)[:fix_num]:
        movieid = zuhe[0]
        score = round(zuhe[1], 3)
        recom_list.append((movieid,score))
    return recom_list


def ana_recom_result(train_data,userid,recom_list):
    '''
    debug
    :param train_data: 训练数据
    :param userid:要分析的用户
    :param recom_list:模型给出的对用户的推荐结果
    :return:
    '''
    movie_info = read.get_item_info('../data/movies.txt')
    for data_instance in train_data:
        tmp_userid, movieid, label = data_instance
        if label == 1 and tmp_userid == userid:
            print(movie_info[movieid])
    print('-'*40,'recom result: ')
    for zuhe in recom_list:
        print(movie_info[zuhe[0]])
    print('*'*40)


def train_model_process():
    '''测试lfm模型的训练'''
    train_data = read.get_train_data('../data/ratings.txt')
    user_vec, movie_vec = lfm_train(train_data, 50, 0.01, 0.1, 50)
    for userid in user_vec:
        if userid == '24':
            res = give_recom_result(user_vec, movie_vec, userid)
            ana_recom_result(train_data, userid, res)
    # print('{},\n,{}'.format(user_vec['1'], movie_vec['2455']))
    # print(res)

if __name__ == '__main__':
    train_model_process()



