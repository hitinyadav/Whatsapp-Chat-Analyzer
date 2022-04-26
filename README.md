# Whatsapp-Chat-Analyzer
Whatsapp Chat Analyzer do analysis on chat between two or more users. It tells the sentiment of msg whether the msg sent is positive,negative or neutral. Also we can find out the most active user and the most common words used in chat. We can also check the common emoji sent. Also gives a count of media and links shared in chat.

# Web Development
I have used Streamlit for the web development part, streamlit is easy to use and have some awesome features for the people who dont know much about web development.

# Files
1) App.py is the main application file it contain all code for web development using streamlit. It is our main source file.
2) Helper.py is a support file which was created to write all the helper function which are directly used in app.py just for the maintenance and visibility of our code.
3) Preprocessor.py was created to create our ready to use dataframe whihc is further used to do more analysis on data.
4) Whatsapp_CA_new.ipynb is a jupyter notebook file which shows how I have read the dataset and transformed raw data, cleaned it for the visualization and prepared our dataframe for further analysis use.
5) Stop_hinglish.txt is a file containing some handmade limited stopwords for hinglish language. Anyone can add more stopwords in it for their further use.

# Application
1) First the website ask user to upload any whatsapp chat file(group chat or individual chat)
2) After file upload a dropdown containing all group member and Overall will be shown. Here Overall refer to the all group. Overall consider all member as a single individual used to show gorup level analysis.
3) We can select either Overall or any other group member form the dropdown and click on Show Analysis.
4) Our code shows-- 
        > Statistical Analysis on data 
        > Polarity Score, whether the msg sent has positive,negative or neutral sentimnets 
        > Monthly Timeline, which month of year was most active 
        > Most Active User in between two user or group
        > Word Cloud, cloud containing words used in chat
        > Most Active Hour Of Day
        > Most Common Words Used in chat
        > Most Common Emoji Used in chat
