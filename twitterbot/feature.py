import Levenshtein
import datetime
from dateutil import parser
from numpy import mean
import re



class Feature_Engine_cl(object):
    def __init__(self):
        self.features = {
            "followers_count":self.__followers_count,
            "friends_count":self.__friends_count,
            "listed_count":self.__listed_count,
            "created_at":self.__created_at,
            "favourites_count":self.__favourites_count,
            "geo_enabled":self.__geo_enabled,
            "verified":self.__verified,
            "statuses_count":self.__statuses_count,
            "has_extended_profile":self.__has_extended_profile,
            "default_profile":self.__default_profile,
            "levNameScreenName":self.__levNameScreenName,          # Calculate Levenshtein distance between Name and Screen Name
            "screen_name_digits":self.__screen_name_digits,         
            "botinnames":self.__botinnames,                         # "bot" in name or screen_name
            "tokencount":self.__tokencount,
            "average_time_betweet_tweets":self.__average_time_betweet_tweets,
            "url_in_tweet_count":self.__url_in_tweet_count,
            "average_favourite_count_tweets":self.__average_favourite_count_tweets,
            "average_retweet_count_tweets":self.__average_retweet_count_tweets,
            "average_tweet_length":self.__average_tweet_length,
            "giveway_in_tweets_count":self.__giveway_in_tweets_count,
            "airdrop_in_tweets_count":self.__airdrop_in_tweets_count,
            "retweet_count":self.__retweet_count
        }

    def getFeatures(self):
        fl = []
        for feature in self.features.keys():
            fl.append(feature)
        return fl


    ###################################################################################
    # Account based feature methods
    ###################################################################################

    def __followers_count(self, uObject):
        return uObject["followers_count"]

    def __friends_count(self, uObject):
        return uObject["friends_count"]

    def __listed_count(self, uObject):
        return uObject["listed_count"]

    def __created_at(self, uObject):
        d1 = parser.parse(uObject["created_at"])
        return d1.year

    def __favourites_count(self, uObject):
        return uObject["favourites_count"]

    def __geo_enabled(self, uObject):
        return bool(uObject["geo_enabled"])

    def __verified(self, uObject):
        return bool(uObject["verified"])

    def __statuses_count(self, uObject):
        return uObject["statuses_count"]

    def __has_extended_profile(self, uObject):
        return bool(uObject["has_extended_profile"])

    def __default_profile(self, uObject):
        return bool(uObject["default_profile"])

    def __levNameScreenName(self, uObject):
        return Levenshtein.distance(uObject["name"], uObject["screen_name"])

    def __screen_name_digits(self, uObject):
        c = 0
        for letter in uObject["screen_name"]:
            if letter.isdigit():
                c = c + 1
        return c

    def __botinnames(self, uObject):
        return ("bot" in uObject["name"]) or ("bot" in uObject["screen_name"])


    ###################################################################################
    # Tweet based feature methods
    ###################################################################################

    def __tokencount(self, uObject):
        cs = []
        for tweet in uObject["tweets"]:
            a = len(tweet["text"].split("!"))
            b = len(tweet["text"].split("?"))
            c = len(tweet["text"].split("."))
            d = len(tweet["text"].split("#"))
            e = len(tweet["text"].split("@"))
            cs.append(a+b+c+d+e)
        return sum(cs)/len(cs) if sum(cs)>0 else 0
        # if sum(cs) > 0:
        #     return sum(cs)/len(cs)
        # else:
        #    return 0
        return sum()

    def __average_time_betweet_tweets(self, uObject):
        diffs = []
        if len(uObject["tweets"]) < 2:
            return 0
        for i in range(0, len(uObject["tweets"])-1):
            d1 = parser.parse(uObject["tweets"][i]["created_at"])
            d2 = parser.parse(uObject["tweets"][i+1]["created_at"])
            diffs.append(abs(d2-d1).days)
        return round(mean(diffs),3)

    def __url_in_tweet_count(self, uObject):
        # Quelle: https://www.geeksforgeeks.org/python-check-url-string/
        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        c = 0
        for tweet in uObject["tweets"]:
            if len(re.findall(regex,tweet["text"])) > 1:
                c = c + 1
        return c

    def __average_favourite_count_tweets(self, uObject):
        c = 0
        for tweet in uObject["tweets"]:
            c = c + int(tweet["favorite_count"])
        return c / len(uObject["tweets"]) if c>0 else 0

    def __average_retweet_count_tweets(self, uObject):
        c = 0
        for tweet in uObject["tweets"]:
            c = c + int(tweet["retweet_count"])
        return c / len(uObject["tweets"]) if c>0 else 0

    def __average_tweet_length(self, uObject):
        cs = []
        for tweet in uObject["tweets"]:
            cs.append(len(tweet["text"]))
        return mean(cs) if len(cs)>0 else 0

    def __giveway_in_tweets_count(self, uObject):
        c = 0
        for tweet in uObject["tweets"]:
            if "giveaway" in tweet["text"].lower():
                c = c + 1
        return c

    def __airdrop_in_tweets_count(self, uObject):
        c = 0
        for tweet in uObject["tweets"]:
            if "airdrop" in tweet["text"].lower() or "air drop" in tweet["text"].lower():
                c = c + 1
        return c
        
    def __retweet_count(self, uObject):
        c = 0
        for tweet in uObject["tweets"]:
            if tweet["text"].startswith("RT"):
                c = c + 1
        return c