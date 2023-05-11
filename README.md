# Flask Challenge

## Description
This project is main objective is to create a URL shortener API.

## Architecture
![Architecture Diagram](diagram.svg)
1. long_url or `url` is the user input
2. The system checks if long_url is in database.
3. If it is, it means the long_url was converted to short_url before. In this case, fetch the short_url from the database and return it.
4. If not, the long_url is new. A new unique ID and short_code is generated.
5. Converted the long_url to the short_url.
6. Save in the database.

## Shorten Algorithm
It is the `shorten()` method within `UrlShortner`.
This is how it works:

This function shorten() takes an integer num as input and returns a string representing the base 62 encoding of that integer.

Base 62 encoding is a method of representing numbers using a character set of 62 alphanumeric characters, consisting of 0-9, a-z, and A-Z. Each character can represent a digit in a number with a different weight, based on its position. The base 62 encoding scheme is commonly used in URL shortening services, where a long URL is converted into a shorter code consisting of alphanumeric characters.

The function first initializes a string alphabet containing all the 62 alphanumeric characters used in the base 62 encoding scheme. It then calculates the length of the alphabet string and stores it in the variable base.

Next, the function initializes an empty list result. It then enters a while loop that keeps running as long as the input integer num is greater than zero. In each iteration of the loop, the function uses the divmod() function to calculate the quotient and remainder of num divided by base. The remainder is then used to index into the alphabet string and the corresponding character is appended to the result list. The quotient is updated to num for the next iteration.

Finally, the result list is reversed and concatenated into a string using the join() method. This string is then returned as the output of the function, representing the base 62 encoding of the input integer num.

## How to run the project
* Be sure to be running python 3.10^
* Create a virtualenv: `python -m venv virtualenv` and activate it `. virtualenv/bin/activate`.
* Install dependencies: `pip install -r requirements.txt`
* Start the api service: `cd api_service ; flask db migrate; flask db upgrade ; flask run`

## How to run the bot
* Be sure to be running python 3.10^
* Create a virtualenv: `python -m venv virtualenv` and activate it `. virtualenv/bin/activate`.
* Install dependencies: `pip install -r requirements.txt`
* Run the flask command: `cd api_service; flask crawler`