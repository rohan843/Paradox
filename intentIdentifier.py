import time
import os
import numpy as np
import tensorflow as tf


class IntentIdentifier:
    def __init__(self, intents: list, thresh: float = 0.5):
        self.__intents = intents
        self.__thresh = thresh

        path_to_glove_file = os.path.join(
            'glove.6B.100d.txt'
        )
        embeddings_index = {}
        with open(path_to_glove_file) as f:
            for line in f:
                word, coefs = line.split(maxsplit=1)
                coefs = np.fromstring(coefs, "f", sep=" ")
                embeddings_index[word] = coefs
        print("Found %s word vectors." % len(embeddings_index))
        self.vectorizer = tf.keras.layers.TextVectorization(
            output_sequence_length=20)
        self.vectorizer.set_vocabulary(list(embeddings_index.keys()))
        print(
            f'Stored {len(self.vectorizer.get_vocabulary())} words in vocabulary.')
        voc = self.vectorizer.get_vocabulary()
        word_index = dict(zip(voc, range(len(voc))))
        num_tokens = len(voc) + 2
        embedding_dim = 100  # We are using 100 dim embeddings
        hits = 0
        misses = 0

        # Prepare embedding matrix
        embedding_matrix = np.zeros((num_tokens, embedding_dim))
        for word, i in word_index.items():
            embedding_vector = embeddings_index.get(word)
            if embedding_vector is not None:
                # Words not found in embedding index will be all-zeros.
                # This includes the representation for "padding" and "OOV"
                embedding_matrix[i] = embedding_vector
                hits += 1
            else:
                misses += 1
        print("Converted %d words (%d misses)" % (hits, misses))
        self.embedding_layer = tf.keras.layers.Embedding(
            num_tokens,
            embedding_dim,
            embeddings_initializer=tf.keras.initializers.Constant(
                embedding_matrix
            ),
            trainable=False,
            input_length=20
        )

        self.model_path = 'sentence_matching_model'
        self.model = tf.keras.models.load_model(self.model_path)

    def getSimilarityProbability(self, s1: str, s2: str):
        s1 = s1.lower()
        s2 = s2.lower()
        v1 = self.vectorizer(s1)
        v2 = self.vectorizer(s2)
        e1 = self.embedding_layer(v1)
        e2 = self.embedding_layer(v2)
        return self.model.predict({"sentence1": np.array(e1).reshape((1, 20, 100)), "sentence2": np.array(e2).reshape((1, 20, 100))}, verbose=0)[0][0]

    def getMatchingIntentIndex(self, userRequest: str):
        mxProb = 0
        mxI = -1
        for i in range(len(self.__intents)):
            matchingProb = self.__getMatchingProb(
                userRequest, self.__intents[i])
            if matchingProb > mxProb:
                mxI = i
                mxProb = matchingProb
        return mxI if mxProb >= self.__thresh else -1

    def __getMatchingProb(self, s1: str, s2: str):
        return self.getSimilarityProbability(s1, s2)
        # return 0 if s1 != s2 else 1


def turnLights(params: list):
    on = params[0]
    if on:
        print('Turning lights ON')
    else:
        print('Turning lights OFF')


def getTime(params: list):
    print('The time is', time.ctime())


def runAction(s: str, actions: list, defaultAction):
    i = intentIdentifier.getMatchingIntentIndex(s)
    if i == -1:
        defaultAction()
    else:
        actions[i][0](actions[i][1])


if __name__ == '__main__':
    intents = [
        'Turn on the lights',
        'Turn off the lights',
        'What is the time?'
    ]
    actions = [
        [turnLights, [True]],
        [turnLights, [False]],
        [getTime, []]
    ]

    def defaultAction():
        print('Not a supported intent')
    intentIdentifier = IntentIdentifier(intents)
    for s in intents:
        runAction(s, actions, defaultAction)
    runAction('Start the timer.', actions, defaultAction)
