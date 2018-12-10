# followed this tutorial for working with csv files in pandas
# https://www.shanelynn.ie/python-pandas-read_csv-load-data-from-csv-files/

import pandas as pd
import nltk
import random
from nltk.corpus import stopwords
from markov import MarkovChain

def read_file():
    file_name = "tweets.csv"
    print("reading", file_name)
    # use pandas read_csv function to read in csv as an object
    data = pd.read_csv(file_name)
    # convert the "text" column in the csv to a list of strings
    tweets = data['text'].astype(str).values.tolist()
    
    return tweets

def get_counts(tweets):
    common_words = {}
    words_in_tweets = []
    lengths = []

    # using nltk's stop words list, remove stop words from tweets
    stop_words = set(stopwords.words('english'))

    # split tweets into words and then keep track of word frequencies in a dictionary
    for tweet in tweets:
        split_tweet = tweet.split()
        lengths.append(len(split_tweet))
        for word in split_tweet:
            words_in_tweets.append(word) # do we need the individual words?
            if word in common_words and not word in stop_words:
                common_words.update({word: common_words.get(word)+1})
            else:
                common_words.update({word: 1})

    return lengths, words_in_tweets, sorted(common_words.items(), key=lambda kv: kv[1], reverse=True)

# return dictionary {(sentence length: probability)} 
def length_probability(lengths):
    total_tweets = len(lengths)
    length_prob = {}
    for length in lengths:
        length_prob.update({length: (lengths.count(length) / total_tweets)})
    return length_prob

def get_top_users(word_freq):
    top_users = {}
    for (word, freq) in word_freq:
        length = len(word)
        if (word[0] == '@'):
            top_users.update({word: freq})
    
    return sorted(top_users.items(), key=lambda kv: kv[1], reverse=True)

def get_bigrams(tweets):
    print ("generating bigrams")
    bigrams = {}
    for tweet in tweets:
        # print(tweet)
        words_in_tweet = tweet.split()
        # print(words_in_tweet)
        for i in range(len(words_in_tweet)):
            frequency = 1
            # account for sentence boundaries, create bigram with word and blank
            if (i == len(words_in_tweet)-1):
                bigram = (words_in_tweet[i], "")
            else:
                bigram = (words_in_tweet[i], words_in_tweet[i+1])

            if bigram not in bigrams:
                bigrams[bigram] = frequency
            else:
                frequency = bigrams[bigram] + 1
                bigrams.update({bigram: frequency})

    return bigrams

# from Lab 2 
# Build the bigram model
# Model key is bigram and value is its probability
# Probability is bigram count / unigram count of first element
def bigram_model(unigrams, bigrams):
    print ("building hidden markov model")
    model = {}

    for (word1, word2) in bigrams:
        bigram = (word1, word2)
        for (unigram, frequency) in unigrams:
            if unigram == word1:
                    unigram_count = frequency
        probability = (bigrams.get(bigram)/unigram_count)
        model.update({(word1, word2): probability})
    return model

# Use your model to get a sentence probability
# Add together probability P (word | previous) for each word in sentence

def get_sentence_probability(model,unigrams,sentence):
    # print(model)
    prob = 1
    previous = None
    # wordList = sentence.split()
    for word in sentence:
        bigram = (previous, word)
        # print(bigram)
        if bigram in model:
            for (unigram, frequency) in unigrams:
                if unigram == previous:
                    unigram_count = frequency
            prob += (model[bigram]/unigram_count)
            # print(prob)
        previous = word
    return prob

def generate_sentences(length_prob, markov, bigram_model, unigrams, num):
    keys = list(length_prob.keys())
    probs = length_prob.values()

    # weighted random choice: https://stackoverflow.com/questions/10803135/weighted-choice-short-and-simple/15907274
    # using list of possible tweet lengths and the probability of each one,
    # generate lengths of num amount of tweets
    list_of_lengths = random.choices(keys, probs, k=num)

    output = []

    for length in list_of_lengths:
        probability = 0;
        tweet = ""
        while probability < 0.9:
            tweet = markov.generate(length)
            probability = get_sentence_probability(bigram_model, unigrams, tweet)
        output.append(tweet)
    
    return output
        

def main():

    # read file, return list of tweets
    list_of_tweets = read_file()

    # returns 2 lists
    # first is list of each word used in all of my tweets
    # second is list of unigrams and frequencies i.e. {(word, frequency)}
    lengths, list_of_words, word_freq = get_counts(list_of_tweets)
    # print(word_freq)
    
    # get top users I have replied to
    top_users = get_top_users(word_freq)

    # return bigrams where {(word1, word2): frequency}
    bigrams = get_bigrams(list_of_tweets)
    # print(bigrams)
    # print(bigrams.keys())

    # create model for calculating the probability of a given sentence
    model = bigram_model(word_freq, bigrams)
    # print(model)

    #create Markov chain
    m = MarkovChain()
    m.learn(bigrams.keys())
    # print(m.memory)
    
    # generate length probability dictionary {length of sentence: frequency of sentences of that length}
    length_prob = length_probability(lengths)
    
    # output generated sentences, must have probability > 0.5
    generated_tweets = generate_sentences(length_prob, m, model, word_freq, 50)

    for tweet in generated_tweets:
        print(tweet)
    
if __name__ == "__main__":
    main()

