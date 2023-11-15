// Function to change the displayed recipes based on the selected page
// Function to generate the page buttons
function generatePageButtons(totalPages) {
    const pageBoxes = document.getElementById("page-boxes");
    pageBoxes.innerHTML = ''; // Clear the existing buttons

    for (let i = 1; i <= totalPages; i++) {
        const pageButton = document.createElement("div");
        pageButton.className = "page-button";
        pageButton.setAttribute("data-page", i);
        pageButton.textContent = i;
        pageButton.onclick = function () {
            changePage(i);
        };

        pageBoxes.appendChild(pageButton);
    }
}

// Initial display of the first page
changePage(1);

// You can update the total pages from your data, e.g., totalRecipes / itemsPerPage
const totalRecipes = 1042;
const itemsPerPage = 20;
const totalPages = Math.ceil(totalRecipes / itemsPerPage);

// Generate the page buttons
generatePageButtons(totalPages);

function changePage(page) {
    const pageButtons = document.getElementsByClassName("page-button");
    const itemsPerPage = 20; // Number of recipes per page
    const start = (page - 1) * itemsPerPage;
    const end = start + itemsPerPage;

    // Hide all recipes
    const recipes = document.querySelectorAll(".recipe-card");
    recipes.forEach(function (recipe) {
        recipe.style.display = "none";
    });

    // Show the recipes for the selected page
    for (let i = start; i < end; i++) {
        if (recipes[i]) {
            recipes[i].style.display = "block";
        }
    }
}

// Initial display of the first page
changePage(1);

// Pagination button click handlers
const previousButton = document.getElementById("previous-button");
const nextButton = document.getElementById("next-button");

previousButton.addEventListener("click", function () {
    const pageButtons = document.getElementsByClassName("page-button");
    let currentPage = 1;

    for (let i = 0; i < pageButtons.length; i++) {
        if (pageButtons[i].style.display === "inline-block") {
            currentPage = parseInt(pageButtons[i].getAttribute("data-page"));
            break;
        }
    }

    if (currentPage > 1) {
        changePage(currentPage - 1);
    }
});

nextButton.addEventListener("click", function () {
    const pageButtons = document.getElementsByClassName("page-button");
    let currentPage = 1;

    for (let i = 0; i < pageButtons.length; i++) {
        if (pageButtons[i].style.display === "inline-block") {
            currentPage = parseInt(pageButtons[i].getAttribute("data-page"));
            break;
        }
    }

    const totalPages = pageButtons.length;
    if (currentPage < totalPages) {
        changePage(currentPage + 1);
    }
});
