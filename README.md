<img src="https://github.com/Qcarvalhooliveira/Meu_Diario_Oficial/blob/main/image/logo.png" width="1000" height="400">

# **Meu Diário Oficial - Back-End**


## **Overview**

Meu Diário Oficial is a Python-based application designed to monitor the official gazette of Salvador, Brazil, and notify users via email when their names appear in the publications. The application automates the process of checking the gazette daily, making it easier for users to stay informed about public notices that involve them, such as job postings, legal notifications, and other relevant updates.

## **Technologies Used**

This project utilizes the following technologies and libraries:

- **Python**: The primary programming language used to develop the application.
- **Flask**: A lightweight WSGI web application framework used for building the web server.
- **Flask-SQLAlchemy**: An extension for Flask that adds support for SQLAlchemy, an ORM for managing database operations.
- **Flask-Migrate**: Handles database migrations for SQLAlchemy models in Flask applications.
- **pypdf**: A pure Python PDF library used to extract text from PDFs.
- **requests**: A simple, yet powerful HTTP library for making requests to web services.
- **pytest**: A testing framework for Python, used for writing unit tests.
- **pytest-flask**: A plugin for testing Flask applications with pytest.
- **Selenium**: A tool for automating web browsers, potentially used for interaction with web elements.
- **sib-api-v3-sdk**: SDK to interact with the Sendinblue API for sending emails.
- **APScheduler**: A lightweight in-process task scheduler for Python, used for scheduling the daily gazette checks.
- **bcrypt**: A library to hash and check passwords securely.
- **PyJWT**: A Python library for creating and verifying JSON Web Tokens, used for handling authentication.


## **Key Features**

* **Automated Daily Monitoring:** The application downloads the official gazette daily and checks for user-specified keywords.

* **Email Notifications:** Sends an email to the user if their name or specified keyword is found in the daily publication.

* **User Management:** Users can register with their email and desired keyword(s) to start receiving notifications.

## **Installation**

### **Prerequisites**

Ensure you have the following installed on your system:

* Python 3.8 or higher

* Git

### **Steps to Install**

**1. Clone the Repository**

First, clone the repository to your local machine using the following command:

```
git clone https://github.com/Qcarvalhooliveira/Meu_Diario_Oficial.git
cd Meu_Diario_Oficial
```

**2. Create a Virtual Environment**

It's recommended to use a virtual environment to manage dependencies. You can create one using:

```
python3 -m venv venv
```

Activate the virtual environment:

* On macOS/Linux:
```
source venv/bin/activate
```

* On Windows:
```
venv\Scripts\activate
```

**3. Install Dependencies**

Install the required Python packages using pip:

```
pip install -r requirements.txt
```

**4. Set Up Environment Variables**

You need to set up environment variables for the application to function correctly. Create a **.env** file in the root directory of your project and add the following:

```
SENDINBLUE_API_KEY=your_sendinblue_api_key
MAIL_DEFAULT_SENDER=your_default_sender_email
SECRET_KEY=your_secret_key_for_jwt
```

Replace your_sendinblue_api_key, your_default_sender_email, and your_secret_key_for_jwt with your actual credentials.

**5. Apply Migrations**

Before running the application, apply the database migrations:

```
flask db upgrade
```

**6. Run the Application**

Start the Flask development server:

```
python run.py
```

The application will start running on http://127.0.0.1:5000/.

## **Usage**

### **Registering a New User**

Users can register their names and email addresses to receive notifications when their name appears in the gazette.


### **Checking the Gazette**

The application automatically checks the official gazette daily and sends notifications if any matches are found.

### **Stopping the Application**

To stop the Flask development server, press CTRL+C in your terminal.

## **Aplication flow**

#### **1. Success**

This is the standard flow when everything works as expected, and the application finds matches in the official gazette.

**Start daily process**
The application is started and checks if it should run on the current day.
If it's a weekday and not a holiday, the process continues.

**Download PDF**
The application downloads the official gazette for the day.

**Extract text**
The text is extracted from the downloaded PDF.

**Search for keywords**
The application checks if any user-specified keywords are present in the text.

**Send notification**
If a keyword is found, a notification email is sent to the corresponding user.

**End**
The process ends successfully.

**Representation:**
```
Start daily process => Download PDF => Extract text => Search for keywords => Send notification => End
```

#### **2. Non-running day**

This flow occurs when the application is started on a day that does not require checking, such as weekends or holidays.

**Start daily process**
The application checks if it should run on the current day.
If it's a weekend or holiday, the process stops.

**End**
The process ends without performing any actions.

**Representation:**
```
Start daily process => Check if it's a working day => End
```


#### **3. Failure**

This flow occurs when there is a failure during the process, such as an error in downloading the PDF or extracting the text.

**Start daily process**
The application is started and checks if it should run on the current day.

**Attempt to download PDF**
The application attempts to download the official gazette PDF.

**Failure in download or text extraction**
If the PDF download or text extraction fails, the application retries until the maximum number of attempts is reached.

**Send failure notification**
If all attempts fail, a failure notification email is sent to users informing them of the issue.

**End**
The process ends after notifying users of the failure.

**Representation:**
```
Start daily process => Attempt to download PDF => Failure in download/extraction => Send failure notification => End
```

## **Database Process Flow**

#### **1. Create User**

This flow describes the process when a user registers in the application.

**User registration**
The user submits their name, email, and password to the registration endpoint.

**Save user in the database**
The application saves the user's details (with a hashed password) in the database.

**Send welcome email**
A welcome email is sent to the user confirming their registration.

**End**
The registration process ends successfully.

**Representation:**
```
User registration => Save user in database => Send welcome email => End
```


#### **2. User Login**

This flow describes the process when a user logs into the application.

**User login**
The user submits their email and password to the login endpoint.

**Authenticate user**
The application checks if the email exists and if the password matches the stored hash.

**Generate JWT token**
If authentication is successful, a JWT token is generated and returned to the user.

**End**
The login process ends successfully.

**Representation:**
```
User login => Authenticate user => Generate JWT token => End
```


##### **3. Delete User**

This flow describes the process when a user is deleted from the application.

**Request user deletion**
The user sends a request to delete their account, including their user ID.

**Verify token**
The application verifies the JWT token to ensure the request is authorized.

**Delete user from the database**
The application removes the user's data from the database.

**Send deletion confirmation**
A confirmation email is sent to the user, notifying them that their account has been deleted.

**End**
The deletion process ends successfully.

**Representation:**
```
Request user deletion => Verify token => Delete user from database => Send deletion confirmation => End
```

These flow descriptions provide a clear and concise overview of the different processes within your application, both for daily operations and for user management.


## **Testing**

Testing is a crucial part of our development process, ensuring that the application behaves as expected under various conditions. This section provides an overview of the types of tests implemented, how they are executed, and the reasoning behind certain testing decisions.
Types of Tests

We have implemented a variety of tests to cover different aspects of the application:

**Unit Tests:** These tests focus on individual components of the application, such as functions and methods, to ensure they perform as expected in isolation. The majority of our tests fall into this category, as we aim to validate the functionality of specific pieces of logic independently. For example, test_should_run_today verify if the constraint that the app should not run on specific days is respected, other example might be verifying that password hashing in our user model works as expected.

**Integration Tests:** These tests check the interaction between different components of the application. For instance, they verify that the process of downloading a PDF, extracting its content, and matching it with user-provided keywords works seamlessly together. An example is testing the flow where a PDF is downloaded, its text is extracted, and notifications are sent if keywords are found, this would involve diferent parts of our code to work together, so we test them together.

**End-to-End (E2E) Tests:** We currently do not have specific end-to-end tests, but these would typically simulate real user scenarios, testing the entire application workflow from start to finish.

### **Use of Mocks**

Mocks are extensively used in our testing suite to simulate external dependencies and isolate the functionality under test. This approach ensures that our tests are both fast and reliable, as they do not depend on external systems or live data.

**Email Sending:** When testing functions that send emails, we mock the actual email-sending process to avoid sending real emails during testing. Instead, we verify that the correct email content would be sent based on the inputs.

**PDF Downloading and Parsing:** In most cases, we mock the downloading and text extraction process from the official gazette to ensure our tests are repeatable and not dependent on external resources.

**Example:** When testing the process_daily_pdf function, we mock the PDF content to control the test environment. This allows us to focus on verifying that the notification logic works correctly without relying on an actual PDF download.

### **Realistic Testing Without Mocks**

While mocks are essential for most tests, we intentionally include test without mocks to ensure the application behaves correctly in a real-world scenario.

**Example:** The test on test_utils.py for the download_pdf function actually downloads the daily official gazette of Salvador and searches for specific names, such as the current mayor and a secretary. This ensures the entire PDF processing pipeline works as expected with real data. We use the name of the mayor and a secretary to keep this test runing longer without crashes since these names should be in must publications of the gazette.

**Reason for Real Data Testing:** Testing with real data ensures that our application remains robust against changes in the PDF structure or content from the official source. It also helps identify issues that might not be apparent in a fully mocked environment.

**Note on Potential Test Failures:** Due to the reliance on real-world data, these tests may occasionally fail if the specific names we search for are not present in the gazette on a given day. Such failures are expected and should prompt a manual check to confirm whether the names indeed appear in the gazette.

### **Running Tests**

You can run the entire test suite using the following command:
```
pytest
```
This will execute all tests, including unit and integration tests (we currently do not have explicit end-to-end tests), and provide a summary of any failures or errors.

### **Test Coverage Across the Application**

Each core file of the application has an associated test file, where we aim to cover most of the functionalities within that file. However, it's not always a one-to-one mapping—in some cases, a single test can cover multiple aspects of the application. For instance, the test_process_daily_pdf_success test not only verifies that a notification is sent, but by doing so, it implicitly tests that the PDF was correctly downloaded and parsed, and that the keyword matching logic is functioning as intended.

### **Additional Notes**

**Comprehensive Testing:** We strive to ensure that our tests cover as many scenarios as possible, including edge cases. However, as with any testing suite, there are trade-offs between thoroughness and practicality.

**Testing Strategy:** Our strategy includes a mix of isolated unit tests for critical logic, integration tests to ensure components work together, and a few real-world tests that interact with live data to validate the entire system under actual conditions.


## **Author** :black_nib:

* **Queise Carvalho de Oliveira** - [Queise Oliveira](https://github.com/Qcarvalhooliveira)


## License :page_with_curl:
This project is licensed under the [MIT License](https://opensource.org/license/mit/).