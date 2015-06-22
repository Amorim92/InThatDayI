# -*- coding: latin-1 -*-

import re
import math

en_stopwords = [u'a',u'about',u'above',u'across',u'after',u'afterwards',u'again',u'against',u'all',
                u'almost',u'alone',u'along',u'already',u'also',u'although',u'always',u'am',u'among',
                u'amongst',u'amoungst',u'amount',u'an',u'and',u'another',u'any',u'anyhow',u'anyone',
                u'anything',u'anyway',u'anywhere',u'are',u'around',u'as',u'at',u'back',u'be',u'became',
                u'because',u'become',u'becomes',u'becoming',u'been',u'before',u'beforehand',u'behind',
                u'being',u'below',u'beside',u'besides',u'between',u'beyond',u'bill',u'both',u'bottom',
                u'but',u'by',u'call',u'can',u'cannot',u'cant',u'co',u'computer',u'con',u'could',u'couldnt',
                u'cry',u'de',u'describe',u'detail',u'do',u'done',u'down',u'due',u'during',u'each',u'eg',
                u'eight',u'either',u'eleven',u'else',u'elsewhere',u'empty',u'enough',u'etc',u'even',
                u'ever',u'every',u'everyone',u'everything',u'everywhere',u'except',u'few',u'fifteen',
                u'fify',u'fill',u'find',u'fire',u'first',u'five',u'for',u'former',u'formerly',u'forty',
                u'found',u'four',u'from',u'front',u'full',u'further',u'get',u'give',u'go',u'had',u'has',
                u'hasnt',u'have',u'he',u'hence',u'her',u'here',u'hereafter',u'hereby',u'herein',
                u'hereupon',u'hers',u'him',u'his',u'how',u'however',u'hundred',u'i',u'ie',u'if',u'in',
                u'inc',u'indeed',u'interest',u'into',u'is',u'it',u'its',u'keep',u'last',u'latter',
                u'latterly',u'least',u'less',u'ltd',u'made',u'many',u'may',u'me',u'meanwhile',u'might',
                u'mill',u'mine',u'more',u'moreover',u'most',u'mostly',u'move',u'much',u'must',u'my',
                u'name',u'namely',u'neither',u'never',u'nevertheless',u'next',u'nine',u'no',u'nobody',
                u'none',u'noone',u'nor',u'not',u'nothing',u'now',u'nowhere',u'of',u'off',u'often',u'on',
                u'once',u'one',u'only',u'onto',u'or',u'other',u'others',u'otherwise',u'our',u'ours',
                u'ourselves',u'out',u'over',u'own',u'part',u'per',u'perhaps',u'please',u'put',u'rather',
                u're',u'same',u'see',u'seem',u'seemed',u'seeming',u'seems',u'serious',u'several',u'she',
                u'should',u'show',u'side',u'since',u'sincere',u'six',u'sixty',u'so',u'some',u'somehow',
                u'someone',u'something',u'sometime',u'sometimes',u'somewhere',u'still',u'such',
                u'system',u'take',u'ten',u'than',u'that',u'the',u'their',u'them',u'themselves',u'then',
                u'thence',u'there',u'thereafter',u'thereby',u'therefore',u'therein',u'thereupon',
                u'these',u'they',u'thick',u'thin',u'third',u'this',u'those',u'though',u'three',u'through',
                u'throughout',u'thru',u'thus',u'to',u'together',u'too',u'top',u'toward',u'towards',
                u'twelve',u'twenty',u'two',u'un',u'under',u'until',u'up',u'upon',u'us',u'very',u'via',
                u'was',u'we',u'well',u'were',u'what',u'whatever',u'when',u'whence',u'whenever',u'where',
                u'whereafter',u'whereas',u'whereby',u'wherein',u'whereupon',u'wherever',u'whether',
                u'which',u'while',u'whither',u'who',u'whoever',u'whole',u'whom',u'whose',u'why',u'will',
                u'with',u'within',u'without',u'would',u'yet',u'you',u'your',u'yours',u'yourself',u'yourselves'
]


pt_stopwords = [u'a',u'\xe0',u'acordo',u'agora',u'ainda',u'al\xe9m',u'algumas',u'alguns',u'altura',
                u'ano',u'anos',u'antes',u'ant\xf3nio',u'ao',u'aos',u'apenas',u'apesar',u'apoio',u'ap\xf3s',
                u'aqui',u'\xe1rea',u'as',u'\xe0s',u'assim',u'associa\xe7\xe3o',u'at\xe9',u'atrav\xe9s',
                u'banco',u'bem',u'cada',u'c\xe2mara',u'capital',u'carlos',u'casa',u'caso',u'causa',u'cento',
                u'centro',u'cerca',u'cidade',u'cinco',u'com',u'comiss\xe3o',u'como',u'conselho',u'conta',
                u'contos',u'contra',u'cultura',u'da',u'dar',u'das',u'de',u'decis\xe3o',u'depois',u'desde',
                u'desta',u'deste',u'dia',u'dias',u'direc\xe7\xe3o',u'disse',u'diz',u'dizer',u'do',u'dois',
                u'dos',u'duas',u'durante',u'e',u'\xe9',u'economia',u'ele',u'elei\xe7\xf5es',u'eles',u'em',
                u'embora',u'empresa',u'empresas',u'enquanto',u'entanto',u'ent\xe3o',u'entre',u'equipa',
                u'era',u'essa',u'esse',u'esta',u'est\xe1',u'estado',u'estados',u'est\xe3o',u'estar',u'estava',
                u'este',u'estes',u'eu',u'europa',u'europeia',u'exemplo',u'facto',u'falta',u'faz',u'fazer',
                u'fernando',u'fez',u'fim',u'final',u'foi',u'fora',u'foram',u'forma',u'frente',u'geral',
                u'governo',u'grande',u'grandes',u'grupo',u'guerra',u'h\xe1',u'hist\xf3ria',u'hoje',u'homem',
                u'in\xedcio',u'internacional',u'isso',u'isto',u'j\xe1',u'jo\xe3o',u'jogo',u'jorge',u'jos\xe9',
                u'l\xe1',u'lado',u'lei',u'lhe',u'lisboa',u'local',u'lugar',u'maior',u'maioria',u'mais',
                u'manuel',u'mas',u'me',u'meio',u'melhor',u'menos',u'mercado',u'm\xeas',u'meses',u'mesma',
                u'mesmo',u'mil',u'milh\xf5es',u'minist\xe9rio',u'ministro',u'momento',u'muito',u'muitos',
                u'mundo',u'm\xfasica',u'na',u'nacional',u'nada',u'n\xe3o',u'nas',u'nem',u'neste',u'no',
                u'noite',u'nome',u'nos',u'nova',u'novo',u'num',u'numa',u'n\xfamero',u'nunca',u'o',u'obras',
                u'onde',u'ontem',u'os',u'ou',u'outra',u'outras',u'outro',u'outros',u'pa\xeds',u'pa\xedses',
                u'para',u'parece',u'parte',u'partido',u'partir',u'passado',u'pela',u'pelas',u'pelo',u'pelos',
                u'pessoas',u'pode',u'poder',u'poder\xe1',u'pol\xedcia',u'pol\xedtica',u'pontos',u'por',
                u'porque',u'porto',u'portugal',u'portugu\xeas',u'portuguesa',u'portugueses',u'poss\xedvel',
                u'pouco',u'presidente',u'primeira',u'primeiro',u'problema',u'problemas',u'processo',
                u'programa',u'projecto',u'pr\xf3prio',u'pr\xf3ximo',u'p\xfablico',u'quais',u'qual',u'qualquer',
                u'quando',u'quanto',u'quase',u'quatro',u'que',u'quem',u'quer',u'quest\xe3o',u'regi\xe3o',
                u'rela\xe7\xe3o',u'rep\xfablica',u's\xe3o',u'se',u'segunda',u'segundo',u'seguran\xe7a',
                u'seis',u'seja',u'sem',u'semana',u'sempre',u'sentido',u'ser',u'ser\xe1',u'seu',u'seus',u'sido',
                u'silva',u'sistema',u'situa\xe7\xe3o',u's\xf3',u'sobre',u'social',u'sociedade',u'sua',u'suas',
                u'tal',u'tamb\xe9m',u't\xe3o',u'tarde',u'tem',u't\xeam',u'tempo',u'ter',u'ter\xe1',u'teve',
                u'tinha',u'toda',u'todas',u'todo',u'todos',u'trabalho',u'tr\xeas',u'tudo',u'\xfaltimo',
                u'\xfaltimos',u'um',u'uma',u'vai',u'v\xe3o',u'ver',u'vez',u'vezes',u'vida',u'zona',u''
]


def delete_stopwords(doc):

    # Sets because its faster
    set_en = set(en_stopwords)
    set_pt = set(pt_stopwords)

    # Filter the list of words
    en_filter = [word for word in set(doc) if word not in set_en]
    pt_filter = [word for word in en_filter if word not in set_pt]

    return pt_filter


# Number of times term word appears in a document 
def freq(word, doc):
    return doc.count(word)
 

# Total number of terms in the document
def word_count(doc):
    return len(doc)
 

# How frequently a term occurs in a document
def tf(word, doc):
    return (freq(word, doc) / float(word_count(doc)))
 

# Number of documents with term t in it ERRO AQUI
def num_docs_containing(word, list_of_docs):
    count = 0
    for doc in list_of_docs:
        if freq(word, doc) > 0:
            count += 1
    return 1 + count
 

# How important a term is
def idf(word, list_of_docs):
    return math.log(len(list_of_docs) / 
                    float(num_docs_containing(word, list_of_docs)))
 

# TF-IDF weight
def tf_idf(word, doc, list_of_docs):
    return tf(word, doc), idf(word, list_of_docs), (tf(word, doc) * idf(word, list_of_docs)) 


# Compute the frequency for each term.
def compute_tfidf(list_of_docs, source, ids, creators, dates, status = [], start = [], end = []):
    # print list_of_docs
    
    # List of filtered words
    list_filter = []
    # TF-IDF dictionary
    tfidf_dict = {}


    # Filter words in documents
    for doc in list_of_docs:
        doc = doc.decode('utf8')
        doc_words = re.split('\W+', doc, flags = re.UNICODE)
        # print doc_words
        # List of documents with filtered words
        list_filter.append(delete_stopwords(doc_words))


    for doc_filter, length in zip(list_filter, range(len(list_filter))):
        
        if ids:
            id = ids[length]
        if creators:
            creator = creators[length]
        if dates:
            date = dates[length]
        if status:
            e_status = status[length]
        if start:
            e_start = start[length]
        if end:
            e_end = end[length]

        for word in doc_filter:
            # print word
            term_freq, term_imp, tfidf = tf_idf(word, doc_filter, list_filter)
            
            # List and set of related terms
            related_terms = [filter_word for filter_word in doc_filter if filter_word != word]
            set_related_terms = set(related_terms)

            # Dictionary of words and TF-IDF related to their sources
            if source == 'Google Calendar':
                if tfidf_dict.has_key(word.encode('utf8')):
                    tfidf_dict[word.encode('utf8')]['Id'].append(id)
                    tfidf_dict[word.encode('utf8')]['Status'].append(e_status)
                    tfidf_dict[word.encode('utf8')]['Creator'].append(creator)
                    tfidf_dict[word.encode('utf8')]['Date'].append(date)
                    tfidf_dict[word.encode('utf8')]['Start'].append(e_start)
                    tfidf_dict[word.encode('utf8')]['End'].append(e_end)
                    tfidf_dict[word.encode('utf8')]['TF-IDF'] = (tfidf_dict[word.encode('utf8')]['TF-IDF'] + tfidf) / 2
                    tfidf_dict[word.encode('utf8')]['Importance'] = (tfidf_dict[word.encode('utf8')]['Importance'] + term_imp) / 2
                    tfidf_dict[word.encode('utf8')]['Frequency'] = (tfidf_dict[word.encode('utf8')]['Frequency'] + term_freq) / 2
                    tfidf_dict[word.encode('utf8')]['Related Terms'] = list(set(tfidf_dict[word.encode('utf8')]['Related Terms'] + list(set_related_terms)))
                else:
                    tfidf_dict[word.encode('utf8')] = {'Source': source, 'Id': [id], 'Status': [e_status], 'Creator': [creator],
                                                       'Date': [date], 'Start': [e_start], 'End': [e_end], 'TF-IDF': tfidf,
                                                       'Importance': term_imp, 'Frequency': term_freq, 'Related Terms': list(set_related_terms)}
            if source == 'Google Drive':
                if tfidf_dict.has_key(word.encode('utf8')):
                    tfidf_dict[word.encode('utf8')]['Id'].append(id)
                    tfidf_dict[word.encode('utf8')]['Creator'].append(creator)
                    tfidf_dict[word.encode('utf8')]['Date'].append(date)
                    tfidf_dict[word.encode('utf8')]['TF-IDF'] = (tfidf_dict[word.encode('utf8')]['TF-IDF'] + tfidf) / 2
                    tfidf_dict[word.encode('utf8')]['Importance'] = (tfidf_dict[word.encode('utf8')]['Importance'] + term_imp) / 2
                    tfidf_dict[word.encode('utf8')]['Frequency'] = (tfidf_dict[word.encode('utf8')]['Frequency'] + term_freq) / 2
                    tfidf_dict[word.encode('utf8')]['Related Terms'] = list(set(tfidf_dict[word.encode('utf8')]['Related Terms'] + list(set_related_terms)))
                else:
                    tfidf_dict[word.encode('utf8')] = {'Source': source, 'Id': [id], 'Creator': [creator], 'Date': [date], 'TF-IDF': tfidf,
                                                       'Importance': term_imp, 'Frequency': term_freq, 'Related Terms': list(set_related_terms)}

            # if source == 'Google Drive':
            #     if tfidf_dict.has_key(word.encode('utf8')):
            #         tfidf_dict[word.encode('utf8')]['Id'].append(id)
            #         tfidf_dict[word.encode('utf8')]['Creator'].append(creator)
            #         tfidf_dict[word.encode('utf8')]['Date'].append(date)
            #         tfidf_dict[word.encode('utf8')]['TF-IDF'] = (tfidf_dict[word.encode('utf8')]['TF-IDF'] + tfidf) / 2
            #         tfidf_dict[word.encode('utf8')]['Importance'] = (tfidf_dict[word.encode('utf8')]['Importance'] + term_imp) / 2
            #         tfidf_dict[word.encode('utf8')]['Frequency'] = (tfidf_dict[word.encode('utf8')]['Frequency'] + term_freq) / 2
            #         tfidf_dict[word.encode('utf8')]['Related Terms'] = list(set(tfidf_dict[word.encode('utf8')]['Related Terms'] + list(set_related_terms)))
            #     else:
            #         tfidf_dict[word.encode('utf8')] = {'Source': source, 'Id': [id], 'Creator': [creator], 'Date': [date], 'TF-IDF': tfidf,
            #                                            'Importance': term_imp, 'Frequency': term_freq, 'Related Terms': list(set_related_terms)}

    # print tfidf_dict
    return tfidf_dict