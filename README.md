# student_app
This is full-stack web app built using Flask. this application is made to manage their academic activities by providing tools like TO-DO, blog, and posting notes

## Features are 
1. User Authentication
-login and signup
- only that user can see thier task, blogs, and notes
- logout 

2. TO-DO list
- write down the task they have
- edit the tasks 
- mark task as complete 
- also can delete form the list 

3. blogs
- create and delete blog posts
- view blog post
- delete blog

4. image uplods
- upload notes image
-view uploaded image
- delete image


## project structure
app.py
templates/
base.html
blog.html
dashboard.html
index.html
login.html
notes.html
signup.html
todo.html

static/
style.css

app.py - main backend file that controls the entire app

## templates/
base.hmtl
base layout of all page

index.html
homepage of app

signup.html
singup page for new user 
collect the info and store in db

login.html
login page for users

dashboard.html
main user dashboard after login show all the tools

todo.hmtl
task managment page where user can add,update,complete and delete tasks

blog.html
blog page for user
user can add blogs 

notes.html
user can upload image of notes and delete

## static/
style.css
frontend styling file helps to design app

uploads/
folder that store the uploaded image

Nihar_app.db
SQLite database file.
Stores all data including users, tasks, blogs, likes, comments, and images.\


## How to Run
pip install flask
python app.py



## Database
SQLite database: `Nihar_app.db`

## Author
Nihar Patel
