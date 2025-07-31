

document.addEventListener('DOMContentLoaded', function() {
    const symptomsListDiv = document.getElementById('symptomsList');
    const predictBtn = document.getElementById('predictBtn');
    const resetBtn = document.getElementById('resetBtn');

    const loadingSymptomsMsg = document.getElementById('loadingSymptoms');
    const errorSymptomsMsg = document.getElementById('errorSymptoms');
    const loadingPredictionMsg = document.getElementById('loadingPrediction');
    const errorPredictionMsg = document.getElementById('errorPrediction');

    const predictionResultDiv = document.getElementById('predictionResult');
    const predictedDiseaseSpan = document.getElementById('predictedDisease');
    const confidenceScoreSpan = document.getElementById('confidenceScore');
    const suggestionsSpan = document.getElementById('suggestions');

    let selectedSymptoms = new Set(); // Use a Set to store unique selected symptom names

    const API_BASE_URL = window.location.origin; // Dynamically get the base URL

    // --- Helper Functions ---
    function showElement(element) {
        element.style.display = 'block';
    }

    function hideElement(element) {
        element.style.display = 'none';
    }

    function clearPredictionResult() {
        predictedDiseaseSpan.textContent = '';
        confidenceScoreSpan.textContent = '';
        suggestionsSpan.textContent = '';
        hideElement(predictionResultDiv);
    }

    function updatePredictButtonState() {
        predictBtn.disabled = selectedSymptoms.size === 0;
    }

    // --- Fetch Symptoms ---
    async function fetchSymptoms() {
        showElement(loadingSymptomsMsg);
        hideElement(errorSymptomsMsg);
        symptomsListDiv.innerHTML = '<p>Loading...</p>'; // Clear and show loading in grid

        try {
            const response = await fetch(`${API_BASE_URL}/api/symptoms/`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const symptoms = await response.json();
            renderSymptoms(symptoms);
        } catch (error) {
            console.error('Error fetching symptoms:', error);
            hideElement(loadingSymptomsMsg);
            showElement(errorSymptomsMsg);
            symptomsListDiv.innerHTML = '<p>Failed to load symptoms.</p>'; // Update grid message
        } finally {
            hideElement(loadingSymptomsMsg);
        }
    }

    function renderSymptoms(symptoms) {
        symptomsListDiv.innerHTML = ''; // Clear previous content
        if (symptoms.length === 0) {
            symptomsListDiv.innerHTML = '<p>No symptoms available in the database.</p>';
            return;
        }

        symptoms.forEach(symptom => {
            const symptomItem = document.createElement('div');
            symptomItem.classList.add('symptom-item');
            symptomItem.textContent = symptom.name;
            symptomItem.dataset.symptomName = symptom.name; // Store the name for easy access

            symptomItem.addEventListener('click', () => {
                symptomItem.classList.toggle('selected');
                if (symptomItem.classList.contains('selected')) {
                    selectedSymptoms.add(symptom.name);
                } else {
                    selectedSymptoms.delete(symptom.name);
                }
                updatePredictButtonState();
                clearPredictionResult(); // Clear old results when symptoms change
            });
            symptomsListDiv.appendChild(symptomItem);
        });
        updatePredictButtonState(); // Initial state update
    }

    // --- Send Prediction Request ---
    async function sendPredictionRequest() {
        showElement(loadingPredictionMsg);
        hideElement(errorPredictionMsg);
        hideElement(predictionResultDiv); // Hide previous results

        if (selectedSymptoms.size === 0) {
            alert("Please select at least one symptom.");
            hideElement(loadingPredictionMsg);
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/api/predict/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken') // Important for Django POST requests
                },
                body: JSON.stringify({ symptoms: Array.from(selectedSymptoms) }) // Convert Set to Array
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(`HTTP error! status: ${response.status} - ${errorData.error || response.statusText}`);
            }

            const result = await response.json();
            displayPredictionResult(result);

        } catch (error) {
            console.error('Error during prediction:', error);
            showElement(errorPredictionMsg);
            errorPredictionMsg.textContent = `Prediction failed: ${error.message}`;
        } finally {
            hideElement(loadingPredictionMsg);
        }
    }

    function displayPredictionResult(result) {
        predictedDiseaseSpan.textContent = result.predicted_disease;
        confidenceScoreSpan.textContent = `${(result.confidence * 100).toFixed(2)}%`;
        suggestionsSpan.textContent = result.suggestions || 'No specific suggestions.';
        showElement(predictionResultDiv);
    }

    // --- Event Listeners ---
    predictBtn.addEventListener('click', sendPredictionRequest);
    resetBtn.addEventListener('click', () => {
        selectedSymptoms.clear();
        document.querySelectorAll('.symptom-item.selected').forEach(item => {
            item.classList.remove('selected');
        });
        updatePredictButtonState();
        clearPredictionResult();
    });


    // --- CSRF Token Helper (Standard Django practice) ---
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // --- Initial Load ---
    fetchSymptoms(); // Fetch symptoms when the page loads
});