const API_URL = 'http://localhost:8000';

// DOM Elements
const uploadBox = document.getElementById('uploadBox');
const imageInput = document.getElementById('imageInput');
const preview = document.getElementById('preview');
const previewImage = document.getElementById('previewImage');
const detectBtn = document.getElementById('detectBtn');
const resultSection = document.getElementById('resultSection');
const loading = document.getElementById('loading');
const resultCard = document.getElementById('resultCard');
const resultIcon = document.getElementById('resultIcon');
const resultText = document.getElementById('resultText');
const confidenceFill = document.getElementById('confidenceFill');
const confidenceText = document.getElementById('confidenceText');
const details = document.getElementById('details');

let selectedFile = null;

// Upload handlers
uploadBox.addEventListener('click', () => imageInput.click());
uploadBox.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadBox.style.borderColor = '#138808';
    uploadBox.style.background = '#f0f8f0';
});

uploadBox.addEventListener('dragleave', () => {
    uploadBox.style.borderColor = '#FF9933';
    uploadBox.style.background = 'transparent';
});

uploadBox.addEventListener('drop', (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    handleFile(file);
});

imageInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    handleFile(file);
});

function handleFile(file) {
    if (file && file.type.startsWith('image/')) {
        selectedFile = file;
        const reader = new FileReader();
        reader.onload = (e) => {
            previewImage.src = e.target.result;
            preview.style.display = 'block';
            uploadBox.style.display = 'none';
            detectBtn.disabled = false;
            resultSection.style.display = 'none';
        };
        reader.readAsDataURL(file);
    }
}

// Detect button
detectBtn.addEventListener('click', async () => {
    if (!selectedFile) return;
    
    // Show loading
    resultSection.style.display = 'block';
    loading.style.display = 'block';
    resultCard.style.display = 'none';
    
    const formData = new FormData();
    formData.append('file', selectedFile);
    
    try {
        const response = await fetch(`${API_URL}/predict`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        // Hide loading, show result
        setTimeout(() => {
            loading.style.display = 'none';
            resultCard.style.display = 'block';
            displayResult(data);
        }, 1500);
        
    } catch (error) {
        loading.style.display = 'none';
        resultCard.style.display = 'block';
        resultIcon.textContent = '❌';
        resultText.textContent = 'Error!';
        confidenceText.textContent = 'Could not connect to API';
        details.innerHTML = '<p>Make sure API is running on http://localhost:8000</p>';
    }
});

function displayResult(data) {
    if (data.error) {
        resultIcon.textContent = '❌';
        resultText.textContent = 'Error';
        confidenceText.textContent = data.error;
        return;
    }
    
    const confidence = parseFloat(data.confidence);
    
    if (data.result === 'AI Generated') {
        resultIcon.textContent = '🤖';
        resultText.textContent = 'AI Generated Image Detected!';
        resultText.style.color = '#e74c3c';
    } else {
        resultIcon.textContent = '📷';
        resultText.textContent = 'Real Image Confirmed!';
        resultText.style.color = '#27ae60';
    }
    
    // Animate confidence bar
    setTimeout(() => {
        confidenceFill.style.width = `${confidence}%`;
    }, 100);
    
    confidenceText.textContent = `Confidence: ${data.confidence}`;
    
    // Details
    let detailsHTML = '<strong>Analysis Details:</strong><br><br>';
    if (data.details) {
        for (let key in data.details) {
            detailsHTML += `<strong>${key}:</strong> ${data.details[key]}<br>`;
        }
    }
    detailsHTML += `<br><small>Model: ${data.model_version} | Made in ${data.country}</small>`;
    details.innerHTML = detailsHTML;
}
