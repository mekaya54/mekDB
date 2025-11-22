import { initApp } from "../app.js";
import { initSearchBar } from "../components/searchbar.js";
import { getQueryParam } from "../utils/router.js";
import { fetchMovieDetails, rateMovie } from "../api/movies.api.js";

document.addEventListener("DOMContentLoaded", async () => {
    initApp();

    initSearchBar({
        placeholder: "Search titles",
        onSearch: () => {
            const input = document.getElementById("search-input");
            const q = input ? input.value.trim() : "";
            if (!q) return;
            window.location.href = `index.html?search=${encodeURIComponent(q)}`;
        }
    });

    const id = getQueryParam("id");
    if (!id) return;

    const titleEl = document.getElementById("movie-title");
    const posterEl = document.getElementById("movie-poster");
    const submetaEl = document.getElementById("movie-submeta");
    const genresEl = document.getElementById("movie-genres");
    const overviewEl = document.getElementById("movie-overview");
    const castEl = document.getElementById("movie-cast");
    const crewEl = document.getElementById("movie-crew");
    const ratingsEl = document.getElementById("movie-ratings");
    const starsBox = document.getElementById("user-rating-stars");
    const hintEl = document.getElementById("user-rating-hint");

    if (ratingsEl) ratingsEl.textContent = "Loading...";

    try {
        const data = await fetchMovieDetails(id);
        const movie = data.movie || data;

        if (titleEl && movie.primary_title) titleEl.textContent = movie.primary_title;
        if (posterEl && movie.poster_url) {
            posterEl.src = movie.poster_url;
        }
        if (submetaEl) {
            const year = movie.start_year || "N/A";
            const runtime = movie.runtime_minutes ? `${movie.runtime_minutes} min` : "Unknown runtime";
            submetaEl.textContent = `${year} • ${runtime}`;
        }
        if (genresEl && movie.genres && movie.genres.length) {
            genresEl.textContent = movie.genres.join(" • ");
        }
        if (overviewEl && movie.overview) {
            overviewEl.textContent = movie.overview;
        }

        if (castEl && data.cast && Array.isArray(data.cast)) {
            castEl.innerHTML = "";
            data.cast.forEach((person) => {
                const div = document.createElement("div");
                div.className = "person-item";
                div.textContent = person.name;
                div.addEventListener("click", () => {
                    if (person.person_id) {
                        window.location.href = `person.html?id=${encodeURIComponent(person.person_id)}`;
                    }
                });
                castEl.appendChild(div);
            });
        }

        if (crewEl && data.crew && Array.isArray(data.crew)) {
            crewEl.innerHTML = "";
            data.crew.forEach((person) => {
                const div = document.createElement("div");
                div.className = "person-item";
                const role = person.job || person.role || "";
                div.textContent = role ? `${person.name} (${role})` : person.name;
                div.addEventListener("click", () => {
                    if (person.person_id) {
                        window.location.href = `person.html?id=${encodeURIComponent(person.person_id)}`;
                    }
                });
                crewEl.appendChild(div);
            });
        }

        if (ratingsEl) {
            ratingsEl.innerHTML = "";
            const avg = movie.average_rating || (data.ratings && data.ratings.average_rating);
            const votes = movie.num_votes || (data.ratings && data.ratings.num_votes);
            const p = document.createElement("p");
            p.textContent = avg ? `Average rating: ${avg} (${votes || 0} votes)` : "No rating data.";
            ratingsEl.appendChild(p);
        }

        if (starsBox) {
            initUserRatingStars(starsBox, hintEl, id);
        }
    } catch (err) {
        if (ratingsEl) {
            ratingsEl.textContent = err.message || "Title details could not be loaded.";
        }
    }
});

function initUserRatingStars(container, hintEl, movieId) {
    container.innerHTML = "";
    const current = 0;

    for (let i = 1; i <= 10; i++) {
        const span = document.createElement("span");
        span.className = "rating-star";
        span.textContent = "★";
        span.dataset.value = String(i);

        span.addEventListener("mouseenter", () => {
            highlightStars(container, i);
            if (hintEl) hintEl.textContent = `${i}/10`;
        });

        span.addEventListener("mouseleave", () => {
            highlightStars(container, current);
            if (hintEl) hintEl.textContent = "";
        });

        span.addEventListener("click", async () => {
            try {
                await rateMovie(movieId, i);
                if (hintEl) hintEl.textContent = `Your rating has been saved: ${i}/10`;
            } catch (err) {
                if (hintEl) hintEl.textContent = err.message || "Your rating could not be saved.";
            }
        });

        container.appendChild(span);
    }
}

function highlightStars(container, value) {
    const stars = Array.from(container.querySelectorAll(".rating-star"));
    stars.forEach((star) => {
        const v = parseInt(star.dataset.value, 10);
        if (v <= value) {
            star.classList.add("active");
        } else {
            star.classList.remove("active");
        }
    });
}
