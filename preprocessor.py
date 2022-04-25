import pandas as pd
import streamlit as st

def preprocess(df):

    #st.dataframe(df)
    def split_time(a):
        return a.split('-')[0]
    df['time'] = df[0].apply(split_time)

    def split_msg(a):
        l = a.split('-')[1:]
        return ' '.join(l)
    df['msg'] = df[0].apply(split_msg)

    def user(a):
        if ':' in a:
            return a.split(':')[0]
        else:
            return 'Group_Notification'
    df['user'] = df['msg'].apply(user)

    def user_msg(a):
        if ':' in a:
            l = a.split(':')[1:]
            return ' '.join(l)
        else:
            return a
    df['msg1'] = df['msg'].apply(user_msg)

    df.drop(columns=[0, 'msg'], axis=1, inplace=True)
    df['time2'] = pd.to_datetime(df.time,dayfirst = True ,errors='coerce')
    df.dropna(inplace=True)
    df.drop('time', axis=1, inplace=True)

    df['year'] = df.time2.dt.year
    df['month'] = df.time2.dt.month_name()
    df['day'] = df.time2.dt.day
    df['hour'] = df.time2.dt.hour
    df['min'] = df.time2.dt.minute
    df['mont_num'] = df['time2'].dt.month
    df['day_name'] = df['time2'].dt.day_name()
    df['hour1'] = df['hour'].replace(0, 24)


    return df
