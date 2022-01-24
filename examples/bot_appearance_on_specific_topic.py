# Counting bot accounts on specific topics using the Framework with a self-trained model, adding them to a dataset of classified accounts and exporting the dataset as a csv file (AccountID:classification)

from twitterbot import *

def main():
    CL = collect.Collect_cl()
    CL.setAPIcredentials("consumer_key", "consumer_secret", "access_token", "secret_token")
    CL.openDB("./tweetstream_bitcoin.sqlite")
    CL.parse_from_stream_by_keyword("Bitcoin", 100)
    CL.saveAccountsToDB()


    FS2 = "followers_count, friends_count, listed_count, created_at, favourites_count, geo_enabled, verified, statuses_count, default_profile, levNameScreenName, screen_name_digits, botinnames, tokencount, average_time_betweet_tweets, url_in_tweet_count, average_favourite_count_tweets, average_retweet_count_tweets, average_tweet_length, retweet_count".split(", ")
    TST_model = test.Classify_cl("./model.joblib", FS2)
    CL.clearAccountData()
    CL.getDB()
    
    Botcount_model = 0
    
    for uObject in CL.AccountData:
        if TST_model.predictByuObject(uObject) == "bot":
            Botcount_model = Botcount_model + 1
    print("Accounts: " + str(len(CL.AccountData)) + "\nPredicted Bots by model.joblib: " + str(Botcount_model))
    
    # Classifiying collected accounts with model.joblib
    for uObject in CL.AccountData:
        CL.annotate(uObject["id_str"], TST_model.predictByuObject(uObject))
    CL.exportAnnotated("./tweetstream_bitcoin.csv")
if __name__ == "__main__":
    main()
