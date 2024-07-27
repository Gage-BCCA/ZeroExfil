# ZeroExfil - 🔐 A Link Shortener with Password Protection 🔐
I want to be a security-focused developer, and what better place to start than our first unit project? In this app, you provide a URL (like https://google.com) and a password. You'll get back a link that'll look like http://127.0.0.1:5000/0/*random gibberish*. This link would look different if it was ever published on the internet, but that'll have to be when I have the money to rent processor time for a server and to register a domain name.

You can then share this link with your friends. When they navigate to it, they'll run into a "URL Gate", which asks for a password. If they can correctly enter this password, they'll automatically redirect to the original link. If they can't enter the correct password, they'll never get access to the original URL. Pretty cool, right?

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
