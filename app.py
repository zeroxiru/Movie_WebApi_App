from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from datamanager.json_data_manager import JSONDataManager
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField
from wtforms.validators import DataRequired

class UpdateMovieForm(FlaskForm):
    # Define your form fields here
    title = StringField('Title', validators=[DataRequired()])
    director = StringField('Director', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired()])
    rating = FloatField('Rating', validators=[DataRequired()])

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Choose the data manager implementation (use either DataManager or CSVDataManager)

data_manager = JSONDataManager()


# data_manager = CSVDataManager('data/movies.csv')

# Routes
# @app.route('/')
# def index():
#     # Pass the movie data to the template
#     return render_template('index.html', movies=data_manager.load_movies_data())
# Replace this with your actual logic to calculate total pages

@app.route('/')
def index():
    try:
        # Get the movie data from the data manager
        movies_data = data_manager.load_movies_data()

        # Calculate total pages (assuming you have a function for this)
        total_pages = data_manager.calculate_total_pages(movies_data)

        # Render the template with the movie data and total pages
        return render_template('index.html', movies=movies_data, total_pages=total_pages)

    except Exception as e:
        # Handle any exceptions that might occur
        error_message = f"An error occurred: {e}"

        # You might want to render an error template or log the error
        return render_template('error.html', error_message=error_message)

@app.route('/users', methods=['GET'])
def list_users():
    try:
        users_list = data_manager.get_all_users()

        # Render the template with the list of users
        return render_template('list_of_users.html', users=users_list)

    except ValueError as ve:
        # Handle specific validation errors
        error_message = str(ve)
        return render_template('error.html', error_message=error_message)

    except Exception as e:
        # Handle any exceptions that might occur
        error_message = f"An error occurred: {e}"
        return render_template('error.html', error_message=error_message)



@app.route('/movies_by_user/<int:user_id>', methods=['GET'])
def list_of_movies_by_user(user_id):
    movies_by_user = data_manager.get_user_movies(user_id)
    print(f"{movies_by_user}")
    return jsonify(movies_by_user)


@app.route('/add_user', methods=['GET', 'POST'])
def add_new_user():
    try:
        if request.method == 'POST':
            # Get the Data from the form
            if request.form:
                user_name = request.form.get('name')
            else:
                data = request.get_json()
                user_name = data.get('name')

            if not user_name:
                raise ValueError("User name is required")

            data_manager.add_user(user_name)

            # Flash a success message
            # flash("User added successfully!", "success")

            flash("showSuccessPopup()", "javascript")

            # Redirect to the list of users or another appropriate page
            return redirect(url_for('list_users'))

        # If it's a GET request, render the form
        return render_template('add_user.html')

    except ValueError as e:
        # Handle specific validation errors
        error_message = str(e)

        # Check if the request is JSON and return JSON response
        if request.is_json:
            return jsonify({"error": error_message}), 400

        flash(error_message, "danger")
        return render_template('error.html', error_message=error_message)

    except Exception as e:
        # Handle any exceptions that might occur
        error_message = f"An error occurred: {e}"

        # Check if the request is JSON and return JSON response
        if request.is_json:
            return jsonify({"error": error_message}), 500

        flash(error_message, "danger")
        return render_template('error.html', error_message=error_message)


# @app.route('/add_user', methods=['GET', 'POST'])
# def add_new_user():
#     try:
#         if request.method == 'POST':
#
#             # Get the Data from the form
#             if request.form:
#                 user_name = request.form.get('name')
#             else:
#                 data = request.get_json()
#                 user_name = data.get('name')
#
#             if not user_name:
#                 raise ValueError("User name is required")
#
#             # generate a unique user_id(e.g., incrementing IDs)
#                 # Get the current list of the  user
#             # user_list = [user["name"] for user in data_manager._movies_data.values()]
#             #
#             # user_id = str(len(user_list))
#             # print(user_id)
#             data_manager.add_user(user_name)
#
#             # Flash a success message
#             flash("User added successfully!", "success")
#
#             # Redirect to the list of users or another appropriate page
#             return redirect(url_for('list_users'))
#
#         # If it's a GET request, render the form
#         return render_template('add_user.html')
#
#     except ValueError as e:
#         # Handle specific validation errors
#         error_message = str(e)
#
#         # Check if the request is JSON and return JSON response
#         if request.is_json:
#             return jsonify({"error": error_message}), 400
#
#         flash(error_message, "danger")
#         return render_template('error.html', error_message=error_message)
#
#
#     except Exception as e:
#         # Handle any exceptions that might occur
#         error_message = f"An error occurred: {e}"
#
#         # Check if the request is JSON and return JSON response
#         if request.is_json:
#             return jsonify({"error": error_message}), 500
#
#         flash(error_message, "danger")
#         return render_template('error.html', error_message=error_message)
#

@app.route('/users/<user_id>/add_movie', methods=['GET', 'POST'])
def add_movie_route(user_id):
    try:
        if request.method == 'POST':
            # Get the data from json file/ postman
            if request.is_json:
                data = request.get_json()
                movie_name = data.get('name')
                director = data.get('director')
                year = data.get('year')
                rating = data.get('rating')

            else:
                # Get data from the form
                movie_name = request.form.get('name')
                director = request.form.get('director')
                year = request.form.get('year')
                rating = request.form.get('rating')


            if year is None or rating is None:
                raise ValueError("Year and Rating are required fields")

            year = int(year)
            rating = float(rating)

            # validate and add the movie to the user's list
            data_manager.add_movie(user_id, movie_name, director, year, rating)

            # Flash a success message
            flash("Movie added successfully!", "success")

            # Check  if the request is Json, and return JSON response
            if request.is_json:
                return jsonify({"Message": "Movie added Successfully!"})

            # Redirect to the movies list for the user
            return redirect(url_for('list_of_movies_by_user', user_id=user_id))

        # if it's a Get  request, render the form
        return render_template('add_movie.html', user_id=user_id)

    except ValueError as e:
        # Handle specific validation errors
        error_message = str(e)

        # Check if the request is json and return json response
        if request.is_json:
            return jsonify({"error": error_message}), 400

        return render_template('error.html', error_message=error_message)


    except Exception as e:
        # Handle any exceptions that might occur
        error_message = f"An error occurred: {e}"

        # Check if the request is JSON, and return JSON response
        if request.is_json:
            return jsonify({"error": error_message}), 500

        return render_template('error.html', error_message=error_message)


@app.route('/list_of_users')
def list_of_users():
    try:
        # Retrieve the list of users from the data manager
        users = data_manager.get_all_users()

        # Render the template with the list of users
        return render_template('list_of_users.html', users=users)

    except Exception as e:
        # Handle any exceptions that might occur
        error_message = f"An error occurred: {e}"
        return render_template('error.html', error_message=error_message)


@app.route('/users/<user_id>/update_movie/<movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):


    user = data_manager.load_movies_data().get(str(user_id))

    if not user:
        return render_template('error.html', error_message="User not found")

    movie_details = user.get('movies', {}).get(str(movie_id))

    if not movie_details:
        return render_template('error.html', error_message="Movie not found")

    if request.method == 'GET':
        # Render the update movie form and populate the form fields
        return render_template('update_movie_form.html', user_id=user_id, movie_id=movie_id,
                               movie_details=movie_details)

    new_movie_data = None  # Define new_movie_data outside the try block
    if request.method == 'POST':
        try:
            # Check for form data
            if request.form:
                new_movie_data = {}
                if "name" in request.form:
                    new_movie_data["name"] = request.form.get("name")
                if "director" in request.form:
                    new_movie_data["director"] = request.form.get("director")
                if "year" in request.form:
                    new_movie_data["year"] = int(request.form.get("year"))
                if "rating" in request.form:
                    new_movie_data["rating"] = float(request.form.get("rating"))
                if "poster" in request.form:
                    new_movie_data["poster"] = request.form.get("poster")
                if "actors" in request.form:
                    new_movie_data["actors"] = request.form.get("actors")
                if "plot" in request.form:
                    new_movie_data["plot"] = request.form.get("plot")

            else:
                # If it's not form data, assume it's JSON
                new_movie_data = request.json

            # Update movie details in JSONDataManager
            success = data_manager.update_movie(user_id, movie_id, new_movie_data)

            if success:
                return redirect(url_for('user_movies', user_id=user_id))
            else:
                return render_template('error.html', error_message='Failed to update movie details')

        except ValueError as e:
            return render_template('error.html', error_message=f'Error parsing data: {e}')

@app.route('/users/<user_id>/movies')
def user_movies(user_id):
    user = data_manager.load_movies_data().get(str(user_id))

    if not user:
        return render_template('error.html', error_message='User not found')

    return render_template('user_movies.html', user=user)


@app.route('/users/<user_id>/delete_movie/<movie_id>', methods=['GET', 'POST'])
def delete_movie_route(user_id, movie_id):
    if request.method == 'POST':
        success = data_manager.delete_movie(user_id, movie_id)
        if success:
            return redirect(url_for('user_movies', user_id=user_id))
        else:
            return render_template('error.html', error_message='Failed to delete movie')

    # If the request method is GET, render the delete confirmation page
    return render_template('delete_confirmation.html', user_id=user_id, movie_id=movie_id)


if __name__ == '__main__':
    app.run(debug=True)
