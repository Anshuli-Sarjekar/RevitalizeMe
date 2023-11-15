document.addEventListener("DOMContentLoaded", function () {
    const pageBoxes = document.getElementById("page-boxes");
    const pageButtons = pageBoxes.getElementsByClassName("page-button");
    const previousButton = document.getElementById("previous-button");
    const nextButton = document.getElementById("next-button");

    const itemsPerPage = 15; // Number of items (page buttons) per page
    let currentPage = 1;

    function showPage(page) {
        const start = (page - 1) * itemsPerPage;
        const end = Math.min(start + itemsPerPage, pageButtons.length);

        for (let i = 0; i < pageButtons.length; i++) {
            pageButtons[i].style.display = "none";
        }

        for (let i = start; i < end; i++) {
            pageButtons[i].style.display = "inline-block";
        }
    }

    // Initial display
    showPage(currentPage);

    previousButton.addEventListener("click", function () {
        if (currentPage > 1) {
            currentPage--;
            showPage(currentPage);
        }
    });

    nextButton.addEventListener("click", function () {
        const totalPages = Math.ceil(pageButtons.length / itemsPerPage);
        if (currentPage < totalPages) {
            currentPage++;
            showPage(currentPage);
        }
    });
});
