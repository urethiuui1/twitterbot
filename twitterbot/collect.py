import logging
import importlib
logging.basicConfig(filename='error.log', format='%(asctime)s:%(levelname)s:%(filename)s:%(funcName)s:%(message)s')
from . import database
from . import TwitterAPI
from . import feature
import pandas as pd
import csv
from progress.bar import IncrementalBar



class Collect_cl(object):
    def __init__(self):
        self.DB = object
        self.API = object
        self.FT = feature.Feature_Engine_cl()
        self.__login = False
        self.AccountData = [] # List of uObjects
        self.df = pd.DataFrame() # Pandas Dataframe für Features


    ###################################################################################
    ###################################################################################
    
    def setAPIcredentials(self, consumer_key, consumer_secret, access_token, secret_token):
        try:
            self.API = TwitterAPI.TwitterAPI_cl(consumer_key, consumer_secret, access_token, secret_token)
            if self.API.verify_credentials():
                self.__login = True
                return 0
            else:
                self.__login = False
                logging.error("Twitter API credentials invalid")
                return -1
        except Exception as e:
            logging.error(e)
            return -1
    def openDB(self, path):
        if len(path) < 1:
            logging.error("please specify a database")
            return -1
        try:
            self.DB = database.Database_cl(path)
            return 0
        except:
            return -1


    ###################################################################################
    # Collecting based methods
    ###################################################################################

    # parse from annotated data (accID:bot)
    def parseDataset(self, path):
        if not(self.__login) and type(self.DB) == type:
            logging.warning("didn't log in with setAPIcredentials() or database not opened with openDB()")
            return -1
        if path.lower().endswith(".tsv"):
            delimiter = '	'
        elif path.lower().endswith(".csv"):
            delimiter = ','
        else:
            logging.warning("please provide a .tsv or .csv file")
            return -1
        ulist = []
        try:
            with open(path) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=delimiter)
                for row in csv_reader:
                    ulist.append(row)
        except EnvironmentError as e:
            logging.error("Error while opening file")
            logging.error(e)
            return -1
        except Exception as e:
            logging.error(e)
            return -1

        bar = IncrementalBar("ParsingData", max = len(ulist))
        for i in ulist:
            uObject = self.API.getAccount(i[0])
            if (uObject != -1) and (type(uObject) is dict):
                uObject["bot"] = i[1]
                self.AccountData.append(uObject.copy())
                bar.next()
        bar.finish()
        return 0

    def parse_from_stream_by_keyword(self, keyword, amount):
        if not(self.__login) and type(self.DB) == type:
            logging.warning("didn't log in with setAPIcredentials() or database not opened with openDB()")
            return -1
        uids = self.API.collect_uids_by_stream(keyword, amount)
        bar = IncrementalBar("ParsingData", max = len(uids))
        for uid in uids:
            uObject = self.API.getAccount(uid)
            if (uObject != -1) and (type(uObject) is dict):
                self.AccountData.append(uObject.copy())
                bar.next()
        bar.finish()
        return 0
        
    def addAccount(self, handle):
        if not(self.__login) and type(self.DB) == type:
            logging.warning("didn't log in with setAPIcredentials() or database not opened with openDB()")
            return -1
        uObject = self.API.getAccountbyHandle(handle)
        if (uObject != -1) and (type(uObject) is dict):
            self.AccountData.append(uObject.copy())
            return 0
        else:
            return -1

    def getAccount(self, handle):
        if not(self.__login) and type(self.DB) == type:
            logging.warning("didn't log in with setAPIcredentials() or database not opened with openDB()")
            return -1
        uObject = self.API.getAccountbyHandle(handle)
        if (uObject != -1) and (type(uObject) is dict):
            return uObject
        else:
            return -1

    def parseDatasetToDB(self, path):
        if not(self.__login) and type(self.DB) == type:
            logging.warning("didn't log in with setAPIcredentials() or database not opened with openDB()")
            return -1
        if path.lower().endswith(".tsv"):
            delimiter = '	'
        elif path.lower().endswith(".csv"):
            delimiter = ','
        else:
            logging.warning("please provide a .tsv or .csv file")
            return -1
        ulist = []
        try:
            with open(path) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=delimiter)
                for row in csv_reader:
                    ulist.append(row)
        except EnvironmentError as e:
            logging.error("Error while opening file")
            logging.error(e)
            return -1
        except Exception as e:
            logging.error(e)
            return -1
        bar = IncrementalBar("ParsingData", max = len(ulist))
        for i in ulist:
            uObject = self.API.getAccount(i[0])
            if (uObject != -1) and (type(uObject) is dict):
                # print("added " + str(i[1]))
                uObject["bot"] = i[1]
                self.saveAccountToDB(uObject)
                bar.next()
        bar.finish()
        return 0
    

    ###################################################################################
    # general persistence based methods
    ###################################################################################

    def saveAccountsToDB(self, overwrite=True):
        if type(self.DB) == type:
            logging.warning("didn't open database with openDB()")
            return -1
        for uObject in self.AccountData:
            self.DB.persist(uObject, overwrite)
        return 0

    def saveAccountToDB(self, uObject, overwrite=True):
        if type(self.DB) == type:
            logging.warning("didn't open database with openDB()")
            return -1
        try:
            if self.DB.persist(uObject, overwrite) != -1:
                return 0
            else:
                return -1
        except:
            logging.error("saving to database failed")
            return -1

    def getDB(self):
        if type(self.DB) == type:
            logging.warning("didn't open database with openDB()")
            return -1
        try:
            self.AccountData = self.DB.getAccounts()
            return 0
        except:
            logging.error("retrieving from database failed")
            return -1

    def get_unannotated_from_DB(self):
        if type(self.DB) == type:
            logging.warning("didn't open database with openDB()")
            return -1
        try:
            self.AccountData = self.DB.get_unannotated()
            return 0
        except:
            logging.error("retrieving unannotated from database failed")
            return -1

    def get_single_unannotated_from_DB(self):
        if type(self.DB) == type:
            logging.warning("didn't open database with openDB()")
            return -1
        try:
            return self.DB.get_single_unannotated()
        except:
            logging.error("retrieving single unannotated from database failed")
            return -1

    def get_bots_from_DB(self):
        if type(self.DB) == type:
            logging.warning("didn't open database with openDB()")
            return -1
        try:
            self.AccountData = self.DB.get_bots()
            return 0
        except:
            logging.error("retrieving bots from database failed")
            return -1

    def get_humans_from_DB(self):
        if type(self.DB) == type:
            logging.warning("didn't open database with openDB()")
            return -1
        try:
            self.AccountData = self.DB.get_humans()
            return 0
        except:
            logging.error("retrieving humans from database failed")
            return -1

    def annotate(self, id_str, bot):
        if type(self.DB) == type:
            logging.warning("didn't open database with openDB()")
            return -1
        try:
            self.DB.annotate(id_str, bot)
            return 0
        except:
            logging.error("changing annotation from database entry failed")
            return -1

    def get_annotated(self):
        if type(self.DB) == type:
            logging.warning("didn't open database with openDB()")
            return -1
        try:
            self.AccountData = self.DB.get_annotated()
            return 0
        except:
            logging.error("retrieve annotated from database failed")
            return -1

    def deleteAccount(self, id_str):
        if type(self.DB) == type:
            logging.warning("didn't open database with openDB()")
            return -1
        try:
            if self.DB.deleteAccount(id_str) != -1:
                return 0
            else:
                return -1
        except:
            logging.error("delete account from database failed")
            return -1

    def clearDataFrame(self):
        self.df = pd.DataFrame()
        return 0

    def clearAccountData(self):
        self.AccountData = []
        return 0
    
    def exportAnnotated(self, path_accounts="./dataset_accounts.csv"):
        self.clearAccountData()
        if self.get_annotated() == -1:
            return -1
        dataset_accounts = pd.DataFrame(columns=('id', 'bot'))
        for account in self.AccountData:
            dataset_accounts = dataset_accounts.append({"id": account["id_str"], "bot":account["bot"]}, ignore_index=True)

        try:
            dataset_accounts.to_csv(path_accounts, sep=',', encoding='utf-8', index=False)
        except EnvironmentError as e:
            logging.error("Error saving to file")
            logging.error(e)
            return -1
        except Exception as e:
            logging.error(e)
            return -1


    ###################################################################################
    # feature based methods
    ###################################################################################
    def reloadFeatures(self):
        try:
            importlib.reload(feature)
            self.FT = feature.Feature_Engine_cl()
            return 0
        except Exception as e:
            logging.error(e)
            return -1

    def getFeatureNames(self):
        fnames = []
        for name in self.FT.features.keys():
            fnames.append(name)
        return fnames

    def generateFeatures(self, fnames):
        if type(fnames) != list or len(fnames) == 0:
            logging.error("please provide a list with at least one feature")
            return -1
        bar = IncrementalBar("Generating Features", max = len(fnames))
        for name in fnames:
            rows = []
            for i in range(0, len(self.AccountData)):
                feature = self.FT.features[name](self.AccountData[i])
                rows.append(feature)
            self.df[name] = rows
            rows = []
            for i in range(0, len(self.AccountData)):
                bot = self.AccountData[i]["bot"]
                rows.append(bot)
            self.df["bot"] = rows
            bar.next()
        bar.finish()
        return  0

    def exportDFcsv(self, path="./out.csv"):
        try:
            self.df.to_csv(path, sep=',', encoding='utf-8', index=False)
            return 0
        except EnvironmentError as e:
            logging.error("Error saving to file")
            logging.error(e)
            return -1
        except Exception as e:
            logging.error(e)
            return -1