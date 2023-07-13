import json


class JSONDataManager:
    def __init__(self, filename):
        """
        Initializes a JSONDataManager object.

        Args:
            filename (str): The name of the JSON file to load and save data.
        """
        self.filename = filename
        self.data = []

    def load_data(self):
        """
        Loads data from the JSON file and updates the internal data attribute.
        """
        try:
            with open(self.filename, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = []

    def save_data(self, user_id):
        """
        Saves the data to the JSON file.

        Args:
            user_id (str): The ID of the user to save data for.
        """
        with open(self.filename, 'w') as file:
            json.dump(self.data, file)

    def get_all_users(self):
        """
        Retrieves all users.

        Returns:
            list: A list of all users.
        """
        self.load_data()
        return self.data

    def get_user_movies(self, user_id):
        """
        Retrieves movies for a specific user.

        Args:
            user_id (str): The ID of the user.

        Returns:
            list: A list of movies associated with the user.
        """
        self.load_data()
        for user in self.data:
            if user['id'] == user_id:
                return user['movies']
        return []

    def add_user(self, user):
        """
        Adds a new user.

        Args:
            user (dict): The user object to be added.
        """
        user['id'] = str(JSONDataManager.user_counter)
        JSONDataManager.user_counter += 1

        self.load_data()
        self.data.append(user)
        self.save_data(user["id"])

    def delete_user(self, user_id):
        """
        Deletes a user.

        Args:
            user_id (str): The ID of the user to be deleted.
        """
        self.load_data()
        self.data = [user for user in self.data if user['id'] != user_id]
        self.save_data(user_id)

    def add_movie_to_user(self, user_id, movie):
        """
        Adds a movie to a user's collection.

        Args:
            user_id (str): The ID of the user.
            movie (dict): The movie object to be added.
        
        Raises:
            ValueError: If the user with the specified ID is not found.
        """
        self.load_data()
        for user in self.data:
            if user['id'] == user_id:
                user['movies'].append(movie)
                self.save_data(user_id)
                return
        raise ValueError(f"User with ID {user_id} not found.")

    def delete_movie(self, user_id, movie_title):
        """
        Deletes a movie from a user's collection.

        Args:
            user_id (str): The ID of the user.
            movie_title (str): The title of the movie to be deleted.
        """
        users = self.get_all_users()

        for user in users:
            if user['id'] == user_id:
                movies = user['movies']
                for movie in movies:
                    if movie['Title'] == movie_title:
                        movies.remove(movie)
                        self.save_data(users)
                        return

    def update_movie_rating(self, user_id, movie_id, new_rating):
        """
        Updates the rating of a movie in a user's movie list.

        Args:
            user_id (str): The ID of the user.
            movie_id (str): The ID of the movie.
            new_rating (str): The new rating of the movie.
        
        Raises:
            ValueError: If the movie with the specified ID is not found for the user.
        """
        users = self.get_all_users()

        for user in users:
            if user['id'] == user_id:
                movies = user['movies']
                for movie in movies:
                    if movie['id'] == movie_id:
                        movie['Rating'] = new_rating
                        self.save_data(user_id)
                        return

        raise ValueError(f"Movie with ID {movie_id} not found for user with ID {user_id}.")

    def update_movie(self, user_id, movie_id, new_title, new_rating):
        """
        Updates the title and rating of a movie in a user's movie list.

        Args:
            user_id (str): The ID of the user.
            movie_id (str): The ID of the movie.
            new_title (str): The new title of the movie.
            new_rating (str): The new rating of the movie.

        Raises:
            Exception: If the user or movie is not found.
        """
        # Load the data from the JSON file
        self.load_data()

        # Find the user
        user = next((user for user in self.data if user['id'] == user_id), None)
        if user:
            # Find the movie
            movie = next((movie for movie in user['movies'] if movie['imdbID'] == movie_id), None)
            if movie:
                # Update the movie's title and rating
                movie['Title'] = new_title
                movie['Rating'] = new_rating

                # Save the data to the JSON file
                self.save_data(user_id)
            else:
                raise Exception("Movie not found.")
        else:
            raise Exception("User not found.")
