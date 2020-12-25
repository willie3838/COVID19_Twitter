######## NOTES #########
'''
- investigate the use of comparing the list of cities in Canada to clean location
- using or statement for full province and abbreviation
- remove non-english words
'''

# make sure to run pip install pandas if this doesn't work
import pandas as pd
import nltk

def clean_data(filename : str):

    # reading the csv file
    df = pd.read_csv(filename,error_bad_lines=False, engine="python")


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
    provinces = {"prince edward island", "nova scotia", "new brunswick", "quebec", "ontario", "manitoba", "saskatchewan",
                 "alberta", "british columbia", "yukon", "northwest territories", "nunavut"}
    for x in provinces:
        temp_df = temp_df.append(df[df['user_location'].str.contains(x)])


    ################# CITY ANALYSIS ##################
    cities = pd.read_csv("Cities/cities.csv", engine='python')
    # make all text lower case
    cities.Name = cities.Name.str.lower()
    # dropping all NaN values
    cities.dropna(subset=['Name'],inplace=True)

    for city in cities.Name:
        for x in provinces:
            # checks to see if any user location starts with or ends with the city
            if(x in df['user_location']):
                temp_df = temp_df.append(df[df['user_location'].str.startswith(city)])
                temp_df = temp_df.append(df[df['user_location'].str.endswith(city)])



    # checks to see which cities made the cut
    list_of_cities = {}
    for city in cities.Name:
        if temp_df['user_location'].str.contains(city).any():
            if(list_of_cities.get(city) is None):
                list_of_cities[city] = 1
            else:
                list_of_cities[city] += 1

    for k, v in list_of_cities.items():
        print(k, v)


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
    print("Dimensions of original: {}\n".format(og_tweets_df.shape))

def main():
    while True:
        filename = input("Enter the file(s) that you wish to be cleaned (press q to exit): ")
        if filename == "q":
            break

        filename = filename.split(" ")
        counter = 0
        while counter < len(filename):
            file = "./Data/"
            file = file + filename[counter]

            # try:
            open(file)
            print("Cleaning {}...\n".format(filename[counter]))
            clean_data(file)
            # except:
            #     print("File not found try again")
            #     break

            counter+=1



main()
