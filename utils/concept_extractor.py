# utils/concept_extractor.py

import re
from typing import List, Dict

import nltk
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download("punkt", quiet=True)
nltk.download("averaged_perceptron_tagger", quiet=True)

# -------------------------------
# CONFIG
# -------------------------------

MAX_WORDS_IN_CONCEPT = 3

MIN_TFIDF_SCORE = 0.1

BAD_START_WORDS = {
    "very",
    "big",
    "important",
    "many",
    "several",
    "various",
    "different",
    "modern"
}

BAD_END_WORDS = {
    "accelerates",
    "helps",
    "provides",
    "ensures",
    "allows",
    "supports",
    "using",
    "making",
    "performing",
    "executing"
}

# ⭐ UPDATED — Strong filtering
BAD_CONCEPTS = {

    # Generic weak concepts
    "people",
    "system",
    "effort",
    "society",
    "technology",
    "internet",
    "threat",
    "threats",
    "attack",
    "attacks",
    "data",
    "process",
    "tool",
    "method",
    "security",
    "risk",
    "risks",

    # ⭐ NEW FILTERS
    "common targets",
    "effective attack methods",
    "processing data",
    "critical data",
    "digital world",
    "modern systems",
    "new technologies",

    # Existing
    "big impact",
    "broad range",
    "technology affects",
    "core objective",
    "very crucial",
    "modern technology",
    "new system"
}

# -------------------------------
# Sentence Split
# -------------------------------

def split_sentences(text: str) -> List[str]:

    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    return nltk.sent_tokenize(text)


# -------------------------------
# Normalize Phrase
# -------------------------------

def normalize_phrase(phrase: str):

    phrase = phrase.lower()

    # Remove plural 's'
    if phrase.endswith("s"):

        phrase = phrase[:-1]

    return phrase


# -------------------------------
# Noun Phrase Extraction
# -------------------------------

def extract_noun_phrases(
    sentences: List[str]
) -> List[str]:

    noun_phrases = []

    seen = set()

    for sent in sentences:

        tokens = nltk.word_tokenize(sent)

        tags = nltk.pos_tag(tokens)

        chunk = []

        for word, tag in tags:

            if tag.startswith("JJ") or tag.startswith("NN"):

                chunk.append((word, tag))

            else:

                phrase = build_phrase(chunk)

                if phrase:

                    norm = normalize_phrase(phrase)

                    if norm not in seen:

                        noun_phrases.append(phrase)

                        seen.add(norm)

                chunk = []

        phrase = build_phrase(chunk)

        if phrase:

            norm = normalize_phrase(phrase)

            if norm not in seen:

                noun_phrases.append(phrase)

                seen.add(norm)

    return noun_phrases


# -------------------------------
# Phrase Builder
# -------------------------------

def build_phrase(chunk):

    if not chunk:
        return None

    words = [w for w, t in chunk]

    tags = [t for w, t in chunk]

    # Must contain noun
    if not any(
        t.startswith("NN")
        for t in tags
    ):
        return None

    # Too long
    if len(words) > MAX_WORDS_IN_CONCEPT:
        return None

    phrase = " ".join(words)

    if not is_valid_concept(phrase):
        return None

    return phrase


# -------------------------------
# TF-IDF Ranking
# -------------------------------

def rank_concepts(
    phrases: List[str],
    sentences: List[str]
):

    if not phrases:
        return []

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 3)
    )

    tfidf = vectorizer.fit_transform(
        sentences
    )

    feature_names = (
        vectorizer
        .get_feature_names_out()
    )

    scores = tfidf.sum(axis=0).A1

    scored_phrases = dict(
        zip(feature_names, scores)
    )

    ranked = []

    for phrase in phrases:

        score = scored_phrases.get(
            phrase.lower(),
            0
        )

        if score < MIN_TFIDF_SCORE:
            continue

        ranked.append(
            (phrase, score)
        )

    ranked.sort(
        key=lambda x: (
            len(x[0].split()),  # ⭐ multi-word first
            x[1]
        ),
        reverse=True
    )

    return ranked


# -------------------------------
# Concept Validator
# -------------------------------

def is_valid_concept(
    phrase: str
):

    phrase = phrase.strip()

    if not phrase:
        return False

    phrase_lower = phrase.lower()

    words = phrase_lower.split()

    # Too short single word
    if len(words) == 1:

        if len(words[0]) < 5:
            return False

    # Too long
    if len(words) > MAX_WORDS_IN_CONCEPT:
        return False

    # Weak concept list
    if phrase_lower in BAD_CONCEPTS:
        return False

    # Bad starting word
    if words[0] in BAD_START_WORDS:
        return False

    # Bad ending word
    if words[-1] in BAD_END_WORDS:
        return False

    # Numeric phrase
    if any(
        w.isdigit()
        for w in words
    ):
        return False

    # Must contain letters
    if not re.search(
        r"[a-zA-Z]",
        phrase
    ):
        return False

    return True


# -------------------------------
# Main Extraction
# -------------------------------

def extract_concepts(
    text: str,
    top_k: int = 10
) -> List[Dict]:

    sentences = split_sentences(text)

    if not sentences:
        return []

    phrases = extract_noun_phrases(
        sentences
    )

    ranked = rank_concepts(
        phrases,
        sentences
    )

    results = []

    for concept, score in ranked:

        if len(results) >= top_k:
            break

        related = [

            s for s in sentences

            if concept.lower()
            in s.lower()

        ]

        if related:

            results.append({

                "concept": concept,

                "score": round(
                    float(score),
                    3
                ),

                "sentences": related

            })

    return results