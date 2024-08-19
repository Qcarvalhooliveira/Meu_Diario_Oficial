# **Meu Diário Oficial - Back-End**


## **Overview**

Meu Diário Oficial is a Python-based application designed to monitor the official gazette of Salvador, Brazil, and notify users via email when their names appear in the publications. The application automates the process of checking the gazette daily, making it easier for users to stay informed about public notices that involve them, such as job postings, legal notifications, and other relevant updates.


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

## **Author** :black_nib:

* **Queise Carvalho de Oliveira** - [Queise Oliveira](https://github.com/Qcarvalhooliveira)


## License :page_with_curl:
This project is licensed under the [MIT License](https://opensource.org/license/mit/).