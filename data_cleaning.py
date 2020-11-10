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

###### COUNTRY SEMANTICS #######
# adding all data that include 'Canada' in user_location to the new dataframe
temp_df = temp_df.append(df[df['user_location'].str.contains('canada')])

##### PROVINCE ANALYSIS ########
# Using the full name of the province + internationally approved abbreviations

## NEWFOUNDLAND AND LABRADOR ##

# adding all data that include 'Ontario' in user_location to the new dataframe
temp_df = temp_df.append(df[df['user_location'].str.contains('newfoundland and labrador')])
# adding all data that include 'ON' in user_location to the new dataframe
temp_df = temp_df.append(df[df['user_location'].str.contains('nl')])

## PRINCE EDWARD ISLAND ##

# adding all data that include 'Ontario' in user_location to the new dataframe
temp_df = temp_df.append(df[df['user_location'].str.contains('prince edward island')])
# adding all data that include 'ON' in user_location to the new dataframe
temp_df = temp_df.append(df[df['user_location'].str.contains('pei')])

## NOVA SCOTIA ##

# adding all data that include 'Ontario' in user_location to the new dataframe
temp_df = temp_df.append(df[df['user_location'].str.contains('nova scotia')])
# adding all data that include 'ON' in user_location to the new dataframe
temp_df = temp_df.append(df[df['user_location'].str.contains('ns')])

## NEW BRUNSWICK ##

# adding all data that include 'Ontario' in user_location to the new dataframe
temp_df = temp_df.append(df[df['user_location'].str.contains('new brunswick')])
# adding all data that include 'ON' in user_location to the new dataframe
temp_df = temp_df.append(df[df['user_location'].str.contains('nb')])

## QUEBEC ##

# adding all data that include 'Ontario' in user_location to the new dataframe
temp_df = temp_df.append(df[df['user_location'].str.contains('quebec')])
# adding all data that include 'ON' in user_location to the new dataframe
temp_df = temp_df.append(df[df['user_location'].str.contains('QC')])

## ONTARIO ##

# adding all data that include 'Ontario' in user_location to the new dataframe
temp_df = temp_df.append(df[df['user_location'].str.contains('ontario')])
# adding all data that include 'ON' in user_location to the new dataframe
temp_df = temp_df.append(df[df['user_location'].str.contains('on')])

## MANITOBA ##

# adding all data that include 'Ontario' in user_location to the new dataframe
temp_df = temp_df.append(df[df['user_location'].str.contains('manitoba')])
# adding all data that include 'ON' in user_location to the new dataframe
temp_df = temp_df.append(df[df['user_location'].str.contains('MB')])

## SASKATCHEWAN ##

# adding all data that include 'Saskatchewan' in user_location to the new dataframe
temp_df = temp_df.append(df[df['user_location'].str.contains('saskatchewan')])
# adding all data that include 'ON' in user_location to the new dataframe
temp_df = temp_df.append(df[df['user_location'].str.contains('sk')])

## ALBERTA ##

# adding all data that include 'Ontario' in user_location to the new dataframe
temp_df = temp_df.append(df[df['user_location'].str.contains('alberta')])
# adding all data that include 'ON' in user_location to the new dataframe
temp_df = temp_df.append(df[df['user_location'].str.contains('ab')])

## BRITISH COLUMBIA ##

# adding all data that include 'Ontario' in user_location to the new dataframe
temp_df = temp_df.append(df[df['user_location'].str.contains('british columbia')])
# adding all data that include 'ON' in user_location to the new dataframe
temp_df = temp_df.append(df[df['user_location'].str.contains('bc')])

## YUKON ##

# adding all data that include 'Ontario' in user_location to the new dataframe
temp_df = temp_df.append(df[df['user_location'].str.contains('yukon')])
# adding all data that include 'ON' in user_location to the new dataframe
temp_df = temp_df.append(df[df['user_location'].str.contains('yt')])

## NORTHWEST TERRITORIES ##

# adding all data that include 'Ontario' in user_location to the new dataframe
temp_df = temp_df.append(df[df['user_location'].str.contains('northwest territories')])
# adding all data that include 'ON' in user_location to the new dataframe
temp_df = temp_df.append(df[df['user_location'].str.contains('nt')])

## NUNAVUT ##

# adding all data that include 'Ontario' in user_location to the new dataframe
temp_df = temp_df.append(df[df['user_location'].str.contains('nunavut')])
# adding all data that include 'ON' in user_location to the new dataframe
temp_df = temp_df.append(df[df['user_location'].str.contains('nu')])



# creating a separate dataframe for retweets
rt_tweets_df = pd.DataFrame()

rt_tweets_df = rt_tweets_df.append(temp_df[temp_df['text'].str.contains('rt @')])
og_tweets_df = temp_df[temp_df['text'].str.contains('rt @') == False]

rt_tweets_df.to_csv('./clean_data/retweets.csv')
og_tweets_df.to_csv('./clean_data/og_tweets.csv')