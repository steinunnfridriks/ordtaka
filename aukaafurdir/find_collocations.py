from rmh_extractor import RmhWord, RmhExtractor

# choose the folder you want to run on 
RMH = RmhExtractor(folder='*')
words = RMH.extract(forms=True, lemmas=True, pos=True)

def verb_plus_prep(words):
    # Get a verb - proposition/adverb pair
    freqdic = {}
    for word in words:
        try:
            if word.pos.startswith('s'):
                verb = word.lemma
                word2 = next(words)
                if word2.pos.startswith('a'):
                    prop = word2.word_form
                    word3 = next(words)
                    if word3.pos.startswith('n'):
                        noun = word3.word_form
                        colloc = (verb, prop, noun)
                        if colloc in freqdic:
                            freqdic[colloc]+=1
                        else:
                            freqdic[colloc] = 1
        except StopIteration:
            continue
    
    sorted_freqdic = {k: v for k, v in sorted(freqdic.items(), key=lambda item: item[1], reverse=True)}

    with open('colloc_verb_plus_prep.txt', 'w') as f:
        for key, value in sorted_freqdic.items():
            if value > 100:
                print(key,value)
                f.write(str(key)+'\t'+str(value)+'\n')
                

def adjective_plus_noun(words):                    
    # Get an ajdevtive - noun pair
    freqdic = {}
    for word in words:
        try:
            if "lken" in word.pos:
                adjective = word.lemma
                word2 = next(words)
                if "nken" in word2.pos:
                    noun_ = word2.lemma
                    colloc = (adjective, noun_)
                    if colloc in freqdic:
                        freqdic[colloc]+=1
                    else:
                        freqdic[colloc] = 1
        except StopIteration:
            continue

    sorted_freqdic = {k: v for k, v in sorted(freqdic.items(), key=lambda item: item[1], reverse=True)}

    with open('colloc_adj_plus_noun.txt', 'w') as f:
        for key, value in sorted_freqdic.items():
            if value > 100:
                print(key,value)
                f.write(str(key)+'\t'+str(value)+'\n')

def verb_pronoun_noun(words):
    # Get a verb, personal pronoun, noun triplet
    freqdic = {}
    for word in words:
        try:
            if word.pos.startswith('s'):
                verb = word.lemma
                word2 = next(words)
                if word2.pos.startswith('fp'):
                    pron = word2.word_form
                    word3 = next(words)
                    if word3.pos.startswith('n'):
                        noun = word3.word_form
                        colloc = (verb, pron, noun)
                        if colloc in freqdic:
                            freqdic[colloc]+=1
                        else:
                            freqdic[colloc] = 1
        except StopIteration:
            continue
    
    sorted_freqdic = {k: v for k, v in sorted(freqdic.items(), key=lambda item: item[1], reverse=True)}

    with open('colloc_verb_pron_noun.txt', 'w') as f:
        for key, value in sorted_freqdic.items():
            if value > 100:
                print(key,value)
                f.write(str(key)+'\t'+str(value)+'\n')

def verb_adjective_noun(words):
    # Get a verb, adjective, noun triplet
    freqdic = {}
    for word in words:
        try:
            if word.pos.startswith('s'):
                verb = word.lemma
                word2 = next(words)
                if word2.pos.startswith('l'):
                    adjective = word2.word_form
                    word3 = next(words)
                    if word3.pos.startswith('n'):
                        noun = word3.word_form
                        colloc = (verb, adjective, noun)
                        if colloc in freqdic:
                            freqdic[colloc]+=1
                        else:
                            freqdic[colloc] = 1
        except StopIteration:
            continue
    
    sorted_freqdic = {k: v for k, v in sorted(freqdic.items(), key=lambda item: item[1], reverse=True)}

    with open('colloc_verb_adjective_noun.txt', 'w') as f:
        for key, value in sorted_freqdic.items():
            if value > 100:
                print(key,value)
                f.write(str(key)+'\t'+str(value)+'\n')

def noun_prep_noun(words):
    # Get a noun, preposition, noun triplet
    freqdic = {}
    for word in words:
        try:
            if word.pos.startswith('n'):
                noun = word.lemma
                bug_words = ["klukka", "tími", "króna"]
                if noun not in bug_words:
                    word2 = next(words)
                if word2.pos.startswith('a'):
                    prep = word2.word_form
                    word3 = next(words)
                    if word3.pos.startswith('n'):
                        noun2 = word3.word_form
                        colloc = (noun, prep, noun2)
                        if colloc in freqdic:
                            freqdic[colloc]+=1
                        else:
                            freqdic[colloc] = 1
        except StopIteration:
            continue
    
    sorted_freqdic = {k: v for k, v in sorted(freqdic.items(), key=lambda item: item[1], reverse=True)}

    with open('colloc_noun_prep_noun.txt', 'w') as f:
        for key, value in sorted_freqdic.items():
            if value > 300:
                print(key,value)
                f.write(str(key)+'\t'+str(value)+'\n')

def genetive_noun(words):
    # Get a genetive noun and noun pair
    freqdic = {}
    for word in words:
        try:
            if word.pos.startswith('n'):
                if word.pos[3] == "e":
                    genetive = word.word_form
                    word2 = next(words)
                    if word2.pos.startswith('n'):
                        noun = word2.word_form
                        colloc = (genetive, noun)
                        if colloc in freqdic:
                            freqdic[colloc]+=1
                        else:
                            freqdic[colloc] = 1
        except StopIteration:
            continue
    
    sorted_freqdic = {k: v for k, v in sorted(freqdic.items(), key=lambda item: item[1], reverse=True)}

    with open('colloc_genetive_noun.txt', 'w') as f:
        for key, value in sorted_freqdic.items():
            if value > 100:
                print(key,value)
                f.write(str(key)+'\t'+str(value)+'\n')

def verb_noun_prep_noun(words):
    # Get a verb, noun, preposition, noun quadruplet 
    freqdic = {}
    for word in words:
        try:
            if word.pos.startswith('s'):
                verb = word.lemma
                word2 = next(words)
                if word2.pos.startswith('n'):
                    noun = word2.word_form
                    word3 = next(words)
                    if word3.pos.startswith('a'):
                        prop = word3.word_form
                        word4 = next(words)
                        if word4.pos.startswith('n'):
                            noun2 = word4.word_form
                            colloc = (verb, noun, prop, noun2)
                            if colloc in freqdic:
                                freqdic[colloc]+=1
                            else:
                                freqdic[colloc] = 1
        except StopIteration:
            continue
    
    sorted_freqdic = {k: v for k, v in sorted(freqdic.items(), key=lambda item: item[1], reverse=True)}

    with open('colloc_verb_noun_prep_noun.txt', 'w') as f:
        for key, value in sorted_freqdic.items():
            if value > 100:
                print(key,value)
                f.write(str(key)+'\t'+str(value)+'\n')


# uncomment the function you want to run

#verb_plus_prep(words)
#adjective_plus_noun(words)
verb_pronoun_noun(words)
#verb_adjective_noun(words)
#noun_prep_noun(words)
#genetive_noun(words)
#verb_noun_prep_noun(words)