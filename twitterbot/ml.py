import logging
logging.basicConfig(filename='error.log', format='%(asctime)s:%(levelname)s:%(filename)s:%(funcName)s:%(message)s')
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RepeatedKFold, cross_val_score
from sklearn import svm
from sklearn.metrics import roc_auc_score, accuracy_score
from progress.bar import IncrementalBar
import joblib
from numpy import mean



class ML_cl(object):
    def __init__(self):
        self.account_data = pd.DataFrame()
        self.X = pd.DataFrame()
        self.y = pd.DataFrame()
        self.model = object
        # settings
        self.kfold_splits = 5
        self.kfold_repeats = 10

    def load_csv(self, path):
        try:
            self.account_data = pd.read_csv(path)
            self.X = self.account_data.drop(columns=['bot'])
            self.y = self.account_data['bot']
            return 0
        except EnvironmentError as e:
            logging.error("Error loading file")
            logging.error(e)
            return -1
        except Exception as e:
            logging.error(e)
            return -1

    def set_data(self, df):
        if(type(df) is pd.DataFrame):
            self.account_data = df
            self.X = self.account_data.drop(columns=['bot'])
            self.y = self.account_data['bot']
            return 0
        else:
            logging.warning("please provide a pandas DataFrame")
            return -1

    def tryDecisionTree(self, criterion="gini", splitter="best", max_depth=None, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features=None, random_state=None, max_leaf_nodes=None, min_impurity_decrease=0.0, class_weight=None, ccp_alpha=0.0):
        try:
            self.model = DecisionTreeClassifier(criterion=criterion, splitter=splitter, max_depth=max_depth, min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf, min_weight_fraction_leaf=min_weight_fraction_leaf, max_features=max_features, random_state=random_state, max_leaf_nodes=max_leaf_nodes, min_impurity_decrease=min_impurity_decrease, class_weight=class_weight, ccp_alpha=ccp_alpha)
            cv = RepeatedKFold(n_splits=self.kfold_splits, n_repeats=self.kfold_repeats, random_state=1)
            ACCscores = cross_val_score(self.model, self.X, self.y, scoring='accuracy', cv=cv, n_jobs=-1)
            AUCscores = cross_val_score(self.model, self.X, self.y, scoring='roc_auc', cv=cv, n_jobs=-1)
            return {"accuracy": mean(ACCscores), "AUC": mean(AUCscores)}
        except Exception as e:
            logging.error(e)
            return -1

    def tryRandomForest(self, n_estimators=100, criterion="gini", max_depth=None, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features="auto", max_leaf_nodes=None, min_impurity_decrease=0.0, bootstrap=True, oob_score=False, n_jobs=None, random_state=None, warm_start=False, class_weight=None, ccp_alpha=0.0, max_samples=None):
        try:
            self.model = RandomForestClassifier(n_estimators=n_estimators, criterion=criterion, max_depth=max_depth, min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf, min_weight_fraction_leaf=min_weight_fraction_leaf, max_features=max_features, max_leaf_nodes=max_leaf_nodes, min_impurity_decrease=min_impurity_decrease, bootstrap=bootstrap, oob_score=oob_score, n_jobs=n_jobs, random_state=random_state, warm_start=warm_start, class_weight=class_weight, ccp_alpha=ccp_alpha, max_samples=max_samples)     
            cv = RepeatedKFold(n_splits=self.kfold_splits, n_repeats=self.kfold_repeats, random_state=1)
            ACCscores = cross_val_score(self.model, self.X, self.y, scoring='accuracy', cv=cv, n_jobs=-1)
            AUCscores = cross_val_score(self.model, self.X, self.y, scoring='roc_auc', cv=cv, n_jobs=-1)
            return {"accuracy": mean(ACCscores), "AUC": mean(AUCscores)}
        except Exception as e:
            logging.error(e)
            return -1

    def tryAdaBoost(self, base_estimator=None, n_estimators=50, learning_rate=1.0, algorithm="SAMME.R",random_state=None):
        try:
            self.model = AdaBoostClassifier(base_estimator=base_estimator, n_estimators=n_estimators, learning_rate=learning_rate, algorithm=algorithm, random_state=random_state)
            cv = RepeatedKFold(n_splits=self.kfold_splits, n_repeats=self.kfold_repeats, random_state=1)
            ACCscores = cross_val_score(self.model, self.X, self.y, scoring='accuracy', cv=cv, n_jobs=-1)
            AUCscores = cross_val_score(self.model, self.X, self.y, scoring='roc_auc', cv=cv, n_jobs=-1)
            return {"accuracy": mean(ACCscores), "AUC": mean(AUCscores)}
        except Exception as e:
            logging.error(e)
            return -1
            
    def tryLogisticRegression(self, penalty="l2", dual=False, tol=1e-4, C=1.0, fit_intercept=True, intercept_scaling=1, class_weight=None, random_state=None, solver="lbfgs", max_iter=10000, multi_class="auto", warm_start=False, n_jobs=None, l1_ratio=None):
        try:
            self.model = LogisticRegression(penalty=penalty, dual=dual, tol=tol, C=C, fit_intercept=fit_intercept, intercept_scaling=intercept_scaling, class_weight=class_weight, random_state=random_state, solver=solver, max_iter=max_iter, multi_class=multi_class, warm_start=warm_start, n_jobs=n_jobs, l1_ratio=l1_ratio)
            cv = RepeatedKFold(n_splits=self.kfold_splits, n_repeats=self.kfold_repeats, random_state=1)
            ACCscores = cross_val_score(self.model, self.X, self.y, scoring='accuracy', cv=cv, n_jobs=-1)
            AUCscores = cross_val_score(self.model, self.X, self.y, scoring='roc_auc', cv=cv, n_jobs=-1)
            return {"accuracy": mean(ACCscores), "AUC": mean(AUCscores)}
        except Exception as e:
            logging.error(e)
            return -1

    def benchmark(self):
        bar = IncrementalBar("Progress", max = 4)
        DT = self.tryDecisionTree()
        bar.next()
        RF = self.tryRandomForest()
        bar.next()
        AB = self.tryAdaBoost()
        bar.next()
        LR = self.tryLogisticRegression()
        bar.next()
        bar.finish()
        return {"DecisionTree": DT, "RandomForest": RF, "AdaBoost": AB, "LogisticRegression": LR}

    def getbestalgorithmbyacc(self):
        bar = IncrementalBar("Progress", max = 4)
        DT = self.tryDecisionTree()
        bar.next()
        RF = self.tryRandomForest()
        bar.next()
        AB = self.tryAdaBoost()
        bar.next()
        LR = self.tryLogisticRegression()
        bar.next()
        bar.finish()
        if DT["accuracy"] > max(RF["accuracy"], AB["accuracy"], LR["accuracy"]):
            DT["algo"] = "DecisionTree"
            return DT
        elif RF["accuracy"] > max(DT["accuracy"], AB["accuracy"], LR["accuracy"]):
            RF["algo"] = "RandomForest"
            return RF
        elif AB["accuracy"] > max(DT["accuracy"], RF["accuracy"], LR["accuracy"]):
            AB["algo"] = "AdaBoost"
            return AB
        elif LR["accuracy"] > max(DT["accuracy"], RF["accuracy"], AB["accuracy"]):
            LR["algo"] = "LogisticRegression"
            return LR
        else:
            return -1

    def getbestalgorithmbyauc(self):
        bar = IncrementalBar("Progress", max = 4)
        DT = self.tryDecisionTree()
        bar.next()
        RF = self.tryRandomForest()
        bar.next()
        AB = self.tryAdaBoost()
        bar.next()
        LR = self.tryLogisticRegression()
        bar.next()
        bar.finish()
        if DT["AUC"] > max(RF["AUC"], AB["AUC"], LR["AUC"]):
            DT["algo"] = "DecisionTree"
            return DT
        elif RF["AUC"] > max(DT["AUC"], AB["AUC"], LR["AUC"]):
            RF["algo"] = "RandomForest"
            return RF
        elif AB["AUC"] > max(DT["AUC"], RF["AUC"], LR["AUC"]):
            AB["algo"] = "AdaBoost"
            return AB
        elif LR["AUC"] > max(DT["AUC"], RF["AUC"], AB["AUC"]):
            LR["algo"] = "LogisticRegression"
            return LR
        else:
            return -1

    def trainRandomForest(self, n_estimators=100, criterion="gini", max_depth=None, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features="auto", max_leaf_nodes=None, min_impurity_decrease=0.0, bootstrap=True, oob_score=False, n_jobs=None, random_state=None, warm_start=False, class_weight=None, ccp_alpha=0.0, max_samples=None):
        try:
            self.model = RandomForestClassifier(n_estimators=n_estimators, criterion=criterion, max_depth=max_depth, min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf, min_weight_fraction_leaf=min_weight_fraction_leaf, max_features=max_features, max_leaf_nodes=max_leaf_nodes, min_impurity_decrease=min_impurity_decrease, bootstrap=bootstrap, oob_score=oob_score, n_jobs=n_jobs, random_state=random_state, warm_start=warm_start, class_weight=class_weight, ccp_alpha=ccp_alpha, max_samples=max_samples)
            self.model.fit(self.X, self.y)
            return 0
        except Exception as e:
            logging.error(e)
            return -1

    def trainDecisionTree(self, criterion="gini", splitter="best", max_depth=None, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features=None, random_state=None, max_leaf_nodes=None, min_impurity_decrease=0.0, class_weight=None, ccp_alpha=0.0):
        try:
            self.model = DecisionTreeClassifier(criterion=criterion, splitter=splitter, max_depth=max_depth, min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf, min_weight_fraction_leaf=min_weight_fraction_leaf, max_features=max_features, random_state=random_state, max_leaf_nodes=max_leaf_nodes, min_impurity_decrease=min_impurity_decrease, class_weight=class_weight, ccp_alpha=ccp_alpha)
            self.model.fit(self.X, self.y)
            return 0
        except Exception as e:
            logging.error(e)
            return -1

    def trainAdaBoost(self, base_estimator=None, n_estimators=50, learning_rate=1.0, algorithm="SAMME.R",random_state=None):
        try:
            self.model = AdaBoostClassifier(base_estimator=base_estimator, n_estimators=n_estimators, learning_rate=learning_rate, algorithm=algorithm, random_state=random_state)
            self.model.fit(self.X, self.y)
            return 0
        except Exception as e:
            logging.error(e)
            return -1

    def trainLogisticRegression(self, penalty="l2", dual=False, tol=1e-4, C=1.0, fit_intercept=True, intercept_scaling=1, class_weight=None, random_state=None, solver="lbfgs", max_iter=10000, multi_class="auto", warm_start=False, n_jobs=None, l1_ratio=None):
        try:
            self.model = LogisticRegression(penalty=penalty, dual=dual, tol=tol, C=C, fit_intercept=fit_intercept, intercept_scaling=intercept_scaling, class_weight=class_weight, random_state=random_state, solver=solver, max_iter=max_iter, multi_class=multi_class, warm_start=warm_start, n_jobs=n_jobs, l1_ratio=l1_ratio)
            self.model.fit(self.X, self.y)
            return 0
        except Exception as e:
            logging.error(e)
            return -1

    def exportModel(self, path):
        try:
            joblib.dump(self.model, path)
            return 0
        except Exception as e:
            logging.error(e)
            return -1

    def crossvalidateModel(self, path):
        if type(self.model) == type or len(path) < 1:
            return -1
        try:
            account_data2 = pd.read_csv(path)
        except EnvironmentError as e:
            logging.error("Error loading file")
            logging.error(e)
            return -1
        except Exception as e:
            logging.error(e)
            return -1
        try:
            X1 = account_data2.drop(columns=['bot'])
            y2 = account_data2['bot']
        except Exception as e:
            logging.error(e)
            return -1
        try:
            clf = self.model
            AUCscore = float("nan")
            ACCscore = float("nan")
            try:
                AUCscore = roc_auc_score(y2, clf.predict_proba(X1)[:, 1])
            except Exception as e:
                logging.error(e)
            try:
                ACCscore = accuracy_score(y2, clf.predict(X1))
            except Exception as e:
                logging.error(e)
        except Exception as e:
            logging.error(e)
            return -1
        return {"accuracy": ACCscore, "AUC": AUCscore}
        
    def loadModel(self, path):
        try:
            self.model = joblib.load(path)
            return 0
        except EnvironmentError as e:
            logging.error("Error loading file")
            logging.error(e)
            return -1
        except Exception as e:
            logging.error(e)
            return -1