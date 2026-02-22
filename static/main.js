document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('masterForm');
    const resultsContainer = document.getElementById('resultsContainer');
    const resultsList = document.getElementById('resultsList');
    const submitBtn = document.getElementById('submitBtn');

    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            // UI Feedback
            submitBtn.textContent = 'Processing...';
            submitBtn.disabled = true;
            
            // Gather form data
            const formData = new FormData(e.target);
            const data = {};

            formData.forEach((value, key) => {
                const element = e.target.querySelector(`[name="${key}"]`);
                if (element && element.type === 'checkbox') {
                    data[key] = element.checked ? 1 : 0;
                } else {
                    data[key] = isNaN(value) || value === '' ? value : parseFloat(value);
                }
            });

            // Ensure unchecked checkboxes are recorded
            const checkboxes = e.target.querySelectorAll('input[type="checkbox"]');
            checkboxes.forEach(cb => {
                if (!cb.checked) {
                    data[cb.name] = 0;
                }
            });

            try {
                // Send to backend
                const response = await fetch('/api/vaccination', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data),
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const responseData = await response.json();
                displayResults(responseData.predictions);
                
            } catch (error) {
                console.error("Error submitting data:", error);
                alert("An error occurred. Make sure the backend server is running.");
            } finally {
                submitBtn.textContent = 'Sync Data & Run Predictions';
                submitBtn.disabled = false;
            }
        });
    }

    function displayResults(predictions) {
        resultsContainer.style.display = 'block';
        resultsList.innerHTML = ''; 

        if (!predictions || predictions.length === 0) {
            resultsList.innerHTML = '<li>No predictions generated. Check model_files directory.</li>';
            resultsContainer.scrollIntoView({ behavior: 'smooth' });
            return;
        }

        predictions.forEach(pred => {
            const li = document.createElement('li');
            li.className = `result-item risk-${pred.risk_level.toLowerCase()}`;
            
            // Standardize output name
            const niceName = pred.vaccine.toUpperCase().replace('.JSON', '');
            
            li.innerHTML = `
                <span class="vaccine-name">${niceName}</span>
                <span class="vaccine-score">${pred.probability}% <span class="risk-label">${pred.risk_level}</span></span>
            `;
            resultsList.appendChild(li);
        });
        
        // Scroll back to top smoothly
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
});
