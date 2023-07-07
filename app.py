from flask import Flask, render_template, request, redirect, url_for
from datamanager.json_data_manager import JSONDataManager


app = Flask(__name__)
data_manager = JSONDataManager('movies.json') # Use the appropriate path to your JSON file


@app.route('/')
def home():
    return "Welcome to MovieWeb App!"


# @app.route('/users')
# def get_users():
#     users = data_manager.get_all_users()
#     return render_template('users.html', users=users)
@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<user_id>')
def  get_user_movies(user_id):
    movies = data_manager.get_user_movies(user_id)
    return render_template('movies.html', movies=movies)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        user_id = request.form['user_id']
        username = request.form['username']
        user = {'id': user_id, 'username': username, 'movies': []}
        data_manager.add_user(user)
        return redirect(url_for('get_user'))
    return render_template('add_user.html')


@app.route('/users/<user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    if request.method == 'POST':
        movie_title = request.form['movie_title']
        movie_rating = request.form['movie_rating']
        movie = {'title': movie_title, 'rating': movie_rating}
        data_manager.add_movie_to_user(user_id,movie)
        return redirect(url_for('get_user_movies', user_id=user_id))
    return render_template('add_movie.html')


@app.route('/users/<user_id>/update_movie/<movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    if request.method == 'POST':
        new_rating = request.form['new_rating']
        data_manager.update_movie_rating(user_id, movie_id, new_rating)
        return redirect(url_for('get_user_movies', user_id=user_id))
    movie = data_manager.get_movie_by_id(user_id, movie_id)
    return render_template('update_movie.html', movie=movie)


@app.route('/users/<user_id>/delete_movie/<movie_id>')
def delete_movie(user_id, movie_id):
    data_manager.delete_movie(user_id, movie_id)
    return redirect(url_for('get_user_movies', user_id=user_id))


if __name__ == '__main__':
    app.run(debug=True)