from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
import seaborn as sns
pd.options.mode.chained_assignment = None

##DataClean##
df = pd.read_csv('movie_metadata.csv')
df = df.applymap(lambda s: s.lower() if type(s) == str else s)

df.isnull().sum()
df['color'].value_counts()
sns.countplot(df['color'])

df['title_year'].fillna(0, inplace=True)
df['title_year'] = df['title_year'].apply(np.int64)

##Movie Sorting##
df2 = df.sort_values('imdb_score', ascending=False)
dataset = df[['director_name', 'actor_2_name', 'genres', 'title_year', 'actor_1_name', 'movie_title', 'actor_3_name']]

##Clean Genres, movie_titles & Remove Symbols##
dataset['genres'] = dataset['genres'].apply(lambda a: str(a).replace('|', ' '))
dataset['movie_title'] = dataset['movie_title'].apply(lambda a: a[:-1])

##Grab features for Cosine Similarity score##
dataset['director_genre_actors'] = dataset['director_name'] + ' ' + dataset['actor_1_name'] + ' ' + ' ' + dataset[
    'actor_2_name'] + ' ' + dataset['actor_3_name'] + ' ' + dataset['genres']

##Fill empty (na) values##
dataset.fillna('', inplace=True)

##CosineSimilarity##
vec = CountVectorizer()
vec_matrix = vec.fit_transform(dataset['director_genre_actors'])
similarity = cosine_similarity(vec_matrix)

##Recommendation Function##
def recommend_movie(movie):
    if movie not in dataset['movie_title'].unique():
        return (
            'The movie entered is not in our dataset. Please check spelling or type in a new movie title.'
        )
    else:
        i = dataset.loc[dataset['movie_title'] == movie].index[0]
        lst = list(enumerate(similarity[i]))
        lst = sorted(lst, key=lambda x: x[1], reverse=True)
        lst = lst[1:11]
        l = []
        for i in range(len(lst)):
            a = lst[i][0]
            l.append(dataset['movie_title'][a])
        my_string = ''
        for x in l:
            my_string += '\n ' + x
        my_string = my_string.replace('\n', '<br>')

        return my_string.title()

##Cosine Score Function##
def cosine_score(movie):
    if movie not in dataset['movie_title'].unique():
        return ('Please try again')
    else:
        i = dataset.loc[dataset['movie_title'] == movie].index[0]
        lst = list(enumerate(similarity[i]))
        lst = sorted(lst, key=lambda x: x[1], reverse=True)
        lst = lst[1:11]  # excluding first item since it is the requested movie itself
        l = []
        for i in range(len(lst)):
            a = lst[i][0]
            l.append(dataset['movie_title'][a])
        cosine_list = [x[1] for x in lst]
        cosine_int = cosine_list[0]
        cosine_int = str(cosine_int)
        return 'Cosine Score: ' + cosine_int

##Movie Title Return Function##
def movie_name_return(movie):
    if movie not in dataset['movie_title'].unique():
        return (
            'The movie entered is not in our dataset. Please check spelling or type in a new movie title.'
        )
    else:
        i = dataset.loc[dataset['movie_title'] == movie].index[0]
        lst = list(enumerate(similarity[i]))
        lst = sorted(lst, key=lambda x: x[1], reverse=True)
        lst = lst[1:11]  # excluding first item since it is the requested movie itself
        l = []
        for i in range(len(lst)):
            a = lst[i][0]
            l.append(dataset['movie_title'][a])

        for x in range(len(l)):
                return str(l[x])

##Change h1 depending on movie title##
def h1_tag(movie):
    if movie not in dataset['movie_title'].unique():
        return (
            'Error'
        )
    else:
        i = dataset.loc[dataset['movie_title'] == movie].index[0]
        lst = list(enumerate(similarity[i]))
        lst = sorted(lst, key=lambda x: x[1], reverse=True)
        lst = lst[1:11]  # excluding first item since it is the requested movie itself
        l = []
        for i in range(len(lst)):
            a = lst[i][0]
            l.append(dataset['movie_title'][a])

        for x in range(len(l)):
            movie_upper = str(l[x])
            return movie_upper.title()

##Change p1 depending on if error or not##
def p1_tag(movie):
    if movie not in dataset['movie_title'].unique():
        return 'Please find error below'
    else:
        return 'Similar movies recommended below...'
