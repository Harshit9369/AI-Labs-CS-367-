import spacy
import re
from Levenshtein import distance as lev_distance
import random

nlp_model = spacy.load('en_core_web_sm')

def clean_and_tokenize(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    doc = nlp_model(text)
    sentences = [sent.text for sent in doc.sents]
    
    tokenized_sentences = []
    for sentence in sentences:
        doc = nlp_model(sentence)
        tokens = [token.lemma_ for token in doc if token.is_alpha and not nlp_model.vocab[token.text].is_stop]
        tokenized_sentences.append(' '.join(tokens))
    
    return tokenized_sentences

def synonymize_nouns(sentence):
    doc = nlp_model(sentence)
    transformed_words = []
    for word in doc:
        if word.pos_ == 'NOUN':
            similar_words = [syn.lemma_ for syn in nlp_model.vocab if syn.has_vector and word.text != syn.text]
            transformed_words.append(random.choice(similar_words) if similar_words else word.text)
        else:
            transformed_words.append(word.text)
    return ' '.join(transformed_words)

def a_star_algorithm(sent1, sent2):
    len1, len2 = len(sent1), len(sent2)
    open_set = [(0 + heuristic_calculation(0, 0, len1, len2), 0, 0, 0)]
    cost_map = {(0, 0): 0}
    path_map = {}
    
    while open_set:
        open_set.sort()
        _, current_cost, i, j = open_set.pop(0)

        if i == len1 and j == len2:
            break

        for new_i, new_j in [(i + 1, j), (i, j + 1), (i + 1, j + 1)]:
            if new_i <= len1 and new_j <= len2:
                additional_cost = lev_distance(sent1[i], sent2[j]) if new_i < len1 and new_j < len2 else 0
                new_total_cost = current_cost + additional_cost
                if (new_i, new_j) not in cost_map or new_total_cost < cost_map[(new_i, new_j)]:
                    cost_map[(new_i, new_j)] = new_total_cost
                    f_score = new_total_cost + heuristic_calculation(new_i, new_j, len1, len2)
                    open_set.append((f_score, new_total_cost, new_i, new_j))
                    path_map[(new_i, new_j)] = (i, j)

    return backtrack_alignment(path_map, sent1, sent2)

def heuristic_calculation(i, j, total_i, total_j):
    return abs(total_i - i) + abs(total_j - j)

def backtrack_alignment(path_map, sentences1, sentences2):
    alignments = []
    current = (len(sentences1), len(sentences2))
    while current in path_map:
        previous = path_map[current]
        if previous[0] < len(sentences1) and previous[1] < len(sentences2):
            alignments.append((sentences1[previous[0]], sentences2[previous[1]]))
        current = previous
    return list(reversed(alignments))

def similarity_score(s1, s2):
    distance = lev_distance(s1, s2)
    max_length = max(len(s1), len(s2))
    return 1 - (distance / max_length) if max_length > 0 else 1.0

def plagiarism_detection(sentences1, sentences2):
    alignments = a_star_algorithm(sentences1, sentences2)
    detected_pairs = []
    
    for s1, s2 in alignments:
        sim = similarity_score(s1, s2)
        detected_pairs.append((s1, s2, sim))
    
    return detected_pairs

def overall_plagiarism_level(detected_pairs):
    if not detected_pairs:
        return 0.0
    
    total_similarity = sum(sim for _, _, sim in detected_pairs)
    return total_similarity / len(detected_pairs)

test_cases = [
    {
        "name": "Test Case 1: Identical Documents",
        "doc1": "The cat sat on the mat.",
        "doc2": "The cat sat on the mat.",
    },
    {
        "name": "Test Case 2: Slightly Modified Document",
        "doc1": "The cat sat on the mat.",
        "doc2": "The feline rested on the mat.",
    },
    {
        "name": "Test Case 3: Completely Different Documents",
        "doc1": "The quick brown fox jumps over the lazy dog.",
        "doc2": "An elephant never forgets.",
    },
    {
        "name": "Test Case 4: Partial Overlap",
        "doc1": "The cat sat on the mat. It was a sunny day.",
        "doc2": "The cat rested on the rug. It was a bright afternoon.",
    }
]

for case in test_cases:
    print(f"\n{case['name']}")
    
    cleaned_sent1 = clean_and_tokenize(case['doc1'])
    cleaned_sent2 = clean_and_tokenize(case['doc2'])

    paraphrased_sent1 = [synonymize_nouns(sent) for sent in cleaned_sent1]
    paraphrased_sent2 = [synonymize_nouns(sent) for sent in cleaned_sent2]

    detected_pairs = plagiarism_detection(paraphrased_sent1, paraphrased_sent2)

    if detected_pairs:
        print("Detected Plagiarized Pairs:")
        for s1, s2, sim in detected_pairs:
            print(f"'{s1}' is similar to '{s2}' with a similarity score of {sim:.2f}")
    else:
        print("No plagiarism detected.")

    plagiarism_level = overall_plagiarism_level(detected_pairs)
    print(f"Overall level of plagiarism: {plagiarism_level:.2f}")