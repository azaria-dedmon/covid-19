# Covid-19
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/db1476eb3cc745d8b2b82b762228c0b6)](https://app.codacy.com/gh/azaria-dedmon/covid-19?utm_source=github.com&utm_medium=referral&utm_content=azaria-dedmon/covid-19&utm_campaign=Badge_Grade_Settings)
[![Coverage Status](https://coveralls.io/repos/github/azaria-dedmon/covid-19/badge.svg?branch=master)](https://coveralls.io/github/azaria-dedmon/covid-19?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/939cec24acf41c03c578/maintainability)](https://codeclimate.com/github/azaria-dedmon/covid-19/maintainability)

## Description
This app helps people find their nearest covid-19 testing site.
https://covid-19-testing-app.herokuapp.com/
### Features
#### All users can
-   View testing locations on our interactive map.

#### Registered users can
-   Customize their profiles by adding images of themselves.
-   Make available their status so that other users can see.
-   Search other users and see their status.
-   Post/Views reviews for testing sites.

## Tech Stack

### Back-end
-   Python
-   PostgreSQL
-   Flask

### Front-end
-   HTML
-   CSS
-   Mapbox GL JS

### Resources
- Database Schema: https://dbdiagram.io/d/6005df5680d742080a36d952
-   Covid-19 API: https://documenter.getpostman.com/view/8854915/SzS7PR3t?version=latest
-   Mapquest API (Geocoding): https://developer.mapquest.com/
-   Mapbox API: https://docs.mapbox.com/api/overview/

### Features / Endpoints
**User**

-   **GET** `/` homepage shows covid-19 symptoms and a drop down list for visitors to search available states and their testing locations on an interactive map.
-   **GET** `/location` page renders interactive map of the visitor's selected state. All testing location's for the state will be listed here.
-   **GET** `/register` shows form to register for an account.
-   **POST** `register` creates an account.

**Endpoints For Authorized Users**

-   **GET** `/login` shows form to login to account.
-   **POST** `/login` logs in to account.
-   **GET** `/logout` logs out of account.
-   **GET** `/user` shows user profile and their selected state's testing locations.
-   **GET** `/user/edit` shows user information and allows them to make edits to their profile.
-   **POST** `/user/edit` add changes to user profile.
-   **GET** `/user/delete` allows users to delete their accounts.
-   **POST** `/user/delete` processes user account deletion.
-   **GET** `/search-user` shows searched user's profile page.
-   **GET** `/add/location/review` allows user to leave reviews for testing sites.
-   **POST** `/add/location/review` posts user review of testing site.
-   **GET** `/location/review` allows users to see testing site reviews.
-   **GET** `/edit/review/<int:review_id>` allows user to edit their reviews.
-   **POST** `/edit/review/<int:review_id>` posts review changes.
-   **GET** `/delete/review/<int:review_id>` allows users to delete their reviews.
-   **POST** `/delete/review/<int:review_id>` processes review deletion.

### Setup Instructions

-   Clone the repository `https://github.com/azaria-dedmon/covid-19.git`

-   Go to https://developer.mapquest.com/ to sign up and get your FREE API key.

-   Go to https://account.mapbox.com/auth/signup/ to sign up for an account and
 receive your Mapbox access token.

-   Create an environment variable named `key` and set the value equal to your Mapquest API key

-   In `location.html`:
    -   Set `mapboxgl.accessToken` equal to your Mapbox access token.

-   In `config.py`:
    -   Set up the following:

    -   ` DevelopmentConfig `
        -   ``postgresql:///your_database_name``
    -   ` TestingConfig `
        -   ``postgresql:///your_database_name``

-   Setup a virual environment:
    -   `python3 -m venv venv`
    -   `source venv/bin/activate`

-   Install project requirements:
    -   `pip3 install -r requirements.txt`

-   Create Local Database:
    -   `createdb <your_database_name>`

-   Run the application:
    -   `Python3 run.py`

-   Run application in the browser:
    -   `localhost:5000`

-   Test application by running the following command in the terminal:
    -   `coverage run -m unittest discover tests -v`