# taken from https://sookocheff.com/post/nlp/ngram-modeling-with-markov-chains/
import random

class MarkovChain:

    def __init__(self):
        self.memory = {}

    def _learn_key(self, key, value):
        if key not in self.memory:
            self.memory[key] = []

        self.memory[key].append(value)

    def learn(self, bigrams):
        for bigram in bigrams:
            self._learn_key(bigram[0], bigram[1])

    def _next(self, current_state):
        next_possible = self.memory.get(current_state)

        if not next_possible:
            next_possible = self.memory.keys()

        return random.sample(next_possible, 1)[0]

    def generate(self, amount, state=''):
        if not amount:
            return state

        next_word = self._next(state)
        return state + ' ' + self.generate(amount - 1, next_word)