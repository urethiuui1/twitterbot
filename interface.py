from twitterbot import *
from time import sleep
import platform, os
import configparser
CL = collect.Collect_cl()
ML = ml.ML_cl()
clear = "clear"
# WebBrowser https://stackoverflow.com/questions/64363402/how-to-make-an-web-browser-with-python-3-8
import sys
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QApplication
app = QApplication(sys.argv)
web = QWebEngineView()
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--enable-logging --log-level=3"
web.page().javaScriptConsoleMessage = lambda self, level, msg, line, sourceID: None
config = object
consumer_key = ""
consumer_secret = ""
access_token = ""
secret_token = ""


#######################################################################################
# 1. collect menu methods
#######################################################################################
def collect_from_stream():
    print("# Collect n accounts by keyword from global tweet stream #\n\n")
    keyword = input("Keyword: ")
    amount = 0
    try:
        amount = int(input("Amount: "))
    except ValueError:
        os.system(clear)
        input("Fehlerhafte Eingabe.\nEnter zum bestätigen...")
        return -1
    try:
        CL.parse_from_stream_by_keyword(keyword, amount)
    except:
        print("Fehler beim Parsen.")
        return -1
    try:
        CL.saveAccountsToDB()
        input((str(len(CL.AccountData))) + " Accounts gesparsed.\nEnter zum bestätigen...")
    except:
        print("Fehler beim abspeichern in Datenbank.")
    CL.clearAccountData()

def account_by_handle():
    print("Add single account by handle or id")
    handle = str(input("Handle: "))
    CL.clearAccountData()
    CL.addAccount(handle)
    try:
        CL.saveAccountsToDB()
        input((str(len(CL.AccountData))) + " Accounts gespeichert.\nEnter zum bestätigen...")
    except:
        print("Fehler beim abspeichern in Datenbank.")
    CL.clearAccountData()

def parse_dataset():
    print("# Parse accounts from csv/tsv (id:bot) #\n\n")
    path = input("File: ")
    res = CL.parseDatasetToDB(path)
    if res == 1:
        print("Fehler beim laden der Datei")
    input((str(res)) + " Accounts gespeichert.\nEnter zum bestätigen...")

def collectmenu():
    run = True
    command = ""
    while(run):
        print("# Collect Accounts #\n\n")
        print("1. Collect n accounts by keyword from global tweet stream")
        print("2. Add single account by handle or id")
        print("3. Parse accounts from csv/tsv (id:bot)")
        print("0. exit")
        command = input("Auswahl: ")
        if not(command.isdigit()):    
            os.system(clear)
            input("please enter a number\nEnter zum bestätigen...")
        else:
            command = int(command)

        if command == 0:
            run = False
            break
        elif command == 1:
            os.system(clear)
            collect_from_stream()
        elif command == 2:
            os.system(clear)
            account_by_handle()
        elif command == 3:
            os.system(clear)
            parse_dataset()
        os.system(clear)


#######################################################################################
# 2. annotate menu methods
#######################################################################################
def annotatemenu():
    run = True
    command = ""
    used_features = []
    try:
        f = open("./examples/model.features", "r")
        used_features = f.read().split(", ")
        f.close()
    except:
        print("Fehler beim laden der Features")
        return -1
    Test = test.Classify_cl("./examples/model.joblib", used_features)
    if Test.setAPIcredentials(consumer_key, consumer_secret, access_token, secret_token) == -1:
        input("Fehler beim Twitter-API login\nEnter zum bestätigen...")
        return -1
    while(run):
        uObject = CL.get_single_unannotated_from_DB()
        if uObject == -1:
            os.system(clear)
            print("# Annotate Accounts #\n\n")
            print("Keine unannotierten Accounts vorhanden.")
            print("3. refresh")
            print("0. exit")
        else:
            web.load(QUrl("https://twitter.com/" + uObject["screen_name"]))
            web.show()
            os.system(clear)
            print("# Annotate Accounts #\n\n")
            print("1. Human")
            print("2. Bot")
            print("91. Delete")
            print("0. exit\n\n")
            
            print("https://twitter.com/" + uObject["screen_name"])
            print("Name: " + uObject["name"])
            print("Screen_Name: " + uObject["screen_name"])
            print("Follower: " + str(uObject["followers_count"]))
            print("Friends: " + str(uObject["friends_count"]))
            print("Tweets: " + str(uObject["statuses_count"]))
            print("Verified: " + str(uObject["verified"]))
            print("\nPrediciton: " + str(Test.predict(uObject["screen_name"])))
        command = input("Auswahl: ")
        if not(command.isdigit()):    
            os.system(clear)
            input("please enter a number\nEnter zum bestätigen...")
        else:
            command = int(command)
        if command == 0:
            run = False
            # sys.exit(app.exec_())
            break
        elif command == 1 and uObject != 1 and type(uObject) == dict:
            CL.annotate(uObject["id_str"], "human")
        elif command == 2 and uObject != 1 and type(uObject) == dict:
            CL.annotate(uObject["id_str"], "bot")
        elif command == 91 and uObject != 1 and type(uObject) == dict:
            CL.deleteAccount(uObject["id_str"])
        elif command == 3:
            os.system(clear)
            pass
        os.system(clear)


#######################################################################################
# 3. machine learning menu methods
#######################################################################################

def reloadfeatures():
    CL.reloadFeatures()
    os.system(clear)

def genfeatures():
    CL.clearDataFrame()
    run = True
    command = ""
    fnames = CL.getFeatureNames()
    while(run):
        print("# generate Features #\n\n")
        print("verfügbare Features: ")
        print(*fnames, sep='\n')
        print("\nEingabebeispiel: feature1, feature2, feature3")
        used_fnames = input("Auswahl features: ")
        if used_fnames.isdigit() and int(used_fnames) == 0:
            os.system(clear)
            run = False
            break
        else:
            try:
                lst = used_fnames.split(", ")
                CL.generateFeatures(lst)
                os.system(clear)
                input("\n" + str(len(CL.df)) + " features generiert.\nEnter zum bestätigen...")
                os.system(clear)
                outfile = input("Exportieren nach (z.B. ./features.csv): ")
                try:
                    CL.exportDFcsv(outfile)
                except:
                    os.system(clear)
                    input("\nFehler beim speichern.\nEnter zum bestätigen...")
            except:
                os.system(clear)
                input("\nFehler beim Generieren der Features.\nEnter zum bestätigen...")
        os.system(clear)

def benchmarkmenu():
    run = True
    command = ""
    print("# benchmark #\n\n")
    input_csv = input("Feature-Datei: ")
    try:
        ML.load_csv(input_csv)
        os.system(clear)
        print("benchmarking...")
        data = ML.benchmark()
        os.system(clear)
        print("# Benchmark results #\n\n")
        print("Decision Tree:")
        print("Accuracy: " + str(data["DecisionTree"]["accuracy"]) + " | AUC: " +  str(data["DecisionTree"]["AUC"]))
        print("Random Forest:")
        print("Accuracy: " + str(data["RandomForest"]["accuracy"]) + " | AUC: " +  str(data["RandomForest"]["AUC"]))
        print("AdaBoost:")
        print("Accuracy: " + str(data["AdaBoost"]["accuracy"]) + " | AUC: " +  str(data["AdaBoost"]["AUC"]))
        print("Logistic Regression:")
        print("Accuracy: " + str(data["LogisticRegression"]["accuracy"]) + " | AUC: " +  str(data["LogisticRegression"]["AUC"]))
        print("\n\nBest by Accuracy:")
        if data["DecisionTree"]["accuracy"] > max(data["RandomForest"]["accuracy"], data["AdaBoost"]["accuracy"], data["LogisticRegression"]["accuracy"]):
            print("DecisionTree: " + str(data["DecisionTree"]["accuracy"]))
        elif data["RandomForest"]["accuracy"] > max(data["DecisionTree"]["accuracy"], data["AdaBoost"]["accuracy"], data["LogisticRegression"]["accuracy"]):
            print("RandomForest: " + str(data["RandomForest"]["accuracy"]))
        elif data["AdaBoost"]["accuracy"] > max(data["DecisionTree"]["accuracy"], data["RandomForest"]["accuracy"], data["LogisticRegression"]["accuracy"]):
            print("AdaBoost: " + str(data["AdaBoost"]["accuracy"]))
        elif data["LogisticRegression"]["accuracy"] > max(data["DecisionTree"]["accuracy"], data["RandomForest"]["accuracy"], data["AdaBoost"]["accuracy"]):
            print("LogisticRegression: " + str(data["LogisticRegression"]["accuracy"]))
        else:
            print("Fehler")
        print("\n\nBest by AUC:")
        if data["DecisionTree"]["AUC"] > max(data["RandomForest"]["AUC"], data["AdaBoost"]["AUC"], data["LogisticRegression"]["AUC"]):
            print("DecisionTree: " + str(data["DecisionTree"]["AUC"]))
        elif data["RandomForest"]["AUC"] > max(data["DecisionTree"]["AUC"], data["AdaBoost"]["AUC"], data["LogisticRegression"]["AUC"]):
            print("RandomForest: " + str(data["RandomForest"]["AUC"]))
        elif data["AdaBoost"]["AUC"] > max(data["DecisionTree"]["AUC"], data["RandomForest"]["AUC"], data["LogisticRegression"]["AUC"]):
            print("AdaBoost: " + str(data["AdaBoost"]["AUC"]))
        elif data["LogisticRegression"]["AUC"] > max(data["DecisionTree"]["AUC"], data["RandomForest"]["AUC"], data["AdaBoost"]["AUC"]):
            print("LogisticRegression: " + str(data["LogisticRegression"]["AUC"]))
        else:
            print("Fehler")
        input("\nEnter zum bestätigen...")
        os.system(clear)
    except:
        os.system(clear)
        input("\nFehler beim öffnen der Datei.\nEnter zum bestätigen...")

def trainrandomforest():
    input_csv = input("Feature-Datei: ")
    try:
        ML.load_csv(input_csv)
    except:
        os.system(clear)
        input("\nFehler beim öffnen der Datei.\nEnter zum bestätigen...")
    ML.trainRandomForest()
    out_file = input("Exportieren nach (z.B. ./model.joblib): ")
    try:
        f = open(str(out_file.rstrip(".joblib")) + ".features", "w")
        out = ""
        for i in list(ML.X.columns.values):
            out = out + i + ", "
        out = out.rstrip(", ")
        f.write(out)
        f.close()
    except:
        os.system(clear)
        print("Fehler beim speichern der Features")
    ML.exportModel(out_file)
    os.system(clear)

def traindecisiontree():
    input_csv = input("Feature-Datei: ")
    try:
        ML.load_csv(input_csv)
    except:
        os.system(clear)
        input("\nFehler beim öffnen der Datei.\nEnter zum bestätigen...")
    ML.trainDecisionTree()
    out_file = input("Exportieren nach (z.B. ./model.joblib): ")
    try:
        f = open(str(out_file.rstrip("joblib")) + "features", "w")
        out = ""
        for i in list(ML.X.columns.values):
            out = out + i + ", "
        out = out.rstrip(", ")
        f.write(out)
        f.close()
    except:
        os.system(clear)
        print("Fehler beim speichern der Features")
    ML.exportModel(out_file)
    os.system(clear)

def trainadaboost():
    input_csv = input("Feature-Datei: ")
    try:
        ML.load_csv(input_csv)
    except:
        os.system(clear)
        input("\nFehler beim öffnen der Datei.\nEnter zum bestätigen...")
    ML.trainAdaBoost()
    out_file = input("Exportieren nach (z.B. ./model.joblib): ")
    try:
        f = open(str(out_file.rstrip(".joblib")) + ".features", "w")
        out = ""
        for i in list(ML.X.columns.values):
            out = out + i + ", "
        out = out.rstrip(", ")
        f.write(out)
        f.close()
    except:
        os.system(clear)
        print("Fehler beim speichern der Features")
    ML.exportModel(out_file)
    os.system(clear)

def trainlogisticregression():
    input_csv = input("Feature-Datei: ")
    try:
        ML.load_csv(input_csv)
    except:
        os.system(clear)
        input("\nFehler beim öffnen der Datei.\nEnter zum bestätigen...")
    ML.trainLogisticRegression()
    out_file = input("Exportieren nach (z.B. ./model.joblib): ")
    try:
        f = open(str(out_file.rstrip(".joblib")) + ".features", "w")
        out = ""
        for i in list(ML.X.columns.values):
            out = out + i + ", "
        out = out.rstrip(", ")
        f.write(out)
        f.close()
    except:
        os.system(clear)
        print("Fehler beim speichern der Features")
    ML.exportModel(out_file)
    os.system(clear)

def trainmenu():
    print("# train #\n\n")
    print("1. Random Forest")
    print("2. Decision Tree")
    print("3. AdaBoost")
    print("4. Logistic Regression")
    command = input("Auswahl: ")
    if not(command.isdigit()):    
        os.system(clear)
        input("please enter a number\nEnter zum bestätigen...")
    else:
        command = int(command)
    if command == 1:
        trainrandomforest()
    elif command == 2:
        traindecisiontree()
    elif command == 3:
        trainadaboost()
    elif command == 4:
        trainlogisticregression()
    
def mlmenu():
    run = True
    command = ""
    print("Lade accounts...")
    CL.get_annotated()
    os.system(clear)
    while(run):
        os.system(clear)
        print("# Machine Learning #\n\n")
        print(str(len(CL.AccountData)) + " verfügbare Accounts\n\n")
        print("1. generate Features")
        print("2. benchmark")
        print("3. train")
        print("4. reload Features")
        print("0. exit")
        command = input("\n\nAuswahl: ")
        if not(command.isdigit()):    
            os.system(clear)
            input("please enter a number\nEnter zum bestätigen...")
        else:
            command = int(command)
        if command == 0:
            run = False
            break
        elif command == 1:
            os.system(clear)
            genfeatures()
        elif command == 2:
            os.system(clear)
            benchmarkmenu()
        elif command == 3:
            os.system(clear)
            trainmenu()
        elif command == 4:
            os.system(clear)
            reloadfeatures()

def checkmenu():
    os.system(clear)
    run = True
    print("# Check Account with trained model #\n\n")
    used_features = []
    trained_model = input("Model: ")
    try:
        f = open(str(trained_model).rstrip("joblib") + "features", "r")
        used_features = f.read().split(", ")
        f.close()
    except:
        os.system(clear)
        input("Fehler beim laden der Features\nEnter zum bestätigen...")
    TST = test.Classify_cl(trained_model, used_features)
    if TST.setAPIcredentials(consumer_key, consumer_secret, access_token, secret_token) == -1:
        input("Fehler beim Twitter-API login\nEnter zum bestätigen...")
        return -1
    if TST.model == None:
        print("no model loaded")
        return -1
    print(type(TST.model))
    while(run):
        inp = input("User: ")
        if inp.isdigit() and int(inp) == 0:
            run = False
            break
        else:
            try:
                res = TST.predict(inp)
            except:
                print("Fehler bei Vorhersage.")
            if res == "human":
                print(str(inp) + ": MENSCH")
            elif res == "bot":
                print(str(inp) + ": BOT")

def exportDataset():
    file_name = input("Speichern nach (z.B. ./dataset.csv): ")
    try:
        CL.exportAnnotated(file_name)
    except:
        os.system(clear)
        input("Fehler beim speichern\nEnter zum bestätigen...")
        
def main():
    global consumer_key, consumer_secret, access_token, secret_token
    run = True
    command = ""
    OS = platform.system()
    if OS == "Windows":
        clear = "cls"
    else:
        clear = "clear"
    os.system(clear)

    #INIT
    config = configparser.ConfigParser()
    try:
        config.read('config.ini')
        if CL.setAPIcredentials(config["TwitterAPI"]["consumer_key"], config["TwitterAPI"]["consumer_secret"], config["TwitterAPI"]["access_token"], config["TwitterAPI"]["secret_token"]) == -1:
            input("Fehler beim Twitter-API login\nEnter zum bestätigen...")
            return -1
        CL.openDB(config["Database"]["location"])
        consumer_key = config["TwitterAPI"]["consumer_key"]
        consumer_secret = config["TwitterAPI"]["consumer_secret"]
        access_token = config["TwitterAPI"]["access_token"]
        secret_token = config["TwitterAPI"]["secret_token"]
    except:
        db = input("Database location: ")
        CL.openDB(db)
        consumer_key = input("consumer_key: ")
        consumer_secret = input("consumer_secret: ")
        access_token = input("access_token: ")
        secret_token = input("secret_token: ")
        if CL.setAPIcredentials(consumer_key, consumer_secret, access_token, secret_token) == -1:
            input("Fehler beim Twitter-API login\nEnter zum bestätigen...")
            return -1
        sc = input("Daten in Configdatei speichern? ja/nein: ")
        if sc.lower() == "ja":
            config.add_section("TwitterAPI")
            config.add_section("Database")
            config["TwitterAPI"] = {'consumer_key': consumer_key,
            'consumer_secret': consumer_secret,
            'access_token': access_token,
            'secret_token': secret_token}
            config["Database"]["location"] = db
            try:
                with open('config.ini', 'w') as configfile:
                    config.write(configfile)
            except:
                input("Fehler beim schreiben der Configdatei\nEnter zum bestätigen...")

    os.system(clear)
    while(run):
        print("# Twitter Bot Framework #\n\n")
        print("1. Collect Accounts")
        print("2. Annotate Accounts")
        print("3. Machine Learning")
        print("4. Check Account with trained model")
        print("5. Export Dataset (id:bot)")
        print("0. exit")

        command = input("Auswahl: ")
        if not(command.isdigit()):    
            os.system(clear)
            input("please enter a number\nEnter zum bestätigen...")
        else:
            command = int(command)
        if command == 0:
            run = False
            break
        elif command == 1:
            os.system(clear)
            collectmenu()
        elif command == 2:
            os.system(clear)
            annotatemenu()
        elif command == 3:
            os.system(clear)
            mlmenu()
        elif command == 4:
            os.system(clear)
            checkmenu()
        elif command == 5:
            os.system(clear)
            exportDataset()
        os.system(clear)

if __name__ == "__main__":
    main()
