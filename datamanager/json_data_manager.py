from data_manager_interface import DataManagerInterface
import os

import json

class JSONDataManager(DataManagerInterface):
    def __init__(self):
        self._file_path = self.get_movies_json_path()
        self._movies_data = self.load_movies_data()

    @property
    def file_path(self):
        return self._file_path
    @file_path.setter
    def file_path(self, value):
        self._file_path =value

    def get_movies_json_path(self):
        # Get the absolute path to the project root directory
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

        # Construct the path to static/movies.json
        return os.path.join(project_root, 'Movie_WebApi_App', 'static', 'movies.json')

    def load_movies_data(self):
        try:
            with open(self._file_path, 'r') as fileobj:
                return json.load(fileobj)

        except Exception as e:
            print(f"Error loading data: {e}")
        return {}
    def save_data(self):
        """Save data to the JSON file."""
        try:
            with open(self._file_path, 'w') as file:
                json.dump(self._movies_data, file, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")
    def get_all_users(self):

        """
        Retrieves a list of username from the movie database.

        Returns: A list of usernames.
        """
        try:
            user_list = self._movies_data
            return user_list


        except KeyError as e:
            # Handle the case where a user entry is missing the "name" key
            print(f"Error: {e}. 'name' key not found in a user entry.")
            return {}

    def get_user_movies(self, user_id):
        """
        Retrieves all the movies for a given user

        Return all the movies of a specific user
        """
        try:
            list_of_movies = self._movies_data.get(str(user_id))
            if list_of_movies:
                return list_of_movies.get("movies", {})
            else:
                print(f"User with ID {user_id} is not found.")
                return {}

        except KeyError as e:
            # Handle the case where a user entry is missing the "name" key
            print(f"Error: {e}. 'name' key not found in a user entry.")
            return []

    def add_movie(self, user_id, movie_name, director, year, rating):
        """
                Adds a new movie to a user's list of favorite movies.

                Args:
                - user_id: The ID of the user.
                - movie_name: The name of the movie.
                - director: The director of the movie.
                - year: The year the movie was released.
                - rating: The rating of the movie.
                """
        try:
            # Check if the user exists in the data
            if user_id not in self._movies_data:
                raise KeyError(f"User with ID {user_id} not found")

            # Get the user's current list of movies
            user_movies = self._movies_data[user_id].get("movies", {})



            # checks if the movie already exist in the databasse or not
            for movie_id, movie_data in user_movies.items():
                if movie_data["name"].lower() == movie_name.lower():
                    raise ValueError(f"Movie {movie_name} is already exist in the user's list")

            # Generate a new movie ID
            new_movie_id = str(len(user_movies) + 1)

            # Add the new movie to the user's list
            user_movies[new_movie_id] = {
                "name": movie_name,
                "director": director,
                "year": year,
                "rating": rating,
            }

            # Add the new movie list in the data structure
            self._movies_data[user_id]["movies"] = user_movies

            # save the new movie data into database
            self.save_data()
        except KeyError as e:
            # Handle the case where the user is not found
            raise ValueError(f"Error: {e}. User with ID {user_id} not found.")

    def add_user(self, user_name):
        try:
            # Get the max current list of users
            max_user_id = max(int(user_id) for user_id in self._movies_data.keys())

            # Generate a unique user_id (incrementing IDs)
            user_id = str(max_user_id + 1)

            # Add the new user to the data
            self._movies_data[user_id] = {"id": user_id, "name": user_name, "movies": {}}

            # Save the updated data
            self.save_data()

            # Success message
            success_message = f"User {user_name} added successfully with ID {user_id}"
            return success_message

        except Exception as e:
            raise ValueError(f"An error occurred: {e}")


    def update_movie(self, user_id, movie_id, updated_data):
        """
        updated the user movie information
        """
        try:
            user_data = self._movies_data.get(str(user_id))

            # user not Found
            if not user_data:
                return False

            movies = user_data.get('movies', {})

            if str(movie_id) not in movies:
                return False
            movies[str(movie_id)].update(updated_data)

            self.save_data()
            return True
        except Exception as e:
            raise ValueError(f"An error occurred: {e}")





















