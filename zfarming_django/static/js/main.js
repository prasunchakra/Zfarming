// ZFarming JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            if (alert.classList.contains('alert-success') || alert.classList.contains('alert-info')) {
                var bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        });
    }, 5000);

    // Image upload preview
    const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    imageInputs.forEach(function(input) {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    // Find or create preview element
                    let preview = input.parentNode.querySelector('.image-preview');
                    if (!preview) {
                        preview = document.createElement('div');
                        preview.className = 'image-preview mt-3';
                        input.parentNode.appendChild(preview);
                    }
                    
                    preview.innerHTML = `
                        <img src="${e.target.result}" class="img-fluid rounded" style="max-height: 200px;" alt="Preview">
                        <p class="small text-muted mt-2">File: ${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)</p>
                    `;
                };
                reader.readAsDataURL(file);
            }
        });
    });

    // Drag and drop for file uploads
    const dropZones = document.querySelectorAll('.upload-area');
    dropZones.forEach(function(dropZone) {
        const fileInput = dropZone.querySelector('input[type="file"]');
        
        dropZone.addEventListener('dragover', function(e) {
            e.preventDefault();
            dropZone.classList.add('dragover');
        });

        dropZone.addEventListener('dragleave', function(e) {
            e.preventDefault();
            dropZone.classList.remove('dragover');
        });

        dropZone.addEventListener('drop', function(e) {
            e.preventDefault();
            dropZone.classList.remove('dragover');
            
            const files = e.dataTransfer.files;
            if (files.length > 0 && fileInput) {
                fileInput.files = files;
                // Trigger change event
                const event = new Event('change', { bubbles: true });
                fileInput.dispatchEvent(event);
            }
        });

        dropZone.addEventListener('click', function() {
            if (fileInput) {
                fileInput.click();
            }
        });
    });

    // Plant search functionality
    const searchInput = document.querySelector('#plant-search');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(function() {
                filterPlants(searchInput.value);
            }, 300);
        });
    }

    // Filter plants function
    function filterPlants(query) {
        const plantCards = document.querySelectorAll('.plant-card-item');
        const noResults = document.querySelector('#no-results');
        let visibleCount = 0;

        plantCards.forEach(function(card) {
            const plantName = card.dataset.plantName.toLowerCase();
            const scientificName = card.dataset.scientificName.toLowerCase();
            const searchQuery = query.toLowerCase();

            if (plantName.includes(searchQuery) || scientificName.includes(searchQuery)) {
                card.style.display = 'block';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });

        if (noResults) {
            noResults.style.display = visibleCount === 0 ? 'block' : 'none';
        }
    }

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Plant recommendation form
    const recommendationForm = document.querySelector('#plant-recommendation-form');
    if (recommendationForm) {
        recommendationForm.addEventListener('submit', function(e) {
            e.preventDefault();
            showLoadingSpinner();
            
            // Simulate API call delay
            setTimeout(function() {
                hideLoadingSpinner();
                recommendationForm.submit();
            }, 1000);
        });
    }

    // Loading spinner functions
    function showLoadingSpinner() {
        const spinner = document.querySelector('#loading-spinner');
        if (spinner) {
            spinner.style.display = 'block';
        }
    }

    function hideLoadingSpinner() {
        const spinner = document.querySelector('#loading-spinner');
        if (spinner) {
            spinner.style.display = 'none';
        }
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Copy to clipboard functionality
    const copyButtons = document.querySelectorAll('.copy-btn');
    copyButtons.forEach(function(btn) {
        btn.addEventListener('click', function() {
            const targetId = btn.dataset.target;
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                navigator.clipboard.writeText(targetElement.textContent).then(function() {
                    // Show success feedback
                    const originalText = btn.innerHTML;
                    btn.innerHTML = '<i class="fas fa-check"></i> Copied!';
                    btn.classList.add('btn-success');
                    
                    setTimeout(function() {
                        btn.innerHTML = originalText;
                        btn.classList.remove('btn-success');
                    }, 2000);
                });
            }
        });
    });

    // Back to top button
    const backToTopBtn = document.createElement('button');
    backToTopBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
    backToTopBtn.className = 'btn btn-success position-fixed bottom-0 end-0 m-3 rounded-circle';
    backToTopBtn.style.display = 'none';
    backToTopBtn.style.zIndex = '1000';
    document.body.appendChild(backToTopBtn);

    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopBtn.style.display = 'block';
        } else {
            backToTopBtn.style.display = 'none';
        }
    });

    backToTopBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
});

// Utility functions
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Setup CSRF token for AJAX requests
const csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

// Set up CSRF for jQuery if available
if (typeof $ !== 'undefined') {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
}
