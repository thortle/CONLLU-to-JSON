import json
from collections import Counter, defaultdict

def read_conllu(file_name):
    # On initialise une liste vide qui contiendra toutes les phrases
    # et une liste temporaire pour stocker les lignes de la phrase courante
    sentences = []
    current_sentence = []

    # Ouverture du fichier en lecture avec encodage UTF-8
    with open(file_name, 'r', encoding='utf-8') as file:
        for line in file:
            # On enlève les espaces et retours à la ligne superflus
            line = line.strip()

            # On ignore les lignes de commentaires
            if line.startswith('# text'):
                continue

            if not line:
                # Si on a des lignes dans la phrase courante,
                # on ajoute la phrase à notre liste de phrases
                if current_sentence:
                    sentences.append(current_sentence)
                    current_sentence = []

            # Analyse la ligne et ajoute les infos pertinentes à la phrase courante si valide.
            else:
                parts = line.split('\t')
                if len(parts) >= 4:
                    current_sentence.append({
                        "id": parts[0],
                        "form": parts[1],
                        "lemma": parts[2],
                        "upos": parts[3],
                        "deprel": parts[7] if len(parts) > 7 else None
                    })
    # Pour ne pas oublier la dernière phrase si le fichier ne se termine pas par une ligne vide
    if current_sentence:
        sentences.append(current_sentence)
    return sentences

def validate_conllu(sentences):
    # On s'assure d'avoir un fichier CONLLU fiable
    for sentence in sentences:
        for token in sentence:
            if not all(key in token for key in ["id", "form", "lemma", "upos"]):
                raise ValueError("CONLLU n'est pas trouvé ou est endommagé")

def process_sentences(sentences):
    """
    Analyse les statistiques d'un ensemble de phrases au format CONLLU.
    Prend en paramètre une liste de phrases (output de read_conllu).
    Retourne un hachage avec les statistiques demandées.
    """
    # Initialisation des compteurs
    nb_toks = 0
    nb_sents = len(sentences)
    forms = []
    lemmas = []
    nb_puncts = 0
    pos_counts = defaultdict(Counter)

    for sentence in sentences:
        # On compte le nombre de tokens
        nb_toks += len(sentence)
        for token in sentence:
            # On compte le nombre de ponctuations
            if token["upos"] == "PUNCT":
                nb_puncts += 1
                continue
            # On récupère les formes, les lemmes et les POS
            forms.append(token["form"])
            lemmas.append(token["lemma"])
            pos_counts[token["upos"]][token["lemma"]] += 1

    # On compte le nombre de formes et de types
    nb_forms = len(forms)
    nb_types = len(set(forms))
    # Calcul des moyennes
    average_sent_length = nb_toks / nb_sents
    average_form_length = sum(len(form) for form in forms) / nb_forms

    # Création du dictionnaire de retour
    return {
        "nbToks": nb_toks,
        "nbSents": nb_sents,
        "nbForms": nb_forms,
        "nbPuncts": nb_puncts,
        "nbTypes": nb_types,
        "averageSentLength": average_sent_length,
        "averageFormLength": average_form_length,
        # Conversion des dictionnaires en tableaux triés par fréquence
        "noun2freq": sorted(pos_counts["NOUN"].items(), key=lambda x: x[1], reverse=True),
        "verb2freq": sorted(pos_counts["VERB"].items(), key=lambda x: x[1], reverse=True),
        "adj2freq": sorted(pos_counts["ADJ"].items(), key=lambda x: x[1], reverse=True),
        "adv2freq": sorted(pos_counts["ADV"].items(), key=lambda x: x[1], reverse=True),
        "lem2freq": sorted(Counter(lemmas).items(), key=lambda x: x[1], reverse=True)
    }

def generate_ngrams(lemmas, min_len=2, max_len=6):
    # Calcul des n-grammes
    lemmas = [lemma for lemma in lemmas if lemma not in [",", ".", "!", "?", ":", ";", "-", "_", "(", ")"]]

    ngrams = defaultdict(list)
    for n in range(min_len, max_len + 1):
        for i in range(len(lemmas) - n + 1):
            ngram = tuple(lemmas[i:i + n])
            ngrams[n].append(ngram)
    # Tri par fréquence
    return {key: sorted(Counter(value).items(), key=lambda x: x[1], reverse=True) for key, value in ngrams.items()}

# Supprime les n-grammes plus courts redondants si leur fréquence est inférieure à un seuil.
def deduplicate_ngrams(ngrams, seuil_dedoublonnage):
    for n in sorted(ngrams.keys(), reverse=True):
        if n - 1 not in ngrams:
            continue
        for longer_ngram, freq_longer in ngrams[n]:
            shorter_candidates = [longer_ngram[:i] + longer_ngram[i + 1:] for i in range(len(longer_ngram))]
            for shorter_ngram in shorter_candidates:
                for idx, (short_ngram, freq_short) in enumerate(ngrams[n - 1]):
                    if short_ngram == shorter_ngram and freq_short <= seuil_dedoublonnage * freq_longer:
                        ngrams[n - 1].pop(idx)
                        break
    return ngrams

# Extrait et compte les fréquences des séquences de lemmes correspondant à des motifs POS donnés.
def extract_patterns(sentences, patterns):
    pattern_freqs = Counter()
    for sentence in sentences:
        lemmas = [token["lemma"] for token in sentence]
        pos_tags = [token["upos"] for token in sentence]
        for pattern in patterns:
            pattern_len = len(pattern)
            for i in range(len(lemmas) - pattern_len + 1):
                if pos_tags[i:i + pattern_len] == pattern:
                    pattern_freqs[" ".join(lemmas[i:i + pattern_len])] += 1
    return sorted(pattern_freqs.items(), key=lambda x: x[1], reverse=True)


# Écrit les statistiques dans un fichier JSON avec une mise en forme lisible.
def generate_skipgrams(lemmas, gap=1, min_len=2, max_len=3):
    skipgrams = defaultdict(int)
    n = len(lemmas)

    for length in range(min_len, max_len + 1):
        for i in range(n - length + 1):
            skipgram = tuple(lemmas[i:i + length:gap])
            skipgrams[skipgram] += 1

    return sorted(skipgrams.items(), key=lambda x: x[1], reverse=True)

 # SKIPGRAMS SANS PUNCT

 # def generate_skipgrams(lemmas, gap=1, min_len=2, max_len=3):
 #    lemmas = [lemma for lemma in lemmas if lemma not in [",", ".", "!", "?", ":", ";", "-", "_", "(", ")"]]
 #
 #    skipgrams = defaultdict(int)
 #    n = len(lemmas)
 #
 #    for length in range(min_len, max_len + 1):
 #        for i in range(n - length + 1):
 #            skipgram = tuple(lemmas[i:i + length:gap])
 #            skipgrams[skipgram] += 1
 #
 #    return sorted(skipgrams.items(), key=lambda x: x[1], reverse=True)


def main(conllu_file, json_file, pattern_file=None, seuil_dedoublonnage=1.3, ngram_min=2, ngram_max=6, skipgram_gap=1):
    # Lecture et validation du fichier CoNLL-U
    sentences = read_conllu(conllu_file)
    validate_conllu(sentences)
    stats = process_sentences(sentences)

    # Génération des n-grammes
    lemmas = [token["lemma"] for sentence in sentences for token in sentence]
    ngrams = generate_ngrams(lemmas, ngram_min, ngram_max)
    stats["ngrams"] = deduplicate_ngrams(ngrams, seuil_dedoublonnage)

    # Extraction des motifs si un fichier de motifs est fourni
    if pattern_file:
        try:
            with open(pattern_file, 'r', encoding='utf-8') as pf:
                patterns = json.load(pf)
            stats["patterns"] = extract_patterns(sentences, patterns)
        except FileNotFoundError:
            print(f"Fichier de patterns '{pattern_file}' introuvable.")

    # Génération des skip-grammes
    stats["skipgrams"] = generate_skipgrams(lemmas, gap=skipgram_gap, min_len=ngram_min, max_len=ngram_max)

    # Écriture des résultats dans un fichier JSON
    with open(json_file, 'w', encoding='utf-8') as json_out:
        json.dump(stats, json_out, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    conllu_file_path = "./fr_rhapsodie-ud-test.conllu"
    json_file_path = "results.json"
    pattern_file_path = "patterns.json"

    main(conllu_file_path, json_file_path, pattern_file=pattern_file_path)