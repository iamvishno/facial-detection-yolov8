// Tab switching functionality
document.addEventListener('DOMContentLoaded', function() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabName = btn.getAttribute('data-tab');

            // Remove active class from all tabs and contents
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            // Add active class to clicked tab and corresponding content
            btn.classList.add('active');
            document.getElementById(`${tabName}-tab`).classList.add('active');
        });
    });

    // Setup file upload handlers
    setupImageUpload();
    setupVideoUpload();
    setupBatchUpload();
    setupWebcam();
});

// Image upload functionality
function setupImageUpload() {
    const input = document.getElementById('image-input');
    const uploadArea = document.getElementById('image-upload-area');
    const preview = document.getElementById('image-preview');
    const detectBtn = document.getElementById('detect-image-btn');

    let selectedFile = null;

    // Click to upload
    uploadArea.addEventListener('click', () => input.click());

    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#764ba2';
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.style.borderColor = '#667eea';
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#667eea';
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleImageSelect(files[0]);
        }
    });

    input.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleImageSelect(e.target.files[0]);
        }
    });

    function handleImageSelect(file) {
        selectedFile = file;
        const reader = new FileReader();
        reader.onload = (e) => {
            preview.innerHTML = `<img src="${e.target.result}" alt="Preview">`;
            detectBtn.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }

    detectBtn.addEventListener('click', () => {
        if (selectedFile) {
            uploadAndDetect(selectedFile, 'image');
        }
    });
}

// Video upload functionality
function setupVideoUpload() {
    const input = document.getElementById('video-input');
    const uploadArea = document.getElementById('video-upload-area');
    const preview = document.getElementById('video-preview');
    const detectBtn = document.getElementById('detect-video-btn');

    let selectedFile = null;

    uploadArea.addEventListener('click', () => input.click());

    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#764ba2';
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.style.borderColor = '#667eea';
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#667eea';
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleVideoSelect(files[0]);
        }
    });

    input.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleVideoSelect(e.target.files[0]);
        }
    });

    function handleVideoSelect(file) {
        selectedFile = file;
        const reader = new FileReader();
        reader.onload = (e) => {
            preview.innerHTML = `<video controls src="${e.target.result}"></video>`;
            detectBtn.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }

    detectBtn.addEventListener('click', () => {
        if (selectedFile) {
            uploadAndDetect(selectedFile, 'video');
        }
    });
}

// Batch upload functionality
function setupBatchUpload() {
    const input = document.getElementById('batch-input');
    const uploadArea = document.getElementById('batch-upload-area');
    const preview = document.getElementById('batch-preview');
    const detectBtn = document.getElementById('detect-batch-btn');

    let selectedFiles = [];

    uploadArea.addEventListener('click', () => input.click());

    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#764ba2';
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.style.borderColor = '#667eea';
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#667eea';
        const files = Array.from(e.dataTransfer.files);
        if (files.length > 0) {
            handleBatchSelect(files);
        }
    });

    input.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleBatchSelect(Array.from(e.target.files));
        }
    });

    function handleBatchSelect(files) {
        selectedFiles = files;
        let html = '<ul class="file-list">';
        files.forEach(file => {
            html += `<li>${file.name} <span>(${(file.size / 1024 / 1024).toFixed(2)} MB)</span></li>`;
        });
        html += '</ul>';
        preview.innerHTML = html;
        detectBtn.style.display = 'block';
    }

    detectBtn.addEventListener('click', () => {
        if (selectedFiles.length > 0) {
            uploadBatchAndDetect(selectedFiles);
        }
    });
}

// Upload and detect for single file
function uploadAndDetect(file, type) {
    const formData = new FormData();
    formData.append('file', file);

    showLoading();

    fetch(`/detect/${type}`, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        hideLoading();
        if (data.success) {
            displayResults(data, type);
        } else {
            alert('Error: ' + (data.error || 'Unknown error'));
        }
    })
    .catch(error => {
        hideLoading();
        alert('Error: ' + error.message);
    });
}

// Upload and detect for batch
function uploadBatchAndDetect(files) {
    const formData = new FormData();
    files.forEach(file => {
        formData.append('files[]', file);
    });

    showLoading();

    fetch('/detect/batch', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        hideLoading();
        if (data.success) {
            displayBatchResults(data.results);
        } else {
            alert('Error: ' + (data.error || 'Unknown error'));
        }
    })
    .catch(error => {
        hideLoading();
        alert('Error: ' + error.message);
    });
}

// Display results
function displayResults(data, type) {
    const resultsSection = document.getElementById('results-section');
    const resultsContent = document.getElementById('results-content');

    let html = '<div class="result-card">';

    if (type === 'image') {
        html += `
            <h4>Detection Complete</h4>
            <p><strong>Faces Detected:</strong> ${data.face_count}</p>
            <div class="result-image-container">
                <img src="/outputs/${data.output_filename}" alt="Detection result" class="result-image">
            </div>
            <div class="result-actions">
                <a href="/outputs/${data.output_filename}" download class="btn btn-primary">Download Result</a>
            </div>
        `;
    } else if (type === 'video') {
        html += `
            <h4>Video Processing Complete</h4>
            <p><strong>Total Frames:</strong> ${data.total_frames}</p>
            <p><strong>Processed Frames:</strong> ${data.processed_frames}</p>
            <p><strong>Total Detections:</strong> ${data.total_detections}</p>
            <div class="result-image-container">
                <video controls src="/outputs/${data.output_filename}" class="result-image"></video>
            </div>
            <div class="result-actions">
                <a href="/outputs/${data.output_filename}" download class="btn btn-primary">Download Result</a>
            </div>
        `;
    }

    html += '</div>';
    resultsContent.innerHTML = html;
    resultsSection.style.display = 'block';

    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// Display batch results
function displayBatchResults(results) {
    const resultsSection = document.getElementById('results-section');
    const resultsContent = document.getElementById('results-content');

    let html = '';

    results.forEach((result, index) => {
        html += '<div class="result-card">';
        html += `<h4>File ${index + 1}: ${result.filename}</h4>`;

        if (result.error) {
            html += `<p style="color: red;">Error: ${result.error}</p>`;
        } else {
            if (result.type === 'image') {
                html += `<p><strong>Faces Detected:</strong> ${result.face_count}</p>`;
                html += `
                    <div class="result-image-container">
                        <img src="/outputs/${result.output_filename}" alt="Detection result" style="max-width: 100%; max-height: 300px;">
                    </div>
                `;
            } else if (result.type === 'video') {
                html += `<p><strong>Total Detections:</strong> ${result.total_detections}</p>`;
            }
            html += `
                <div class="result-actions">
                    <a href="/outputs/${result.output_filename}" download class="btn btn-primary">Download</a>
                </div>
            `;
        }

        html += '</div>';
    });

    resultsContent.innerHTML = html;
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// Webcam functionality
function setupWebcam() {
    const startBtn = document.getElementById('start-webcam-btn');
    const stopBtn = document.getElementById('stop-webcam-btn');
    const webcamFeed = document.getElementById('webcam-feed');
    const webcamStatus = document.getElementById('webcam-status');

    startBtn.addEventListener('click', () => {
        webcamFeed.src = '/video_feed';
        webcamFeed.classList.add('active');
        webcamStatus.style.display = 'none';
        startBtn.style.display = 'none';
        stopBtn.style.display = 'block';
    });

    stopBtn.addEventListener('click', () => {
        webcamFeed.src = '';
        webcamFeed.classList.remove('active');
        webcamStatus.style.display = 'block';
        webcamStatus.textContent = 'Webcam stopped';
        stopBtn.style.display = 'none';
        startBtn.style.display = 'block';

        // Call stop endpoint
        fetch('/stop_webcam')
            .then(() => {
                webcamStatus.textContent = 'Click "Start Webcam" to begin';
            });
    });
}

// Loading indicator
function showLoading() {
    document.getElementById('loading').style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}
