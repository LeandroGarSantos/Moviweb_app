from flask import Flask, render_template, request, redirect, url_for
from datamanager.json_data_manager import JSONDataManager
import requests

app = Flask(__name__)
data_manager = JSONDataManager('movies.json') # Use the appropriate path to your JSON file


def fetch_movie_details(movie_title):
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
    return render_template('index.html')


@app.route('/users')
def list_users():
    try:
        users = data_manager.get_all_users()
        return render_template('users.html', users=users)
    except Exception as e:
        # Handle exceptions related to getting users
        print("An error occurred while retrieving user data:", str(e))
        return render_template('error.html', error_message="An error occurred while retrieving user data")


@app.route('/users/<user_id>')
def get_user_movies(user_id):
    try:
        movies = data_manager.get_user_movies(user_id)
        return render_template('movies.html', movies=movies)
    except Exception as e:
        # Handle exceptions related to getting user movies
        print("An error occurred while retrieving user movies:", str(e))
        return render_template('error.html', error_message="An error occurred while retrieving user movies")


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
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
    if request.method == 'POST':
        try:
            new_rating = request.form['new_rating']
            data_manager.update_movie_rating(user_id, movie_id, new_rating)
            return redirect(url_for('get_user_movies', user_id=user_id))
        except Exception as e:
            # Handle exceptions related to updating a movie
            print("An error occurred while updating a movie:", str(e))
            return render_template('error.html', error_message="An error occurred while updating a movie")

    try:
        movie = data_manager.get_movie_by_id(user_id, movie_id)
        return render_template('update_movie.html', movie=movie)
    except Exception as e:
        # Handle exceptions related to getting a movie for update
        print("An error occurred while retrieving a movie for update:", str(e))
        return render_template('error.html', error_message="An error occurred while retrieving a movie for update")


@app.route('/users/<user_id>/delete_movie/<movie_id>')
def delete_movie(user_id, movie_id):
    try:
        data_manager.delete_movie(user_id, movie_id)
        return redirect(url_for('get_user_movies', user_id=user_id))
    except Exception as e:
        # Handle exceptions related to deleting a movie
        print("An error occurred while deleting a movie:", str(e))
        return


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)