# Movie-Match
Project Description: Movie Recommendation System  This project is a web-based Movie Recommendation System built using Streamlit. It allows users to select a movie they like and instantly receive personalized movie recommendations, each displayed with its poster and title in an attractive card layout.  
Key Features:

User-Friendly Interface: Clean, modern UI with a dark theme and card-based design for recommendations.
Instant Recommendations: Select a movie from the dropdown to get five similar movies recommended.
Movie Posters: Each recommendation is shown with its official poster fetched from The Movie Database (TMDB) API
The app loads a precomputed similarity matrix and a movie list (from pickled files).
When a user selects a movie and clicks "Recommend," the app finds the most similar movies using the similarity matrix.
For each recommended movie, the app fetches and displays the poster and title in a responsive layout.
Tech Stack:

Frontend & App Framework: Streamlit
Backend: Python
Data: Precomputed movie similarity matrix and movie metadata (pickled pandas DataFrames)
API: TMDB API for fetching movie posters
This project is ideal for learning about recommendation systems, web app deployment with Streamlit, and integrating external APIs for enhanced user experience.

