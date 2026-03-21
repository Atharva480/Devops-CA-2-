/**
 * STUDENT FEEDBACK FORM VALIDATION SYSTEM
 * ========================================
 * Professional-grade form validation with real-time input sanitization
 * 
 * This script provides:
 * - Server-side style validation (form submission level)
 * - Real-time input sanitization and formatting
 * - User-friendly error messaging with emoji indicators
 * - Robust field validation with multiple checks
 * - Accessibility-focused error reporting
 * 
 * Dependencies: index.html (form elements)
 * Browser Support: Modern browsers (ES6+)
 */

/* ============================================================================
   SECTION 1: MAIN FORM VALIDATION FUNCTION
   ============================================================================ */

/**
 * validateForm() - Main form validation function
 * 
 * Called when the form is submitted. Validates all 6 required fields
 * and displays any errors before allowing submission.
 * 
 * Returns: boolean
 *   - true: All validations passed, form can submit
 *   - false: Validation errors found, form submission blocked
 * 
 * Process:
 * 1. Clear any previous errors
 * 2. Validate each field with specific rules
 * 3. Collect all errors in an array
 * 4. Display errors if any found
 * 5. Return validation status
 */
function validateForm() {
    // ========== Step 1: Clear Previous Errors ==========
    const errorP = document.getElementById('error');
    errorP.innerHTML = '';
    errorP.style.display = 'none';

    // Initialize validation tracking
    let errors = [];
    let isValid = true;

    // ========== Step 2: Validate Student Name Field ==========
    const name = document.getElementById('name').value.trim();
    
    if (name === '') {
        errors.push('📋 Student Name is required. Please enter your full name.');
        isValid = false;
    } else if (name.length < 2) {
        errors.push('📋 Student Name must be at least 2 characters long. Please provide a valid name.');
        isValid = false;
    } else if (/\d/.test(name)) {
        errors.push('📋 Student Name cannot contain numbers. Please use only letters and spaces.');
        isValid = false;
    }

    // ========== Step 3: Validate Email Field ==========
    const email = document.getElementById('email').value.trim().toLowerCase();
    
    // Professional email regex pattern for comprehensive validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    if (email === '') {
        errors.push('✉️ Email ID is required. Please enter your college email address.');
        isValid = false;
    } else if (!emailRegex.test(email)) {
        errors.push('✉️ Please enter a valid email address (format: student@college.edu).');
        isValid = false;
    }

    // ========== Step 4: Validate Mobile Number Field ==========
    const mobile = document.getElementById('mobile').value.trim();
    
    // Regex to match exactly 10 digits
    const mobileRegex = /^\d{10}$/;
    
    if (mobile === '') {
        errors.push('📱 Mobile Number is required. Please enter your 10-digit phone number.');
        isValid = false;
    } else if (!/^\d+$/.test(mobile)) {
        errors.push('📱 Mobile Number must contain only digits (0-9). Special characters and spaces are not allowed.');
        isValid = false;
    } else if (mobile.length !== 10) {
        errors.push('📱 Mobile Number must be exactly 10 digits. You entered ' + mobile.length + ' digits.');
        isValid = false;
    } else if (!mobileRegex.test(mobile)) {
        errors.push('📱 Please enter a valid 10-digit mobile number.');
        isValid = false;
    }

    // ========== Step 5: Validate Department Selection ==========
    const department = document.getElementById('department').value.trim();
    
    if (department === '') {
        errors.push('🏢 Please select a valid department. All departments must be chosen.');
        isValid = false;
    }

    // ========== Step 6: Validate Gender Selection ==========
    const gender = document.querySelector('input[name="gender"]:checked');
    
    if (!gender) {
        errors.push('👤 Please select a gender option (Male, Female, or Other).');
        isValid = false;
    }

    // ========== Step 7: Validate Feedback Comments ==========
    let feedback = document.getElementById('feedback').value.trim();
    
    if (feedback === '') {
        errors.push('💬 Feedback Comments are required. Please share your thoughts and suggestions.');
        isValid = false;
    } else {
        // Count words (splits on whitespace and filters empty strings)
        const wordCount = feedback.split(/\s+/).filter(word => word.length > 0).length;
        
        if (wordCount < 10) {
            errors.push(`💬 Feedback Comments must contain at least 10 words. You entered ${wordCount} word(s). Please provide more detailed feedback.`);
            isValid = false;
        } else if (feedback.length < 50) {
            errors.push('💬 Feedback Comments seem too short. Please provide more comprehensive and detailed feedback for better evaluation.');
            isValid = false;
        }
    }

    // ========== Step 8: Display Errors or Submit ==========
    if (errors.length > 0) {
        // Show all collected errors with professional formatting
        errorP.innerHTML = '<strong>❌ Please fix the following errors before submitting:</strong><br><br>' + errors.join('<br>');
        errorP.style.display = 'block';
        errorP.style.color = '#c0392b';
        
        // Prevent form submission
        return false;
    }

    // If validation passed, update email to lowercase and show success
    if (isValid) {
        document.getElementById('email').value = email;
        alert('✅ Form submitted successfully! Thank you for providing your valuable feedback. We appreciate your time.');
    }

    return isValid; // Return validation status to prevent/allow submission
}

/* ============================================================================
   SECTION 2: REAL-TIME INPUT SANITIZATION & FORMATTING
   ============================================================================ */

/**
 * DOMContentLoaded Event Listener
 * 
 * Runs after the HTML document is fully loaded.
 * Sets up real-time input sanitization for each form field.
 * 
 * Features:
 * - Name field: Removes numbers as user types
 * - Email field: Converts to lowercase automatically
 * - Mobile field: Strips non-digits and limits to 10 digits
 * - All fields: Trim spaces on blur (field loses focus)
 * - Feedback field: Real-time character and word counting
 */
document.addEventListener('DOMContentLoaded', function() {
    
    /* -------- NAME FIELD: Prevent Numbers -------- */
    const nameField = document.getElementById('name');
    if (nameField) {
        // Remove numbers as user types
        nameField.addEventListener('input', function() {
            /**
             * Replace regex: /[0-9]/g
             * [0-9] = character class matching digits 0 through 9
             * g = global flag, replace all occurrences
             */
            this.value = this.value.replace(/[0-9]/g, '');
        });
        
        // Trim trailing and leading spaces when field loses focus
        nameField.addEventListener('blur', function() {
            this.value = this.value.trim();
        });
    }

    /* -------- EMAIL FIELD: Convert to Lowercase -------- */
    const emailField = document.getElementById('email');
    if (emailField) {
        // Convert to lowercase as user types for case-insensitive processing
        emailField.addEventListener('input', function() {
            this.value = this.value.toLowerCase();
        });
        
        // Trim spaces on blur
        emailField.addEventListener('blur', function() {
            this.value = this.value.trim();
        });
    }

    /* -------- MOBILE FIELD: Only Digits, 10 Digit Limit -------- */
    const mobileField = document.getElementById('mobile');
    if (mobileField) {
        // Real-time input validation and formatting
        mobileField.addEventListener('input', function() {
            /**
             * First replace: /[^\d]/g
             * [^\d] = negated character class, matches anything that is NOT a digit
             * Effectively removes all non-digit characters
             */
            this.value = this.value.replace(/[^\d]/g, '');
            
            // Enforce maximum 10 digit limit
            if (this.value.length > 10) {
                this.value = this.value.slice(0, 10);
            }
        });
        
        // Trim spaces on blur
        mobileField.addEventListener('blur', function() {
            this.value = this.value.trim();
        });
    }

    /* -------- FEEDBACK FIELD: Trim and Count Characters/Words -------- */
    const feedbackField = document.getElementById('feedback');
    if (feedbackField) {
        // Trim spaces when field loses focus
        feedbackField.addEventListener('blur', function() {
            this.value = this.value.trim();
        });
        
        // Real-time character and word counting for user feedback
        feedbackField.addEventListener('input', function() {
            // Split by whitespace and filter empty strings
            const wordCount = this.value.trim().split(/\s+/).filter(w => w.length > 0).length;
            
            // Count visible characters (excluding leading/trailing spaces)
            const charCount = this.value.trim().length;
            
            // Log for debugging purposes (visible in browser console)
            console.log(`📊 Feedback Stats - Characters: ${charCount}, Words: ${wordCount}`);
        });
    }
});
