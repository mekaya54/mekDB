import { initNavbar } from "../components/navbar.js";
import { initSearchBar } from "../components/searchbar.js";
import { createMovieCard } from "../components/movieCard.js";
import { createPagination } from "../components/pagination.js";
import { apiGetHome, apiSearchMovies } from "../api/movies.api.js";
import { $ } from "../utils/dom.js";

initNavbar();

initSearchBar({
    wrapperId: "search-bar",
    placeholder: "Search titles",
    onSearch: () => loadSearch()
});

let currentFilter = "all";
let currentPage = 1;
let totalPages = 1;

function formatRuntime(minutes) {
    if (!minutes) return "N/A";
    const h = Math.floor(minutes / 60);
    const m = minutes % 60;
    return `${h}h ${m}m`;
}

function renderMovies(list) {
    const container = $("#movie-container");
    container.innerHTML = "";

    if (!list || list.length === 0) {
        container.innerHTML = "<p class='empty-text'>No results found.</p>";
        return;
    }

    list.forEach(m => {
        const card = createMovieCard(m);
        container.appendChild(card);
    });
}

async function loadHome() {
    const data = await apiGetHome();
    renderMovies(data.movies || []);
}

async function loadSearch() {
    const q = $("#search-input")?.value.trim() ?? "";
    const data = await apiSearchMovies(q, currentFilter, currentPage);

    renderMovies(data.results || []);
    totalPages = data.total_pages || 1;

    createPagination({
        containerId: "pagination-wrapper",
        currentPage,
        totalPages,
        onPageChange: (p) => {
            currentPage = p;
            loadSearch();
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    loadHome();
});
