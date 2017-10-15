from rake_nltk import Rake
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize

# Rake setup
# http://textminingonline.com/getting-started-with-keyword-extraction
# http://www.nltk.org/book/ch07.html
# https://github.com/csurfer/rake-nltk
fortune_stopwords = ["the", "and", "by","in", "raised", "was", "other", "joined", "round", "-", "based","has","fortune", "read", "more", "from", "an"]
r = Rake( fortune_stopwords, [","] ) # Uses stopwords for english from NLTK, and all puntuation characters.

# Stanford NER setup
# https://www.quora.com/What-are-the-best-python-libraries-for-extracting-location-from-text
# http://textminingonline.com/how-to-use-stanford-named-entity-recognizer-ner-in-python-nltk-and-other-programming-languages
# https://pythonprogramming.net/named-entity-recognition-stanford-ner-tagger/
# https://nlp.stanford.edu/software/CRF-NER.shtml#Download
st = StanfordNERTagger('./resources/english.all.3class.distsim.crf.ser.gz','./resources/stanford-ner.jar',encoding='utf-8')

def processSentence( sentence ):
    print ( sentence )
    r.extract_keywords_from_text(sentence)
    phrases = r.get_ranked_phrases()
    company = sentence.split( ",")[0]
    funding_round, funding_amount = getFundingDetails( phrases )
    vc_firms, locations = getLocationAndFirms( sentence )
    print ( funding_round, funding_amount, vc_firms, locations )

def getFundingDetails( phrases ):
    funding_round = None
    funding_amount = []
    for phrase in phrases :
        if( "$" in phrase or "million" in phrase ):
            funding_amount.append( phrase )
        if( "series" in phrase or "funding" in phrase ):
            funding_round = phrase
    return funding_round, funding_amount

def getLocationAndFirms( text ):
    text = text.replace( "-based", "")
    tokenized_text = word_tokenize(text)
    classified_text = st.tag(tokenized_text)
    vc_firms = []
    current_vc_firm = []
    locations = []
    current_location = []
    previous_classification = None
    for phrase in classified_text :
        if( phrase[1] == "LOCATION" ):
            current_location.append( phrase[0])
            previous_classification = "LOCATION"
        if ( phrase[1] == "O" and previous_classification == "LOCATION" ):
                previous_classification = None
                current_location_string = " ".join( current_location )
                locations.append(current_location_string)
                current_location = []
        if( phrase[1] == "ORGANIZATION" or phrase[1] == "PERSON" ):
            current_vc_firm.append(phrase[0])
            previous_classification = "ORGANIZATION"
        if ( phrase[1] == "O" and previous_classification == "ORGANIZATION" ):
            if( current_vc_firm ):
                previous_classification = None
                current_vc_firm_string = " ".join( current_vc_firm )
                vc_firms.append(current_vc_firm_string)
                current_vc_firm = []
    if current_vc_firm and current_vc_firm not in vc_firms:
        current_vc_firm_string = " ".join( current_vc_firm )
        vc_firms.append( current_vc_firm_string )
    if current_location and current_location not in locations:
        current_location_string = " ".join( current_location )
        locations.append( current_location_string )
    return vc_firms, locations
