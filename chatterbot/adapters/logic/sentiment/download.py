from nltk import download
from nltk.data import path


path.append("./nltk_data/")


x = download("movie_reviews")

print ">>>", x
