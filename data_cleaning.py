######## NOTES #########
'''
- investigate the use of comparing the list of cities in Canada to clean location
- using or statement for full province and abbreviation
- remove non-english words
'''

# make sure to run pip install pandas if this doesn't work
import pandas as pd
import nltk

# reading the csv file
df = pd.read_csv("April_23/coronavirus-tweet-id-2020-04-23-00.csv")

################# UNECESSARY COLUMNS ##################

df.drop(columns=['place','possibly_sensitive','user_created_at','user_default_profile_image',
                 'user_favourites_count','user_listed_count','user_name','user_time_zone',
                 'user_urls'], inplace=True)


################## REMOVING VERIFIED ACCOUNTS ##############
df = df[df['user_verified'] == False]

# creating a temporary dataframe to store cleaned data
temp_df = pd.DataFrame()

# make all text lower case
df.text = df.text.str.lower()

################# REMOVING RANDOM CHARACTERS ##################

# uses regex and removes all characters that arent part of the alphabet, number set, puncation set, and special character set
df.text = df.text.str.replace(r'[^a-z0-9~`!@#$%^&*()_+[{\]\}\|;:\'\",<.>/? ]+','')

################# LOCATION DATA ##################

# finding rows that  contain the word "Canada" in user_location
# dropping all NA/NaN values in the column user_location
df.dropna(subset=['user_location'],inplace=True)

# ###### COUNTRY SEMANTICS #######
# # adding all data that include 'Canada' in user_location to the new dataframe
# temp_df = temp_df.append(df[df['user_location'].str.contains('canada')])
#
# ##### PROVINCE ANALYSIS ########
# # Using the full name of the province + internationally approved abbreviations
#
# ## NEWFOUNDLAND AND LABRADOR ##
# temp_df = temp_df.append(df[df['user_location'].str.contains('newfoundland and labrador')])
#
#
# ## PRINCE EDWARD ISLAND ##
# temp_df = temp_df.append(df[df['user_location'].str.contains('prince edward island')])
#
#
# ## NOVA SCOTIA ##
# temp_df = temp_df.append(df[df['user_location'].str.contains('nova scotia')])
#
# ## NEW BRUNSWICK ##
# temp_df = temp_df.append(df[df['user_location'].str.contains('new brunswick')])
#
#
# ## QUEBEC ##
# temp_df = temp_df.append(df[df['user_location'].str.contains('quebec')])
#
# ## ONTARIO ##
#
# temp_df = temp_df.append(df[df['user_location'].str.contains('ontario')])
#
#
# ## MANITOBA ##
# temp_df = temp_df.append(df[df['user_location'].str.contains('manitoba')])
#
#
# ## SASKATCHEWAN ##
# temp_df = temp_df.append(df[df['user_location'].str.contains('saskatchewan')])
#
# ## ALBERTA ##
# temp_df = temp_df.append(df[df['user_location'].str.contains('alberta')])
#
# ## BRITISH COLUMBIA ##
# temp_df = temp_df.append(df[df['user_location'].str.contains('british columbia')])
#
#
# ## YUKON ##
# temp_df = temp_df.append(df[df['user_location'].str.contains('yukon')])
#
# ## NORTHWEST TERRITORIES ##
# temp_df = temp_df.append(df[df['user_location'].str.contains('northwest territories')])
#
# ## NUNAVUT ##
# temp_df = temp_df.append(df[df['user_location'].str.contains('nunavut')])

################# CITY ANALYSIS ##################
# cities = pd.read_csv("Cities/list_of_municipalities_of_canada-1633j.csv", engine='python')
# # make all text lower case
# cities.Name = cities.Name.str.lower()
# # dropping all NaN values
# cities.dropna(subset=['Name'],inplace=True)
#
# for city in cities.Name:
#     print(city)
#     # checks to see if any user location starts with, ends with, or has the city name in between its description
#     temp_df = temp_df.append(df[df['user_location'].str.startswith(city+" ")])
#     temp_df = temp_df.append(df[df['user_location'].str.endswith(city + " ")])
#     temp_df = temp_df.append(df[df['user_location'].str.find(" " + city + " ")!=-1])
#     temp_df = temp_df.append(df[df['user_location'].str.find(" ," + city + ", ") != -1])
#     temp_df = temp_df.append(df[df['user_location'].str.find(" ," + city + " ") != -1])
#     temp_df = temp_df.append(df[df['user_location'].str.find(" " + city + ", ") != -1])





# creating a separate dataframe for retweets
rt_tweets_df = pd.DataFrame()

rt_tweets_df = rt_tweets_df.append(temp_df[temp_df['text'].str.contains('rt @')])
og_tweets_df = temp_df[temp_df['text'].str.contains('rt @') == False]

# exporting files with different names each time based on the year, month, and day
import time
timestr = time.strftime("%Y%m%d-%H%M%S")

rt_tweets_df.to_csv('./clean_data/retweets-{}.csv'.format(timestr))
print("Dimensions of retweets: {}".format(rt_tweets_df.shape))

og_tweets_df.to_csv('./clean_data/og_tweets-{}.csv'.format(timestr))
print("Dimensions of original: {}".format(og_tweets_df.shape))