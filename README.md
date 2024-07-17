
# E-Commerce 

This is an E-Commerce Website with 

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Requirements](#requirements)
- [Contributing](#contributing)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/pranshuthakur15/E-Commerce.git
    ```

2. Change to the project directory:

    ```bash
    cd E-Commerce
    ```

3. Create a virtual environment:

    ```bash
    python -m venv venv
    ```

4. Activate the virtual environment:

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

5. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

Make sure you Create a superuser Using the command :
 ```bash
python manage.py createsuperuser
```
Create an Admin account to manage Vendors, Purchase Orders, Return Orders etc.
Create a Customer Account to add the product to your cart and make payments.
Create a Vendor Account to Get Purchase Orders (via Admin).
Note: There is no direct access to vendor Login you have to use a URL to access Vendor creation and login.

## Requirements

This project requires the following Python packages:

- asgiref==3.8.1
- certifi==2024.2.2
- charset-normalizer==3.3.2
- Django==5.0.4
- django-formset-js==0.5.0
- django-jquery-js==3.1.1
- djangorestframework==3.15.1
- idna==3.7
- pillow==10.3.0
- requests==2.31.0
- sqlparse==0.4.4
- urllib3==2.2.1

## Contributing

1. Fork the repository.
2. Create a new branch:

    ```bash
    git checkout -b feature-branch
    ```

3. Make your changes.
4. Commit your changes:

    ```bash
    git commit -m 'Added feature'
    ```

5. Push to the branch:

    ```bash
    git push origin feature-branch
    ```

6. Create a new Pull Request.




