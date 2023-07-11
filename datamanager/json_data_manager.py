import json


class JSONDataManager:
    def __init__(self, filename):
        self.filename = filename
        self.data = []

    def load_data(self):
        try:
            with open(self.filename, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = []

    def save_data(self, user_id):
        with open(self.filename, 'w') as file:
            json.dump(self.data, file)

    def get_all_users(self):
        self.load_data()
        return self.data

    def get_user_movies(self, user_id):
        self.load_data()
        for user in self.data:
            if user['id'] == user_id:
                return user['movies']
        return []

    # Add more methods as needed
    user_counter = 1

    def add_user(self, user):
        user['id'] = str(JSONDataManager.user_counter)
        JSONDataManager.user_counter += 1

        self.load_data()
        self.data.append(user)
        self.save_data(user["id"])

    def delete_user(self, user_id):
        self.load_data()
        self.data = [user for user in self.data if user['id'] != user_id]
        self.save_data(user_id)

    def add_movie_to_user(self, user_id, movie):
        self.load_data()
        for user in self.data:
            if user['id'] == user_id:
                user['movies'].append(movie)
                self.save_data(user_id)
                return
        raise ValueError(f"User with ID {user_id} not found.")

    def delete_movie(self, user_id, movie_title):
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
