import pandas as pd
t = pd.read_csv('tweet/bitcoin_tweets.csv')
counts = t['id'].value_counts()
print(t)


t.drop_duplicates(subset='id', keep='first', inplace=True)


t.to_csv('tweets.csv')
print(t)