from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from datamanager.json_data_manager import JSONDataManager

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Choose the data manager implementation (use either DataManager or CSVDataManager)

data_manager = JSONDataManager()


# data_manager = CSVDataManager('data/movies.csv')

# Routes

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
        return render_template('error.html', error_message="User not found")

    # check the content type of the request
    content_type = request.headers.get('Content-Type')

    try:
        if content_type == 'application/json':
            # If the content type is JSON, update movie details using JSON data
            new_movie_data = request.json

        # Assuming request.json returns a dictionary with updated movie details
        elif content_type == 'application/x-www-form-urlencoded':
            # If the content type is form data, update movie details using form data

            # Get data from the form
            new_movie_data = {

                "name": request.form.get('name'),
                "director": request.form.get('director'),
                "year": int(request.form.get('year')),
                "rating": float(request.form.get('rating'))
            }
        else:
            raise ValueError('Unsupported content type')
    except ValueError as e:
        return render_template('error.html', error_message=f'Error parsing data: {e}')

        # Update movie details in JSONDataManager
        success = data_manager.update_movie(user_id, movie_id, new_movie_data)

        if success:
            return redirect(url_for('user_movies', user_id=user_id))
        else:
            return render_template('error.html', error_message='Failed to update movie details')


@app.route('/users/<int:user_id>/movies')
def user_movies(user_id):
    user = data_manager.load_movies_data().get(str(user_id))

    if not user:
        return render_template('error.html', error_message='User not found')

    return render_template('user_movies.html', user=user)


if __name__ == '__main__':
    app.run(debug=True)
