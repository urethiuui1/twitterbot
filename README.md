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

## Usage
For a quick overview please look at the examples folder and the command-line interface.
