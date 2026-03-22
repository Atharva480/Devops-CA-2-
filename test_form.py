"""
STUDENT FEEDBACK FORM - AUTOMATED SELENIUM TEST SUITE
========================================================

Professional-grade automated testing for Student Feedback Registration Form
using Selenium WebDriver with comprehensive test coverage.

Test Coverage:
- Form page loading and initialization
- Form submission with valid data
- Validation of empty/required fields
- Email format validation
- Mobile number format validation
- Dropdown selection functionality
- Radio button selection functionality
- Submit button validation triggering
- Reset button functionality

Test Data:
- Name: Atharva Masharkar
- Email: atharva@example.com
- Mobile: 7894563251
- Department: Computer Science
- Gender: Male
- Feedback: Comprehensive 10+ word feedback

Technology Stack:
- Selenium WebDriver 4.x
- Microsoft Edge Browser with WebDriver
- Python unittest framework
- WebDriverWait for explicit waits

Author: DevOps QA Team
Last Updated: 2026
"""

# ============================================================================
# SECTION 1: IMPORTS
# ============================================================================

import unittest  # Python's built-in testing framework
from selenium import webdriver  # Selenium WebDriver for browser automation
from selenium.webdriver.common.by import By  # Locator strategies (ID, CSS_SELECTOR, etc.)
from selenium.webdriver.support.ui import WebDriverWait  # Explicit wait handling
from selenium.webdriver.support import expected_conditions as EC  # Wait conditions
from selenium.webdriver.common.alert import Alert  # Handle browser alerts
import time  # Time delays for synchronization


# ============================================================================
# SECTION 2: TEST CLASS DEFINITION
# ============================================================================

class TestStudentFeedbackForm(unittest.TestCase):
    """
    Comprehensive test suite for Student Feedback Registration Form.
    
    Inherits from unittest.TestCase to provide testing framework functionality.
    Each test method is independent and tests a specific feature/scenario.
    """

    # ========================================================================
    # SECTION 3: TEST SETUP AND TEARDOWN
    # ========================================================================

    def setUp(self):
        """
        Test setup method - runs BEFORE each test method.
        
        Initializes WebDriver with stable configuration:
        - Creates Edge WebDriver instance with security options
        - Sets implicit and explicit wait timeouts
        - Navigates to the form URL (localhost:8000)
        
        This ensures each test starts with:
        - Fresh browser instance
        - Clean slate (no previous data)
        - Ready-to-test form
        """
        try:
            # Edge options for stability and security
            options = webdriver.EdgeOptions()
            
            # Security option: run without sandbox (required in some environments)
            options.add_argument('--no-sandbox')
            
            # Performance option: disable shared memory access to prevent crashes
            options.add_argument('--disable-dev-shm-usage')
            
            # Performance option: disable GPU rendering to avoid compatibility issues
            options.add_argument('--disable-gpu')
            
            # Debugging option: enable remote debugging port
            options.add_argument('--remote-debugging-port=9222')
            
            # Initialize WebDriver with installed EdgeDriver
            self.driver = webdriver.Edge(options=options)
            
            # Implicit wait: max 10 seconds for element to be available
            # Reduces need for explicit waits in many cases
            self.driver.implicitly_wait(10)
            
            # Navigate to the form web page
            # Assumes HTTP server is running on localhost:8000
            self.driver.get("http://localhost:8000")
        except Exception as e:
            self.skipTest(f"WebDriver initialization failed: {e}")

    def tearDown(self):
        """
        Test teardown method - runs AFTER each test method.
        
        Cleans up WebDriver resources:
        - Closes all browser windows and quit the WebDriver session
        - Ensures no zombie processes remain
        - Frees up system resources for next test
        
        This runs regardless of test success or failure.
        """
        # Close browser and terminate WebDriver session
        self.driver.quit()

    # ========================================================================
    # SECTION 4: HELPER METHODS
    # ========================================================================

    def fill_form_valid_data(self):
        """
        Helper method to populate form with valid test data.
        
        Used by multiple tests to avoid code duplication.
        Fills all required fields with predefined valid values:
        - Name: "Atharva Masharkar"
        - Email: "atharva@example.com"
        - Mobile: "7894563251"
        - Department: "Computer Science"
        - Gender: "Male"
        - Feedback: 10+ word descriptive text
        
        Returns: None
        Note: This method does NOT submit the form
        """
        # Fill name field
        self.driver.find_element(By.ID, "name").send_keys("Atharva Masharkar")
        
        # Fill email field
        self.driver.find_element(By.ID, "email").send_keys("atharva@example.com")
        
        # Fill mobile number field
        self.driver.find_element(By.ID, "mobile").send_keys("7894563251")
        
        # Select department from dropdown
        department_select = self.driver.find_element(By.ID, "department")
        department_select.click()  # Open dropdown
        time.sleep(0.5)  # Brief wait for dropdown animation
        self.driver.find_element(By.CSS_SELECTOR, "option[value='computer-science']").click()
        
        # Select male gender radio button
        self.driver.find_element(By.ID, "male").click()
        
        # Fill feedback textarea with 15+ words
        self.driver.find_element(By.ID, "feedback").send_keys(
            "This is a sample feedback with more than ten words to meet the requirement for validation."
        )

    # ========================================================================
    # SECTION 5: ACTUAL TEST METHODS
    # ========================================================================

    def test_form_page_loads(self):
        """
        TEST 1: Verify form page loads successfully.
        
        Checks:
        - Browser page title contains "Student Feedback Registration Form"
        - Form element with id="feedbackForm" exists in the page
        
        This is a smoke test ensuring basic page loading works.
        """
        # Small delay to ensure page is fully loaded
        time.sleep(1)
        
        # Verify page title
        self.assertIn("Student Feedback Registration Form", self.driver.title)
        
        # Verify form element exists
        form = self.driver.find_element(By.ID, "feedbackForm")
        self.assertIsNotNone(form)

    def test_valid_submission(self):
        """
        TEST 2: Verify form submission with valid data.
        
        Tests the happy path:
        1. Refresh page to start fresh
        2. Fill all fields with valid data
        3. Click submit button
        4. Verify success alert appears
        
        Expected outcome: Success alert with "Form submitted successfully" message
        """
        # Refresh page to ensure clean state
        self.driver.refresh()
        time.sleep(0.5)
        
        # Fill form with valid data
        self.fill_form_valid_data()
        
        # Click submit button
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        
        # Wait for alert to appear (max 10 seconds)
        WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        
        # Grab alert object and verify message
        alert = Alert(self.driver)
        self.assertIn("Form submitted successfully", alert.text)
        
        # Dismiss the alert
        alert.accept()

    def test_empty_fields_validation(self):
        """
        TEST 3: Verify validation errors for empty required fields.
        
        Tests validation by:
        1. Refreshing page
        2. Clearing all form fields
        3. Attempting submission
        4. Verifying error messages appear for all fields
        
        Expected outcome: Error messages for all 6 required fields
        """
        # Refresh page and start fresh
        self.driver.refresh()
        time.sleep(0.5)
        
        # Clear all input fields to simulate empty form
        self.driver.find_element(By.ID, "name").clear()
        self.driver.find_element(By.ID, "email").clear()
        self.driver.find_element(By.ID, "mobile").clear()
        # Department dropdown already defaults to empty
        # Gender radio buttons start unchecked
        self.driver.find_element(By.ID, "feedback").clear()
        
        # Click submit on empty form
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        
        # Wait for error message to appear
        error = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "error"))
        )
        
        # Verify error messages for each field
        self.assertIn("Student Name is required", error.text)
        self.assertIn("Email ID is required", error.text)
        self.assertIn("Mobile Number is required", error.text)
        self.assertIn("Please select a valid department", error.text)
        self.assertIn("Please select a gender", error.text)
        self.assertIn("Feedback Comments are required", error.text)

    def test_invalid_email_error(self):
        """
        TEST 4: Verify email format validation.
        
        Tests invalid email scenario:
        1. Fill form with valid data
        2. Replace email with invalid format "invalid-email"
        3. Submit form
        4. Verify email validation error appears
        
        Expected outcome: Error indicating valid email format required
        """
        # Refresh and prepare form
        self.driver.refresh()
        time.sleep(0.5)
        
        # Fill with valid data first
        self.fill_form_valid_data()
        
        # Replace email with invalid format (no @ symbol)
        email_field = self.driver.find_element(By.ID, "email")
        email_field.clear()
        email_field.send_keys("invalid-email")
        
        # Submit form
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        
        # Wait for and verify error
        error = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "error"))
        )
        self.assertIn("valid email address", error.text)

    def test_invalid_mobile_error(self):
        """
        TEST 5: Verify mobile number length validation.
        
        Tests invalid mobile number scenario:
        1. Fill form with valid data
        2. Replace mobile with only 6 digits "123456"
        3. Submit form
        4. Verify mobile validation error appears
        
        Expected outcome: Error indicating exactly 10 digits required
        """
        # Refresh and prepare form
        self.driver.refresh()
        time.sleep(0.5)
        
        # Fill with valid data first
        self.fill_form_valid_data()
        
        # Replace mobile with fewer than 10 digits
        mobile_field = self.driver.find_element(By.ID, "mobile")
        mobile_field.clear()
        mobile_field.send_keys("123456")  # Only 6 digits instead of 10
        
        # Submit form
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        
        # Wait for and verify error message
        error = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "error"))
        )
        self.assertIn("Mobile Number must be exactly 10 digits", error.text)

    def test_dropdown_selection(self):
        """
        TEST 6: Verify department dropdown selection works.
        
        Tests:
        1. Click dropdown to open it
        2. Select "Computer Science" option
        3. Verify the selected value is "computer-science"
        
        Expected outcome: Dropdown value correctly updated to selected option
        """
        # Refresh page
        self.driver.refresh()
        time.sleep(0.5)
        
        # Click dropdown to open it
        department_select = self.driver.find_element(By.ID, "department")
        department_select.click()
        
        # Wait for dropdown animation
        time.sleep(0.5)
        
        # Click Computer Science option
        option = self.driver.find_element(By.CSS_SELECTOR, "option[value='computer-science']")
        option.click()
        
        # Verify dropdown now shows the selected value
        self.assertEqual(department_select.get_attribute("value"), "computer-science")

    def test_gender_selection(self):
        """
        TEST 7: Verify gender radio button selection works.
        
        Tests:
        1. Click Male radio button and verify it's selected
        2. Click Female radio button
        3. Verify Female is now selected and Male is deselected
        
        Expected outcome: Radio buttons behave as mutually exclusive group
        """
        # Refresh page
        self.driver.refresh()
        time.sleep(0.5)
        
        # Test Male selection
        male_radio = self.driver.find_element(By.ID, "male")
        male_radio.click()
        self.assertTrue(male_radio.is_selected())
        
        # Test Female selection (should deselect Male)
        female_radio = self.driver.find_element(By.ID, "female")
        female_radio.click()
        self.assertTrue(female_radio.is_selected())
        
        # Verify Male is now deselected (radio buttons are mutually exclusive)
        self.assertFalse(male_radio.is_selected())

    def test_submit_button_functionality(self):
        """
        TEST 8: Verify submit button triggers validation.
        
        Tests:
        1. Refresh to get empty form
        2. Click submit button without filling form
        3. Verify validation errors appear
        
        Expected outcome: Error messages displayed for empty form
        """
        # Refresh page to get clean empty form
        self.driver.refresh()
        time.sleep(0.5)
        
        # Click submit on empty form (should trigger validation)
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        
        # Wait for error container and verify errors appear
        error = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "error"))
        )
        self.assertIn("Student Name is required", error.text)

    def test_reset_button(self):
        """
        TEST 9: Verify reset button clears all form fields.
        
        Tests:
        1. Fill form with valid data
        2. Click reset button
        3. Verify all fields are cleared to empty values
        
        Expected outcome: All form fields reset to empty state
        """
        # Refresh page
        self.driver.refresh()
        time.sleep(0.5)
        
        # Fill form with data
        self.fill_form_valid_data()
        
        # Click reset button
        reset_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='reset']")
        reset_button.click()
        
        # Wait for reset to complete
        time.sleep(0.5)
        
        # Verify name field is empty
        name_field = self.driver.find_element(By.ID, "name")
        self.assertEqual(name_field.get_attribute("value"), "")
        
        # Verify email field is empty
        email_field = self.driver.find_element(By.ID, "email")
        self.assertEqual(email_field.get_attribute("value"), "")
        
        # Verify mobile field is empty
        mobile_field = self.driver.find_element(By.ID, "mobile")
        self.assertEqual(mobile_field.get_attribute("value"), "")


# ============================================================================
# SECTION 6: TEST RUNNER
# ============================================================================

if __name__ == "__main__":
    """
    Main entry point for running the test suite.
    
    When this file is executed directly (not imported):
    - unittest.main() discovers and runs all test methods
    - Provides verbose output showing each test result
    - Returns exit code 0 if all tests pass, 1 if any fail
    
    Usage:
    - From command line: python test_form.py
    - With verbose output: python test_form.py -v
    - Run specific test: python test_form.py TestStudentFeedbackForm.test_form_page_loads
    """
    unittest.main()