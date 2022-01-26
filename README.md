# twitterbot
Prototypical implementation of a Framework for detecting Bots on Twitter using Supervised Machine-Learning which I designed for my Bachelor Thesis.

## Functionalities
- Collecting Twitter accounts
    - By global tweet stream (keywords, hashtags)
    - By lists of account-IDs
    - single accounts
- Classification of Twitter accounts as bot or human
- Feature engineering
- Training a Machine-Learning model
- Testing the performance of feature matrices
    - with different Machine-Learning algorithms
    - k-fold-cross validation
    - performance with different datasets
    - Accuracy and AUC as performance indicators
- Classifying accounts with trained Model
    - single accounts
    - whole datasets

## Requirements
- Python 3.8.8
- Installation of dependencies over pip:
    ```
    pip3 install -r ./requirements.txt
- Twitter-API access

## Main dependencies
- scikit-learn for Machine-Learning tasks
- joblib for serializing trained  models
- sqlite3 for persisting data
- tweepy 3.10.0 for Twitter-API access
- PyQtWebEngine for displaying Twitter profiles for easier classification of accounts

## Performance measurements with default developer API-access
- retrieving account- and tweet-data of 1500 accounts in 12-14 minutes (API restriction resets after 15 minutes -> no multithreading implemented)
- loading 34766 Twitter accounts with their Tweet-data into the AccountData runtime-variable takes about 10 seconds

## Usage
For a quick but detailed overview please look into the examples folder and the command-line interface.

## Quick overview over the most important methods
### General information
The data of Twitter accounts gets translated into a python-dictionary, called uObject, which also contains a list of the 20 most recent Tweets.
Within the Collect_cl() component data gets cached in a list of uObject dictionaries called AccountData.


### Collect_cl()
 Method | Description |
| --- | --- |
| **setAPIcredentials**(consumer_key, consumer_secret, access_token, secret_token) | set Twitter-API credentials |
| **openDB**(path) | Open sqlite3 database |
| **parseDataset**(path) | Parsing Twitter Accounts from a .csv or .tsv file (AccountID:Classification) and saving the accounts with their tweets into the AccountData variable |
| **parseDatasetToDB**(path) | Same as previous method, but directly saving the data to the SQLite database |
| **parse_from_stream_by_keyword**(keyword, amount) | retrieving n Twitter accounts with their tweet data by parsing the global filtered Tweet-stream and saving the data to the AccountData variable|
| **addAccount**(handle) | Adding a Twitter account with its Tweet-data to the AccountData variable using its handle |
| **getAccount**(handle) | Getting a Twitter account with its Tweet-data using its handle. The return value is an uObject. |
| **saveAccountsToDB**(overwrite=True) | Saving the data from the AccountData variable to the SQLite database |
| **saveAccountToDB**(uObject, overwrite=True) | Save a specific uObject to the SQLite database |
| **getDB**() | Loading all Twitter accounts with their Tweet-data from the SQLite database into the AccountData variable |
| **get_unannotated_from_DB**() | Loading all unclassified accounts into the AccountData variable |
| **get_single_unannotated_from_DB**() | Loading the next unclassified account into the AccountData variable |
| **get_bots_from_DB**() | Load all accounts classified as Bot into the AccountData variable |
| **get_humans_from_DB**() | Load all accounts classified as Human into the AccountData variable |
| **get_annotated**() | Get all accounts which got classified |
| **annotate**(id_str, bot) | Classifying an account as human or bot |
| **deleteAccount**(id_str) | Delete an account with its Tweet-data from the SQLite database |
| **clearDataFrame**() | Clear the feature matrix |
| **clearAccountData**() | Clear the AccountData variable |
| **exportAnnotated**(path_accounts) | Export all classified accounts to a .csv file (AccountID:Classification) |
| **reloadFeautes**() | Reloading the feature class after adding or modifying a feature |
| **generateFeatures**() | Generate a feature matrix using all accounts from the AccountData variable and a list of feature names |
| **exportDFcsv**(path) | Export the feature matrix to a .csv file |


### ML_cl()
 Method | Description |
| --- | --- |
| **load_csv**() | Loading feature matrix from .csv |
| **set_data**(df) | Loading feature matrix from Pandas dataframe |
| **tryDecisionTree**('params') |  Getting accuracy and AUC |
| **tryRandomForest**('params') | Getting accuracy and AUC |
| **tryAdaBoost**('params') | Getting accuracy and AUC |
| **tryLogisticRegression**('params') | Getting accuracy and AUC |
| **benchmark**() | Getting accuracy and AUC for all algorithms and using the default parameters |
| **getbestalgorithmbyacc**() | Get algorithm with highest accuracy value and using the default parameters |
| **getbestalgorithmbyauc**() | Get algorithm with highest AUC value and using the default parameters |
| **trainRandomForest**('params') | Train a model using RandomForest |
| **trainDecisionTree**('params') | Train a model using DecisionTree |
| **trainAdaBoost**('params') | Train a model using AdaBoost |
| **trainLogisticRegression**('params') | Train a model using LogisticRegression |
| **exportModel**(path) | Export trained model to file |
| **crossvalidateModel**(path) | Validate (accuracy and AUC) your trained model with a different dataset by providing another feature matrix |
| **loadModel**(path) | Load a previously trained model | 


### Classify_cl()
 Method | Description |
| --- | --- |
| **\_\_init\_\_**(model, featurelist) | The constructor needs the trained model and a list of used features |
| **setAPIcredentials**(consumer_key, consumer_secret, access_token, secret_token) | set Twitter-API credentials |
| **predict**(handle) | Classify a single Twitter account as human or bot using the trained model |
| **predictByuObject**(uObject) | Classify an account by already retrieved account data |
