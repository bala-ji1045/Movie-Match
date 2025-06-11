import streamlit as st
import pickle
import requests

# Improved, compact, responsive gallery CSS
st.markdown("""
    <style>
    
    .movie-title {
        font-size: 17px;
        font-weight: 600;
        color: #00adb5;
        margin-bottom: 10px;
        margin-top: 8px;
        letter-spacing: 0.3px;
        text-shadow: 0 2px 8px rgba(0,0,0,0.10);
    }
    img {
        border-radius: 10px;
        margin-bottom: 10px;
        width: 100%;
        height: 220px;
        object-fit: cover;
        background: #222831;
        box-shadow: 0 2px 8px 0 rgba(0,0,0,0.10);
    }
    @media (max-width: 900px) {
        img { height: 140px; }
        .movie-card { min-height: 200px; }
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
    except Exception:
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
    # Gallery: 5 columns for desktop, fewer for mobile
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            
            if posters[idx]:
                st.image(posters[idx], use_container_width=True)
            else:
                st.write("No poster available")
            st.markdown(f"<div class='movie-title'>{names[idx]}</div>", unsafe_allow_html=True)
            
