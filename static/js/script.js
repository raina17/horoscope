// In static/js/script.js
document.getElementById('horoscope-form').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent the default form submission

    // Get form data
    const name = document.getElementById('name').value;
    const dob = document.getElementById('dob').value;
    const placeOfBirth = document.getElementById('placeOfBirth').value;
    const gender = document.getElementById('gender').value;

    // Show loader and results container
    const resultsContainer = document.getElementById('results-container');
    const loader = document.getElementById('loader');
    const horoscopeResultDiv = document.getElementById('horoscope-result');
    
    resultsContainer.style.display = 'block';
    loader.style.display = 'block';
    horoscopeResultDiv.innerHTML = ''; // Clear previous results

    try {
        // Send data to the backend API
        const response = await fetch('/generate-horoscope', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name, dob, placeOfBirth, gender }),
        });

        loader.style.display = 'none'; // Hide loader once response is received

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Something went wrong on the server.');
        }

        const data = await response.json();

        // Display the results
        horoscopeResultDiv.innerHTML = `
            <h2 class="text-center mb-4">Your Horoscope for ${name}</h2>
            <div class="card mb-3">
                <div class="card-header bg-primary text-white">
                    <strong>Daily Horoscope</strong>
                </div>
                <div class="card-body">
                    <p class="card-text">${data.daily}</p>
                </div>
            </div>
            <div class="card mb-3">
                <div class="card-header bg-success text-white">
                    <strong>Weekly Horoscope</strong>
                </div>
                <div class="card-body">
                    <p class="card-text">${data.weekly}</p>
                </div>
            </div>
            <div class="card">
                <div class="card-header bg-info text-white">
                    <strong>Monthly Horoscope</strong>
                </div>
                <div class="card-body">
                    <p class="card-text">${data.monthly}</p>
                </div>
            </div>
        `;

    } catch (error) {
        loader.style.display = 'none';
        horoscopeResultDiv.innerHTML = `
            <div class="alert alert-danger" role="alert">
                <strong>Error:</strong> ${error.message}
            </div>
        `;
    }
});