# ZeroExfil - A Link Shortener with Password Protection 🔐
Welcome to ZeroExfil, a simple web app with a REST API that allows you to shorten and protect sensitive URLs with a password. This simple extra layer of security can help stop OSINT operations and data exfiltration against your organization.

## Features
- **Secure Links with Ease**: Provide a link and password, click submit, and share the new protected link with other parties
- **Battle Hardened Encryption**: ZeroExfil uses Scrypt, a purposely slow hashing algorithm, and salting, to insure that your links stay safe.
- **REST API**: programatically secure links with a simple API that exposes all app features to the shell

## Getting Started
### Prerequisites
- Flask
- Flask_Scrypt
- Pytest

### Installation
1. Git clone the repo
2. Navigate to the project directory, and "pip install -r requirements.txt" in your shell or terminal to install the needed libraries
3. Use the built-in Flask developmental web server by using "flask run" in the src directory, or by running the app.py file
The app should be running at http://localhost:5000

### Usage
There are two methods of using the application: the web browser or the REST API.

#### Web Browser
To use the app in your web browser, you can use any modern web browser and navigate to http://localhost:5000. From here, you will be greeted with the homepage that asks for a URL to secure.

#### REST API
The API for the program exposes all of the same functionality as the front-end.

## API Endpoints

- **POST** /api/secure_link

This endpoint takes a POST request with JSON in the body, consisting of a "url" field and a "password" field.

```
{
    "url": "https://google.com",
    "password": "12345"
}
```

Returns the new secured URL.

- **POST** /api/unlock_link
  
This endpoint takes an ID and password in a POST request. If the password is correct, it returns the original URL.

```
{
    "id": "UASDF12FA",
    "password": "12345"
}
```

- **GET** /api/database_info
  
This endpoint just returns the number of rows in the database.

## How It's Done ✔️
### Creation of Secured Links
When you first enter a link and password, a random string is generated to serve as the unique ID for the link. We search the database and check for any collisions of IDs (to really, really make sure they're all unique), and if there are no problems, we use this ID as the endpoint for the URL. We can then move onto securely storing the password. 

#### Password Storage 💻
Password storage can be a complicated topic, but the general overview is:
- A password is NEVER stored in plain text, but rather "hashed" with a hashing algorithm. In this app, the algorithm is called "scrypt". When you run a string through a hashing algorithm, you get back a fixed-length string of seemingly random characters. The important thing to note is that when you run the exact same string through a hashing algorithm twice, you'll get the same "random" string of characters returned. This cannot be reverse-engineered, meaning that we cannot take the random string of characters and derive the original string.
- We then "salt" the password. We take another randomly generated string, and throw it in the mix. It makes it where, in the event that the database is stolen and your password is "password123", hackers can't instantly guess it. Looking at you, Jet.
- We store these two values (the hashed password and the salt in plain text) in a single field with a dollar sign as the delimiter.

After that, the entry is stored in the main data file and is ready for further use.

### Using the Secured Links 🛂
When your friend navigates to a ZeroExfil link, they'll run into the URL Gate, which asks for the password. Once a password is provided, the process looks like this:
- We find the row that contains the Unique ID
- We hash the provided password using the same hashing algorithm that was used in the creation process. If the password used when creating the link and the password provided during the process are exactly the same, we get the same hash.
- The server sends a HTTP 302 and redirects the user to the orignal website.

If the password provided is not correct, it just redirects to the same URL Gate page, prompting a refresh on the user's browser.

## Cool Things
Here are some cool things of note in this project.

### Scrypt is *slow*... on purpose
To prevent hackers from writing a scrypt that can try 17 billion combinations a second, the scrypt hashing algorithm is purposely slow. A good actor that is properly using the site will not be inconveinced, but a bad actor trying to brute force a password will have a massive amount of time added to the overall process.

### I created a simple API to use in the command line
I honestly didn't read that output had to be in the terminal, so I threw this on top of the project. It is still cool, though.
