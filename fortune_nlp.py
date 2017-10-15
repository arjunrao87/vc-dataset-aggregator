from rake_nltk import Rake

r = Rake(["the", "and", "by","in", "raised", "was", "other", "joined", "round", "-", "based","has","fortune", "read", "more", "from", "an"], [","]) # Uses stopwords for english from NLTK, and all puntuation characters.

# http://textminingonline.com/getting-started-with-keyword-extraction
# http://www.nltk.org/book/ch07.html
# https://github.com/csurfer/rake-nltk
def processSentence( sentence ):
    r.extract_keywords_from_text(sentence)
    extract = r.get_ranked_phrases()
    print ( extract )
