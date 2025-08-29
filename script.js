var searchForm = document.getElementById("searchForm");
var searchInput = document.getElementById("searchInput");
var submitBtn = document.getElementById("submitBtn");
var closeSearchBtn = document.getElementById("closeSearchBtn");
var moviesGrid = document.getElementById("movies-grid");
var loadMoreBtn = document.getElementById("load-more-movies-btn");
var movieDiv = document.getElementById("movieDiv");
let currentPage = 1;
let searchTerm = '';

//Instead of repeating process, create function for movie cards
function createMovieCard(movie) {
    const movieCard = document.createElement("div");
    movieCard.classList.add("movie-card");

    const img = document.createElement("img");
    img.classList.add("movie-poster");
    const path = "http://image.tmdb.org/t/p/w154";
    img.src = path + movie.poster_path;
    movieCard.appendChild(img);

    const title = document.createElement("h3");
    title.classList.add("movie-title");
    title.textContent = movie.title;
    movieCard.appendChild(title);

    const votes = document.createElement("p");
    votes.classList.add("movie-votes");
    votes.textContent = `⭐ ${movie.vote_average}`;
    movieCard.appendChild(votes);

    movieCard.addEventListener("click", () => {
        showMovieDetails(movie);
    });

    return movieCard;

}

//function to display result based on search
submitBtn.addEventListener("click", async (event) => {
    event.preventDefault(); // Prevent form submission (optional)

    try {
        const apiKey = "26a8b5e8111d2b3fd500afd21defd060";
        searchTerm = searchInput.value;
        const url = `https://api.themoviedb.org/3/search/movie?api_key=${apiKey}&query=${(searchTerm)}`; //searchTerm is what is taken in from the user's input

        const response = await fetch(url);                   // response is a string. "{movies: ["tile": "John Wick"]}"
        const container = await response.json();
        const movie_temp = container.results;

        moviesGrid.innerHTML = ''; //clears prev movie cards

        movie_temp.forEach(movie => {
            const movieCard = createMovieCard(movie);        //creates a Div element in (thru js) for each movie card
            moviesGrid.appendChild(movieCard);
        });

        searchInput.value = '';
        console.log(container);

        // Process the data returned from the API
    } catch (error) {
        // Handle any errors that occur during the fetch request
        console.log(error);
    }

    // Perform your desired action here
    console.log("Button clicked!");
})

//Function to display movies for a specific page
async function displayMovies(page) {
    try {
        const apiKey = "26a8b5e8111d2b3fd500afd21defd060";
        let url = '';

        if (searchTerm === '') {
            url = `https://api.themoviedb.org/3/movie/now_playing?api_key=${apiKey}&page=${page}`;
        } else {
            url = `https://api.themoviedb.org/3/search/movie?api_key=${apiKey}&query=${(searchTerm)}`;
        }

        const response = await fetch(url);
        const data = await response.json();
        const movies = data.results;

        movies.forEach(movie => {
            const movieCard = createMovieCard(movie);
            moviesGrid.appendChild(movieCard);
        });


    } catch (error) {
        console.log(error);
    }
}


closeSearchBtn.addEventListener("click", () => {
    currentPage = 1
    moviesGrid.innerHTML = "";
    displayAllPictures();
});


// Function to display all pictures by default
async function displayAllPictures() {
    try {
        const apiKey = "26a8b5e8111d2b3fd500afd21defd060";
        const url = `https://api.themoviedb.org/3/movie/now_playing?api_key=${apiKey}&page=${currentPage}`;

        const response = await fetch(url);
        const container = await response.json();
        const movie_temp = container.results;

        movie_temp.forEach(movie => {
            const movieCard = createMovieCard(movie);            //Each movie will have its movie card in a div
            moviesGrid.appendChild(movieCard);                   //append each card(with complete detail) to the Grids
        });

        //   movieDiv.appendChild(moviesGrid);                   //fit all complete grids into the div
        console.log(container);
        currentPage++
    } catch (error) {
        console.log(error);
    }
}

// Call the displayAllPictures function to show all pictures by default
displayAllPictures();


// Event listener for the "Load More" button

loadMoreBtn.addEventListener("click", (event) => {
    event.preventDefault();
    displayAllPictures();
});

function showMovieDetails(movie) {
    const movieDetails = `Title: ${movie.title}\n\nOverview: ${movie.overview}\n\nPopularity : ${movie.popularity}`;
    alert(movieDetails);
}