# -*- coding:utf-8 -*-
import os

import simplejson
import tablib


def sort_data(l):
    l = sorted(l, key=lambda x: x['rank'])
    l = sorted(l, key=lambda x: x['date'])
    return l


def remove_duplicate(l):
    s = set()
    for d in l:
        tmp = frozenset(d.items())
        s.add(tmp)

    clean_l = []
    for i in s:
        d = {k: v for k, v in i}
        clean_l.append(d)
    return clean_l


def list_of_dict_to_dataset(l):
    data = tablib.Dataset()
    data.headers = 'rank', 'url', 'title', 'date'
    for d in l:
        data.append([d[h] for h in data.headers])
    return data


def load_jsonlines():
    with open('naver_news.jl', 'r') as f:
        r = f.readlines()
    return [simplejson.loads(i) for i in r]


def main():
    l = load_jsonlines()
    l = remove_duplicate(l)
    l = sort_data(l)
    data = list_of_dict_to_dataset(l)

    os.makedirs('result', mode=0o777, exist_ok=True)

    with open('result/result.xlsx', 'wb') as o:
        o.write(data.xlsx)

    with open('result/result.csv', 'w') as o:
        o.write(data.csv)

    with open('result/result.tsv', 'w') as o:
        o.write(data.tsv)


if __name__ == '__main__':
    main()