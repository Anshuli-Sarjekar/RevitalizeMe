console.log("JavaScript code executed");

document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM is fully loaded.");
    const pageBoxes = document.getElementById("page-boxes");
    const pageButtons = pageBoxes.getElementsByClassName("page-button");
    const previousButton = document.getElementById("previous-button");
    const nextButton = document.getElementById("next-button");

    const itemsPerPage = 20;
    let currentPage = 1;
    let totalRecipes = 1042; // Total number of recipes

    function showRecipes(start, end) {
        // Hide all recipe cards
        const recipeCards = document.getElementsByClassName("recipe-card");
        for (let i = 0; i < recipeCards.length; i++) {
            recipeCards[i].style.display = "none";
        }

        // Show the recipes for the current page
        for (let i = start; i < end; i++) {
            recipeCards[i].style.display = "block";
        }
    }

    function updatePagination() {
        const totalPages = Math.ceil(totalRecipes / itemsPerPage);

        previousButton.disabled = currentPage === 1;
        nextButton.disabled = currentPage === totalPages;

        const start = (currentPage - 1) * itemsPerPage;
        const end = Math.min(start + itemsPerPage, totalRecipes);

        showRecipes(start, end);
    }

    // Attach event listeners to the elements using class or data attributes
    const pageButtonElements = document.querySelectorAll(".page-button");

    pageButtonElements.forEach(function (button) {
        button.addEventListener("click", function () {
            const page = parseInt(button.dataset.page);
            goToPage(page);
            console.log("Button clicked:", page);
        });
    });

    previousButton.addEventListener("click", function () {
        if (currentPage > 1) {
            currentPage--;
            updatePagination();
        }
    });

    nextButton.addEventListener("click", function () {
        const totalPages = Math.ceil(totalRecipes / itemsPerPage);
        if (currentPage < totalPages) {
            currentPage++;
            updatePagination();
        }
    });

    function goToPage(page) {
        console.log('goToPage called with page:', page);
        if (page >= 1 && page <= Math.ceil(totalRecipes / itemsPerPage)) {
            currentPage = page;
            updatePagination();
        }
    }

    // Add an event listener for the "View Recipe" buttons
    const viewRecipeButtons = document.querySelectorAll(".view-recipe-button");
    viewRecipeButtons.forEach(function (button) {
        button.addEventListener("click", function (event) {
            // Handle the button click event here
            event.preventDefault();  // Prevent the default link behavior
            const recipeId = button.dataset.recipeId;  // You can use data attributes to store the recipe ID
            // Implement the logic to show the full recipe details using the recipeId
            // You can use AJAX to load the recipe details or navigate to the recipe page
        });
    });

    showRecipes(0, itemsPerPage);
    updatePagination();
});
