from nltk import NaiveBayesClassifier, FreqDist, apply_features
from nltk.corpus import movie_reviews

POSITIVE = "positive"
NEGATIVE = "negative"
NEUTRAL = "neutral"

pos_tweets = [
        ('I love this car', POSITIVE),
        ('This view is amazing', POSITIVE),
        ('I feel great this morning', POSITIVE),
        ('I am so excited about the concert', POSITIVE),
        ('He is my best friend', POSITIVE),
        ("I love this sandwich.", POSITIVE),
        ("This is an amazing place!", POSITIVE),
        ("I feel very good about these beers.", POSITIVE),
        ("This is my best work.", POSITIVE),
        ("What an awesome view", POSITIVE),
        ("I am happy today.", POSITIVE),
        ("I loved the ending of that movie!", POSITIVE),
        ("I had a great time hanging out with you and your friends.", POSITIVE),
        ("The trip to the beach was so much fun!", POSITIVE),
    ]

neg_tweets = [
        ('I do not like this car', NEGATIVE),
        ('This view is horrible', NEGATIVE),
        ('I feel tired this morning', NEGATIVE),
        ('I am not looking forward to the concert', NEGATIVE),
        ('He is my enemy', NEGATIVE),
        ("I do not like this restaurant.", NEGATIVE),
        ("I am tired of this stuff.", NEGATIVE),
        ("I can't deal with this crap right now.", NEGATIVE),
        ("He is my sworn enemy!", NEGATIVE),
        ("My boss is horrible and yells all the time.", NEGATIVE),
        ("I hate it when they get my order wrong.", NEGATIVE),
        ("It makes me angry when I am alone and you are out with your friends.", NEGATIVE),
        ("I can't stand how boring this movie is.", NEGATIVE),
        ("This risotto is disgusting.", NEGATIVE),
    ]

neu_tweets = [
        ("The average airspeed velocity of an unladen swallow is eleven meters per second.", NEUTRAL),
        ("Darkness is merely the absence of light.", NEUTRAL),
        ("Inverse kinematics transforms the motion plan into joint actuator trajectories for the robot.", NEUTRAL),
        ("Robots have replaced humans in the assistance of performing repetitive and dangerous tasks.", NEUTRAL),
        ("The Irish Sea lies northwest of England and the Celtic Sea lies to the southwest.", NEUTRAL),
        ("The province has proved rich in prehistoric antiquities that date from the 4th and 5th centuries.", NEUTRAL),
        ("Joseph Smith, founder of the Latter Day Saint movement, originally prayed about which church to join.", NEUTRAL),
        ("Scrying is not supported by mainstream science as a method of predicting the future. ", NEUTRAL),
        ("In traditional belief and fiction, a ghost is a manifestation of the spirit or soul of a person.", NEUTRAL),
        ("Tucana is a constellation of stars in the southern sky, named after the toucan, a South American bird.", NEUTRAL),
        ("It is one of twelve constellations conceived in the late sixteenth century by Petrus Plancius", NEUTRAL),
        ("It first appeared on a 1598 celestial globe by Plancius and Jodocus Hondius in Amsterdam.", NEUTRAL),
        ("It was depicted in Johann Bayer's star atlas Uranometria of 1603.", NEUTRAL),
        ("French explorer and astronomer Nicolas Louis de Lacaille gave its stars Bayer designations in 1756.", NEUTRAL),
        ("Tucana is not a prominent constellation, for all of its stars are a third of it's magnitude", NEUTRAL),
        ("The brightest is Alpha Tucanae with an apparent visual magnitude of 2.87.", NEUTRAL),
        ("Beta Tucanae is a star system with six member stars, while Kappa is a quadruple system.", NEUTRAL),
        ("Five star systems have been found to have exoplanets to date.", NEUTRAL),
        ("An exoplanet or extrasolar planet is a planet that orbits a star other than the Sun", NEUTRAL),
        ("The Kepler space telescope has also detected a few thousand candidate planets", NEUTRAL),
        ("Kepler is a space observatory launched by NASA to discover Earth-like planets orbiting other stars.", NEUTRAL),
        ("The spacecraft, named after the Renaissance astronomer Johannes Kepler, was launched on March 7, 2009.", NEUTRAL),
        ("Kepler is part of NASA's Discovery Program of relatively low-cost, focused primary science missions.", NEUTRAL),
        ("The telescope's construction and initial operation were managed by NASA's Jet Propulsion Laboratory.", NEUTRAL),
        ("The Jet Propulsion Laboratory (JPL) is a federally funded research and development center.", NEUTRAL),
        ("The JPL is managed by the nearby California Institute of Technology (Caltech)", NEUTRAL),
        ("The laboratory's primary function is the construction and operation of robotic planetary spacecraft.", NEUTRAL),
        ("It also conducts Earth-orbit and astronomy missions.", NEUTRAL),
        ("It is also responsible for operating NASA's Deep Space Network.", NEUTRAL),
        ("The rover carries a variety of scientific instruments designed by an international team.", NEUTRAL),
    ]

reviews = [
    (list(movie_reviews.words(fileid)), category)
    for category in movie_reviews.categories()
    for fileid in movie_reviews.fileids(category)
]

new_train, new_test = reviews[0:100], reviews[101:200]



tweets = []

#tweets += new_test + new_train

for (words, sentiment) in pos_tweets + neg_tweets + neu_tweets:
    words_filtered = [e.lower() for e in words.split() if len(e) >= 3] 
    tweets.append((words_filtered, sentiment))

def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
      all_words.extend(words)
    return all_words

def get_word_features(wordlist):
    wordlist = FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features

word_features = get_word_features(get_words_in_tweets(tweets))

def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

training_set = apply_features(extract_features, tweets)

classifier = NaiveBayesClassifier.train(training_set)

tweet = 'This is an example of the african grey turtle'
print classifier.classify(extract_features(tweet.split()))

prob_dist = classifier.prob_classify(extract_features(tweet.split()))

print "MAX", prob_dist.max()
print POSITIVE, prob_dist.prob(POSITIVE)
print NEGATIVE, prob_dist.prob(NEGATIVE)
print NEUTRAL, prob_dist.prob(NEUTRAL)

print classifier.show_most_informative_features(6)
