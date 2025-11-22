import { initNavbar } from "../components/navbar.js";
import { fetchProfile } from "../api/auth.api.js";
import { fetchMyRatings } from "../api/profile.api.js";
import { createMovieCard } from "../components/movieCard.js";
import { getToken } from "../utils/storage.js";
import { goTo } from "../utils/router.js";

document.addEventListener("DOMContentLoaded", async () => {
    initNavbar();

    const token = getToken();
    if (!token) {
        goTo("login.html");
        return;
    }

    const usernameEl = document.getElementById("profile-username");
    const emailEl = document.getElementById("profile-email");
    const ratingsContainer = document.getElementById("profile-ratings");

    try {
        const profile = await fetchProfile();
        if (profile) {
            if (usernameEl && profile.username) usernameEl.textContent = profile.username;
            if (emailEl && profile.email) emailEl.textContent = profile.email;
        }
    } catch {}

    if (!ratingsContainer) return;

    ratingsContainer.innerHTML = "Loading...";

    try {
        const ratings = await fetchMyRatings();
        ratingsContainer.innerHTML = "";

        if (!ratings || ratings.length === 0) {
            ratingsContainer.textContent = "You have not rated any titles yet.";
            return;
        }

        ratings.forEach((item) => {
            const movieData = { ...item };
            if (item.user_rating && !item.average_rating) {
                movieData.average_rating = item.user_rating;
            }
            const card = createMovieCard(movieData);
            ratingsContainer.appendChild(card);
        });
    } catch (err) {
        ratingsContainer.textContent = err.message || "Ratings could not be loaded.";
    }
});
