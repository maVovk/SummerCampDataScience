from flask import Flask, render_template, request
from bokeh.plotting import figure, show
import plotly.express as plt
import pandas as pd
import vk
import time

ACCESS_TOKEN = ''
session = vk.Session(access_token=ACCESS_TOKEN)
api = vk.API(session)


def get_users():
    group_name = input('Введите название группы: ')

    groups_list = api.groups.get(v='5.120')
    group_list = api.groups.getById(group_ids=groups_list['items'], v='5.120')

    ids = None

    for elem in group_list:
        if group_name.lower() == elem['name'].lower():
            try:
                users = api.groups.getMembers(group_id=elem['id'], v='5.120')
                # print(users['count'])
                ids = []

                for i in range(0, users['count'], 1000):
                    ids += api.groups.getMembers(group_id=elem['id'], offset=i, count=1000, v='5.120')['items']
                    # print(ids)
                    # ids += tmp['items']
                    # print(i, users['count'])
                    print('*', end='')
                    time.sleep(0.5)

                # print(len(ids))
                break
            except:
                return 'Получить данные из группы невозможно'

    if ids is None:
        groups_search_list = api.groups.search(q=group_name, type='group', v='5.120')
        first_group = api.groups.getById(group_id=groups_search_list['items'][0]['id'], v='5.120')
        users = api.groups.getMembers(group_id=first_group['id'], v='5.120')
        ids = []

        for i in range(0, users['count'], 1000):
            ids += api.groups.getMembers(group_id=first_group['id'], offset=i, v='5.120')['items']

    return ids


def create_dataframe(ids):
    # print(len(ids))
    data = []

    for i in range(0, len(ids), 1000):
        data += api.users.get(user_ids=ids[i:i+1000], offset=i, fields=['sex', 'city', 'country'], v='5.120')
        time.sleep(0.5)

    df = pd.DataFrame.from_dict(data)
    df['deactivated'] = df['deactivated'].fillna(0)
    df = df[df['deactivated'] == 0]
    df.drop(['deactivated'], axis=1)
    df.reset_index()

    return df


def show_pie_graph(df):
    fig = plt.pie(df, names=df.index, values=df.values)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.show()


def analise_dataframe(df):
    sex_info = df.groupby('sex')['id'].count()
    sex_info.index = ['Нет данных', 'Женщины', 'Мужчины']
    show_pie_graph(sex_info)

    male_names_info = df[df['sex'] == 2].groupby('first_name')['id'].count().sort_values(ascending=False).head(25)
    show_pie_graph(male_names_info)

    female_names_info = df[df['sex'] == 1].groupby('first_name')['id'].count().sort_values(ascending=False).head(25)
    show_pie_graph(female_names_info)

    country_info = df['country'].dropna().apply(lambda x: x['title']).value_counts().head(10)
    fig = plt.bar(country_info, x=country_info.index, y=country_info.values)
    fig.show()


users = get_users()
df = create_dataframe(users)
analise_dataframe(df)
