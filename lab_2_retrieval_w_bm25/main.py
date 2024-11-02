"""
Lab 2.

Text retrieval with BM25
"""
# pylint:disable=too-many-arguments, unused-argument
from math import log


def tokenize(text: str) -> list[str] | None:
    """
    Tokenize the input text into lowercase words without punctuation, digits and other symbols.

    Args:
        text (str): The input text to tokenize.

    Returns:
        list[str] | None: A list of words from the text.

    In case of corrupt input arguments, None is returned.
    """
    if not isinstance(text, str):
        return None
    for sign in text.lower():
        if not sign.isalpha():
            text = text.lower().replace(sign, ' ')
    text = text.replace('  ', ' ')
    return text.split()

def remove_stopwords(tokens: list[str], stopwords: list[str]) -> list[str] | None:
    """
    Remove stopwords from the list of tokens.

    Args:
        tokens (list[str]): List of tokens.
        stopwords (list[str]): List of stopwords.

    Returns:
        list[str] | None: Tokens after removing stopwords.

    In case of corrupt input arguments, None is returned.
    """
    if not isinstance(tokens, list) or not isinstance(stopwords, list):
        return None
    if tokens == [] or stopwords == []:
        return None
    for data in tokens:
        if not isinstance(data, str):
            return None
    for data in stopwords:
        if not isinstance(data, str):
            return None
    tokens_cleared = [elem for elem in tokens if elem not in stopwords]
    return tokens_cleared

def build_vocabulary(documents: list[list[str]]) -> list[str] | None:
    """
    Build a vocabulary from the documents.

    Args:
        documents (list[list[str]]): List of tokenized documents.

    Returns:
        list[str] | None: List with unique words from the documents.

    In case of corrupt input arguments, None is returned.
    """
    if not isinstance(documents, list) or len(documents) == 0:
        return None
    unique_words = []
    for text in documents:
        if not isinstance(text, list):
            return None
        for word in text:
            if not isinstance(word, str):
                return None
        unique_words += [word for word in text if word not in unique_words]
    return unique_words

def calculate_tf(vocab: list[str], document_tokens: list[str]) -> dict[str, float] | None:
    """
    Calculate term frequency for the given tokens based on the vocabulary.

    Args:
        vocab (list[str]): Vocabulary list.
        document_tokens (list[str]): Tokenized document.

    Returns:
        dict[str, float] | None: Mapping from vocabulary terms to their term frequency.

    In case of corrupt input arguments, None is returned.
    """
    if (not isinstance(vocab, list) or not isinstance(document_tokens, list)
            or len(vocab) == 0 or len(document_tokens) == 0):
        return None
    tf = {}
    for token in document_tokens:
        if not isinstance(token, str):
            return None
        tf[token] = 0.0
    for elem in vocab:
        if not isinstance(elem, str):
            return None
        if not elem in tf:
            tf[elem] = 0.0
    for key_elem in tf:
        tf[key_elem] = float(document_tokens.count(key_elem) / len(document_tokens))
    return tf

def calculate_idf(vocab: list[str], documents: list[list[str]]) -> dict[str, float] | None:
    """
    Calculate inverse document frequency for each term in the vocabulary.

    Args:
        vocab (list[str]): Vocabulary list.
        documents (list[list[str]]): List of tokenized documents.

    Returns:
        dict[str, float] | None: Mapping from vocabulary terms to its IDF scores.

    In case of corrupt input arguments, None is returned.
    """
    if (not isinstance(vocab, list) or not isinstance(documents, list)
            or len(vocab) == 0 or len(documents) == 0):
        return None
    idf = {}
    for elem in vocab:
        if not isinstance(elem, str):
            return None
        doc_number = 0
        for doc in documents:
            if not isinstance(doc, list):
                return None
            for word in doc:
                if not isinstance(word, str):
                    return None
            if elem in doc:
                doc_number += 1
        idf[elem] = log((len(documents) - doc_number + 0.5) / (doc_number + 0.5))
    return idf
def calculate_tf_idf(tf: dict[str, float], idf: dict[str, float]) -> dict[str, float] | None:
    """
    Calculate TF-IDF scores for a document.

    Args:
        tf (dict[str, float]): Term frequencies for the document.
        idf (dict[str, float]): Inverse document frequencies.

    Returns:
        dict[str, float] | None: Mapping from terms to their TF-IDF scores.

    In case of corrupt input arguments, None is returned.
    """
    if not tf or not isinstance(tf, dict) or not all(isinstance(key, str) for key in tf) or \
            not all(isinstance(value, float) for value in tf.values()):
        return None
    if not idf or not isinstance(idf, dict) or not all(isinstance(key, str) for key in idf) or \
            not all(isinstance(value, float) for value in idf.values()):
        return None

    tf_idf = {}
    for word in tf:
        tf_idf[word] = tf[word] * idf[word]
    return tf_idf

    if (not isinstance(tf, dict) or not isinstance(idf, dict)
        or len(tf.keys()) == 0 or len(idf.keys()) == 0):
        return None
    tf_idf = {}
    for key_tf in tf.keys():
        if not isinstance(key_tf, str) or not isinstance(tf[key_tf], float):
            return None
        if key_tf not in idf.keys():
            tf_idf[key_tf] = 0.0
        else:
            if not isinstance(idf[key_tf], float):
                return None
            tf_idf[key_tf] = tf[key_tf] * idf[key_tf]
    for key_idf in idf.keys():
        if not isinstance(key_idf, str) or not isinstance(idf[key_idf], float):
            return None
        if key_idf not in tf.keys():
            tf_idf[key_idf] = 0.0
    return tf_idf

def calculate_bm25(
    vocab: list[str],
    document: list[str],
    idf_document: dict[str, float],
    k1: float = 1.5,
    b: float = 0.75,
    avg_doc_len: float | None = None,
    doc_len: int | None = None,
) -> dict[str, float] | None:
    """
    Calculate BM25 scores for a document.

    Args:
        vocab (list[str]): Vocabulary list.
        document (list[str]): Tokenized document.
        idf_document (dict[str, float]): Inverse document frequencies.
        k1 (float): BM25 parameter.
        b (float): BM25 parameter.
        avg_doc_len (float | None): Average document length.
        doc_len (int | None): Length of the document.

    Returns:
        dict[str, float] | None: Mapping from terms to their BM25 scores.

    In case of corrupt input arguments, None is returned.
    """
    if (not isinstance(vocab, list) or not isinstance(document, list)
        or not isinstance(idf_document, dict) or not isinstance(avg_doc_len, float)
        or not isinstance(doc_len, int)):
        return None
    if (isinstance(doc_len, bool) or not isinstance(k1, float)
        or not isinstance(b, float) or len(document) == 0
        or len(idf_document.keys()) == 0):
        return None
    for key, value in idf_document.items():
        if (not isinstance(key, str) or not isinstance(value, float)
                or len(vocab) == 0):
            return None
    bm25_dic = {}
    for elem in vocab:
        if not isinstance(elem, str):
            return None
        el_num = document.count(elem)
        bm_25 = idf_document[elem] * el_num * (k1 + 1) / (el_num +
                                                          k1 * (1 - b + b * doc_len / avg_doc_len))
        bm25_dic[elem] = bm_25
    for word in document:
        if not isinstance(word, str):
            return None
        if not word in bm25_dic:
            bm_25 = 0.0
            bm25_dic[word] = bm_25
    return bm25_dic


def rank_documents(
    indexes: list[dict[str, float]], query: str, stopwords: list[str]
) -> list[tuple[int, float]] | None:
    """
    Rank documents for the given query.

    Args:
        indexes (list[dict[str, float]]): List of BM25 or TF-IDF indexes for the documents.
        query (str): The query string.
        stopwords (list[str]): List of stopwords.

    Returns:
        list[tuple[int, float]] | None: Tuples of document index and its score in the ranking.

    In case of corrupt input arguments, None is returned.
    """
    if (not isinstance(indexes, list) or not isinstance(query, str)
        or not isinstance(stopwords, list) or len(indexes) == 0):
        return None
    query_new = tokenize(query)
    if query_new is None:
        return None
    search = remove_stopwords(query_new, stopwords)
    if search is None:
        return None
    rel_doc_rating = {}
    for doc_numb, doc in enumerate(indexes):
        if not isinstance(doc, dict):
            return None
        for key, value in doc.items():
            if not isinstance(key, str) or not isinstance(value, float):
                return None
        rating = 0.0
        for token in search:
            token_metric = doc.get(token, 0.0)
            rating += token_metric
        rel_doc_rating[doc_numb] = rating
    final_rating = sorted(rel_doc_rating.items(), key=lambda x: x[1], reverse=True)
    return final_rating


def calculate_bm25_with_cutoff(
    vocab: list[str],
    document: list[str],
    idf_document: dict[str, float],
    alpha: float,
    k1: float = 1.5,
    b: float = 0.75,
    avg_doc_len: float | None = None,
    doc_len: int | None = None,
) -> dict[str, float] | None:
    """
    Calculate BM25 scores for a document with IDF cutoff.

    Args:
        vocab (list[str]): Vocabulary list.
        document (list[str]): Tokenized document.
        idf_document (dict[str, float]): Inverse document frequencies.
        alpha (float): IDF cutoff threshold.
        k1 (float): BM25 parameter.
        b (float): BM25 parameter.
        avg_doc_len (float | None): Average document length.
        doc_len (int | None): Length of the document.

    Returns:
        dict[str, float] | None: Mapping from terms to their BM25 scores with cutoff applied.

    In case of corrupt input arguments, None is returned.
    """
    if not vocab or not isinstance(vocab, list) or not all(isinstance(item, str) for item in vocab)\
            or not document or not isinstance(document, list):
        return None
    if not all(isinstance(item, str) for item in document) or not idf_document \
            or not isinstance(idf_document, dict) \
            or not all(isinstance(key, str) for key in idf_document) \
            or not all(isinstance(value, float) for value in idf_document.values()):
        return None
    if not isinstance(alpha, float) or not isinstance(k1, float) \
            or not isinstance(b, float) or not isinstance(avg_doc_len, float):
        return None
    if not isinstance(doc_len, int) or isinstance(doc_len, bool) or doc_len < 0:
        return None

    bm25_with_cutoff = {}
    for word in vocab:
        if word in idf_document and idf_document[word] >= alpha:
            word_count = document.count(word)
            bm25_with_cutoff[word] = idf_document[word] * ((word_count * (k1 + 1)) / (
                    word_count + k1 * (1 - b + (b * doc_len / avg_doc_len))))
    return bm25_with_cutoff


def save_index(index: list[dict[str, float]], file_path: str) -> None:
    """
    Save the index to a file.

    Args:
        index (list[dict[str, float]]): The index to save.
        file_path (str): The path to the file where the index will be saved.
    """
    if not index or not isinstance(index, list) or \
            not all(isinstance(item, dict) for item in index) or \
            not all(isinstance(key, str) for item in index for key in item) or \
            not all(isinstance(value, float) for item in index for value in item.values()):
        return None
    if not isinstance(file_path, str) or not file_path:
        return None

    with open(file_path, 'w', encoding='utf-8') as file:
        dump(index, file)
    return None


def load_index(file_path: str) -> list[dict[str, float]] | None:
    """
    Load the index from a file.

    Args:
        file_path (str): The path to the file from which to load the index.

    Returns:
        list[dict[str, float]] | None: The loaded index.

    In case of corrupt input arguments, None is returned.
    """
    if not file_path or not isinstance(file_path, str):
        return None

    with open(file_path, 'r', encoding='utf-8') as file:
        index: list[dict[str, float]] = load(file)
    return index


def calculate_spearman(rank: list[int], golden_rank: list[int]) -> float | None:
    """
    Calculate Spearman's rank correlation coefficient between two rankings.

    Args:
        rank (list[int]): Ranked list of document indices.
        golden_rank (list[int]): Golden ranked list of document indices.

    Returns:
        float | None: Spearman's rank correlation coefficient.

    In case of corrupt input arguments, None is returned.
    """
    if not rank or not isinstance(rank, list) or not all(isinstance(item, int) for item in rank):
        return None
    if not golden_rank or not isinstance(golden_rank, list) or \
            not all(isinstance(item, int) for item in golden_rank) or \
            len(rank) != len(golden_rank):
        return None

    n = len(rank)
    rank_differences = 0
    for item in rank:
        if item in golden_rank:
            rank_differences += (golden_rank.index(item) - rank.index(item)) ** 2
    return 1 - (6 * rank_differences) / (n * (n**2 - 1))
