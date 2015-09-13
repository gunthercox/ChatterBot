from nltk.data import path
from textblob.classifiers import NaiveBayesClassifier


path.append("./nltk_data/")

POSITIVE = "positive"
NEGATIVE = "negative"
NEUTRAL = "neutral"

train = [
    ("I love this sandwich.", POSITIVE),
    ("This is an amazing place!", POSITIVE),
    ("I feel very good about these beers.", POSITIVE),
    ("This is my best work.", POSITIVE),
    ("What an awesome view", POSITIVE),
    ("I am happy today.", POSITIVE),
    ("I loved the ending of that movie!", POSITIVE),
    ("I had a great time hanging out with you and your friends.", POSITIVE),
    ("The trip to the beach was so much fun!", POSITIVE),

    ("I do not like this restaurant.", NEGATIVE),
    ("I am tired of this stuff.", NEGATIVE),
    ("I can't deal with this crap right now.", NEGATIVE),
    ("He is my sworn enemy!", NEGATIVE),
    ("My boss is horrible and yells all the time.", NEGATIVE),
    ("I hate it when they get my order wrong.", NEGATIVE),
    ("It makes me angry when I am alone and you are out with your friends.", NEGATIVE),
    ("I can't stand how boring this movie is.", NEGATIVE),
    ("This risotto is disgusting.", NEGATIVE),

    ("The average airspeed velocity of an unladen swallow is eleven meters per second.", NEUTRAL),
    ("Darkness is merely the absence of light.", NEUTRAL),
    ("Inverse kinematics transforms the motion plan into joint actuator trajectories for the robot.", NEUTRAL),
    ("Robots have replaced humans in the assistance of performing repetitive and dangerous tasks.", NEUTRAL),
    ("The Irish Sea lies northwest of England and the Celtic Sea lies to the southwest.", NEUTRAL),
    ("The province of Schleswig has proved rich in prehistoric antiquities that date from the 4th and 5th centuries.", NEUTRAL),
    ("Joseph Smith, founder of the Latter Day Saint movement, originally prayed about which church to join.", NEUTRAL),
    ("Scrying is not supported by mainstream science as a method of predicting the future.", NEUTRAL),
    ("In traditional belief and fiction, a ghost is a manifestation of the spirit or soul of a person.", NEUTRAL),
]

# Analyzer can also be trained with the nltk.corpus movie_reviews

cl = NaiveBayesClassifier(train)

cl.show_informative_features(5)

def sentiment(text):
    prob_dist = cl.prob_classify(text)

    print prob_dist.max(), text
    print POSITIVE, prob_dist.prob(POSITIVE)
    print NEGATIVE, prob_dist.prob(NEGATIVE)
    print NEUTRAL, prob_dist.prob(NEUTRAL)

sentiment("I feel happy this morning.")
sentiment("I hate you so much.")
sentiment("Turtles are in the reptile family.")




from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer, PatternAnalyzer
blob = TextBlob("Would not reccomend it at all.", analyzer=NaiveBayesAnalyzer())
print blob.sentiment
