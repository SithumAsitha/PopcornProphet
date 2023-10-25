import pickle
import streamlit as st
import requests
from streamlit_option_menu import option_menu

# Set page layout to wide to utilize the whole page
st.set_page_config(layout="wide")


def main():

    #sidebar for navigation
    with st.sidebar:
            
        selected = option_menu('Movie Recommendation System',
                                ['Home','Movie Recommendations'],
                                icons = ['house','film'],
                                default_index=0)
        #Home Page
    if selected == 'Home':
            
            st.markdown("<h1 style='color: red; text-align: center;'>Welcome to PopcornProphet!</h1>", unsafe_allow_html=True)
            col1, col2 = st.columns([1, 1])
            with col1:
                # Image
                st.image("movie-theater-popcorn.jpg", use_column_width=True, caption="Image: Movie Time")
            with col2:
                # Description 
                description = """
                <span style="font-size: 30px;"><strong>Welcome to PopcornProphet:</strong></span>  
                PopcornProphet is a movie recommendation system that helps you discover new movies based on your preferences.

                <span style="font-size: 30px;"><strong>How PopcornProphet Works:</strong></span>  

                <span style="font-size: 24px;"><strong>1. Select a Movie:</strong></span>  
                Choose a movie that you've watched and enjoyed. PopcornProphet will use this as a starting point for recommendations.

                <span style="font-size: 24px;"><strong>2. Get Personalized Recommendations:</strong></span>  
                We'll analyze your selected movie and provide you with a list of recommended movies that you're likely to love.

                <span style="font-size: 24px;"><strong>3. Explore New Films:</strong></span>  
                Dive into a world of cinema and discover exciting new movies that match your taste.

                <span style="font-size: 24px;"><strong>4. Enjoy Movie Nights:</strong></span>  
                With PopcornProphet, you'll never run out of great movies to watch with friends and family.

                <span style="font-size: 24px;"><strong>5. Your Movie Journey Starts Here:</strong></span>  
                Let PopcornProphet be your movie companion. Start exploring, and let the cinematic adventure begin!
                """
                
                st.markdown(description, unsafe_allow_html=True)


    if selected == 'Movie Recommendations':
            
            def fetch_poster(movie_id):
                url = "https://api.themoviedb.org/3/movie/{}?api_key=4044aa1bbd3d98365857bda8e710bbda&language=en-US".format(movie_id)
                data = requests.get(url)
                data = data.json()
                poster_path = data['poster_path']
                full_path = "http://image.tmdb.org/t/p/w500/" + poster_path
                return full_path

            def recommend_movies(movie):
                index = movies[movies['title'] == movie].index[0]
                distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
                recommended_movie_name = []
                recommend_movie_poster = []
                for i in distances[1:6]:
                    movie_id = movies.iloc[i[0]]['movie_id']  # Use square brackets here
                    recommended_movie_name.append(movies.iloc[i[0]].title)
                    recommend_movie_poster.append(fetch_poster(movie_id))
                return recommended_movie_name, recommend_movie_poster

            
            movies = pickle.load(open('artifacts/movie_list.pkl', 'rb'))
            similarity = pickle.load(open('artifacts/cosine_similarity.pkl', 'rb'))
            st.header(":popcorn::movie_camera: Select a movie that you watched to get recommendations")
            movie_list = movies['title'].values
            selected_movie = st.selectbox(
                'Type or select a movie that you watched to get recommendations',
                movie_list
            )

            

            if st.button('Show Recommendations'):
                recommend_movie_name, recommend_movie_poster = recommend_movies(selected_movie)
                
                # Set the image width and height for larger images
                image_width = 400  # Adjust this value as needed
                image_height = 600  # Adjust this value as needed
                
                col1, col2, col3, col4, col5 = st.columns(5)
                columns = [col1, col2, col3, col4, col5]
                
                for i in range(5):
                    with columns[i]:
                        st.markdown(f'<p style="font-size: 24px; font-weight: bold;">{recommend_movie_name[i]}</p>', unsafe_allow_html=True)
                        st.markdown(f'<img src="{recommend_movie_poster[i]}" style="width: {image_width}px; height: {image_height}px;">', unsafe_allow_html=True)

if __name__ == '__main__':
    main()

