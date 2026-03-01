let currentStep = 1;
const totalSteps = 6;

function showStep(step) {
    document.querySelectorAll('.step-container').forEach(el => el.classList.remove('active'));
    document.getElementById(`step${step}`).classList.add('active');

    // Update Nav
    document.querySelectorAll('nav ul li a').forEach((el, index) => {
        el.classList.toggle('active', index + 1 === step);
    });

    // Update Buttons
    document.getElementById('prevBtn').style.display = step === 1 ? 'none' : 'block';
    document.getElementById('nextBtn').style.display = step === totalSteps ? 'none' : 'block';

    // Update Progress Bar
    document.getElementById('progressBar').style.width = `${(step / totalSteps) * 100}%`;

    currentStep = step;
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function changeStep(n) {
    if (n === 1 && !validateStep()) return;
    const newStep = currentStep + n;
    if (newStep >= 1 && newStep <= totalSteps) {
        showStep(newStep);
    }
}

function validateStep() {
    const activeStep = document.getElementById(`step${currentStep}`);
    const required = activeStep.querySelectorAll('[required]');
    let valid = true;
    required.forEach(field => {
        if (!field.value) {
            field.style.borderColor = '#ef4444';
            valid = false;
        } else {
            field.style.borderColor = '#e2e8f0';
        }
    });
    if (!valid) alert("Please fill in all required fields.");
    return valid;
}

document.addEventListener('DOMContentLoaded', () => {
    showStep(1);

    const form = document.getElementById('masterForm');
    const resultsContainer = document.getElementById('resultsContainer');
    const resultsList = document.getElementById('resultsList');
    const submitBtn = document.getElementById('submitBtn');

    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            submitBtn.textContent = 'Analyzing Biological Patterns...';
            submitBtn.disabled = true;

            const formData = new FormData(e.target);
            const data = {};

            formData.forEach((value, key) => {
                const element = e.target.querySelector(`[name="${key}"]`);
                if (element && element.type === 'checkbox') {
                    data[key] = element.checked ? 1 : 0;
                } else if (value !== "") {
                    data[key] = isNaN(value) ? value : parseFloat(value);
                }
            });

            // Ensure all checkboxes are counted
            const checkboxes = e.target.querySelectorAll('input[type="checkbox"]');
            checkboxes.forEach(cb => {
                data[cb.name] = cb.checked ? 1 : 0;
            });

            try {
                const response = await fetch('/api/vaccination', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data),
                });

                if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

                const responseData = await response.json();
                displayResults(responseData.predictions);

            } catch (error) {
                console.error("Error:", error);
                alert("Submission failed. Ensure the AI Engine is online.");
            } finally {
                submitBtn.textContent = 'Generate AI Prediction Report';
                submitBtn.disabled = false;
            }
        });
    }

    function displayResults(predictions) {
        resultsContainer.style.display = 'block';
        resultsList.innerHTML = '';

        if (!predictions || predictions.length === 0) {
            resultsList.innerHTML = '<li class="result-item">All current doses are up-to-date. No risks detected.</li>';
        } else {
            predictions.forEach(pred => {
                const li = document.createElement('li');
                li.className = `result-item risk-${pred.confidence_level.toLowerCase()}`;

                const vaccineDisplay = pred.vaccine_name.toUpperCase();

                li.innerHTML = `
                    <div class="vaccine-info">
                        <span class="vaccine-name">${vaccineDisplay}</span>
                        <div class="risk-indicator">
                            <span class="prob-val">${pred.probability}% Miss Risk</span>
                        </div>
                    </div>
                    <span class="risk-label">${pred.confidence_level} Confidence</span>
                `;
                resultsList.appendChild(li);
            });
        }

        resultsContainer.scrollIntoView({ behavior: 'smooth' });
    }
});
