from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError, OperationalError, DataError, ProgrammingError
from flask_wtf import FlaskForm
from flask_migrate import Migrate
from passlib.hash import sha256_crypt  # Used for password hashing
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, validators
from wtforms.validators import DataRequired, Email
from flask_bcrypt import Bcrypt
from tabulate import tabulate
from datetime import datetime
import pandas as pd
import numpy as np
import csv
import ast  # Import the ast module
from wtforms import SubmitField
import requests
from dotenv import load_dotenv
import os

app = Flask(__name__, template_folder='templates', static_url_path='/static')
load_dotenv()

app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

class User(db.Model):
    __tablename__ = 'useraccounts'
    user_id = db.Column(db.Integer, primary_key=True)    
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __init__(self, user_id, fname, lname, email, password):
        self.user_id = user_id
        self.fname = fname
        self.lname = lname
        self.email = email
        self.password = password

class SignupForm(FlaskForm):
    fname = StringField('First Name', validators=[validators.InputRequired(), validators.Regexp('^[A-Za-z]*$', message='Invalid characters in the name.'), validators.Length(min=1, message='Name cannot be empty.')])
    lname = StringField('Last Name', validators=[validators.InputRequired(), validators.Regexp('^[A-Za-z]*$', message='Invalid characters in the name.'), validators.Length(min=1, message='Name cannot be empty.')])
    email = StringField('Email', validators=[validators.InputRequired(), validators.Email(message='Invalid email address.')])
    password = PasswordField('Password', validators=[validators.InputRequired(), validators.Length(min=6, message='Password must be at least 6 characters.')])
    confirm_password = PasswordField('Confirm Password', validators=[validators.EqualTo('password', message='Passwords must match.')])

class LoginForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])

class DeleteAccountForm(FlaskForm):
    submit = SubmitField("Delete Account")

class Meals(db.Model):
    __tablename__ = 'meals'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    meal_date = db.Column(db.Date, nullable=False)
    meal_type = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    calories = db.Column(db.Float)
    protein = db.Column(db.Float)
    carbohydrates = db.Column(db.Float)
    fats = db.Column(db.Float)
    created_at = db.Column(db.TIMESTAMP)

    def __init__(self, user_id, meal_type, description, calories, protein, carbohydrates, fats):
        self.user_id = user_id
        self.meal_date = datetime.now().date()
        self.meal_type = meal_type
        self.description = description
        self.calories = calories
        self.protein = protein
        self.carbohydrates = carbohydrates
        self.fats = fats
        self.created_at = datetime.now()

class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __init__(self, id, name, email, message):
        self.id = id
        self.name = name
        self.email=email
        self.message = message

def load_user(user_id):
    user = User.query.get(int(user_id))
    print(f"Loading user: {user_id}")
    return User.query.get(int(user_id))

@app.route('/health')
def health_check():
    return 'OK', 200

@app.route('/')
def home():
    form = LoginForm()
    return render_template('index.html', form=form)

@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    return render_template('calculator.html')

recipe_data = pd.read_csv('recipe_data.csv', encoding = 'ISO-8859-1')

ITEMS_PER_PAGE = 20  # Number of recipes per page
PAGE_BUTTONS = 12   # Number of page buttons to show

def filter_and_paginate_recipes(page, items_per_page=ITEMS_PER_PAGE, dietary_filter=None, course_filter=None):
    # Apply filters based on dietary preference and course
    recipe_data = pd.read_csv('recipe_data.csv', encoding = 'ISO-8859-1')
    
    print("Dietary Filter:", dietary_filter)
    print("Course Filter:", course_filter)
    filtered_data = recipe_data.copy()  # Create a copy of the original DataFrame
    filtered_data['Dietary Types'] = filtered_data['Dietary Types'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    filtered_data['Meal Types'] = filtered_data['Meal Types'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    
    # Define the check_dietary_types function
    def check_dietary_types(types, dietary_filter):
        if isinstance(types, list):
            if "all" in dietary_filter:
                return True  # "All" option selected, so all recipes should pass
            return any(diet.lower() in [item.lower() for item in types] for diet in dietary_filter)
        else:
            return False
    # Define the check_meal_types function
    def check_meal_types(types, course_filter):
        if isinstance(types, list):
            if "all" in course_filter:
                return True  # "All" option selected, so all recipes should pass
            return any(course.lower() in [item.lower() for item in types] for course in course_filter)
        else:
            return False

    if dietary_filter:
        filtered_data = filtered_data[filtered_data['Dietary Types'].apply(lambda x: check_dietary_types(x, dietary_filter))]

    # Debugging: Print the number of rows after dietary filtering
    print("Number of Rows in filtered_data after Dietary Filter:", len(filtered_data))

    if course_filter:
        filtered_data = filtered_data[filtered_data['Meal Types'].apply(lambda x: check_meal_types(x, course_filter))]

    # Debugging: Print the number of rows after meal type filtering
    print("Number of Rows in filtered_data after Meal Type Filter:", len(filtered_data))

    totalRecipes = len(filtered_data)
    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    recipes = filtered_data.iloc[start_idx:end_idx].to_dict(orient='records')

    return recipes, totalRecipes

# Add it to the Jinja2 environment
app.jinja_env.globals.update(filter_and_paginate_recipes=filter_and_paginate_recipes)

@app.route('/recipes', defaults={'page': 1})
@app.route('/recipes/<int:page>')
def recipes(page):
    dietary_filter = request.args.getlist('dietary_filter')
    course_filter = request.args.getlist('course_filter')

    # Print the selected dietary and course filters
    print("Selected Dietary Filter:", dietary_filter)
    print("Selected Course Filter:", course_filter)

    recipes, totalRecipes = filter_and_paginate_recipes(page, dietary_filter=dietary_filter, course_filter=course_filter)
    totalPages = (totalRecipes + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

    print("Total Number of Recipes:", totalRecipes)
    first_five_recipe_ids = [recipe['recipe_id'] for recipe in recipes[:5]]
    print("First Five Recipe IDs:", first_five_recipe_ids)

    # Calculate the first and last pages for the current set of 12 buttons
    items_per_page_set = PAGE_BUTTONS
    current_set = (page - 1) // items_per_page_set
    first_page_in_set = current_set * items_per_page_set + 1
    last_page_in_set = min(first_page_in_set + items_per_page_set - 1, totalPages)

    return render_template(
        'recipes.html',
        recipes=recipes,
        page=page,
        totalRecipes=totalRecipes,
        totalPages=totalPages,
        page_buttons=items_per_page_set,
        first_page_in_set=first_page_in_set,
        last_page_in_set=last_page_in_set,
        current_set=current_set,
        dietary_filter=dietary_filter,
        course_filter=course_filter
    )

def load_recipe_details(recipe_id):
    with open('recipe_data.csv', 'r', encoding='ISO-8859-1') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if int(row['recipe_id']) == recipe_id:
                return row
    return None

def load_dietary_and_meal_types(recipe_id):
    with open('recipe_data.csv', 'r', encoding='ISO-8859-1') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if int(row['recipe_id']) == recipe_id:
                dietary_types_str = row['Dietary Types']
                meal_types_str = row['Meal Types']
                dietary_types = ast.literal_eval(dietary_types_str) if dietary_types_str else []
                meal_types = ast.literal_eval(meal_types_str) if meal_types_str else []
                
                return dietary_types, meal_types
    return None, None

def parse_time(time_str):
    if time_str:
        minutes = int(time_str)
        if minutes == 0:
            return "--"  # Display "--" for 0 minutes
        elif minutes < 60:
            return f"{minutes} min"  # Display only minutes if less than 60 minutes
        else:
            hours = minutes // 60
            remaining_minutes = minutes % 60
            if remaining_minutes == 0:
                return f"{hours} hr"  # Display only hours if no remaining minutes
            else:
                return f"{hours} hr {remaining_minutes} min"  # Display hours and remaining minutes
    else:
        return ""
    
def filter_recipe(recipe):
    # Get the selected filters from the form or request
    selected_meal_type = request.args.get('meal_type')
    selected_dietary_type = request.args.get('dietary_type')

    # Check if the recipe matches the selected filters
    if selected_meal_type and selected_meal_type not in recipe['Meal Types']:
        return False
    if selected_dietary_type and selected_dietary_type not in recipe['Dietary Types']:
        return False

    return True

app.jinja_env.globals.update(filter_recipe=filter_recipe)

@app.route('/recipe/<int:recipe_id>')
def view_recipe(recipe_id):
    # Load the recipe details from the CSV file based on the recipe_id
    recipe_details = load_recipe_details(recipe_id)

    if recipe_details:
        # Convert the string representation of ingredients to a Python list
        ingredients_str = recipe_details['Ingredients']
        ingredients_list = ast.literal_eval(ingredients_str)
        
        # Pass the list of ingredients to the template
        recipe_details['Ingredients'] = ingredients_list

        # Convert the string representation of steps to a Python list
        steps_str = recipe_details['steps']
        steps_list = ast.literal_eval(steps_str)
        
        # Pass the list of steps to the template
        recipe_details['steps'] = steps_list
        
        # Get dietary types and meal types
        dietary_types, meal_types = load_dietary_and_meal_types(recipe_id)

        # Pass dietary types and meal types to the template
        recipe_details['Dietary Types'] = dietary_types
        recipe_details['Meal Types'] = meal_types

        # Fetch additional nutritional information
        recipe_details['Calories'] = recipe_details.get('Calories', '--')
        recipe_details['Protein'] = recipe_details.get('Protein', '--')
        recipe_details['Carbohydrates'] = recipe_details.get('Carbohydrate', '--')
        recipe_details['Fats'] = recipe_details.get('Fat', '--')
        recipe_details['Serving Size'] = recipe_details.get('Serving Size', '--')

        # Parse prep time and cook time
        prep_time = parse_time(recipe_details['Prep Time'])
        cook_time = parse_time(recipe_details['Cook Time'])

        # Update the recipe dictionary with parsed times
        recipe_details['Prep Time'] = prep_time
        recipe_details['Cook Time'] = cook_time

        return render_template('viewrecipe.html', recipe=recipe_details)
    else:
        return 'Recipe not found'
    
@app.route('/food-log')
def logs():
    totals = {
        'calories': 0,
        'total_carbohydrates': 0,
        'protein': 0,
        'total_fat': 0
    }
    # Add code to render the recipes page here
    return render_template('logs.html', totals=totals)

@app.route('/process-meals', methods=['POST', 'GET'])
def process_meals():
    meal_descriptions = {
        'breakfast_description': request.form.getlist('breakfast_description'),
        'morningSnack_description': request.form.getlist('morningSnack_description'),
        'lunch_description': request.form.getlist('lunch_description'),
        'eveningSnack_description': request.form.getlist('eveningSnack_description'),
        'dinner_description': request.form.getlist('dinner_description')
    }
    nutritional_info = []

    # Set your API key for the api-ninjas API
    api_key = os.environ.get('API_KEY')

    meal_names = ['Breakfast', 'Morning Snack', 'Lunch', 'Evening Snack', 'Dinner']

    for i, meal_type in enumerate(meal_descriptions.keys()):
        meal_name = meal_names[i]
        foods = []
        
        for description in meal_descriptions[meal_type]:
            try:
                query = description
                api_url = f'https://api.api-ninjas.com/v1/nutrition?query={query}'
                response = requests.get(api_url, headers={'X-Api-Key': api_key})
                
                if response.status_code == requests.codes.ok:
                    data = response.json()
                    for item in data:
                        name = item.get("name")
                        if name.lower() in description.lower():
                            food_info = {
                                'name': name,
                                'total_fat': item.get("fat_total_g"),
                                'total_carbohydrates': item.get("carbohydrates_total_g"),
                                'protein': item.get("protein_g"),
                                'calories': item.get("calories"),
                                'serving_size_g': item.get("serving_size_g"),
                                'fiber': item.get("fiber_g"),
                                'sugar': item.get("sugar_g"),
                                'cholesterol': item.get("cholesterol_mg"),
                                'fat_saturated': item.get("fat_saturated_g"),
                                'potassium': item.get("potassium_mg"),
                                'sodium': item.get("sodium_mg")
                            }
                            foods.append(food_info)
                else:
                    foods.append({
                        'error': f'Request failed for {description}: {response.status_code} {response.text}'
                    })
            except Exception as e:
                foods.append({
                    'error': f'Error for {description}: {str(e)}'
                })
        nutritional_info.append({'mealName': meal_name, 'foods': foods})

    # Calculate totals
    totals = {
        'calories': 0,
        'total_carbohydrates': 0,
        'protein': 0,
        'total_fat': 0
    }

    for meal in nutritional_info:
        for food in meal['foods']:
            totals['calories'] += food['calories']
            totals['total_carbohydrates'] += food['total_carbohydrates']
            totals['protein'] += food['protein']
            totals['total_fat'] += food['total_fat']

    for key in totals:
        totals[key] = round(totals[key], 2)

    # Generate the table using tabulate
    table = []
    for meal in nutritional_info:
        for food in meal['foods']:
            table.append([meal['mealName'], food['name'], food['calories'], food['total_fat'],
                          food['total_carbohydrates'], food['protein'], food['serving_size_g'],
                          food['fiber'], food['sugar'], food['cholesterol'], food['fat_saturated'],
                          food['potassium'], food['sodium']])

    table_html = tabulate(table, headers=["Meal Name", "Name", "Calories", "Total Fat (g)", "Total Carbohydrates (g)",
                                          "Protein (g)", "Serving Size (g)", "Fiber (g)", "Sugar (g)", "Cholesterol (mg)",
                                          "Saturated Fat (g)", "Potassium (mg)", "Sodium (mg)"], tablefmt="html")

    df = pd.DataFrame(table, columns=["Meal Name", "Name", "Calories", "Total Fat (g)", "Total Carbohydrates (g)",
                                  "Protein (g)", "Serving Size (g)", "Fiber (g)", "Sugar (g)", "Cholesterol (mg)",
                                  "Saturated Fat (g)", "Potassium (mg)", "Sodium (mg)"])

    # Create a DataFrame with the desired fields as a single row
    fields_order = ["Meal Name", "Name", "Calories", "Total Fat (g)", "Total Carbohydrates (g)",
                    "Protein (g)", "Serving Size (g)", "Fiber (g)", "Sugar (g)", "Cholesterol (mg)",
                    "Saturated Fat (g)", "Potassium (mg)", "Sodium (mg)"]
    fields_df = pd.DataFrame([fields_order], columns=df.columns)

    # Concatenate the fields DataFrame with the original DataFrame
    final_df = pd.concat([fields_df, df])

    # Transpose the DataFrame
    transposed_df = final_df.transpose()
    # Remove the second column from the transposed DataFrame
    transposed_df = transposed_df.iloc[:, 1:]

    # Convert the transposed DataFrame to an HTML table
    transposed_table_html = transposed_df.to_html(header=False)
    return render_template('logs.html', table_html=table_html, transposed_table_html=transposed_table_html, totals = totals)

@app.route('/lifestyle-disorders')
def disorders():
    # Add code to render the recipes page here
    return render_template('lifestyle.html')

@app.route('/diabetes')
def diabetes():
    # Add code to render the recipes page here
    return render_template('diabetes.html')

@app.route('/hypertension')
def bp():
    # Add code to render the recipes page here
    return render_template('bp.html')

@app.route('/cancer')
def cancer():
    # Add code to render the recipes page here
    return render_template('cancer.html')

@app.route('/PCOD')
def pcod():
    # Add code to render the recipes page here
    return render_template('pcod.html')

@app.route('/heart-attack')
def heart():
    # Add code to render the recipes page here
    return render_template('heart-attack.html')

@app.route('/thyroid')
def thyroid():
    # Add code to render the recipes page here
    return render_template('thyroid.html')

@app.route('/fatty-liver')
def liver():
    # Add code to render the recipes page here
    return render_template('fatty-liver.html')

@app.route('/obesity')
def obesity():
    # Add code to render the recipes page here
    return render_template('obesity.html')

@app.route('/blog')
def blog():
    # Add code to render the recipes page here
    return render_template('#')

@app.route('/about-us')
def about():
    # Add code to render the recipes page here
    return render_template('about.html')

@app.route('/privacy-policy-&-terms-of-service')
def privacy():
    return render_template('privacy.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(user_id=None, fname=form.fname.data, lname=form.lname.data, email=form.email.data, password=hashed_password)

        try:
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created!', 'success')
            return redirect(url_for('login'))
        except IntegrityError as e:
            db.session.rollback()  # Rollback the transaction on error
            if 'Duplicate entry' in str(e):
                flash('An account is already registered with this email address. Please use a different email.', 'danger')
            else:
                flash(f'Error: {str(e)}', 'danger')
        except Exception as e:
            db.session.rollback()  # Rollback the transaction on error
            flash(f'Error: {str(e)}', 'danger')
        except OperationalError as e:
            db.session.rollback()
            flash('An operational error occurred. Please try again later.', 'danger')
        except DataError as e:
            db.session.rollback()
            flash('There was an issue with the data. Please ensure your information is correct and try again.', 'danger')
        except ProgrammingError as e:
            db.session.rollback()
            flash('A programming error occurred. Please contact support for assistance.', 'danger')
        except Exception as e:
            db.session.rollback()
            flash('An unexpected error occurred. Please try again or contact support.', 'danger')

    return render_template('signup.html', title='Sign Up', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):         
            session['user_id'] = user.user_id
            session['user_fname'] = user.fname
            session['user_lname'] = user.lname
            with app.test_request_context():
                request.session = session
                flash('Login successful!', 'success')
                request.session = None
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/delete-account-confirmation', methods=['GET', 'POST'])
def delete_account():
    print("Delete Account route accessed")  # Debugging line
    form = DeleteAccountForm()

    if form.validate_on_submit() and request.method == 'POST':
        user = User.query.get(session['user_id'])
        
        try:
            # Attempt to delete the user's account
            db.session.delete(user)
            db.session.commit()
            # Clear any existing flash messages
            # Log the user out after successful deletion
            session.pop('user_id', None)  # Remove user_id from the session
            with app.test_request_context():
                request.session = session
                flash('Your account has been deleted.', 'success')
                request.session = None

            return redirect(url_for('login'))  # Redirect to the login page
        except Exception as e:
            print(f"Error: {str(e)}")
            flash(f'Error: {str(e)}', 'danger')

    return render_template('delete_account.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    with app.test_request_context():
        request.session = session
        flash('Signup successful!', 'success')
        request.session = None
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=False, port = 8000, host = "0.0.0.0")

with app.app_context():
    db.create_all()  # Create database tables