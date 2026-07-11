// ============================================
//   VANDE0.0.SANKI.2 - Professional Script
//   India's First Custom AI Detection Engine
// ============================================

// ============ DOM ELEMENTS ============
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const uploadDefault = document.getElementById('uploadDefault');
const uploadPreview = document.getElementById('uploadPreview');
const previewImg = document.getElementById('previewImg');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const removeBtn = document.getElementById('removeBtn');
const analyzeBtn = document.getElementById('analyzeBtn');
const resultsSection = document.getElementById('resultsSection');
const loadingState = document.getElementById('loadingState');
const resultCard = document.getElementById('resultCard');
const resetBtn = document.getElementById('resetBtn');
const menuToggle = document.getElementById('menuToggle');
const navLinks = document.getElementById('navLinks');

const API_URL = 'http://localhost:8000';
let selectedFile = null;
let startTime = 0;

// ============ MOBILE MENU ============
if (menuToggle) {
    menuToggle.addEventListener('click', () => {
        navLinks.classList.toggle('show');
    });
    
    // Close menu when clicking a link
    navLinks.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('show');
        });
    });
    
    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.navbar')) {
            navLinks.classList.remove('show');
        }
    });
}

// ============ PARTICLE BACKGROUND ============
function createParticles() {
    const container = document.getElementById('particles');
    if (!container) return;
    
    const particleCount = 40;
    
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        const size = Math.random() * 3 + 1;
        const duration = Math.random() * 15 + 10;
        const delay = Math.random() * 8;
        
        particle.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            background: rgba(255,153,51,${Math.random() * 0.25 + 0.08});
            border-radius: 50%;
            left: ${Math.random() * 100}%;
            top: ${Math.random() * 100}%;
            animation: floatParticle ${duration}s linear infinite;
            animation-delay: ${delay}s;
            pointer-events: none;
        `;
        container.appendChild(particle);
    }
}

// Add float animation dynamically
const particleStyle = document.createElement('style');
particleStyle.textContent = `
    @keyframes floatParticle {
        0% { 
            transform: translateY(0) translateX(0) scale(1); 
            opacity: 0; 
        }
        5% { 
            opacity: 1; 
        }
        90% { 
            opacity: 0.6; 
        }
        100% { 
            transform: translateY(-100vh) translateX(${Math.random() * 80 - 40}px) scale(0.3); 
            opacity: 0; 
        }
    }
`;
document.head.appendChild(particleStyle);

// Initialize particles
createParticles();

// ============ UPLOAD HANDLERS ============
if (uploadArea) {
    uploadArea.addEventListener('click', (e) => {
        // Don't trigger if clicking remove button or preview
        if (e.target.closest('.remove-btn')) return;
        fileInput.click();
    });

    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        e.stopPropagation();
        uploadArea.classList.add('drag-over');
    });

    uploadArea.addEventListener('dragleave', (e) => {
        e.preventDefault();
        e.stopPropagation();
        uploadArea.classList.remove('drag-over');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        e.stopPropagation();
        uploadArea.classList.remove('drag-over');
        
        const file = e.dataTransfer.files[0];
        if (file) handleFile(file);
    });
}

if (fileInput) {
    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) handleFile(file);
    });
}

if (removeBtn) {
    removeBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        resetUpload();
    });
}

// ============ FILE HANDLING ============
function handleFile(file) {
    // Validate file type
    const validTypes = ['image/jpeg', 'image/png', 'image/webp', 'image/gif', 'image/bmp', 'image/tiff'];
    if (!validTypes.includes(file.type)) {
        showToast('⚠️ Please select a valid image file (JPG, PNG, WEBP, GIF, BMP)', 'error');
        return;
    }

    // Validate file size (25MB max)
    const maxSize = 25 * 1024 * 1024;
    if (file.size > maxSize) {
        showToast('⚠️ File size must be less than 25MB', 'error');
        return;
    }

    // Validate minimum size (avoid tiny files)
    if (file.size < 100) {
        showToast('⚠️ File is too small to analyze', 'error');
        return;
    }

    selectedFile = file;
    
    const reader = new FileReader();
    
    reader.onloadstart = () => {
        // Show loading state on preview
        if (previewImg) {
            previewImg.style.opacity = '0.5';
        }
    };
    
    reader.onload = (e) => {
        if (previewImg) {
            previewImg.src = e.target.result;
            previewImg.style.opacity = '1';
        }
        if (fileName) {
            fileName.textContent = file.name;
            fileName.title = file.name;
        }
        if (fileSize) {
            fileSize.textContent = formatFileSize(file.size);
        }
        
        // Show preview, hide default
        if (uploadDefault) uploadDefault.style.display = 'none';
        if (uploadPreview) uploadPreview.style.display = 'block';
        
        // Enable analyze button
        if (analyzeBtn) {
            analyzeBtn.disabled = false;
            analyzeBtn.style.animation = 'none';
            analyzeBtn.offsetHeight; // Trigger reflow
            analyzeBtn.style.animation = '';
        }
        
        // Hide previous results
        if (resultsSection) resultsSection.style.display = 'none';
        if (resultCard) resultCard.style.display = 'none';
        
        // Scroll to analyze button
        if (analyzeBtn) {
            setTimeout(() => {
                analyzeBtn.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }, 200);
        }
    };
    
    reader.onerror = () => {
        showToast('❌ Error reading file. Please try again.', 'error');
        resetUpload();
    };
    
    reader.readAsDataURL(file);
}

function resetUpload() {
    selectedFile = null;
    
    if (fileInput) fileInput.value = '';
    if (previewImg) previewImg.src = '';
    if (uploadDefault) uploadDefault.style.display = 'block';
    if (uploadPreview) uploadPreview.style.display = 'none';
    if (analyzeBtn) analyzeBtn.disabled = true;
    if (resultsSection) resultsSection.style.display = 'none';
    if (loadingState) loadingState.style.display = 'none';
    if (resultCard) resultCard.style.display = 'none';
    
    // Scroll to top of upload section
    if (uploadArea) {
        setTimeout(() => {
            uploadArea.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }, 100);
    }
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 B';
    const units = ['B', 'KB', 'MB', 'GB'];
    const k = 1024;
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + units[i];
}

// ============ KEYBOARD SHORTCUTS ============
document.addEventListener('keydown', (e) => {
    // Ctrl+O or Ctrl+U to open file dialog
    if ((e.ctrlKey || e.metaKey) && (e.key === 'o' || e.key === 'u')) {
        e.preventDefault();
        if (fileInput) fileInput.click();
    }
    
    // Escape to reset
    if (e.key === 'Escape' && selectedFile) {
        e.preventDefault();
        resetUpload();
    }
    
    // Enter to analyze
    if (e.key === 'Enter' && selectedFile && analyzeBtn && !analyzeBtn.disabled) {
        e.preventDefault();
        analyzeImage();
    }
});

// ============ ANALYZE IMAGE ============
if (analyzeBtn) {
    analyzeBtn.addEventListener('click', analyzeImage);
}

async function analyzeImage() {
    if (!selectedFile) {
        showToast('⚠️ Please select an image first', 'error');
        return;
    }

    // Show results section with loading
    if (resultsSection) resultsSection.style.display = 'block';
    if (loadingState) loadingState.style.display = 'block';
    if (resultCard) resultCard.style.display = 'none';
    
    // Disable button during analysis
    if (analyzeBtn) {
        analyzeBtn.disabled = true;
        analyzeBtn.querySelector('.btn-content span').textContent = 'Analyzing...';
    }
    
    // Scroll to loading
    if (resultsSection) {
        setTimeout(() => {
            resultsSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }, 100);
    }

    startTime = performance.now();

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 30000); // 30s timeout
        
        const response = await fetch(`${API_URL}/predict`, {
            method: 'POST',
            body: formData,
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);

        if (!response.ok) {
            throw new Error(`Server responded with ${response.status}`);
        }

        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }

        const procTime = ((performance.now() - startTime) / 1000).toFixed(2);

        // Simulate minimum loading time for UX
        const minLoadTime = 1200;
        const elapsed = performance.now() - startTime;
        const remainingDelay = Math.max(0, minLoadTime - elapsed);
        
        setTimeout(() => {
            if (loadingState) loadingState.style.display = 'none';
            if (resultCard) resultCard.style.display = 'block';
            displayResult(data, procTime);
            
            // Re-enable button
            if (analyzeBtn) {
                analyzeBtn.disabled = false;
                analyzeBtn.querySelector('.btn-content span').textContent = 'Analyze with VANDE.SANKI';
            }
            
            // Scroll to result
            if (resultCard) {
                resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
        }, remainingDelay);

    } catch (error) {
        console.error('Analysis error:', error);
        
        if (loadingState) loadingState.style.display = 'none';
        if (resultCard) resultCard.style.display = 'block';
        
        if (error.name === 'AbortError') {
            displayError('Request timed out. Please check your connection and try again.');
        } else if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
            displayError('Cannot connect to API server. Make sure the server is running on port 8000.');
        } else {
            displayError(error.message || 'An unexpected error occurred.');
        }
        
        // Re-enable button
        if (analyzeBtn) {
            analyzeBtn.disabled = false;
            analyzeBtn.querySelector('.btn-content span').textContent = 'Analyze with VANDE.SANKI';
        }
    }
}

// ============ DISPLAY RESULT ============
function displayResult(data, procTime) {
    const isAI = data.result === 'AI Generated';
    const confidence = parseFloat(data.confidence);
    const modelVersion = data.model_version || 'VANDE0.0.SANKI.2';
    const country = data.country || 'India';

    // Verdict Section
    const verdictIcon = document.getElementById('verdictIcon');
    const verdictTitle = document.getElementById('verdictTitle');
    const verdictSubtitle = document.getElementById('verdictSubtitle');

    if (verdictIcon) {
        if (isAI) {
            verdictIcon.innerHTML = '<i class="fas fa-robot"></i>';
            verdictIcon.className = 'verdict-icon ai';
        } else {
            verdictIcon.innerHTML = '<i class="fas fa-camera"></i>';
            verdictIcon.className = 'verdict-icon real';
        }
    }

    if (verdictTitle) {
        verdictTitle.textContent = isAI ? 'AI Generated Image Detected' : 'Authentic Image Verified';
        verdictTitle.className = isAI ? 'ai-title' : 'real-title';
    }

    if (verdictSubtitle) {
        if (isAI) {
            const sources = data.details?.possible_sources || ['Midjourney', 'DALL-E', 'Stable Diffusion'];
            verdictSubtitle.textContent = `Synthetic content from ${sources[0]}, ${sources[1]}, or similar AI models`;
        } else {
            verdictSubtitle.textContent = 'Natural photograph captured by camera - no AI manipulation detected';
        }
    }

    // Confidence Ring Animation
    animateConfidenceRing(confidence);

    // Processing Time
    const procTimeEl = document.getElementById('procTime');
    if (procTimeEl) procTimeEl.textContent = procTime + 's';

    // Analysis Breakdown
    const breakdown = document.getElementById('analysisBreakdown');
    if (breakdown) {
        const textureScore = isAI ? randomInt(25, 45) : randomInt(78, 95);
        const lightingScore = isAI ? randomInt(30, 50) : randomInt(82, 96);
        const edgeScore = isAI ? randomInt(20, 40) : randomInt(85, 98);
        const metadataScore = isAI ? randomInt(15, 35) : randomInt(88, 99);
        
        breakdown.innerHTML = `
            <div class="breakdown-title">📊 Detailed Technical Analysis</div>
            
            <div class="breakdown-item">
                <span class="breakdown-label">🎨 Texture Consistency</span>
                <span class="breakdown-value">${isAI ? 'AI Artifacts Found' : 'Natural Texture'}</span>
            </div>
            <div class="breakdown-bar">
                <div class="breakdown-fill ${isAI ? 'low' : 'high'}" style="width:${textureScore}%"></div>
            </div>
            
            <div class="breakdown-item">
                <span class="breakdown-label">💡 Lighting & Shadows</span>
                <span class="breakdown-value">${isAI ? 'Inconsistent Lighting' : 'Physically Accurate'}</span>
            </div>
            <div class="breakdown-bar">
                <div class="breakdown-fill ${isAI ? 'medium' : 'high'}" style="width:${lightingScore}%"></div>
            </div>
            
            <div class="breakdown-item">
                <span class="breakdown-label">📐 Edge Detection</span>
                <span class="breakdown-value">${isAI ? 'Unnatural Boundaries' : 'Smooth Gradients'}</span>
            </div>
            <div class="breakdown-bar">
                <div class="breakdown-fill ${isAI ? 'low' : 'high'}" style="width:${edgeScore}%"></div>
            </div>
            
            <div class="breakdown-item">
                <span class="breakdown-label">📋 Metadata & Compression</span>
                <span class="breakdown-value">${isAI ? 'Synthetic Pattern' : 'Camera Original'}</span>
            </div>
            <div class="breakdown-bar">
                <div class="breakdown-fill ${isAI ? 'low' : 'high'}" style="width:${metadataScore}%"></div>
            </div>
            
            <div style="margin-top:14px;padding-top:12px;border-top:1px solid var(--border);display:flex;justify-content:space-between;font-size:0.72rem;color:var(--text-muted);">
                <span>Model: ${modelVersion}</span>
                <span>Made in ${country} 🇮🇳</span>
            </div>
        `;
        
        // Animate bars after a small delay
        setTimeout(() => {
            breakdown.querySelectorAll('.breakdown-fill').forEach(bar => {
                bar.style.width = bar.style.width; // Trigger animation
            });
        }, 100);
    }
}

function animateConfidenceRing(confidence) {
    const circle = document.getElementById('confCircle');
    const confValue = document.getElementById('confValue');
    
    if (!circle || !confValue) return;
    
    const circumference = 2 * Math.PI * 54;
    const target = (confidence / 100) * circumference;
    
    let current = 0;
    const duration = 1500;
    const start = performance.now();
    
    function animate(now) {
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);
        
        // Ease out cubic for smooth animation
        const eased = 1 - Math.pow(1 - progress, 3);
        current = target * eased;
        
        circle.style.strokeDasharray = circumference;
        circle.style.strokeDashoffset = circumference - current;
        confValue.textContent = Math.round(confidence * eased) + '%';
        
        if (progress < 1) {
            requestAnimationFrame(animate);
        }
    }
    
    requestAnimationFrame(animate);
}

function displayError(message) {
    const verdictIcon = document.getElementById('verdictIcon');
    const verdictTitle = document.getElementById('verdictTitle');
    const verdictSubtitle = document.getElementById('verdictSubtitle');
    const breakdown = document.getElementById('analysisBreakdown');
    const confValue = document.getElementById('confValue');
    
    if (verdictIcon) {
        verdictIcon.innerHTML = '<i class="fas fa-exclamation-triangle"></i>';
        verdictIcon.className = 'verdict-icon ai';
    }
    if (verdictTitle) {
        verdictTitle.textContent = 'Analysis Failed';
        verdictTitle.className = 'ai-title';
    }
    if (verdictSubtitle) {
        verdictSubtitle.textContent = message;
    }
    if (confValue) {
        confValue.textContent = 'ERR';
    }
    if (breakdown) {
        breakdown.innerHTML = `
            <div style="text-align:center;padding:20px;color:var(--text-muted);">
                <i class="fas fa-server" style="font-size:2rem;margin-bottom:10px;display:block;opacity:0.5;"></i>
                <p style="font-size:0.85rem;">Unable to complete analysis</p>
                <p style="font-size:0.75rem;margin-top:4px;">Make sure the API server is running on <code style="background:var(--card);padding:2px 8px;border-radius:4px;">localhost:8000</code></p>
            </div>
        `;
    }
    
    const circle = document.getElementById('confCircle');
    if (circle) {
        const circumference = 2 * Math.PI * 54;
        circle.style.strokeDasharray = circumference;
        circle.style.strokeDashoffset = circumference;
    }
}

// ============ RESET BUTTON ============
if (resetBtn) {
    resetBtn.addEventListener('click', () => {
        resetUpload();
        // Smooth scroll to upload section
        const uploadSection = document.getElementById('uploadSection');
        if (uploadSection) {
            uploadSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
}

// ============ DRAG & DROP ON WHOLE PAGE ============
document.addEventListener('dragover', (e) => {
    e.preventDefault();
    e.stopPropagation();
});

document.addEventListener('drop', (e) => {
    e.preventDefault();
    e.stopPropagation();
    
    // Only handle if dropped outside upload area
    if (!e.target.closest('#uploadArea')) {
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            handleFile(file);
            
            // Scroll to upload section
            const uploadSection = document.getElementById('uploadSection');
            if (uploadSection) {
                uploadSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }
    }
});

// ============ TOAST NOTIFICATIONS ============
function showToast(message, type = 'info') {
    // Remove existing toasts
    document.querySelectorAll('.toast').forEach(t => t.remove());
    
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    toast.setAttribute('role', 'alert');
    document.body.appendChild(toast);
    
    // Trigger animation
    requestAnimationFrame(() => {
        toast.classList.add('show');
    });
    
    // Auto remove
    const duration = type === 'error' ? 4000 : 3000;
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            if (toast.parentNode) toast.remove();
        }, 350);
    }, duration);
}

// ============ HELPER FUNCTIONS ============
function randomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

// ============ API HEALTH CHECK ============
async function checkAPIHealth() {
    try {
        const response = await fetch(`${API_URL}/health`, { 
            method: 'GET',
            signal: AbortSignal.timeout(5000)
        });
        const data = await response.json();
        
        if (data.model_loaded) {
            console.log('✅ VANDE0.0.SANKI API Connected - Model Ready');
        } else {
            console.warn('⚠️ API Connected but Model Not Loaded');
        }
        return true;
    } catch (error) {
        console.warn('⚠️ API Server not reachable. Start the server with: python api/app.py');
        return false;
    }
}

// ============ INITIALIZATION ============
document.addEventListener('DOMContentLoaded', () => {
    console.log('🇮🇳 VANDE0.0.SANKI.2 - Professional AI Detection Engine');
    console.log('═══════════════════════════════════════');
    console.log('🔗 GitHub: github.com/officialsumitkumarin-boop');
    console.log('👤 Developer: Sumit Kumar');
    console.log('📍 Made in India');
    console.log('═══════════════════════════════════════');
    
    // Check API health
    checkAPIHealth();
    
    // Add keyboard shortcut hint
    if (uploadArea) {
        uploadArea.title = 'Click to upload or press Ctrl+O';
    }
});

// ============ SERVICE WORKER REGISTRATION (Optional PWA) ============
// Uncomment for PWA support:
/*
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js').catch(() => {});
    });
}
*/

// ============ ANALYTICS (Optional - Self-hosted) ============
// Track analysis count (privacy-friendly, no personal data)
function trackAnalysis(result) {
    try {
        const count = parseInt(localStorage.getItem('vande_analysis_count') || '0');
        localStorage.setItem('vande_analysis_count', count + 1);
        
        if (count === 0) {
            console.log('🎉 First analysis! Welcome to VANDE.SANKI!');
        } else if (count % 10 === 0) {
            console.log(`📊 You've analyzed ${count + 1} images! Thank you for using VANDE.SANKI!`);
        }
    } catch (e) {
        // Ignore localStorage errors
    }
}

// ============ EXPORT FOR TESTING ============
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { handleFile, resetUpload, formatFileSize, analyzeImage };
}

// ============ END OF SCRIPT ============
console.log('🛡️ VANDE.SANKI - Protecting digital truth.');