import streamlit as st
import pandas as pd
import pickle
import requests

# Load the artifacts
movies = pd.read_pickle('./artifacts/movie_list.pkl')
similarity = pickle.load(open('./artifacts/similarity.pkl', 'rb'))


def fetch_poster(movie_id):
    # Construct the URL
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    # Send the GET request and convert the response to a JSON object
    data = requests.get(url)
    data = data.json()
    # Extract the poster path and construct the full URL of the poster image
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    # Return the URL of the poster image
    return full_path


# Define a function for getting movie recommendations
def get_recommendations(title, cosine_sim=similarity, movies=movies):
    # Get the index of the movie that matches the title
    idx = movies[movies['title'] == title].index[0]

    # Get the pairwise similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)


    recommended_movie_names = []
    recommended_movie_posters = []
    for i in sim_scores[1:11]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


# Create the web app
st.title('⭐🎬 Movie Recommendation System 🎬⭐')

# Add a text input for getting the movie title
selected_option = st.selectbox('Enter or select the title of a movie:', movies['title'].values)

# Add a button for getting the recommendations
if st.button('Recommend'):
    # Get the recommendations
    recommended_movie_names,recommended_movie_posters = get_recommendations(selected_option)

    # Display the recommendations
    st.write('Recommended Movies:')
    col1, col2, col3, col4, col5, = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
        st.text(recommended_movie_names[5])
        st.image(recommended_movie_posters[5])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
        st.text(recommended_movie_names[6])
        st.image(recommended_movie_posters[6])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
        st.text(recommended_movie_names[7])
        st.image(recommended_movie_posters[7])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
        st.text(recommended_movie_names[8])
        st.image(recommended_movie_posters[8])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
        st.text(recommended_movie_names[9])
        st.image(recommended_movie_posters[9])
    