import logging
logging.basicConfig(filename='error.log', format='%(asctime)s:%(levelname)s:%(filename)s:%(funcName)s:%(message)s')
import tweepy
import json
from progress.bar import IncrementalBar



class MyStreamListener(tweepy.StreamListener):
    def __init__(self, amount):
        self.amount = amount
        self.uids = []
        self.__bar = IncrementalBar("Collecting", max = amount)
        super(MyStreamListener, self).__init__()

    def on_data(self, data):
        id_int = int(json.loads(data)["user"]["id_str"])
        if id_int not in self.uids:
            self.uids.append(id_int)
            self.__bar.next()
        if len(self.uids) >= self.amount:
            self.__bar.finish()
            return False
        else:
            return True


            
class TwitterAPI_cl(object):
    def __init__(self, consumer_key, consumer_secret, access_token, secret_token):
        self.__auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.__auth.set_access_token(access_token, secret_token)
        self.__api = tweepy.API(self.__auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        self.__auth2 = tweepy.AppAuthHandler(consumer_key, consumer_secret)
        self.__api2 = tweepy.API(self.__auth2, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    def verify_credentials(self):
        return self.__api.verify_credentials()

    def getAccount(self, id_str):
        try:
            timeline = self.__api2.user_timeline(user_id=id_str)
            uObject = {}
            if len(timeline) > 0:
                uObject = timeline[0]._json['user']
                uObject["bot"] = "unset"
                del uObject['id'] # id_str reicht
                if "profile_banner_url" not in uObject:
                    uObject["profile_banner_url"] = None
                uObject['tweets'] = []
                for tweet in timeline:
                    twt = tweet._json
                    twt["AccID"] = twt["user"]["id_str"]
                    del twt['user'] # da redundant
                    del twt['id'] #  id_str reicht
                    del twt['in_reply_to_status_id'] # ..._str reicht
                    del twt['in_reply_to_user_id'] # ..._str reicht
                    if "possibly_sensitive" not in twt:   # enthält den Key nur wenn sich ein Link im Tweet befindet
                        twt["possibly_sensitive"] = None
                    uObject['tweets'].append(twt)
                return uObject.copy()
            else:
                return -1
        except tweepy.TweepError as e:
            if e.reason == "Not authorized.":
                print("TweepyError: Twitter profile protected.")
                return -1
            elif e.reason == "User has been suspended.":
                print("Skipping account: Twitter profile suspended.")
            else:
                logging.error(e)
                return -1
        except Exception as e:
            logging.error(e)
            return -1

    def getAccountbyHandle(self, handle):
        try:
            user = self.__api.get_user(handle)
            if not(user.protected):
                uObject = {}
                timeline = user.timeline()
                uObject = user._json
                uObject["bot"] = "unset"
                del uObject['id'] # id_str reicht
                if "profile_banner_url" not in uObject:
                    uObject["profile_banner_url"] = None
                uObject['tweets'] = []
                for tweet in timeline:
                    twt = tweet._json
                    twt["AccID"] = twt["user"]["id_str"]
                    del twt['user'] # da redundant
                    del twt['id'] #  id_str reicht
                    del twt['in_reply_to_status_id'] # ..._str reicht
                    del twt['in_reply_to_user_id'] # ..._str reicht
                    if "possibly_sensitive" not in twt:   # enthält den Key nur wenn sich ein Link im Tweet befindet
                        twt["possibly_sensitive"] = None
                    uObject['tweets'].append(twt)
                return uObject.copy()
            else:
                return -1
        except tweepy.TweepError as e:
            if e.reason == "Not authorized.":
                print("Protected Twitter profile!")
            elif e.reason == "User has been suspended.":
                print("Skipping account: Twitter profile suspended.")
            else:
                logging.error(e) # "TweepyError " + str(e.args[0][0]["code"]) + ": " + e.args[0][0]["message"]
            return -1

    def getTweet(self, id_str):
        try:
            status = self.__api.get_status(id_str)
            tObject = {}
            tObject = status._json
            tObject["AccID"] = tObject["user"]["id_str"]
            del tObject['user'] # da redundant
            del tObject['id'] #  id_str reicht
            del tObject['in_reply_to_status_id'] # ..._str reicht
            del tObject['in_reply_to_user_id'] # ..._str reicht
            if "possibly_sensitive" not in tObject:   # enthält den Key nur wenn sich ein Link im Tweet befindet
                tObject["possibly_sensitive"] = None
            return tObject.copy()
        except tweepy.TweepError as e:
            if e.reason == "Not authorized.":
                print("Skipping account: Twitter profile protected.")
                return -1
            elif e.reason == "User has been suspended.":
                print("Skipping account: Twitter profile suspended.")
            else:
                logging.error(e)
                return -1
        except Exception as e:
            logging.error(e)
            return -1

    def collect_uids_by_stream(self, keyword, amount):
        try:
            myStreamListener = MyStreamListener(amount)
            myStream = tweepy.Stream(auth = self.__api.auth, listener=myStreamListener)
            myStream.filter(track=[str(keyword)])
            uids = myStreamListener.uids
            self.uids_from_stream = uids
            return uids
        except tweepy.TweepError as e:
            logging.error(e)
            return -1

    def collect_fullinfo_by_stream(self, keyword, amount):
        try:
            uids = self.collect_uids_by_stream(keyword, amount)
            ulist = [] # List of uObject
            uObject = {}
            bar = IncrementalBar("ParsingData", max = len(uids))
            for id_str in uids:
                uObject = self.getAccount(id_str)
                if (uObject != -1) and (type(uObject) is dict):
                    ulist.append(uObject.copy())
                    bar.next()
            bar.finish()
            return ulist
        except Exception as e:
            logging.error(e)
            return -1