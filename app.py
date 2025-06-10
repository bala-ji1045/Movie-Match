import streamlit as st
import pickle
import requests

# Custom CSS for background and card styling
st.markdown("""
    <style>
    .main {
        background-color: #222831;
        color: #eeeeee;
    }
    .movie-card {
        background: #393e46;
        border-radius: 15px;
        padding: 20px 10px 10px 10px;
        margin: 10px;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
        text-align: center;
    }
    .movie-title {
        font-size: 18px;
        font-weight: bold;
        color: #00adb5;
        margin-bottom: 10px;
    }
    img {
        border-radius: 10px;
        margin-bottom: 10px;
        max-height: 300px;
        object-fit: cover;
    }
    </style>
""", unsafe_allow_html=True)

def fetch_poster(movie_id):
    try:
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'
        )
        response.raise_for_status()
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path'] if 'poster_path' in data else None
    except Exception as e:
        return None

# Load the DataFrame for indexing
movies_df = pickle.load(open('movie_list.pkl', 'rb'))
movies_list = movies_df['title'].values

similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommend(movie):
    index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[index]
    movies_list_sorted = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list_sorted:
        movie_id = movies_df.iloc[i[0]]['movie_id']
        recommended_movies.append(movies_df.iloc[i[0]]['title'])
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

st.markdown("<h1 style='text-align: center; color: #00adb5;'>🎬 Movie Recommendation System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #eeeeee;'>Select a movie you like and get recommendations instantly!</p>", unsafe_allow_html=True)
st.markdown("---")

selected_movie = st.selectbox(
    'Select a movie to get recommendations:',
    movies_list
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie)
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            col.markdown(f"<div class='movie-card'>", unsafe_allow_html=True)
            col.markdown(f"<div class='movie-title'>{names[idx]}</div>", unsafe_allow_html=True)
            if posters[idx]:
                col.image(posters[idx], use_container_width=True)
            else:
                col.write("No poster available")
            col.markdown("</div>", unsafe_allow_html=True)