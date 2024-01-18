# RevitalizeMe
Welcome to the RevitalizeMe website repository! 🌐✨ Our platform is a holistic health and fitness hub designed to support your well-being in a personalized and user-friendly way.

## Features
- Macronutrients & BMR Calculator:
  Optimize your nutrition by calculating your Basal Metabolic Rate (BMR) for personalized MacroNutrient distribution and calorie requirements. Achieve your fitness goals with customized macronutrient distribution.
- Healthy Recipes:
  Explore a diverse collection of delicious, nutritious recipes tailored to various dietary preferences and course. Whether you are vegan, gluten-free, or seeking low-sodium options, find meals for every taste.
- Calorie & Nutrient Tracking:
  Empower mindful eating through easy meal recording. Track macronutrients, calories, cholesterol, fibre, sugar, sodium, and potassium, gaining insights for a balanced diet.
- Lifestyle Disorders:
  Master your health by making informed choices. Understand and prevent lifestyle disorders like diabetes and heart attack through balanced nutrition, regular exercise, stress management, and healthy habits.
Embark on a journey to a healthier, happier you! 🚀💪

## Repository Information
This repository hosts the code and resources driving our mission. Explore, contribute, and enhance the experience for our community. Your journey to optimal health starts here.

## Author
- Anshuli Sarjekar
  - Contact: 
    -[sarjekaranshuli@gmail.com](Mail to: sarjekaranshuli@gmail.com)

## Acknowledgements
- Special thanks to [API Ninja]( https://api-ninjas.com/api/nutrition) for providing the Nutrition API, which was instrumental in extracting nutritional and calorie information for this project. The API played a crucial role in enhancing the functionality and user experience of our application. We appreciate the valuable service and support provided by API Ninja.
-We are grateful to the creators and communities behind the programming languages and platforms that power this project:
  - [Python](https://www.python.org/): The primary language used for development.
  - HTML, CSS, and JavaScript: The trio of frontend technologies that allowed us to create a dynamic and visually appealing user interface. Special thanks to the creators of these fundamental web technologies.
 -  Flask Framework: The backbone of our server-side logic, making it easy to develop robust and scalable web applications in Python.
- Clone this repository to your local machine.
- Explore the codebase and contribute to our mission.

## Requirements
- To set up the project locally, refer to the instructions in [requirements.txt](requirements.txt).

## How to run?
- Ensure that you have your own API key for API-Ninja database access required in app.py. 
- You have setup to any RDBMS (get hostname, root, password) for flask SQLAlchemy connection(defined as db in app.py)
- The API key and databse details are mentioned in the .env file which can be directly defined in the app.py(For me it is stored in .env file).
- I have a recipes data that I obtained from web scraping and NLP based text transformation techniques using Parrot Library. Yu can create your own recipes data. The columns of these are: recipe_id, Recipe Name,	Prep Time,	Cook Time,	Meal Types,	Dietary Types,	Calories,	Fat,	Carbohydrate,	Protein,	Ingredients,	steps,	Serving Size.
- Once all the above is set, you can run app.py and look up to the RevitalizeMe website.

The purpose of this project is purely academic and educational, aimed at showcasing knowledge and practical application of web development principles for educational purposes only.
Clone this repository, and let's build a better, balanced world together! 🌍👩‍💻👨‍💻

