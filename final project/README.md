# Cambia's Software MVP
#### Video Demo:  <https://www.youtube.com/watch?v=yx8yjB8gtHA>
#### Description:
##### General description of the project:
Cambia's software is a A web application to manage users, products and clients with different user roles. It is an MVP of the software I would like to use for my own business: an import company that distributes plumbery products mainly in Lima, Peru. I have Clients, Products and Workers that will interact. In this first version, the main goal was to define the main pages so the admin roles could do more actions than the salesman.
### Structure of the project:
The software was built with Flask as the framework, Python for the backend and javascript for a couple of interactions.
For the HTML and CSS I used Bootstrap 5. The colors and design was chosen using the colors of my own business: Cambia. For the database I used SQLite3.
##### Database tables:
My database's name is Cambia.db. It has 7 tables as follows:
1. users: this table has the users. I used a hash for the password. It has two supportive tables: banks and user_type.
2. user_type: there are just three user types that will be explain on the next chapter.
3. banks: it has the list of banks by id.
4. clients: it has the list of clients. It is the most complex table. Has three supportive tables: users, districts and provinces.
5. districts: it has a list of the districts.
6. provinces: it has a list of the provinces.
7. products it has the list of products. Each product has a code, a max and min prices.
##### Pages in the software:
We have 4 different pages in the software: Clients, Products and Users.
1. Clients: it has the list of the clients. You can interact with the page seeing the list of clients, creating new clients and editing existing ones. The interactions depend on the permissions.
2. Products: it has the list fo products. You can interact with the page seeing the list of products, creating new products and editing existing ones. The interactions depend on the permissions.
3. Users: it has the list of users. You can interact with the page seeing the list of users, creating new users and editing existing ones. The interactions depend on the permissions.
4. My Account: it has the information of your own account. You can change some information and reset your password.
5. Log out: you close your session.
##### User types:
There are three different user types: super_admin, admin and salesman. Each rol have different permissions as follows:
1. super_admin: can do anything. Visualize, create and edit users and products. Also visualize, create and edit clients, assigning them to a sales user. Can change information and the password of his own user.
2. admin: can do anything except creating, editing an visualizing users. Can change information and the password of his own user.
3. sales: can see his own clients, edit and create new ones but only assigned to himself. Can see the products but can't edit or create new ones. Can't see the users. Can change information and the password of his own user.
##### Backend:
I used Python for the backend with Flask framework. Some of the main learnings doing this projects are:
1. I didn't know how to send information from the HTML but then redirect to another route. Json usually waits a response. It made me look for answers almost 10 hours. Finally I decided to use a href with a variable at the end to redirect to a variable route and use this variable for the new HTML. I am sure is not the best design, but I was crazy to find and answer. Anything worked for me so I could use it for this first MVP.
2. The information about the session variable. My project was about differente roles and permissions so keeping the information about the user that Logs in is crucial. I had some troubles but finally obtained the answer.
3. I used a lot Jinja with for loops and if conditions. It was fun.