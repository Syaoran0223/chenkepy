#coding=utf8
import time
import math

#分页
def paginate(query, page, per_page):
    #总页数
    total_count = query.count()
    total_page = math.ceil(total_count/per_page)
    if page < 1:
        items = []
    else:
        items = query.limit(per_page).offset((page-1) * per_page).all()
    current_page = page
    pagination = {'total_page': total_page, 'current_page': current_page,
                  'items': items,'count':len(items)}
    return pagination