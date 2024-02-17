import streamlit as st
import pickle
import pandas as pd
import requests

def fetch(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=a58479662f9100d28ee5251c13d8b5a2&language=en-US".format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
st.title('Movie Recommender System')
similarity = pickle.load(open('similarity.pkl','rb'))

def recommend(movie):
  movie_index = movies[movies['title']== movie].index[0]
  distances = similarity[movie_index]
  movie_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

  recommended_movie = []
  poster = []
  for i in movie_list:
    movie_id = movies.iloc[i[0]].movie_id
    #fetching the poster
    recommended_movie.append(movies.iloc[i[0]].title)
    poster.append(fetch(movie_id))
  return recommended_movie, poster

option = st.selectbox(
'Select Movie Name?',
movies['title'].values)

if st.button('recommend'):
    name,posters = recommend(option)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(name[0])
        st.image(posters[0])
    with col2:
        st.text(name[1])
        st.image(posters[1])
    with col3:
        st.text(name[2])
        st.image(posters[2])
    with col4:
        st.text(name[3])
        st.image(posters[3])
    with col5:
        st.text(name[4])
        st.image(posters[4])