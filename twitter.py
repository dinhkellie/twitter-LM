# followed this tutorial for working with csv files in pandas
# https://www.shanelynn.ie/python-pandas-read_csv-load-data-from-csv-files/

import pandas as pd
import nltk
from nltk.corpus import stopwords

def read_file():
    file_name = "tweets.csv"
    print("reading", file_name)
    # use pandas read_csv function to read in csv as an object
    data = pd.read_csv(file_name)
    # print(data.columns.tolist())
    # convert the "text" column in the csv to a list of strings
    tweets = data['text'].astype(str).values.tolist()
    
    return tweets

def get_counts(tweets):
    common_words = {}
    words_in_tweets = []

    # using nltk's stop words list, remove stop words from tweets
    stop_words = set(stopwords.words('english'))

    # split tweets into words and then keep track of word frequencies in a dictionary
    for tweet in tweets:
        for word in tweet.split():
            words_in_tweets.append(word) # do we need the individual words?
            if word in common_words and not word in stop_words:
                common_words.update({word: common_words.get(word)+1})
            else:
                common_words.update({word: 1})

    return words_in_tweets, sorted(common_words.items(), key=lambda kv: kv[1], reverse=True)

def get_top_users(word_freq):
    top_users = {}
    for (word, freq) in word_freq:
        length = len(word)
        if (word[0] == '@'):
            # if (word[length-1] == ':'):
            #     stripped_word = word.replace(":", "") #strip : from @user
            #     top_users.update({stripped_word: freq})
            top_users.update({word: freq})
    
    return sorted(top_users.items(), key=lambda kv: kv[1], reverse=True)

def bigram_model(words):
    # create bigrams
    bigrams = {}
    for i in range(len(words)-1):
        frequency = 1
        bigram = (words[i], words[i+1])

        if bigram not in bigrams:
            bigrams[bigram] = frequency
        else:
            frequency = bigrams[bigram] + 1
            bigrams.update({bigram: frequency})

    print(bigrams)

def main():
    list_of_tweets = read_file()
    words, word_freq = get_counts(list_of_tweets)
    top_users = get_top_users(word_freq)
    bigram_model(words)
    
    
    


if __name__ == "__main__":
    main()

