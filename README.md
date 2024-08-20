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
1. Success

This is the standard flow when everything works as expected, and the application finds matches in the official gazette.

    Start daily process
        The application is started and checks if it should run on the current day.
        If it's a weekday and not a holiday, the process continues.

    Download PDF
        The application downloads the official gazette for the day.

    Extract text
        The text is extracted from the downloaded PDF.

    Search for keywords
        The application checks if any user-specified keywords are present in the text.

    Send notification
        If a keyword is found, a notification email is sent to the corresponding user.

    End
        The process ends successfully.

Representation:

java

Start daily process => Download PDF => Extract text => Search for keywords => Send notification => End

2. Non-running day

This flow occurs when the application is started on a day that does not require checking, such as weekends or holidays.

    Start daily process
        The application checks if it should run on the current day.
        If it's a weekend or holiday, the process stops.

    End
        The process ends without performing any actions.

Representation:

mathematica

Start daily process => Check if it's a working day => End

3. Failure

This flow occurs when there is a failure during the process, such as an error in downloading the PDF or extracting the text.

    Start daily process
        The application is started and checks if it should run on the current day.

    Attempt to download PDF
        The application attempts to download the official gazette PDF.

    Failure in download or text extraction
        If the PDF download or text extraction fails, the application retries until the maximum number of attempts is reached.

    Send failure notification
        If all attempts fail, a failure notification email is sent to users informing them of the issue.

    End
        The process ends after notifying users of the failure.

Representation:

java

Start daily process => Attempt to download PDF => Failure in download/extraction => Send failure notification => End

Database Process Flow
1. Create User

This flow describes the process when a user registers in the application.

    User registration
        The user submits their name, email, and password to the registration endpoint.

    Save user in the database
        The application saves the user's details (with a hashed password) in the database.

    Send welcome email
        A welcome email is sent to the user confirming their registration.

    End
        The registration process ends successfully.

Representation:

java

User registration => Save user in database => Send welcome email => End

2. User Login

This flow describes the process when a user logs into the application.

    User login
        The user submits their email and password to the login endpoint.

    Authenticate user
        The application checks if the email exists and if the password matches the stored hash.

    Generate JWT token
        If authentication is successful, a JWT token is generated and returned to the user.

    End
        The login process ends successfully.

Representation:

java

User login => Authenticate user => Generate JWT token => End

3. Delete User

This flow describes the process when a user is deleted from the application.

    Request user deletion
        The user sends a request to delete their account, including their user ID.

    Verify token
        The application verifies the JWT token to ensure the request is authorized.

    Delete user from the database
        The application removes the user's data from the database.

    Send deletion confirmation
        A confirmation email is sent to the user, notifying them that their account has been deleted.

    End
        The deletion process ends successfully.

Representation:

sql

Request user deletion => Verify token => Delete user from database => Send deletion confirmation => End

These flow descriptions provide a clear and concise overview of the different processes within your application, both for daily operations and for user management.

## **Author** :black_nib:

* **Queise Carvalho de Oliveira** - [Queise Oliveira](https://github.com/Qcarvalhooliveira)


## License :page_with_curl:
This project is licensed under the [MIT License](https://opensource.org/license/mit/).