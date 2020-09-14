# AUTOGENERATED! DO NOT EDIT! File to edit: 01_goodness_of_monolingual_embeddings.ipynb (unless otherwise specified).

__all__ = ['Embeddings']

# Cell
import numpy as np

class Embeddings():
    def __init__(self, embeddings, index2word):
        '''embeddings - numpy array of embeddings, index2word - list of words corresponding to embeddings'''
        assert len(embeddings) == len(index2word)
        self.vectors = embeddings
        self.i2w = index2word
        self.w2i = {w:i for i, w in enumerate(index2word)}

    def analogy(self, a, b, c, n=5):
        '''
        a is to b as c is to ?

        Performs the following algebraic calculation: result = emb_a - emb_b + emb_c
        Looks up n closest words to result.

        Implements the embedding space math behind the famous word2vec example:
        king - man + woman = queen
        '''
        question_word_indices = [self.w2i[word] for word in [a, b, c]]
        a, b, c = [self.vectors[idx] for idx in question_word_indices]
        result = a - b + c

        nn_indices = np.flip(
            np.argsort(self.vectors @ result / (np.linalg.norm(self.vectors, axis=1) * np.linalg.norm(result)))
        )

        nn_words = []
        for idx in nn_indices:
            if idx in question_word_indices: continue
            nn_words.append(self.i2w[idx])
            if len(nn_words) == n: break

        return nn_words

    @classmethod
    def create_from_txt_file(cls, path_to_txt_file):
        '''create embeddings from word2vec embeddings text file'''
        index, vectors = [], []
        with open(path_to_txt_file) as f:
            for line in f.readlines()[1:]:
                try:
                    vectors.append(np.array([float(s) for s in line.split()[1:]]))
                    index.append(line.split()[0])
                except ValueError: pass # we may have encountered a 2 word embedding, for instance 'New York' or 'w dolinie'
        return cls(vectors, index)