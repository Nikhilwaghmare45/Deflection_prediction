// Main JavaScript file for Structural Engineering Predictor

// Global variables
let currentChart = null;

// Document ready function
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// Initialize application
function initializeApp() {
    // Initialize Bootstrap tooltips
    initializeTooltips();
    
    // Initialize form validation
    initializeFormValidation();
    
    // Initialize charts if needed
    initializeCharts();
    
    // Add smooth scrolling
    initializeSmoothScrolling();
    
    // Initialize responsive tables
    initializeResponsiveTables();
}

// Initialize Bootstrap tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Initialize form validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
    
    // Real-time validation for numeric inputs
    const numericInputs = document.querySelectorAll('input[type="number"]');
    numericInputs.forEach(input => {
        input.addEventListener('input', validateNumericInput);
        input.addEventListener('blur', validateNumericInput);
    });
}

// Validate numeric input
function validateNumericInput(event) {
    const input = event.target;
    const value = parseFloat(input.value);
    const min = parseFloat(input.min);
    const max = parseFloat(input.max);
    
    // Remove previous validation classes
    input.classList.remove('is-valid', 'is-invalid');
    
    if (input.value === '') {
        return; // Let HTML5 required validation handle empty fields
    }
    
    if (isNaN(value) || (min !== undefined && value < min) || (max !== undefined && value > max)) {
        input.classList.add('is-invalid');
        showValidationMessage(input, getValidationMessage(input, value, min, max));
    } else {
        input.classList.add('is-valid');
        hideValidationMessage(input);
    }
}

// Get validation message for input
function getValidationMessage(input, value, min, max) {
    const fieldName = input.labels[0]?.textContent || 'Field';
    
    if (isNaN(value)) {
        return `${fieldName} must be a valid number.`;
    }
    
    if (min !== undefined && value < min) {
        return `${fieldName} must be at least ${min}.`;
    }
    
    if (max !== undefined && value > max) {
        return `${fieldName} must not exceed ${max}.`;
    }
    
    return `${fieldName} is invalid.`;
}

// Show validation message
function showValidationMessage(input, message) {
    let feedback = input.parentNode.querySelector('.invalid-feedback');
    if (!feedback) {
        feedback = document.createElement('div');
        feedback.className = 'invalid-feedback';
        input.parentNode.appendChild(feedback);
    }
    feedback.textContent = message;
}

// Hide validation message
function hideValidationMessage(input) {
    const feedback = input.parentNode.querySelector('.invalid-feedback');
    if (feedback) {
        feedback.textContent = '';
    }
}

// Initialize charts
function initializeCharts() {
    // Initialize any charts on the page
    const chartElements = document.querySelectorAll('canvas[id$="-chart"]');
    chartElements.forEach(element => {
        if (element.id === 'activity-chart') {
            // Activity chart is handled by the dashboard stats function
            return;
        }
        // Add other chart initializations here
    });
}

// Initialize smooth scrolling
function initializeSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                e.preventDefault();
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Initialize responsive tables
function initializeResponsiveTables() {
    const tables = document.querySelectorAll('.table-responsive table');
    tables.forEach(table => {
        // Add mobile-friendly classes
        table.classList.add('table-sm');
        
        // Add sorting functionality if needed
        const headers = table.querySelectorAll('th');
        headers.forEach(header => {
            if (header.dataset.sortable === 'true') {
                header.style.cursor = 'pointer';
                header.addEventListener('click', function() {
                    sortTable(table, Array.from(headers).indexOf(header));
                });
            }
        });
    });
}

// Sort table function
function sortTable(table, columnIndex) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const header = table.querySelectorAll('th')[columnIndex];
    
    // Determine sort direction
    const isAscending = !header.classList.contains('sort-desc');
    
    // Clear previous sort indicators
    table.querySelectorAll('th').forEach(th => {
        th.classList.remove('sort-asc', 'sort-desc');
    });
    
    // Add current sort indicator
    header.classList.add(isAscending ? 'sort-asc' : 'sort-desc');
    
    // Sort rows
    rows.sort((a, b) => {
        const aValue = a.cells[columnIndex].textContent.trim();
        const bValue = b.cells[columnIndex].textContent.trim();
        
        // Try to parse as numbers
        const aNum = parseFloat(aValue);
        const bNum = parseFloat(bValue);
        
        if (!isNaN(aNum) && !isNaN(bNum)) {
            return isAscending ? aNum - bNum : bNum - aNum;
        }
        
        // Sort as strings
        return isAscending ? 
            aValue.localeCompare(bValue) : 
            bValue.localeCompare(aValue);
    });
    
    // Reorder rows in table
    rows.forEach(row => tbody.appendChild(row));
}

// Utility functions
function showLoading(element) {
    if (element) {
        element.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    }
}

function hideLoading(element, content) {
    if (element) {
        element.innerHTML = content || '';
    }
}

// Format number for display
function formatNumber(num, decimals = 2) {
    return Number(num).toFixed(decimals);
}

// Format date for display
function formatDate(date) {
    return new Date(date).toLocaleDateString();
}

// Show success message
function showSuccessMessage(message) {
    showAlert(message, 'success');
}

// Show error message
function showErrorMessage(message) {
    showAlert(message, 'danger');
}

// Show alert message
function showAlert(message, type = 'info') {
    const alertContainer = document.querySelector('.container');
    if (!alertContainer) return;
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    alertContainer.insertBefore(alert, alertContainer.firstChild);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alert.parentNode) {
            alert.remove();
        }
    }, 5000);
}

// Handle form submission with loading state
function handleFormSubmission(formId) {
    const form = document.getElementById(formId);
    if (!form) return;
    
    form.addEventListener('submit', function() {
        const submitButton = form.querySelector('input[type="submit"], button[type="submit"]');
        if (submitButton) {
            const originalText = submitButton.textContent || submitButton.value;
            submitButton.disabled = true;
            
            if (submitButton.tagName === 'INPUT') {
                submitButton.value = 'Processing...';
            } else {
                submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
            }
            
            // Re-enable after 10 seconds as fallback
            setTimeout(() => {
                submitButton.disabled = false;
                if (submitButton.tagName === 'INPUT') {
                    submitButton.value = originalText;
                } else {
                    submitButton.textContent = originalText;
                }
            }, 10000);
        }
    });
}

// Initialize prediction form if it exists
if (document.getElementById('prediction-form')) {
    handleFormSubmission('prediction-form');
}

// Export functions for use in other scripts
window.StructuralApp = {
    showLoading,
    hideLoading,
    formatNumber,
    formatDate,
    showSuccessMessage,
    showErrorMessage,
    showAlert
};
