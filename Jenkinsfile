/*
 * JENKINS CI/CD PIPELINE CONFIGURATION
 * ====================================
 * 
 * Purpose: Automate the build, testing, and validation of the Student Feedback Form
 * 
 * Pipeline Stages:
 * 1. Checkout: Pull code from repository
 * 2. Setup Python Environment: Install dependencies
 * 3. Start Local Server: Launch HTTP server for form testing
 * 4. Run Selenium Tests: Execute comprehensive test suite
 * 5. Cleanup: Terminate background processes
 * 
 * Technology Stack:
 * - Jenkins (CI/CD orchestration)
 * - Windows Batch scripts (command execution)
 * - Python 3.11+ (test runner)
 * - Selenium WebDriver 4.x (automated testing)
 * - Chrome Browser (test browser)
 * 
 * Environment: Windows Agent
 * 
 * Execution Time: ~2-3 minutes (including server startup, 9 tests, cleanup)
 * 
 * Author: DevOps Team
 * Last Updated: 2026
 */

pipeline {
    /**
     * AGENT CONFIGURATION
     * - "any" allows this pipeline to run on any available Jenkins agent
     * - Removes agent restriction, improves build queue flexibility
     */
    agent any

    stages {
        /**
         * STAGE 1: CHECKOUT
         * ==================
         * Purpose: Retrieve project source code from version control repository
         * 
         * Action: Executes 'checkout scm' which:
         * - Clones the repository to Jenkins workspace
         * - Pulls the latest code from specified branch
         * - Sets up working directory for subsequent stages
         * 
         * Duration: ~5-10 seconds
         * Success Indicator: Code files present in workspace
         */
        stage('Checkout') {
            steps {
                // Check out code from repository
                checkout scm
                echo '✅ CODE CHECKOUT COMPLETE - Project source code retrieved'
            }
        }

        /**
         * STAGE 2: SETUP PYTHON ENVIRONMENT
         * ==================================
         * Purpose: Install required Python dependencies for testing
         * 
         * Action: Runs 'pip install -r requirements.txt' which:
         * - Reads requirements.txt (list of package dependencies)
         * - Downloads and installs each package via pip
         * - Sets up test environment (Selenium, webdriver-manager, etc.)
         * 
         * Dependencies installed:
         * - selenium: WebDriver automation library
         * - webdriver-manager: Automatic ChromeDriver management
         * - unittest: Python's built-in testing framework
         * 
         * Duration: ~30-60 seconds (slower on first run, cached thereafter)
         * Success: All packages installed with no errors
         */
        stage('Setup Python Environment') {
            steps {
                // Install Python packages from requirements.txt
                bat 'pip install -r requirements.txt'
                echo '✅ PYTHON ENVIRONMENT SETUP COMPLETE - All dependencies installed'
            }
        }

        /**
         * STAGE 3: START LOCAL HTTP SERVER
         * =================================
         * Purpose: Launch HTTP server to host the student feedback form
         * 
         * Actions:
         * 1. 'start /B python -m http.server 8000'
         *    - /B = Run in background (non-blocking)
         *    - python -m http.server = Start built-in Python HTTP server
         *    - 8000 = Port number (form accessible at http://localhost:8000)
         * 
         * 2. 'timeout /t 5' = Wait 5 seconds for server to fully start
         *    - Prevents race condition where tests run before server ready
         *    - > nul = Suppress output messages
         * 
         * Server Capabilities:
         * - Serves index.html from current directory
         * - Serves styles.css and script.js (static assets)
         * - Single-threaded, sufficient for testing
         * 
         * Duration: ~5 seconds
         * Verification: http://localhost:8000 responds with form
         */
        stage('Start Local Server') {
            steps {
                // Start Python HTTP server in background
                bat 'start /B python -m http.server 8000'
                echo '✅ HTTP SERVER STARTED - Student feedback form accessible at http://localhost:8000'
                
                // Wait for server to fully start and be ready
                bat 'timeout /t 5 /nobreak > nul'
                echo '✅ SERVER READY - Waiting complete, proceeding to tests'
            }
        }

        /**
         * STAGE 4: RUN SELENIUM TEST SUITE
         * ================================
         * Purpose: Execute comprehensive automated tests on the form
         * 
         * Action: 'python test_form.py' runs the test suite which:
         * - Launches Chrome WebDriver instance
         * - Navigates to http://localhost:8000
         * - Runs 9 independent test cases
         * - Verifies form functionality and validation
         * - Reports pass/fail for each test
         * 
         * Tests Executed:
         * 1. Form page loads successfully
         * 2. Valid form submission
         * 3. Empty fields validation
         * 4. Invalid email format validation
         * 5. Invalid mobile number validation
         * 6. Dropdown selection functionality
         * 7. Gender radio button selection
         * 8. Submit button validation
         * 9. Reset button functionality
         * 
         * Expected Output:
         * - 9 tests run in ~100-120 seconds
         * - "Ran 9 tests" message
         * - "OK" or "FAILED" status
         * 
         * Duration: ~100-120 seconds
         * Success Criteria: All 9 tests pass (exit code 0)
         */
        stage('Run Selenium Tests') {
            steps {
                // Execute the Selenium test suite
                bat 'python test_form.py'
                echo '✅ SELENIUM TESTS COMPLETED - Test suite execution finished'
            }
        }

        /**
         * STAGE 5: CLEANUP
         * ================
         * Purpose: Terminate background processes and clean up resources
         * 
         * Action: 'taskkill /F /IM python.exe' terminates Python processes:
         * - /F = Force kill (immediate termination)
         * - /IM python.exe = Target Python executable
         * - Filter for HTTP server process by window title
         * 
         * Cleanup Procedures:
         * 1. Kill Python HTTP server process
         * 2. Release port 8000 (so next build can use it)
         * 3. Free up system resources
         * 4. Handle errors gracefully ("|| echo..." prevents build failure)
         * 
         * Error Handling:
         * - '2>nul' = Suppress error messages to console
         * - '|| echo...' = Execute fallback message if command fails
         * - Prevents pipeline failure if no server was running
         * 
         * Duration: ~2-5 seconds
         * Result: Port 8000 freed, cleanup complete
         */
        stage('Cleanup') {
            steps {
                // Terminate HTTP server processes
                bat 'taskkill /F /IM python.exe /FI "WINDOWTITLE eq python*" 2>nul || echo No server processes to kill'
                echo '✅ CLEANUP COMPLETE - Background processes terminated, resources freed'
            }
        }
    }

    /**
     * POST-BUILD ACTIONS
     * ==================
     * Execute actions after pipeline stages complete
     * Blocks: always, success, failure, unstable
     */
    post {
        /**
         * ALWAYS Block - Executes regardless of pipeline success/failure
         * 
         * Purpose: Logging and general post-build activities
         */
        always {
            echo '═════════════════════════════════════════════════════════'
            echo 'BUILD PIPELINE COMPLETED'
            echo 'Post-build cleanup and logging finished'
            echo '═════════════════════════════════════════════════════════'
        }
        
        /**
         * SUCCESS Block - Executes only if pipeline succeeds (all tests pass)
         * 
         * Purpose: Celebratory messaging and success logging
         */
        success {
            echo '═════════════════════════════════════════════════════════'
            echo '✅ SUCCESS! ALL TESTS PASSED'
            echo 'Pipeline completed successfully without errors'
            echo 'Form validation working perfectly - ready for deployment'
            echo '═════════════════════════════════════════════════════════'
        }
        
        /**
         * FAILURE Block - Executes if any stage fails
         * 
         * Purpose: Error reporting and troubleshooting guidance
         */
        failure {
            echo '═════════════════════════════════════════════════════════'
            echo '❌ FAILURE - PIPELINE BUILD FAILED'
            echo 'Some tests failed or a stage encountered an error'
            echo 'Review logs above for detailed error information'
            echo 'Common issues:'
            echo '  - Server failed to start: Check if port 8000 is available'
            echo '  - Tests failed: Review Selenium error messages'
            echo '  - Dependencies missing: Verify requirements.txt'
            echo '═════════════════════════════════════════════════════════'
        }
    }
}

/**
 * JENKINS USAGE INSTRUCTIONS
 * =========================
 * 
 * 1. CREATE NEW PIPELINE JOB
 *    - New Item → Pipeline
 *    - Name: "Student-Feedback-Form-CI"
 *    - Configure → Pipeline
 * 
 * 2. POINT TO JENKINSFILE
 *    - Pipeline Definition: "Pipeline script from SCM"
 *    - SCM: Git (if using Git repository)
 *    - Repository URL: [your-git-repo-url]
 *    - Branch: */master (or your branch)
 *    - Script Path: Jenkinsfile (this file)
 * 
 * 3. BUILD TRIGGERS (Optional)
 *    - Poll SCM: H/15 * * * * (every 15 minutes)
 *    - GitHub hook trigger (if using GitHub)
 *    - Manual trigger (click "Build Now")
 * 
 * 4. RUNNING THE PIPELINE
 *    - Click "Build Now" on job page
 *    - Monitor build progress in "Console Output"
 *    - View stage visualization on main job page
 *    - Pipeline completes in ~2-3 minutes
 * 
 * 5. MONITORING RESULTS
 *    - Blue = Pipeline succeeded
 *    - Red = Pipeline failed
 *    - Gray = Still running
 *    - Click stage name to see log output
 * 
 * TROUBLESHOOTING
 * ===============
 * - Port 8000 already in use: Kill other processes or change port
 * - WebDriver errors: Ensure Chrome browser is installed
 * - Test failures: Check Selenium error messages in console
 * - Python not found: Verify Python 3.11+ installed and in PATH
 */