import logging
logging.basicConfig(filename='error.log', format='%(asctime)s:%(levelname)s:%(filename)s:%(funcName)s:%(message)s')
import sklearn
from . import collect
import joblib
from . import feature



class Classify_cl(object):
    def __init__(self, model, featurelist):
        self.CL = collect.Collect_cl()
        try:
            self.model = joblib.load(model)
        except EnvironmentError as e:
            logging.error("Error loading file")
            logging.error(e)
            self.model = None
        except Exception as e:
            logging.error(e)
            self.model = None
        self.FT = feature.Feature_Engine_cl()
        self.featurelist = featurelist
        self.__login = False
        if len(self.featurelist) < 1:
            logging.warning("empty feature list")

    def setAPIcredentials(self, consumer_key, consumer_secret, access_token, secret_token):
        try:
            self.CL.setAPIcredentials(consumer_key, consumer_secret, access_token, secret_token)
            self.__login = True
            return 0
        except Exception as e:
            logging.error(e)
            return -1

    def predict(self, handle):
        if not(self.__login) and self.model == None:
            logging.warning("Please log in first with setAPIcredentials() method.")
            return -1
        if type(self.featurelist) != list or len(self.featurelist) < 1:
            logging.warning("invalid or empty feature list.")
            return -1
        uObject = self.CL.getAccount(handle)
        if (uObject != -1) and (type(uObject) is dict):
            computedfeatures = []
            for f in self.featurelist:
                try:
                    computedfeatures.append(self.FT.features[f](uObject))
                except Exception as e:
                    logging.error("Feature generation error.")
                    logging.error(e)
                    return -1
            try:
                res = self.model.predict([computedfeatures])
                return res[0]
            except Exception as e:
                logging.error(e)
                return -1
        else:
            logging.error("Prediction failed. Please check if handle is correct or model is set.")
            return -1

    def predictByuObject(self, uObject):
        if self.model == None:
            logging.warning("Model not valid.")
            return -1
        if type(self.featurelist) != list or len(self.featurelist) < 1:
            logging.warning("invalid or empty feature list.")
            return -1
        if (uObject != -1) and (type(uObject) is dict):
            computedfeatures = []
            for f in self.featurelist:
                try:
                    computedfeatures.append(self.FT.features[f](uObject))
                except Exception as e:
                    logging.error("Feature generation error.")
                    logging.error(e)
                    return -1
            try:
                res = self.model.predict([computedfeatures])
                return res[0]
            except Exception as e:
                logging.error(e)
                return -1
        else:
            logging.error("Prediction failed. Please check if handle is correct or model is set.")
            return -1