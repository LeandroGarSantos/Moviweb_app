from flask import Flask, render_template, request, redirect, url_for
from datamanager.json_data_manager import JSONDataManager
import requests
"""
MovieWeb App

This Flask application allows users to manage a list of movies and their details. Users can add, delete, and update movies, as well as view a list of users and their associated movies.

Author: [Your Name]
"""

app = Flask(__name__)
data_manager = JSONDataManager('movies.json') # Use the appropriate path to your JSON file


def fetch_movie_details(movie_title):
    """
        Fetches movie details from the OMDb API based on the provided movie title.

        Args:
            movie_title (str): The title of the movie.

        Returns:
            dict: A dictionary containing the movie details, or an empty dictionary if the API request fails.

        Raises:
            requests.RequestException: If an error occurs during the API request.
        """

    api_key = '7cee3b97'
    url = f'http://www.omdbapi.com/?apikey={api_key}&t={movie_title}'

    try:
        response = requests.get(url)
        response.raise_for_status()

        if response.status_code == 200:
            movie_data = response.json()
            return movie_data
        else:
            # Handle the case when the API request fails
            return {}
    except requests.RequestException as e:
        # Handle request exceptions
        print("An error occurred during the API request:", str(e))
        return {}


@app.route('/')
def home():
    """
       Renders the home page of the MovieWeb App.

       Returns:
           str: The rendered HTML template for the home page.
       """
    return render_template('index.html')


@app.route('/users')
def list_users():
    """
        Retrieves and renders a list of users.

        Returns:
            str: The rendered HTML template for the list of users.

        Raises:
            Exception: If an error occurs while retrieving user data.
        """
    try:
        users = data_manager.get_all_users()
        return render_template('users.html', users=users)
    except Exception as e:
        # Handle exceptions related to getting users
        print("An error occurred while retrieving user data:", str(e))
        return render_template('error.html', error_message="An error occurred while retrieving user data")


@app.route('/users/<user_id>')
def get_user_movies(user_id):
    """
        Retrieves and renders the list of movies for a specific user.

        Args:
            user_id (str): The ID of the user.

        Returns:
            str: The rendered HTML template for the list of movies.

        Raises:
            Exception: If an error occurs while retrieving user movies.
        """
    try:
        movies = data_manager.get_user_movies(user_id)
        return render_template('movies.html', movies=movies, user_id=user_id)
    except Exception as e:
        # Handle exceptions related to getting user movies
        print("An error occurred while retrieving user movies:", str(e))
        return render_template('error.html', error_message="An error occurred while retrieving user movies")


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """
        Adds a new user to the system.

        Returns:
            str: The rendered HTML template for adding a user.

        Raises:
            Exception: If an error occurs while adding a user.
        """
    if request.method == 'POST':
        try:
            username = request.form['username']
            user = {'username': username, 'movies': []}
            data_manager.add_user(user)
            return redirect(url_for('list_users'))
        except Exception as e:
            # Handle exceptions related to adding a user
            print("An error occurred while adding a user:", str(e))
            return render_template('error.html', error_message="An error occurred while adding a user")
    return render_template('add_user.html')


@app.route('/users/<user_id>/delete_user', methods=['GET', 'POST'])
def delete_user(user_id):
    """
        Deletes a user from the system.

        Args:
            user_id (str): The ID of the user to be deleted.

        Returns:
            str: The rendered HTML template for deleting a user.

        Raises:
            Exception: If an error occurs while deleting a user.
        """
    if request.method == 'POST':
        try:
            data_manager.delete_user(user_id)
            return redirect(url_for('list_users'))
        except Exception as e:
            # Handle exceptions related to deleting a user
            print("An error occurred while deleting a user:", str(e))
            return render_template('error.html', error_message="An error occurred while deleting a user")

    return render_template('delete_user.html', user_id=user_id)


@app.route('/users/<user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    """
        Adds a new movie to a user's movie list.

        Args:
            user_id (str): The ID of the user.

        Returns:
            str: The rendered HTML template for adding a movie.

        Raises:
            Exception: If an error occurs while adding a movie.
        """
    if request.method == 'POST':
        try:
            movie_title = request.form['movie_title']
            movie_rating = request.form['movie_rating']
            movie = {'title': movie_title, 'rating': movie_rating}

            # Fetch movie details from OMDb API
            movie_details = fetch_movie_details(movie_title)

            # Override the fetched details with user-provided values
            movie_details['Title'] = movie_title
            movie_details['Rating'] = movie_rating

            # Add the movie to the user's list
            data_manager.add_movie_to_user(user_id, movie_details)

            return redirect(url_for('get_user_movies', user_id=user_id))
        except Exception as e:
            # Handle exceptions related to adding a movie
            print("An error occurred while adding a movie:", str(e))
            return render_template('error.html', error_message="An error occurred while adding a movie")
    return render_template('add_movie.html', user_id=user_id)


@app.route('/users/<user_id>/update_movie/<movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    """
        Updates the rating of a movie in a user's movie list.

        Args:
            user_id (str): The ID of the user.
            movie_id (str): The ID of the movie.

        Returns:
            str: The rendered HTML template for updating a movie.

        Raises:
            Exception: If an error occurs while updating a movie.
    """
    if request.method == 'POST':
        try:
            new_title = request.form['new_title']
            new_rating = request.form['new_rating']
            data_manager.update_movie(user_id, movie_id, new_title, new_rating)
            return redirect(url_for('get_user_movies', user_id=user_id))
        except Exception as e:
            # Handle exceptions related to updating a movie
            print("An error occurred while updating a movie:", str(e))
            return render_template('error.html', error_message="An error occurred while updating a movie")

    try:
        user_movies = data_manager.get_user_movies(user_id)
        movie = next((movie for movie in user_movies if movie['imdbID'] == movie_id), None)
        if movie:
            return render_template('update_movie.html', user_id=user_id, movie=movie)
        else:
            return render_template('error.html', error_message="Movie not found.")
    except Exception as e:
        # Handle exceptions related to getting a movie for update
        print("An error occurred while retrieving a movie for update:", str(e))
        return render_template('error.html', error_message="An error occurred while retrieving a movie for update")


@app.route('/users/<user_id>/delete_movie/<movie_id>', methods=['POST'])
def delete_movie(user_id, movie_id):
    """
        Deletes a movie from a user's movie list.

        Args:
            user_id (str): The ID of the user.
            movie_id (str): The ID of the movie to be deleted.

        Returns:
            str: The rendered HTML template for deleting a movie.

        Raises:
            Exception: If an error occurs while deleting a movie.
        """
    try:
        data_manager.delete_movie(user_id, movie_id)
        return redirect(url_for('get_user_movies', user_id=user_id))
    except Exception as e:
        # Handle exceptions related to deleting a movie
        print("An error occurred while deleting a movie:", str(e))
        return render_template('delete_movie.html', user_id=user_id, movie_id=movie_id)


@app.errorhandler(404)
def page_not_found(e):
    """
        Renders a custom 404 page when a page is not found.

        Args:
            e: The exception raised for the page not found error.

        Returns:
            str: The rendered HTML template for the 404 page.
        """
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)