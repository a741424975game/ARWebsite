# -*- coding: utf-8 -*-
import jieba.analyse


def jieba_tags(comments_list):
    comments = '\n'.join([comment.content for comment in comments_list])
    tags = jieba.analyse.textrank(comments, topK=20, withWeight=False,
                                  allowPOS=('n',
                                            'a', 'ad', 'ag', 'an', 'al',
                                            'vd', 'vn',
                                            'uyy',))
    return tags
