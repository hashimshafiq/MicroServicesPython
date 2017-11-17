## Cloud Microservices

This is a demo application for learning "How to build your own "Cloud MicroServices".
We design our own API in this demo.

### Tools and Technologies
* Python
* Flask
* MongoDB
* SQLLite3
* Ajax
* REACT
* Javascript
* HTML5
* CSS

### API Architecture

#### USERS API

**GET /api/v1/info**

Return all the info of the API V1 like build-date-time, methods supported, version

**GET /api/v1/users**

Return all the users stores in the users table in the database. For example name,email,username,password

**GET /api/v1/users/<ID>**
  
Return a specific user of having "ID" as given instead of displaying all.

**POST /api/v1/users**

Insert a new user in the users table.

**DELETE /api/v1/users**

Delete a user with a specific id

**PUT /api/v1/users/<ID>**
  
Update a specific users already present in the users table

#### TWEETS API

**GET /api/v2/info**

Return all the info of the API V1 like build-date-time, methods supported, version

**GET /api/v2/tweets**

Returns all the tweets made by different users

**GET /api/v2/tweets/<ID>**
  
Return a specific tweet shared by a user

**GET /api/v2/tweets/<tweetBy>**
  
Return all the tweets shared by a specific user

**POST /api/v2/tweets**

Insert a new tweet in the tweets table


### USER INTERFACE

#### LOGIN PAGE

![Login Page](http://i63.tinypic.com/262lh7r.jpg "Login Page")

#### SIGNUP PAGE

![Signup Page](http://i63.tinypic.com/eg7m9d.jpg "Signup Page")

#### DASHBOARD PAGE

![Dashboard Page](http://i68.tinypic.com/24d0uq8.jpg "Dashboard Page")

#### PROFILE PAGE

![Profile Page](http://i63.tinypic.com/10xhqad.jpg "Profile Page")
















