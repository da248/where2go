# www.where2go.help

Having trouble figuring out where to go for summer vacation? Have some places you like and want to figure out similar places? Where2go was built to recommend you places2go based on places/characterstics you like or dislike. 

####Go try it out on <www.where2go.help>

## Motivation
There are a lot of websites that tell you the cheapest ways to get to a destinations and the cheapest hotels to stay at. But why don't they tell us where we should go based on our travel taste? The articles like "XX's Top 25 Travel Destinations" or "YY's 100 Places You Must Visit!" tell you about interesting places around the world but I wanted to build a tool that will tell me where I should go based on my own experience and taste.

##Methodology
One of the motivations for this applicaiton was that I wanted to build an unbiased recommendation system that will consider the destination's characterstics instead of looking at destinations that others liked. To do this, I decided to use travel guide data to gather destination information. I found that Wikivoyage provided great travel guides that tell you about the history and culture of the place as well as what to see, how to get around, etc. 

The next question was then to figure out which model to use. The traditional recommendation systems for natural language processing include models like TF-IDF + cos-similarity and TF-IDF + SVD + k-means clustering. These models may do a great job of finding similar destinations but I also wanted to use a model that lets me add place characterstics in my search. So I decided to go with a recent model created at Google called word2vec. Word2vec is an amazing model that turns words into vectors that capture the 'meaning' of words. The cool feature about this model is that you can add/subtract words because they are vectors. For example, you can do something like 'king' - 'man' + 'woman' ~= 'queen'. 



There are two versions of word2vec, one model utilizes continuous bag of words that uses surrounding words to train a word, and the other model that utilizes continuous skip-grams to predict surrounding words of a word. 




