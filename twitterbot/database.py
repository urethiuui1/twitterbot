import logging
logging.basicConfig(filename='error.log', format='%(asctime)s:%(levelname)s:%(filename)s:%(funcName)s:%(message)s')
import sqlite3
sqlite3.enable_callback_tracebacks(True)
import os
import json



class Database_cl(object):
    def __init__(self, path="/database/database.sqlite3"):
        self.__dbpath = os.path.join(path)
        self.__connection = self.__db_connect(self.__dbpath)
        self.__cur = self.__connection.cursor()

    def __db_connect(self, db_path):
        con = sqlite3.connect(db_path, check_same_thread=False)
        return con

    def createTables(self):
        try:
            links_sql = "CREATE TABLE accounts (id_str STRING PRIMARY KEY, name TEXT, screen_name TEXT, location TEXT, description TEXT, url TEXT, entities TEXT, protected TEXT, followers_count TEXT, friends_count TEXT, listed_count TEXT, created_at TEXT, favourites_count TEXT, utc_offset TEXT, time_zone TEXT, geo_enabled TEXT, verified TEXT, statuses_count TEXT, lang TEXT, contributors_enabled TEXT, is_translator TEXT, is_translation_enabled TEXT, profile_background_color TEXT, profile_background_image_url TEXT, profile_background_image_url_https TEXT, profile_background_tile TEXT, profile_image_url TEXT, profile_image_url_https TEXT, profile_banner_url TEXT, profile_link_color TEXT, profile_sidebar_border_color TEXT, profile_sidebar_fill_color TEXT, profile_text_color TEXT, profile_use_background_image TEXT, has_extended_profile TEXT, default_profile TEXT, default_profile_image TEXT, following TEXT, follow_request_sent TEXT, notifications TEXT, translator_type TEXT, withheld_in_countries TEXT, bot TEXT)"
            self.__cur.execute(links_sql)
            links_sql = "CREATE TABLE tweets (AccID STRING NOT NULL, id_str STRING, created_at TEXT, text TEXT, truncated TEXT, entities TEXT, source TEXT, in_reply_to_status_id_str TEXT, in_reply_to_user_id_str TEXT, in_reply_to_screen_name TEXT, geo TEXT, coordinates TEXT, place TEXT, contributors TEXT, is_quote_status TEXT, retweet_count TEXT, favorite_count TEXT, favorited TEXT, retweeted TEXT, possibly_sensitive TEXT, lang TEXT , FOREIGN KEY (AccID) REFERENCES accounts (id_str), PRIMARY KEY (ACCID, id_str))"
            self.__cur.execute(links_sql)
            return 0
        except Exception as e:
            logging.error(e)
            return -1

    def persist(self, uObject, overwrite=True):
        try:
            if self.insertAccount(uObject, overwrite) == -1:
                logging.error("Account already in database")
                return -1
            for tObject in uObject["tweets"]:
                self.insertTweet(tObject, overwrite)
            self.__connection.commit()
            return 0
        except Exception as e:
            logging.error(e)
            return -1

    def persistList(self, ulist, overwrite=True):
        try:
            for uObject in ulist:
                if self.insertAccount(uObject, overwrite) == -1:
                    return -1
                for tObject in uObject["tweets"]:
                    self.insertTweet(tObject, overwrite)
            self.__connection.commit()
            return 0
        except Exception as e:
            logging.error(e)
            return -1
    def insertAccount(self, uObject, overwrite):
        if overwrite:
            link_sql = "INSERT OR REPLACE INTO accounts (id_str, name, screen_name, location, description, url, entities, protected, followers_count, friends_count, listed_count, created_at, favourites_count, utc_offset, time_zone, geo_enabled, verified, statuses_count, lang, contributors_enabled, is_translator, is_translation_enabled, profile_background_color, profile_background_image_url, profile_background_image_url_https, profile_background_tile, profile_image_url, profile_image_url_https, profile_banner_url, profile_link_color, profile_sidebar_border_color, profile_sidebar_fill_color, profile_text_color, profile_use_background_image, has_extended_profile, default_profile, default_profile_image, following, follow_request_sent, notifications, translator_type, withheld_in_countries, bot) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        else:
            link_sql = "INSERT INTO accounts (id_str, name, screen_name, location, description, url, entities, protected, followers_count, friends_count, listed_count, created_at, favourites_count, utc_offset, time_zone, geo_enabled, verified, statuses_count, lang, contributors_enabled, is_translator, is_translation_enabled, profile_background_color, profile_background_image_url, profile_background_image_url_https, profile_background_tile, profile_image_url, profile_image_url_https, profile_banner_url, profile_link_color, profile_sidebar_border_color, profile_sidebar_fill_color, profile_text_color, profile_use_background_image, has_extended_profile, default_profile, default_profile_image, following, follow_request_sent, notifications, translator_type, withheld_in_countries, bot) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        datatuple = (str(uObject["id_str"]),str(uObject["name"]),str(uObject["screen_name"]),str(uObject["location"]),str(uObject["description"]),str(uObject["url"]),json.dumps(str(uObject["entities"])),str(uObject["protected"]),str(uObject["followers_count"]),str(uObject["friends_count"]),str(uObject["listed_count"]),str(uObject["created_at"]),str(uObject["favourites_count"]),str(uObject["utc_offset"]),str(uObject["time_zone"]),str(uObject["geo_enabled"]),str(uObject["verified"]),str(uObject["statuses_count"]),str(uObject["lang"]),str(uObject["contributors_enabled"]),str(uObject["is_translator"]),str(uObject["is_translation_enabled"]),str(uObject["profile_background_color"]),str(uObject["profile_background_image_url"]),str(uObject["profile_background_image_url_https"]),str(uObject["profile_background_tile"]),str(uObject["profile_image_url"]),str(uObject["profile_image_url_https"]),str(uObject["profile_banner_url"]),str(uObject["profile_link_color"]),str(uObject["profile_sidebar_border_color"]),str(uObject["profile_sidebar_fill_color"]),str(uObject["profile_text_color"]),str(uObject["profile_use_background_image"]),str(uObject["has_extended_profile"]),str(uObject["default_profile"]),str(uObject["default_profile_image"]),str(uObject["following"]),str(uObject["follow_request_sent"]),str(uObject["notifications"]),str(uObject["translator_type"]),str(uObject["withheld_in_countries"]), str(uObject["bot"]))
        try:
            self.__cur.execute(link_sql, datatuple)
            return 0
        except sqlite3.OperationalError as e:
            if e.args[0].startswith('no such table'):
                self.createTables()
                self.__cur.execute(link_sql, datatuple)
                return -1
        except Exception as e:
            logging.error(e)
            return -1

    def insertTweet(self, tObject, overwrite):
        if overwrite:
            link_sql = "INSERT OR REPLACE INTO tweets (AccID, id_str, created_at, text, truncated, entities, source, in_reply_to_status_id_str, in_reply_to_user_id_str, in_reply_to_screen_name, geo, coordinates, place, contributors, is_quote_status, retweet_count, favorite_count, favorited, retweeted, possibly_sensitive, lang) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        else:
            link_sql = "INSERT INTO tweets (AccID, id_str, created_at, text, truncated, entities, source, in_reply_to_status_id_str, in_reply_to_user_id_str, in_reply_to_screen_name, geo, coordinates, place, contributors, is_quote_status, retweet_count, favorite_count, favorited, retweeted, possibly_sensitive, lang) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        datatuple = (str(tObject["AccID"]), str(tObject["id_str"]), str(tObject["created_at"]), str(tObject["text"]), str(tObject["truncated"]), json.dumps(str(tObject["entities"])), str(tObject["source"]), str(tObject["in_reply_to_status_id_str"]), str(tObject["in_reply_to_user_id_str"]), str(tObject["in_reply_to_screen_name"]), str(tObject["geo"]), str(tObject["coordinates"]), str(tObject["place"]), str(tObject["contributors"]), str(tObject["is_quote_status"]), str(tObject["retweet_count"]), str(tObject["favorite_count"]), str(tObject["favorited"]), str(tObject["retweeted"]), str(tObject["possibly_sensitive"]), str(tObject["lang"]))
        try:
            self.__cur.execute(link_sql, datatuple)
            return 0
        except sqlite3.OperationalError as e:
            if e.args[0].startswith('no such table'):
                self.createTables()
                self.__cur.execute(link_sql, datatuple)
                return -1
        except Exception as e:
            logging.error(e)
            return -1

    def getAccounts(self):
        try:
            self.__cur.execute("SELECT * FROM accounts")
        except sqlite3.OperationalError as e:
            if e.args[0].startswith('no such table'):
                self.createTables()
                self.__cur.execute("SELECT * FROM accounts")
            logging.error(e)
            return -1
        except Exception as e:
            logging.error(e)
            return -1
        allAccounts = self.__cur.fetchall()
        uObject = {}
        ulist = []
        for account in allAccounts:
            self.__cur.execute('SELECT * FROM tweets WHERE AccID = "' + str(account[0]) + '"')
            allTweets = self.__cur.fetchall()
            uObject = self.__construct_uObject(account, allTweets)
            ulist.append(uObject.copy())
        return ulist

    def getAccount(self, id_str):
        try:
            self.__cur.execute('SELECT * FROM accounts WHERE id_str = "' + str(id_str) + '"')
        except sqlite3.OperationalError as e:
            if e.args[0].startswith('no such table'):
                self.createTables()
                self.__cur.execute('SELECT * FROM accounts WHERE id_str = "' + str(id_str) + '"')
            logging.error(e)
            return -1
        except Exception as e:
            logging.error(e)
            return -1
        try:
            account = self.__cur.fetchall()[0]
        except IndexError:
            return -1
        except Exception as e:
            logging.error(e)
            return -1
        self.__cur.execute('SELECT * FROM tweets WHERE AccID = "' + str(account[0]) + '"')
        allTweets = self.__cur.fetchall()
        uObject = self.__construct_uObject(account, allTweets)
        return uObject

    def get_bots(self):
        try:
            self.__cur.execute("SELECT * FROM accounts WHERE bot='bot'")
        except sqlite3.OperationalError as e:
            if e.args[0].startswith('no such table'):
                self.createTables()
                self.__cur.execute("SELECT * FROM accounts WHERE bot='bot'")
            logging.error(e)
            return -1
        except Exception as e:
            logging.error(e)
            return -1
        allAccounts = self.__cur.fetchall()
        uObject = {}
        ulist = []
        for account in allAccounts:
            # select tweets by account id
            self.__cur.execute('SELECT * FROM tweets WHERE AccID = "' + str(account[0]) + '"')
            allTweets = self.__cur.fetchall()
            uObject = self.__construct_uObject(account, allTweets)
            ulist.append(uObject.copy())
        return ulist

    def get_humans(self):
        try:
            self.__cur.execute("SELECT * FROM accounts WHERE bot='human'")
        except sqlite3.OperationalError as e:
            if e.args[0].startswith('no such table'):
                self.createTables()
                self.__cur.execute("SELECT * FROM accounts WHERE bot='human'")
            logging.error(e)
            return -1
        except Exception as e:
            logging.error(e)
        allAccounts = self.__cur.fetchall()
        uObject = {}
        ulist = []
        for account in allAccounts:
            self.__cur.execute('SELECT * FROM tweets WHERE AccID = "' + str(account[0]) + '"')
            allTweets = self.__cur.fetchall()
            uObject = self.__construct_uObject(account, allTweets)
            ulist.append(uObject.copy())
        return ulist

    def get_unannotated(self):
        try:
            self.__cur.execute("SELECT * FROM accounts WHERE bot='unset'")
        except sqlite3.OperationalError as e:
            if e.args[0].startswith('no such table'):
                self.createTables()
                self.__cur.execute("SELECT * FROM accounts WHERE bot='unset'")
            logging.error(e)
            return -1
        except Exception as e:
            logging.error(e)
            return -1
        allAccounts = self.__cur.fetchall()
        uObject = {}
        ulist = []
        for account in allAccounts:
            self.__cur.execute('SELECT * FROM tweets WHERE AccID = "' + str(account[0]) + '"')
            allTweets = self.__cur.fetchall()
            uObject = self.__construct_uObject(account, allTweets)
            ulist.append(uObject.copy())
        return ulist

    def get_single_unannotated(self):
        try:
            self.__cur.execute("SELECT * FROM accounts WHERE bot='unset' LIMIT 1")
        except sqlite3.OperationalError as e:
            if e.args[0].startswith('no such table'):
                self.createTables()
                self.__cur.execute("SELECT * FROM accounts WHERE bot='unset' LIMIT 1")
            logging.error(e)
            return -1
        except Exception as e:
            logging.error(e)
            return -1
        try:
            account = self.__cur.fetchall()[0]
        except IndexError:
            return -1 # keine unset da
        except Exception as e:
            logging.error(e)
            return -1
        uObject = {}
        self.__cur.execute('SELECT * FROM tweets WHERE AccID = "' + str(account[0]) + '"')
        allTweets = self.__cur.fetchall()
        uObject = self.__construct_uObject(account, allTweets)
        return uObject

    def get_annotated(self):
        try:
            self.__cur.execute("SELECT * FROM accounts WHERE bot='bot' OR bot='human'")
        except sqlite3.OperationalError as e:
            if e.args[0].startswith('no such table'):
                self.createTables()
                self.__cur.execute("SELECT * FROM accounts WHERE bot='bot' OR bot='human'")
            logging.error(e)
            return -1
        except Exception as e:
            logging.error(e)
            return -1
        allAccounts = self.__cur.fetchall()
        uObject = {}
        ulist = []
        for account in allAccounts:
            self.__cur.execute('SELECT * FROM tweets WHERE AccID = "' + str(account[0]) + '"')
            allTweets = self.__cur.fetchall()
            uObject = self.__construct_uObject(account, allTweets)
            ulist.append(uObject.copy())
        return ulist

    def annotate(self, id_str, bot):
        if bot == "bot":
            try:
                self.__cur.execute("UPDATE accounts SET bot='bot' WHERE id_str=" + '"' + str(id_str) +'"')
            except Exception as e:
                logging.error(e)
                return -1
            self.__connection.commit()
        elif bot == "human":
            try:
                self.__cur.execute("UPDATE accounts SET bot='human' WHERE id_str=" + '"' + str(id_str) +'"')
            except Exception as e:
                logging.error(e)
                return -1
            self.__connection.commit()
        else:
            try:
                self.__cur.execute("UPDATE accounts SET bot='unset' WHERE id_str=" + '"' + str(id_str) +'"')
            except Exception as e:
                logging.error(e)
                return -1
            self.__connection.commit()  

    def __construct_uObject(self, account, allTweets):
        uObject = {}
        uObject["id_str"] = account[0]
        uObject["name"] = account[1]
        uObject["screen_name"] = account[2]
        uObject["location"] = account[3]
        uObject["description"] = account[4]
        uObject["url"] = account[5]
        uObject["entities"] = account[6]
        uObject["protected"] = account[7]
        uObject["followers_count"] = account[8]
        uObject["friends_count"] = account[9]
        uObject["listed_count"] = account[10]
        uObject["created_at"] = account[11]
        uObject["favourites_count"] = account[12]
        uObject["utc_offset"] = account[13]
        uObject["time_zone"] = account[14]
        uObject["geo_enabled"] = account[15]
        uObject["verified"] = account[16]
        uObject["statuses_count"] = account[17]
        uObject["lang"] = account[18]
        uObject["contributors_enabled"] = account[19]
        uObject["is_translator"] = account[20]
        uObject["is_translation_enabled"] = account[21]
        uObject["profile_background_color"] = account[22]
        uObject["profile_background_image_url"] = account[23]
        uObject["profile_background_image_url_https"] = account[24]
        uObject["profile_background_tile"] = account[25]
        uObject["profile_image_url"] = account[26]
        uObject["profile_image_url_https"] = account[27]
        uObject["profile_banner_url"] = account[28]
        uObject["profile_link_color"] = account[29]
        uObject["profile_sidebar_border_color"] = account[30]
        uObject["profile_sidebar_fill_color"] = account[31]
        uObject["profile_text_color"] = account[32]
        uObject["profile_use_background_image"] = account[33]
        uObject["has_extended_profile"] = account[34]
        uObject["default_profile"] = account[35]
        uObject["default_profile_image"] = account[36]
        uObject["following"] = account[37]
        uObject["follow_request_sent"] = account[38]
        uObject["notifications"] = account[39]
        uObject["translator_type"] = account[40]
        uObject["withheld_in_countries"] = account[41]
        uObject["bot"] = account[42]

        uObject["tweets"] = []
        tObject = {}
        for tweet in allTweets:
            tObject["AccID"] = tweet[0]
            tObject["id_str"] = tweet[1]
            tObject["created_at"] = tweet[2]
            tObject["text"] = tweet[3]
            tObject["truncated"] = tweet[4]
            tObject["entities"] = tweet[5]
            tObject["source"] = tweet[6]
            tObject["in_reply_to_status_id_str"] = tweet[7]
            tObject["in_reply_to_user_id_str"] = tweet[8]
            tObject["in_reply_to_screen_name"] = tweet[9]
            tObject["geo"] = tweet[10]
            tObject["coordinates"] = tweet[11]
            tObject["place"] = tweet[12]
            tObject["contributors"] = tweet[13]
            tObject["is_quote_status"] = tweet[14]
            tObject["retweet_count"] = tweet[15]
            tObject["favorite_count"] = tweet[16]
            tObject["favorited"] = tweet[17]
            tObject["retweeted"] = tweet[18]
            tObject["possibly_sensitive"] = tweet[19]
            tObject["lang"] = tweet[20]

            uObject["tweets"].append(tObject.copy())
        return uObject

    def deleteAccount(self, id_str):
        link_sql = "DELETE FROM accounts WHERE id_str = " + str(id_str)
        try:
            self.__cur.execute(link_sql)
        except Exception as e:
            logging.error(e)
            return -1
        link_sql = "DELETE FROM tweets WHERE AccID = " + str(id_str)
        try:
            self.__cur.execute(link_sql)
        except Exception as e:
            logging.error(e)
            return -1
        self.__connection.commit()

    def closeConnection(self):
        try:
            self.__connection.commit()
            return 0
        except Exception as e:
            logging.error(e)
            return -1