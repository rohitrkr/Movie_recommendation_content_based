import numpy as np
import pandas as pd
#importing flask framewoek related libraries
from flask import Flask, render_template, request, redirect
# libraries for making count matrix and similarity matrix
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# define a function that creates similarity matrix
# if it doesn't exist
def create_sim():
    data = pd.read_csv('data.csv')
    # creating a count matrix
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(data['comb'])
    # creating a similarity score matrix
    sim = cosine_similarity(count_matrix)
    return data,sim


# defining a function that recommends 20 most similar movies
def rcmd(m):
    m = m.lower()
    # check if data and sim are already assigned
    try:
        data.head()
        sim.shape
    except:
        data, sim = create_sim()
    # check if the movie is in our database or not
    if m not in data['movie_title'].unique():
        return('This movie is not in our database.\nPlease check if you spelled it correct.')
    else:
        # getting the index of the movie in the dataframe
        i = data.loc[data['movie_title']==m].index[0]

        # fetching the row containing similarity scores of the movie
        # from similarity matrix and enumerate it
        lst = list(enumerate(sim[i]))

        # sorting this list in decreasing order based on the similarity score
        lst = sorted(lst, key = lambda x:x[1] ,reverse=True)

        # taking top 1- movie scores
        # not taking the first index since it is the same movie
        lst = lst[1:21]

        # making an empty list that will containg all 20 movie recommendations
        l = []
        for i in range(len(lst)):
            a = lst[i][0]
            l.append(data['movie_title'][a])
        return l

#Creating instance of flask,initialisation of flask,indicating flask main gateway
#__name == __main__
app = Flask(__name__)

#template decoration(rendering to html pages and their linking)
#its generally routing users to different differnt URLs/Pages
@app.route('/')
def index():
    return render_template('base.html')

@app.route('/about_us')
def  about_us():
    return render_template('aboutus.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route("/result")
def result():
    movie = request.args.get('movie')
    r = rcmd(movie)
    movie = movie.upper()
    if type(r)==type('string'):
        return render_template('result.html',movie=movie,r=r,t='s')
    else:
        return render_template('result.html',movie=movie,r=r,t='l')


#server running,code debugging

if __name__ == '__main__':
    app.run()


