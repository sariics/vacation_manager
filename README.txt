#Vacation Management

For this app to work you will have to have the following installed:
- Python > 3.6 (best 3.9)
- MongoDB

##How to use:

1. Download the project and install the requirements form the requirements.txt.
2. Go to app.py and run the script.
3. This app runs on a flask development server, go to http://127.0.0.1:5000.
4. During the creation of the DB, 3 users are created with the following credentials:
    - user: Jane Doe, pw: Jane123
    - user: Bilbo Beutlin, pw: Bilbo123
    - user: Arno Duebel, pw: Arno123
    User any of the above to log into the users account.
    Here you can create new vacation requestes and delete pending ones.

Note:
- One should never store or upload user credentials like this, this is only a small sample project.
- MongoDB will store the database that is created when running this app in the path
you specified when downloading MongoDB.