from urlextract import URLExtract
from wordcloud import WordCloud
from nltk.corpus import stopwords
import re
from collections import Counter
import pandas as pd
from emot.emo_unicode import UNICODE_EMOJI, EMOTICONS_EMO
import emoji
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

url = URLExtract()


def temp_needed(selected_user,df11):
    f = open('stop_hinglish.txt', 'r')
    b2 = f.read()
    b1 = stopwords.words('english')

    if selected_user != 'Overall':
        df11 = df11[df11['user'] == selected_user]

    temp = df11[df11['user'] != 'Group_Notification']
    temp = temp[temp['msg1'] != ' <Media omitted>']

    # replacing emoticons with their names in data
    def convert_emojis(text):
        for emot in UNICODE_EMOJI:
            text = text.replace(emot, "_".join(UNICODE_EMOJI[emot].replace(",", "").replace(":", "").split()))
        return text

    temp['msg1'] = temp['msg1'].apply(convert_emojis)

    #removing digits from dataset
    d = []
    for i in range(0, 1001):
        d.append(str(i))

    # finding users with tags in datset for eg- @ 8700324545
    # removing hinglish stopwords form our data
    # removing english stopwords form our data
    n = []
    for i in temp['msg1']:
        n.extend(re.findall('@.{12}', i))
    r = []
    for i in temp['msg1']:
        r1 = []
        for j in i.lower().split():
            if j not in d and j not in n and j not in b2 and j not in b1:
                r1.append(j)
        r.append(r1)

    temp['msg22'] = r
    def string(a):
        return " ".join(a)
    temp['msg22'] = temp['msg22'].apply(string)

    return temp,r



def fetch_stats(selected_user,df11):
    if selected_user != 'Overall':
        df11 = df11[df11['user'] == selected_user]

    # 1. fetching no. of msg
    num_msg = df11.shape[0]

    # 2. fetching no. of words in msg
    words = []
    for i in df11['msg1']:
        words.extend(i.split(' ')[1:])

    # 3. fetching no. of media msgs
    num_media = df11[df11['msg1'] == ' <Media omitted>'].shape[0]

    # 4. fetch no. of links shared
    links = []
    for i in df11['msg1']:
        links.extend(url.find_urls(i))

    return num_msg,len(words), num_media, len(links),selected_user

def most_busy_user(df11):
    temp = df11[df11['user'] != 'Group_Notification']
    a11 = temp['user'].value_counts()
    a12 = round(temp['user'].value_counts() / df11.shape[0] * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})

    return a11,a12

def word(selected_user,df11):
    temp,r = temp_needed(selected_user,df11)
    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='Black')
    df_wc = wc.generate(temp['msg22'].str.cat(sep=" "))

    return df_wc

def most_common_words(selected_user,df11):
    temp,r = temp_needed(selected_user,df11)
    w111 = []
    for i in r:
        w111.extend(i)
    df_com_wrd = pd.DataFrame(Counter(w111).most_common(10))

    return  df_com_wrd

def most_common_emoji(selected_user,df11):
    if selected_user != 'Overall':
        df11 = df11[df11['user'] == selected_user]
    e = []
    for i in df11['msg1']:
        e.extend([j for j in i if j in emoji.UNICODE_EMOJI['en']])
    ce = pd.DataFrame(Counter(e).most_common(5)).rename(columns={0:'emoji',1:'frequency_count'})
    return ce

def monthly_timeline(selected_user,df11):
    if selected_user != 'Overall':
        df11 = df11[df11['user'] == selected_user]
    timeline = df11.groupby(['year', 'mont_num', 'month']).count()['msg1'].reset_index()
    t = []
    for i in range(timeline.shape[0]):
        t.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['timmi'] = t
    return timeline

def most_active_hour_of_day(selected_user,df11):
    n1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0]
    n2 = []
    for i in df11['hour']:
        if i in n1:
            # print(str(i),"pm")
            n2.append((str(i) + ".00" + " am"))
        else:
            # print(str(i),"am")
            n2.append((str(i) + ".00" + " pm"))
    df11['hour22'] = n2
    pv = pd.pivot_table(df11, index="day_name", columns='hour22', values='msg1', aggfunc='count').fillna(0)
    return pv

def polarity_score(selected_user,df11):
    obj = SentimentIntensityAnalyzer()
    if selected_user != 'Overall':
        df11 = df11[df11['user'] == selected_user]
    temp,r = temp_needed(selected_user,df11)
    l = ''.join(temp['msg22'])
    return  obj.polarity_scores(l)

