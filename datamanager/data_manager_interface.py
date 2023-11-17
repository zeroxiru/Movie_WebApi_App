from abc import ABC, abstractmethod

class DataManagerInterface(ABC):

    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        pass

    @abstractmethod
    def get_movies_json_path(self):
        pass

    @abstractmethod
    def add_movie(self, user_id, movie_name, director, year, rating):
        pass


    @abstractmethod
    def add_user(self, user_name):
        """Add a new user"""
        pass

    @abstractmethod
    def update_user(self, user_id, updated_data):
        """Update user data."""
        pass

    @abstractmethod
    def delete_user(self, user_id):
        """Delete a user."""
        pass


    @abstractmethod
    def update_movie(self, user_id, movie_id, updated_data):
        """Update movie data."""
        pass

    @abstractmethod
    def delete_movie(self, user_id, movie_id):
        """Delete a movie for a user."""
        pass

    @abstractmethod
    def list_movies(self, user_id):
        """List all movies for a user."""
        pass