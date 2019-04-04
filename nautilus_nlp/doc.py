import functools
import pkg_resources
import nautilus_nlp
lang_path = pkg_resources.resource_filename('nautilus_nlp.data', 'lang_identification.ftz')


class NautilusMissingModelException(Exception):
    """Raised when the requested model is missing"""

    pass


class Doc:
    """
    Create a doc instance of text, obtain cleaned, readable text and
    metadata from this doc.

    Properties:
    raw: incoming, unedited text
    language: 2-letter code for the language of the text
    is_detected_language: is the language detected or specified beforehand
    is_reliable_language: is the language specified or was it reliably detected
    _spacy_nlps: nested dictionary {lang: {model_id: model}} with loaded spacy language modules
    """

    def __init__(self, raw, language=None, spacy_nlps=None,langdetect = None):
        self.raw = raw
        self._spacy_nlps = spacy_nlps or dict()
        self._language = language
        self._is_reliable_language = True if language else None
        self._language_detector=langdetect
        self._text_stats = {}

    @property
    def _spacy_doc(self):
        """
        Loads the default spacy doc or creates one if necessary

        >>> doc = Doc('Test sentence for testing text')
        >>> type(doc._spacy_doc)
        <class 'spacy.tokens.doc.Doc'>
        """
        lang = self.language if self.is_reliable_language else self.hint_language

        return self._load_spacy_doc(lang)

    def _load_spacy_doc(self, lang, model_name=None):
        """
        Loads a spacy doc or creates one if necessary
        """
        # Load default spacy model if necessary, if not loaded already
        if lang not in self._spacy_nlps or (
            model_name is None and model_name not in self._spacy_nlps[lang]
        ):
            if lang not in self._spacy_nlps:
                self._spacy_nlps[lang] = {}
            self._spacy_nlps[lang][None] = self._get_default_nlp(lang)
        if model_name not in self._spacy_nlps[lang] and model_name is not None:
            raise NautilusMissingModelException(
                f"Custom model {model_name} " f"is missing."
            )
        nlp = self._spacy_nlps[lang][model_name]
        doc = nlp(self.clean_text())
        return doc

    @staticmethod
    @functools.lru_cache()
    def _get_default_nlp(lang):
        """
        Loads the spacy default language module for the Doc's language
        """
        try:
            return spacy.load(
                "{}_core_{}_sm".format(lang, "web" if lang == "en" else "news")
            )
        except IOError:
            raise NautilusMissingModelException(
                f'Default model for language "{lang}" is not available.'
            )

    @property
    def entities(self):
        """
        A list of the named entities with sensible defaults.

        >>> doc = Doc('Sentence for testing Google text')
        >>> doc.entities
        [('Google', 'ORG')]
        """
        return self.find_entities()

    @functools.lru_cache()
    def find_entities(self, model_name=None):
        """
        Extract a list of the named entities in text, with the possibility of using a custom model.
        >>> doc = Doc('Sentence for testing Google text')
        >>> doc.find_entities()
        [('Google', 'ORG')]
        """
        lang = self.language if self.is_reliable_language else self.hint_language
        return list(
            {
                (ent.text, ent.label_)
                for ent in self._load_spacy_doc(lang, model_name).ents
            }
        )

    @property
    def n_sentences(self):
        """
        Extract the number of sentences from text

        >>> doc = Doc('Test sentence for testing text. And another sentence for testing!')
        >>> doc.n_sentences
        2
        """
        return len(list(self._spacy_doc.sents))

    @property
    def sentences(self):
        """
        Extract the text and character offset (begin) of sentences from text

        >>> doc = Doc('Test sentence for testing text. And another one with, some, punctuation! And stuff.')
        >>> doc.sentences
        [('Test sentence for testing text.', 0), ('And another one with, some, punctuation!', 32), ('And stuff.', 73)]
        """

        return [(span.text, span.start_char) for span in self._spacy_doc.sents]

    @property
    def n_words(self):
        """
        Extract the number of words from text

        >>> doc = Doc('Test sentence for testing text')
        >>> doc.n_words
        5
        """
        return len(self.n_words)

    @property
    def words(self):
        """
        Extract the text and character offset (begin) of words from text

        >>> doc = Doc('Test sentence for testing text.')
        >>> doc.words
        [('Test', 0), ('sentence', 5), ('for', 14), ('testing', 18), ('text', 26), ('.', 30)]
        """

        return [(token.text, token.idx) for token in self._spacy_doc]

    @property
    def word_counts(self):
        """
        Extract words with their counts

        >>> doc = Doc('Test sentence for testing vectorisation of a sentence.')
        >>> doc.word_counts
        {'Test': 1, 'sentence': 2, 'for': 1, 'testing': 1, 'vectorisation': 1, 'of': 1, 'a': 1, '.': 1}
        """

        return dict(Counter(word for word, _ in self.words))

    @property
    def complexity(self):
        """
        Determine the complexity of text using the Flesch
        reading ease test ranging from 0.0 - 100.0 with 0.0
        being the most difficult to read.

        >>> doc = Doc('Test sentence for testing text')
        >>> doc.complexity
        83.32000000000004
        """
        if not self._text_stats:
            self._text_stats = textacy.TextStats(self._spacy_doc)
        if self._text_stats.n_syllables == 0:
            return 100
        return self._text_stats.flesch_reading_ease

    @property
    def sentiment(self):
        """
        Returns polarity score (-1 to 1) and a subjectivity score (0 to 1)

        Currently only English, Dutch, French and Italian supported

        >>> doc = Doc('Dit is een leuke zin.')
        >>> doc.sentiment
        (0.6, 0.9666666666666667)
        """

        if self.language == "en":
            from pattern.text.en import sentiment as sentiment_en

            return sentiment_en(self.clean)
        elif self.language == "nl":
            from pattern.text.nl import sentiment as sentiment_nl

            return sentiment_nl(self.clean)
        elif self.language == "fr":
            from pattern.text.fr import sentiment as sentiment_fr

            return sentiment_fr(self.clean)
        elif self.language == "it":
            from pattern.text.it import sentiment as sentiment_it

            return sentiment_it(self.clean)

        raise NautilusMissingModelException(f"No sentiment model for {self.language}")

    @functools.lru_cache()
    def extract_keyterms(self, ranker="textrank", n_terms=10, **kwargs):
        """
        Extract and rank key terms in the document by proxying to
        `textacy.keyterms`. Returns a list of (term, score) tuples. Depending
        on the ranking algorithm used, terms can consist of multiple words.

        Available rankers are TextRank (textrank), SingleRank (singlerank) and
        SGRank ('sgrank').

        >>> doc = Doc('Amsterdam is the awesome capital of the Netherlands.')
        >>> doc.extract_keyterms(n_terms=3)
        [('awesome', 0.32456160227748454), ('capital', 0.32456160227748454), ('Amsterdam', 0.17543839772251532)]
        >>> doc.extract_keyterms(ranker='sgrank')
        [('awesome capital', 0.5638711013322963), ('Netherlands', 0.22636566128805719), ('Amsterdam', 0.20976323737964653)]
        >>> doc.extract_keyterms(ranker='sgrank', ngrams=(1))
        [('Netherlands', 0.4020557546031188), ('capital', 0.29395103364295216), ('awesome', 0.18105611227666252), ('Amsterdam', 0.12293709947726655)]
        """
        if self.nwords < 1:
            return []
        rankers = ["textrank", "sgrank", "singlerank"]
        if ranker not in rankers:
            raise ValueError(
                f'ranker "{ranker}" not available; use one ' f"of {rankers}"
            )
        ranking_fn = getattr(textacy.keyterms, ranker)
        return ranking_fn(self._spacy_doc, n_keyterms=n_terms, **kwargs)

    @property
    def keyterms(self):
        """
        Return textranked keyterms for the document.

        >>> doc = Doc('Amsterdam is the awesome capital of the Netherlands.')
        >>> doc.extract_keyterms(n_terms=3)
        [('awesome', 0.32456160227748454), ('capital', 0.32456160227748454), ('Amsterdam', 0.17543839772251532)]
        """
        return self.extract_keyterms()

    @property
    def minhash(self):
        """
        A cheap way to compute a hash for finding similarity of docs
        Source: https://ekzhu.github.io/datasketch/minhash.html
        >>> doc = Doc('Sentence for computing the minhash')
        >>> doc.minhash[:5]
        [407326892, 814360600, 1099082245, 1176349439, 1735256]
        """
        return self.find_minhash()

    @functools.lru_cache()
    def find_minhash(self, num_perm=128):
        words = self.words
        doc_hash = MinHash(num_perm=num_perm)
        for word, _ in words:
            doc_hash.update(word.encode("utf8"))
        return list(doc_hash.digest())

    def similarity(self, other_doc, metric="jaccard", hash_method="minhash"):
        """
        Computes similarity for two documents.
        Only minhash Jaccard similarity is implemented.
        >>> doc1 = Doc('Sentence for computing the minhash')
        >>> doc2 = Doc('Sentence for computing the similarity')
        >>> doc1.similarity(doc2)
        0.7265625
        """
        if hash_method == "minhash" and metric == "jaccard":
            hash1 = MinHash(hashvalues=self.minhash)
            hash2 = MinHash(hashvalues=other_doc.minhash)
            return hash1.jaccard(hash2)
        else:
            raise NotImplementedError(
                f"Metric/hash method combination {metric}"
                f"/{hash_method} is not implemented as similarity metric"
            )

    @property
    def word_vectors(self):
        """
        Returns word embeddings for the words in the document.
        """
        return self.generate_word_vectors()

    @functools.lru_cache()
    def generate_word_vectors(self, model_name=None):
        """
        Returns word embeddings for the words in the document.
        The default spacy models don't have "true" word vectors
        but only context-sensitive tensors that are within the document.

        Returns:
        A dictionary mapping words from the document to a dict with the
        corresponding values of the following variables:

        has vector: Does the token have a vector representation?
        vector norm: The L2 norm of the token's vector (the square root of the
                    sum of the values squared)
        OOV: Out-of-vocabulary (This variable always gets the value True since
                                there are no vectors included in the model)
        vector: The vector representation of the word

        >>> doc = Doc('Test sentence')
        >>> doc.word_vectors['Test']['is_oov']
        True
        >>> len(doc.word_vectors['Test']['vector'])
        96
        >>> doc.word_vectors['Test']['vector_norm'] == doc.word_vectors['sentence']['vector_norm']
        False
        """
        lang = self.language if self.is_reliable_language else self.hint_language
        return {
            token.text: {
                "has_vector": token.has_vector,
                "vector_norm": token.vector_norm,
                "is_oov": token.is_oov,
                "vector": token.vector.tolist(),
            }
            for token in self._load_spacy_doc(lang, model_name)
        }

    @property
    def doc_vector(self):
        """
        Returns document embeddings based on the words in the document.

        >>> import numpy
        >>> numpy.array_equiv(Doc('a b').doc_vector, Doc('a b').doc_vector)
        True
        >>> numpy.array_equiv(Doc('a b').doc_vector, Doc('a a b').doc_vector)
        False
        """
        return self.aggregate_word_vectors()

    @functools.lru_cache()
    def aggregate_word_vectors(
        self, model_name=None, aggregation="mean", normalize=False, exclude_oov=False
    ):
        """
        Returns document embeddings based on the words in the document.

        >>> import numpy
        >>> doc1 = Doc('a b')
        >>> doc2 = Doc('a a b')
        >>> numpy.array_equiv(doc1.aggregate_word_vectors(), doc1.aggregate_word_vectors())
        True
        >>> numpy.array_equiv(doc1.aggregate_word_vectors(), doc2.aggregate_word_vectors())
        False
        >>> numpy.array_equiv(doc1.aggregate_word_vectors(aggregation='mean'), doc2.aggregate_word_vectors(aggregation='sum'))
        False
        >>> numpy.array_equiv(doc1.aggregate_word_vectors(aggregation='mean'), doc2.aggregate_word_vectors(aggregation='var'))
        False
        >>> numpy.array_equiv(doc1.aggregate_word_vectors(aggregation='sum'), doc2.aggregate_word_vectors(aggregation='var'))
        False
        >>> doc = Doc('sentence with an out of vector word lsseofn')
        >>> len(doc.aggregate_word_vectors())
        96
        >>> numpy.array_equiv(doc.aggregate_word_vectors(exclude_oov=False), doc.aggregate_word_vectors(exclude_oov=True))
        False
        """
        lang = self.language if self.is_reliable_language else self.hint_language
        tokens = [
            token
            for token in self._load_spacy_doc(lang, model_name)
            if not exclude_oov or not token.is_oov
        ]
        vectors = [
            token.vector / token.vector_norm if normalize else token.vector
            for token in tokens
        ]

        if aggregation == "mean":
            return numpy.mean(vectors, axis=0).tolist()
        elif aggregation == "sum":
            return numpy.sum(vectors, axis=0).tolist()
        elif aggregation == "var":
            return numpy.var(vectors, axis=0).tolist()
        else:
            raise NotImplementedError(
                f"Aggregation method {aggregation} is not implemented."
            )
