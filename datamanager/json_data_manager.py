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

    def add_user(self, user):
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
