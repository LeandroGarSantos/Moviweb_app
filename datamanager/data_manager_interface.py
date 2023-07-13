from abc import ABC, abstractmethod


class DataManagerInterface(ABC):
    @abstractmethod
    def load_data(self):
        """
        Abstract method to load data from a data source.
        """
        pass

    @abstractmethod
    def save_data(self):
        """
        Abstract method to save data to a data source.
        """
        pass

    @abstractmethod
    def get_all_users(self):
        """
        Abstract method to retrieve all users.
        
        Returns:
            A list of all users.
        """
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        """
        Abstract method to retrieve movies for a specific user.
        
        Args:
            user_id (int): The ID of the user.
        
        Returns:
            A list of movies associated with the user.
        """
        pass

    @abstractmethod
    def add_user(self, user):
        """
        Abstract method to add a new user.
        
        Args:
            user: The user object to be added.
        """
        pass

    @abstractmethod
    def delete_user(self, user_id):
        """
        Abstract method to delete a user.
        
        Args:
            user_id (int): The ID of the user to be deleted.
        """
        pass

    @abstractmethod
    def add_movie_to_user(self, user_id, movie):
        """
        Abstract method to add a movie to a user's collection.
        
        Args:
            user_id (int): The ID of the user.
            movie: The movie object to be added.
        """
        pass

    @abstractmethod
    def delete_movie(self, user_id, movie_id):
        """
        Abstract method to delete a movie from a user's collection.
        
        Args:
            user_id (int): The ID of the user.
            movie_id (int): The ID of the movie to be deleted.
        """
        pass

    @abstractmethod
    def update_movie(self, user_id, movie_id, new_title, new_rating):
        """
        Abstract method to update the title and rating of a movie in a user's collection.
        
        Args:
            user_id (int): The ID of the user.
            movie_id (int): The ID of the movie to be updated.
            new_title (str): The new title of the movie.
            new_rating (float): The new rating of the movie.
        """
        pass

    # Add more methods as needed
