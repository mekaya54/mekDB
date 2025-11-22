import { initNavbar } from "../components/navbar.js";
import { getQueryParam } from "../utils/router.js";
import { fetchMovieDetails, rateMovie } from "../api/movies.api.js";

document.addEventListener("DOMContentLoaded", async () => {
    initNavbar();

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

    if (overviewEl) overviewEl.innerHTML = "<span class='loading-text'>Loading details...</span>";

    try {
        const data = await fetchMovieDetails(id);
        const movie = data.movie || data;

        if (titleEl) titleEl.textContent = movie.primary_title || "Untitled";
        
        if (posterEl) {
            posterEl.src = movie.poster_url || "https://via.placeholder.com/500x750?text=No+Poster";
            posterEl.onerror = () => { posterEl.src = "https://via.placeholder.com/500x750?text=Image+Error"; };
        }

        const heroSection = document.getElementById("movie-hero");
        if (heroSection && movie.poster_url) {
            heroSection.style.backgroundImage = `linear-gradient(to bottom, rgba(18,18,18,0.85), var(--bg-color)), url('${movie.poster_url}')`;
        }

        if (submetaEl) {
            const year = movie.start_year || "N/A";
            const runtime = movie.runtime_minutes ? `${movie.runtime_minutes} min` : "";
            const adult = movie.is_adult ? "<span class='meta-tag'>18+</span>" : "";
            submetaEl.innerHTML = `<span>${year}</span> • <span>${runtime}</span> ${adult}`;
        }

        if (genresEl && movie.genres && movie.genres.length) {
            genresEl.innerHTML = movie.genres.map(g => `<span class="genre-tag">${g}</span>`).join("");
        }

        if (overviewEl) {
            overviewEl.textContent = movie.overview || movie.plot || "No overview available.";
        }

        if (castEl && data.cast && Array.isArray(data.cast)) {
            castEl.innerHTML = "";
            if (data.cast.length === 0) castEl.innerHTML = "<p class='text-muted'>No cast information.</p>";
            
            data.cast.forEach((person) => {
                const card = createPersonCard(person, "actor");
                castEl.appendChild(card);
            });
        }

        if (crewEl && data.crew && Array.isArray(data.crew)) {
            crewEl.innerHTML = "";
            if (data.crew.length === 0) crewEl.innerHTML = "<p class='text-muted'>No crew information.</p>";

            data.crew.forEach((person) => {
                const card = createPersonCard(person, "crew");
                crewEl.appendChild(card);
            });
        }

        if (ratingsEl) {
            const avg = movie.average_rating || (data.ratings && data.ratings.average_rating);
            const votes = movie.num_votes || (data.ratings && data.ratings.num_votes);
            
            if (avg) {
                ratingsEl.innerHTML = `
                    <div class="rating-display-big">
                        <span class="rating-star-icon">★</span>
                        <span class="rating-value">${avg}</span>
                        <span class="rating-max">/10</span>
                    </div>
                    <div class="rating-votes">${votes ? votes.toLocaleString() : 0} votes</div>
                `;
            } else {
                ratingsEl.innerHTML = "<p class='text-muted'>Not rated yet.</p>";
            }
        }

        if (starsBox) {
            initUserRatingStars(starsBox, hintEl, id);
        }

    } catch (err) {
        console.error(err);
        if (titleEl) titleEl.textContent = "Error loading movie";
        if (overviewEl) overviewEl.textContent = "Could not load movie details. Please try again later.";
    }
});

function createPersonCard(person, type) {
    const div = document.createElement("div");
    div.className = "person-card";
    
    const initials = person.name ? person.name.split(" ").map(n=>n[0]).join("").slice(0,2) : "??";
    
    let subText = "";
    if (type === "actor") {
        subText = person.characters || "Actor";
    } else {
        subText = person.job || person.category || "Crew";
    }

    div.innerHTML = `
        <div class="person-avatar-small">${initials}</div>
        <div class="person-info">
            <div class="person-name">${person.name}</div>
            <div class="person-role">${subText}</div>
        </div>
    `;

    div.addEventListener("click", () => {
        if (person.person_id) {
            window.location.href = `person.html?id=${encodeURIComponent(person.person_id)}`;
        }
    });

    return div;
}

function initUserRatingStars(container, hintEl, movieId) {
    container.innerHTML = "";
    const current = 0;

    for (let i = 1; i <= 10; i++) {
        const span = document.createElement("span");
        span.className = "rating-star-ui";
        span.innerHTML = "★";
        span.dataset.value = String(i);

        span.addEventListener("mouseenter", () => {
            updateStarsUI(container, i);
            if (hintEl) hintEl.textContent = `Rate: ${i}/10`;
        });

        span.addEventListener("mouseleave", () => {
            updateStarsUI(container, current);
            if (hintEl) hintEl.textContent = "";
        });

        span.addEventListener("click", async () => {
            try {
                await rateMovie(movieId, i);

                alert(`You rated this ${i}/10!`);
            } catch (err) {
                alert("Error saving rating.");
            }
        });

        container.appendChild(span);
    }
}

function updateStarsUI(container, value) {
    const stars = Array.from(container.querySelectorAll(".rating-star-ui"));
    stars.forEach((star, idx) => {
        if (idx < value) star.classList.add("active");
        else star.classList.remove("active");
    });
}