import pandas as pd
import streamlit as st
from io import StringIO
import matplotlib.pyplot as plt
import seaborn as sns

import Helper
import preprocessor

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
     # To read file as bytes:
     bytes_data = uploaded_file.getvalue()
     data = bytes_data.decode('utf-8')
     StringData = StringIO(data)
     df = pd.read_csv(StringData, sep=";", header=None)
     #st.dataframe(df)
     df11 = preprocessor.preprocess(df)
     # printing dataframe
     # st.write(df11)
     # fetching unique users
     user_list = df11['user'].unique().tolist()
     #user_list.remove('Group_Notification')
     user_list.sort()
     user_list.insert(0, 'Overall')

     # showing a select box for the user to choose form a list
     selected_user = st.sidebar.selectbox('Select user from list:', user_list)

     # creating a button which will show analysis for selected user
     if st.sidebar.button('Show Analysis'):

          # Stats Area
          st.title('STATISTICAL ANALYSIS')
          st.write('')
          num_messages, words, num_media, links, s_u = Helper.fetch_stats(selected_user,df11)
          col1, col2, col3, col4 = st.columns(4)
          with col1:
               st.write('Total message sent by--',s_u)
               st.subheader(num_messages)
          with col2:
               st.write('Total words used by--',s_u)
               st.subheader(words)
          with col3:
               st.write('Total media shared by--',s_u)
               st.subheader(num_media)
          with col4:
               st.write('Total links shared by--',s_u)
               st.subheader(links)

          # Polarity Score
          st.title('POLARITY SCORE')
          ps = Helper.polarity_score(selected_user,df11)
          st.write("Positive words used by",s_u ,"in conversation-- ", round(ps['pos']*100,2), "%")
          st.write("Negative words used by",s_u ,"in conversation-- ", round(ps['neg']*100,2), "%")
          st.write("Neutral words used by",s_u ,"in conversation-- ", round(ps['neu'] * 100, 2), "%")

          #Showing Monthly timeline
          st.title('MONTHLY GROUP USAGE TIMELINE')
          t1 = Helper.monthly_timeline(selected_user,df11)
          fig,ax = plt.subplots()
          ax.plot(t1['timmi'],t1['msg1'],color='green',marker='.',mfc ='y',ms=10)
          ax.set_facecolor("black")
          plt.xticks(rotation = 'vertical')
          plt.xlabel('Month of Year')
          plt.ylabel('Message Count')
          st.pyplot(fig)

          # finding most active user in the group
          if selected_user == 'Overall':
               st.title('Most Active User')
               x,y = Helper.most_busy_user(df11)
               fg, ax = plt.subplots()
               col1, col2 = st.columns(2)

               with col1:
                    ax.bar(x.index,x.values, color='red')
                    plt.grid(axis='x', color='black')
                    ax.set_facecolor("lightgreen")
                    plt.xlabel("Group Members")
                    plt.ylabel("Message Count")
                    plt.xticks(rotation='vertical')
                    st.pyplot(fg)
               with col2:
                    st.write(y)

          # WordCloud
          st.write('')
          st.title('WORDS CLOUD')
          w = Helper.word(selected_user,df11)
          fig,ax = plt.subplots()
          ax.imshow(w)
          st.pyplot(fig)

          # Most Active Hour Of Day
          if selected_user == 'Overall':
               st.title('MOST ACTIVE HOUR OF DAY')
               pv = Helper.most_active_hour_of_day(selected_user, df11)
               fig, ax = plt.subplots()
               ax = sns.heatmap(pv)
               st.pyplot(fig)

          # Most Common Words
          st.write('')
          st.title('MOST COMMON WORDS USED')
          cw = Helper.most_common_words(selected_user,df11)
          fg, ax = plt.subplots()
          plt.grid(axis='y', color='black')
          ax.set_facecolor("lightgreen")
          ax.barh(cw[0], cw[1],color='red')
          st.pyplot(fg)

          # Most Common Emojis
          st.write('')
          st.title('MOST COMMON EMOJI USED')
          ce = Helper.most_common_emoji(selected_user,df11)
          col1,col2 = st.columns(2)
          with col1:
               st.dataframe(ce)
          with col2:
               fig, ax = plt.subplots()
               ax.pie(ce['frequency_count'], labels=ce.index, autopct="%0.2f%%")
               st.pyplot(fig)





