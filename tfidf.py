# -*- coding: latin-1 -*-

en_stopwords = ['a','about','above','across','after','afterwards','again','against','all',
                'almost','alone','along','already','also','although','always','am','among',
                'amongst','amoungst','amount','an','and','another','any','anyhow','anyone',
                'anything','anyway','anywhere','are','around','as','at','back','be','became',
                'because','become','becomes','becoming','been','before','beforehand','behind',
                'being','below','beside','besides','between','beyond','bill','both','bottom',
                'but','by','call','can','cannot','cant','co','computer','con','could','couldnt',
                'cry','de','describe','detail','do','done','down','due','during','each','eg',
                'eight','either','eleven','else','elsewhere','empty','enough','etc','even',
                'ever','every','everyone','everything','everywhere','except','few','fifteen',
                'fify','fill','find','fire','first','five','for','former','formerly','forty',
                'found','four','from','front','full','further','get','give','go','had','has',
                'hasnt','have','he','hence','her','here','hereafter','hereby','herein',
                'hereupon','hers','him','his','how','however','hundred','i','ie','if','in',
                'inc','indeed','interest','into','is','it','its','keep','last','latter',
                'latterly','least','less','ltd','made','many','may','me','meanwhile','might',
                'mill','mine','more','moreover','most','mostly','move','much','must','my',
                'name','namely','neither','never','nevertheless','next','nine','no','nobody',
                'none','noone','nor','not','nothing','now','nowhere','of','off','often','on',
                'once','one','only','onto','or','other','others','otherwise','our','ours',
                'ourselves','out','over','own','part','per','perhaps','please','put','rather',
                're','same','see','seem','seemed','seeming','seems','serious','several','she',
                'should','show','side','since','sincere','six','sixty','so','some','somehow',
                'someone','something','sometime','sometimes','somewhere','still','such',
                'system','take','ten','than','that','the','their','them','themselves','then',
                'thence','there','thereafter','thereby','therefore','therein','thereupon',
                'these','they','thick','thin','third','this','those','though','three','through',
                'throughout','thru','thus','to','together','too','top','toward','towards',
                'twelve','twenty','two','un','under','until','up','upon','us','very','via',
                'was','we','well','were','what','whatever','when','whence','whenever','where',
                'whereafter','whereas','whereby','wherein','whereupon','wherever','whether',
                'which','while','whither','who','whoever','whole','whom','whose','why','will',
                'with','within','without','would','yet','you','your','yours','yourself','yourselves'
]


pt_stopwords = ['a','à','acordo','agora','ainda','além','algumas','alguns','altura','ano','anos',
                'antes','antónio','ao','aos','apenas','apesar','apoio','após','aqui','área','as',
                'às','assim','associação','até','através','banco','bem','cada','câmara','capital',
                'carlos','casa','caso','causa','cento','centro','cerca','cidade','cinco','com',
                'comissão','como','conselho','conta','contos','contra','cultura','da','dar','das',
                'de','decisão','depois','desde','desta','deste','dia','dias','direcção','disse','diz',
                'dizer','do','dois','dos','duas','durante','e','é','economia','ele','eleições','eles',
                'em','embora','empresa','empresas','enquanto','entanto','então','entre','equipa',
                'era','essa','esse','esta','está','estado','estados','estão','estar','estava','este',
                'estes','eu','europa','europeia','exemplo','facto','falta','faz','fazer','fernando',
                'fez','fim','final','foi','fora','foram','forma','frente','geral','governo','grande',
                'grandes','grupo','guerra','há','história','hoje','homem','início','internacional',
                'isso','isto','já','joão','jogo','jorge','josé','lá','lado','lei','lhe','lisboa',
                'local','lugar','maior','maioria','mais','manuel','mas','me','meio','melhor','menos',
                'mercado','mês','meses','mesma','mesmo','mil','milhões','ministério','ministro',
                'momento','muito','muitos','mundo','música','na','nacional','nada','não','nas','nem',
                'neste','no','noite','nome','nos','nova','novo','num','numa','número','nunca','o',
                'obras','onde','ontem','os','ou','outra','outras','outro','outros','p.','país','países',
                'para','parece','parte','partido','partir','passado','pela','pelas','pelo','pelos',
                'pessoas','pode','poder','poderá','polícia','política','pontos','por','porque','porto',
                'portugal','português','portuguesa','portugueses','possível','pouco','presidente',
                'primeira','primeiro','problema','problemas','processo','programa','projecto','próprio',
                'próximo','ps','psd','público','quais','qual','qualquer','quando','quanto','quase',
                'quatro','que','quem','quer','questão','r.','região','relação','república','são','se',
                'segunda','segundo','segurança','seis','seja','sem','semana','sempre','sentido','ser',
                'será','seu','seus','sido','silva','sistema','situação','só','sobre','social','sociedade',
                'sua','suas','tal','também','tão','tarde','tem','têm','tempo','ter','terá','teve',
                'tinha','toda','todas','todo','todos','trabalho','três','tudo','último','últimos','um',
                'uma','vai','vão','ver','vez','vezes','vida','zona'
]


def delete_stopwords(doc):
    # Split sentences in a list
    split_doc = doc.split()
    words_list = []

    # Sets because its faster
    set_en = set(en_stopwords)
    set_pt = set(pt_stopwords)

    # Filter the list of words
    en_filter = [word for word in set(split_doc) if word not in set_en]
    pt_filter = [word for word in en_filter if word not in set_pt]
    
    # For each word append to 
    for word in pt_filter:
        print word

    #return ' '.join(words_list)


# Number of times term word appears in a document 
def freq(word, doc):
    split_doc = doc.split()
    return split_doc.count(word)
 

# Total number of terms in the document
def word_count(doc):
    split_doc = doc.split()
    return len(split_doc)
 

# How frequently a term occurs in a document
def tf(word, doc):
    return (freq(word, doc) / float(word_count(doc)))
 

# Number of documents with term t in it
def num_docs_containing(word, list_of_docs):
    count = 0
    for document in list_of_docs:
        if freq(word, document) > 0:
            count += 1
    return 1 + count
 

# How important a term is
def idf(word, list_of_docs):
    return math.log(len(list_of_docs) / 
                    float(num_docs_containing(word, list_of_docs)))
 

# Tf-idf weight
def tf_idf(word, doc, list_of_docs):
    return (tf(word, doc) * idf(word, list_of_docs))


# Compute the frequency for each term.
def compute_tfidf(list_of_docs):
    
    list_of_docs = []
    word_counters = {}
    all_tips = []

    for tip in (venue.tips()):
        
        docs[tip.text] = {'freq': {}, 'tf': {}, 'idf': {},
                            'tf-idf': {}, 'tokens': []}
     
        for token in final_tokens:
            #The frequency computed for each tip
            docs[tip.text]['freq'][token] = freq(token, final_tokens)
            #The term-frequency (Normalized Frequency)
            docs[tip.text]['tf'][token] = tf(token, final_tokens)
            docs[tip.text]['tokens'] = final_tokens
     
        vocabulary.append(final_tokens)
     
    for doc in docs:
        for token in docs[doc]['tf']:
            #The Inverse-Document-Frequency
            docs[doc]['idf'][token] = idf(token, vocabulary)
            #The tf-idf
            docs[doc]['tf-idf'][token] = tf_idf(token, docs[doc]['tokens'], vocabulary)
     
    #Now let's find out the most relevant words by tf-idf.
    words = {}
    for doc in docs:
        for token in docs[doc]['tf-idf']:
            if token not in words:
                words[token] = docs[doc]['tf-idf'][token]
            else:
                if docs[doc]['tf-idf'][token] > words[token]:
                    words[token] = docs[doc]['tf-idf'][token]
     
    for item in sorted(words.items(), key=lambda x: x[1], reverse=True):
        print "%f <= %s" % (item[1], item[0])