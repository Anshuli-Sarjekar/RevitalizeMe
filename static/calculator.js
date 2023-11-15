// JavaScript for BMR and Macronutrient Calculator
document.getElementById("calculate-button").addEventListener("click", calculateBMR);

function displayError(message) {
    // Display error message in the designated error message div
    document.getElementById("error-message").textContent = message;
}

function clearError() {
    document.getElementById("error-message").textContent = "";
}

function calculateBMR() {
    // Retrieve user input
    clearError();
    const gender = document.getElementById("gender").value;
    const age = parseInt(document.getElementById("age").value);
    const weight = parseFloat(document.getElementById("weight").value);
    const height = parseFloat(document.getElementById("height").value);
    const activityLevel = document.getElementById("activity-level").value;
    const fitnessGoal = document.getElementById("fitness-goal").value;

    if (isNaN(age) || isNaN(weight) || isNaN(height) || gender === "" || activityLevel === "" || fitnessGoal === "") {
        displayError('Please fill in all fields and select your gender, activity level, and fitness goal.');
        return;
    }
    // Check for invalid or out-of-range values
    if (age < 1 || age > 150) {
        displayError('Invalid age. Please enter a valid age between 1 and 150.');
        return;
    }

    if (weight < 20 || weight > 500) {
        displayError('Invalid weight. Please enter a valid weight between 20 and 500.');
        return;
    }

    if (height < 50 || height > 300) {
        displayError('Invalid height. Please enter a valid height between 50 and 300.');
        return;
    }
    //Harris Benedict formula
    // Calculate BMR based on gender
    let bmr;
    if (gender === "male") {
        bmr = 66 + (13.7 * weight) + (5 * height) - (6.8 * age);
    } else if (gender === "female") {
        bmr = 655 + (9.6 * weight) + (1.8 * height) - (4.7 * age);
    }

    // Adjust BMR for activity level
    let calorieNeeds;
    switch (activityLevel) {
        case "sedentary":
            calorieNeeds = bmr * 0.8;
            break;
        case "lightly-active":
            calorieNeeds = bmr * 1.0;
            break;
        case "moderately-active":
            calorieNeeds = bmr * 1.2;
            break;
        case "very-active":
            calorieNeeds = bmr * 1.375;
            break;
        case "extra-active":
            calorieNeeds = bmr * 1.55;
            break;
        default:
            calorieNeeds = bmr;
    }
    let fatsPercentage;
    let proteinPercentage;
    let carbsPercentage;

    switch(fitnessGoal) {
        case "fat-loss":
            calorieNeeds = 0.8*calorieNeeds;
            carbsPercentage = 45;
            proteinPercentage = 30;
            fatsPercentage = 25;
            break;
        case "muscle-gain":
            carbsPercentage = 50;
            proteinPercentage = 20;
            fatsPercentage = 30; 
            break;
        case "weight-loss":
            calorieNeeds = 0.85*calorieNeeds;
            carbsPercentage = 45;
            proteinPercentage = 30;
            fatsPercentage = 25; 
            break;
        case "weight-gain":
            carbsPercentage = 55;
            proteinPercentage = 20;
            fatsPercentage = 25;
            break;
        case "general-fitness":
            calorieNeeds = 0.9*calorieNeeds;
            carbsPercentage = 50;
            proteinPercentage = 20;
            fatsPercentage = 30;
            break;
        default:
            carbsPercentage = 40;
            proteinPercentage = 30;
            fatsPercentage = 30;
    }

    const protein = (calorieNeeds * (proteinPercentage / 100)) / 4; // 4 calories per gram of protein
    const carbs = (calorieNeeds * (carbsPercentage / 100)) / 4; // 4 calories per gram of carbs
    const fats = (calorieNeeds * (fatsPercentage / 100)) / 9; // 9 calories per gram of fats

    // Calculate BMI
    const bmi = (weight / (height * height))*10000;

    // Display BMI result
    document.getElementById("bmi-result").textContent = bmi.toFixed(2);
    document.getElementById("bmr-result").textContent =  bmr.toFixed(0);
    document.getElementById("calorie-needs-result").textContent = calorieNeeds.toFixed(0);
    document.getElementById("protein-result").textContent = protein.toFixed(0) + " grams ";
    document.getElementById("carbs-result").textContent = carbs.toFixed(0) + " grams ";
    document.getElementById("fats-result").textContent = fats.toFixed(0) + " grams ";
}
