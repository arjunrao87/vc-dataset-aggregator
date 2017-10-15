from rake_nltk import Rake
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize

# Rake setup
fortune_stopwords = ["the", "and", "by","in", "raised", "was", "other", "joined", "round", "-", "based","has","fortune", "read", "more", "from", "an"]
r = Rake( fortune_stopwords, [","] ) # Uses stopwords for english from NLTK, and all puntuation characters.

# Stanford NER setup
st = StanfordNERTagger('./resources/english.all.3class.distsim.crf.ser.gz','./resources/stanford-ner.jar',encoding='utf-8')

# http://textminingonline.com/getting-started-with-keyword-extraction
# http://www.nltk.org/book/ch07.html
# https://github.com/csurfer/rake-nltk
def processSentence( sentence ):
    print ( sentence )
    r.extract_keywords_from_text(sentence)
    extract = r.get_ranked_phrases()
    company = sentence.split( ",")[0]
    categorize( company, extract )
    entityRecognition( sentence )

def categorize( company, phrases ):
    company_description = None
    lead_venture_firms = []
    venture_firms = []
    funding_round = None
    funding_amount = []

    for phrase in phrases :
        if( company in phrase or company == phrase ):
            continue
        if( "$" in phrase or "million" in phrase ):
            funding_amount.append( phrase )
        if( "series" in phrase or "funding" in phrase ):
            funding_round = phrase

def entityRecognition( text ):
    tokenized_text = word_tokenize(text)
    classified_text = st.tag(tokenized_text)
    print ( classified_text )
