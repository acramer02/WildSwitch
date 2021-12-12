Our design can be split into a few parts. There is a SQL database, the app.py file, which contains the code to make the app work, the helpers file, from which functions are called in app.py, the layout page for the html, and the html pages themselves. This file will go over the design decisions that we made while coding each of them.

#
#
#
# SQL database

We used 11 tables within our data 7 of which we continue to use to run the app. Those four are Batting, Pitching, Cards, Users, Market, Search and SearchUser.
Users stores every user's unique id, username, hashed password, and cash values.
Cards stores the playerID, fullName, position (0 or 1 for batter or pitcher), status (0 or 1 for for sale or not for sale) and username of the owner). Note that not every player is in the cards file. Only the players whose cards' are currently owned.
Batting and Pitching store the names, playerIDs, years, teamID, and other relevant stat for every player in our database. 
Market is a table that gets deleted and re-created with each new log in. It stores the eight players who appear on the buy page.
Search and SearchUser are used within the search function to store whatever information the user is looking up. We can then access those tables to get the data to display on the HTML pages.


When we refer to SQL commands below, they are addressing these four tables.

#
#
#
# APP.PY
Our fundamental principle throughout the implementation of this file was to deal with any POST method submissions first by checking for all possible errors, then updating all relevant SQL tables, then redirecting the user to wherever we want to take them. After that, we then have the relatively easier code which deals with the GET method, in which we merely have to display information. We will explain how this manifests itself in each section, but that pattern will hold true for every function we call. A lot of our coding included SQL querying, using if statements to address different options and deal with possible errors, and storing and passing the correct information either to HTML pages or using it in SQL queries.

# Set up
The first 44 lines of our code are devoted to loading and importing all of the tools we need to run our app.

# register
If the method is POST, we run three quick checks to make sure that the user has entered a username, password, and confirmation. We then check via a count query in SQL if that username is already taken, then we check that the password and confirmation match. We get all of this work using the syntax request.form.get, a syntax we use throughout the code. I will just explicitly explain here that it is the simplest way for us to get user input from a form. Once we have ensured that none of those errors are present, we hash the password, then store the username and hashed password in our SQL table Users, and then we log the user in, build a market, and return them to the homepage. If it is just a GET method, we simply show the user the register.html page.

# login
We first clear the session to make sure no user is logged in. Then, if it's a POST method, we ensure that the user inputs both a username and password into the form. We then query our Users table to make sure first that the username exists and then that the password is correct. If that is all true, we then set the session's user_id equal to that user's id, use a SQL command to add 5 to cash, build their random market, and take them to the homepage. If the user is at the page via a GET method, we simply show them the login.html page.

# log out
Clears session, returns the user to the login.html page

# NOTE: All the following have the @login_requried decoration to ensure they can only be accessed if a user is logged in

# index
Displays the index.html page

# mycards
We create two empty lists for batters and pitchers. We then append every batter to the batters list where the username matches and its position is equal to batter, and then do the same thing for hitters. We then also use SQL queries to get the user's cash and number of cards. We then pass all of that through to the mycards.html template so that it can use this information when displaying cards.


# search
When the user inputted anything via POST, we first made sure to get their input via request.form.get. The two things that a user could input were a user/player name and the criteria (batter, pitcher, or user) from the dropdown menu. We used if statements for each criteron. Within each, we checked if their inputted name was within the corresponding database.  If their search was valid, we took the corresponding information, put it into a list, and passed it through to either the search_user or search_player function, which then will deal with buying from search more specifically with the correct case. It also redirects to the GET method for either search_user or search_player, so it will display all of the cards for the player. If their search was invalid, we returned an error. If the user got to search via a GET method, we simply displayed the text field and the dropdown menu.

# search_user
When the user inputted anything via POST, we first made sure to get their input via request.form.get. The two things that a user could input were a player name and year. We made sure that both of these fields were filled out with if statements. If they were filled out, we stored the input and got all of the data that was stored in the SearchUser table. Then we compared the input to the table. If they did not match any player in the table, we return an error. If they did match, we checked to see if the player was for sale by using a SQL query to get the card’s status. If it was for sale, we used a SQL query to determine the auction price of the card. If the user's cash was less than the auction price, they could afford the card. If they could afford it, we then updated the Cards table to set a new user who owned it and to indicate it wasn't for sale. We then updated the user's cash to subtract the cost, then changed the value in the Batting or Pitching table to indicate that it wasn't for sale, and then updated the previous owner's cash to indicate the changes. We did all of that with SQL. And after all of these changes, we show the users the mycards.html page.

If the user reached via GET (i.e. redirected via Search) we use the same concepts we use in mycarrds to display the information. We create empty lists for batters and pitchers. We then queried the pitchers and batters databases to get all of the user's cards, appended that information to our lists, and then passed that information through to the usersearch.html page.

# search_player
When the user inputted anything via POST, we first got all the info that we just added to the Search table about these cards. We then made sure the user inputted wa year.  If they were filled out, we stored the input. Then we compared the input to the data from the table. We then get the player's position and check from the corresponding table to count the number of players with that year. If there are no matches, we return an error. We then check if the card is owned with a SQL query. If it is, we return an error. Otherwise, we get the user's cash and the value of the card with SQL queries to make sure they can afford the card. We then do a few SQL queries to update the user's cash stores and change the card's status. After all of that, we redirect the user to their mycards.html page.

' If they could afford it, we then updated the Cards table to set a new user who owned it and to indicate it wasn't for sale. We then updated the user's cash to subtract the cost, then changed the value in the Batting or Pitching table to indicate that it wasn't for sale, and then updated the previous owner's cash to indicate the changes. We did all of that with SQL. And after all of these changes, we show the users the mycards.html page.

If the user reached via GET (i.e. redirected via Search) we use the same concepts we use in mycarrds to display the information. We create empty lists for batters and pitchers. We then queried the pitchers and batters databases to get all of the user's cards, appended that information to our lists, and then passed that information through to the usersearch.html page.

# buy
We implement our buy function to work as follows. When the user submits some input to site via a POST method, we execute a SQL query to get the user's cash value and another one to get the the player's information that was selected in the dropdown menu by the user. We then wanted to first check that the card isn't already owned. If it is, we return an error. Then we check if the user can afford the card. If not, we return an error. But then, if the user can afford it and the card is available, we execute three SQL commands which adds the information into the cards table with the right data, updates the user's cash and makes sure the card is unavailable. WE also make sure the card's status within the batting or pitching table is then changed to own. After all of this, we take the user back to their colleciton page. If they are just coming to the buy page but haven't submitted anything, we deal with the GET method. In there, we create empty lists for batters and pitchers and make a list of the eight players listed in the market table. From there, we then fill out the lists of batters and players by checking their positions, and appending their information to the lists. After all of that, we pass the batters and pitchers' information through to the buy.html page.

# sell
Far and away the most complex function call within our code. We're going to try to break it down to its fundamental elements here. First, we check that the user submitted something via the POST method. If they did, we are then going to check if they submitted the sell to market form.

If we are dealing with the sell to market form, we're first going to ensure that the user inputted a name and a year. We then check via a SQL query that that card does exist and is owned by the user. If all of that is true, we then get the market value, position, and status of the card and the cash stores of the user via SQL queries and then save those values. Then we can update the user's cash to add the value of the carrd. We then want to delete the card from the Cards table (which only stores currently owned cards). After that, we then update the status in either the pitching or batting file to show that it isn't owned by anyone (again, via SQL commands). Finally, after all of that we can redirect the user back to their mycards.html page.

If they submitted the place for sale form, we are going to make sure they submitted a player name, a year, and a value. Just like selling to market, we then use a SQL command to make sure the user owns the card they inputted. If they do, we then will set the auction price to the inputted price and change the status to for sale within the Cards table. After that, we will get the position and update their status to "For Auction"

If the user simply reached the page via a GET method, we are going to do essentially the same process as in mycards to display the user's cards. We created empty lists for batters and pitchers, then used SQL queries to Select all the batters and pitchers from Cards owned by that user. We then iterated through that data, appending it to the batters and pitchers' lists. We then queried for the cash stores and number of cards for the user. We then passed all the information to sell.htm.

#
#
#
# HELPERS.PY
We used this file to define a bunch of helper functions that we call repeatedly in app.py

# login_required
honestly, we just took it from Finance, but the way it works is that it checks if the session has a user_id. If not, it takes you back to the login page without giving you access. Otherwise, it grants you access to whatever function you apply it to.

# apology
prints an inputted error message on apology.html

# generate_user
takes a username as input, and returns the equivalent of the mycards page for that user, albeit without their cash stores value. This was easier than coding it in the way we did for mycards because we had to be able to make some modifications to allow users to buy cards off of that page. We implemented this by using SQL queries to get the info for the players and creating two empty lists for batters and pitchers. We then for-looped through all of the players we got through our SQL query, appending them to pitchers and batters accordingly, and then passing that info through to usersearch.html.

# usd
Again, something we took from Finance. But the way it works is it takes a number, converts it to a two-decimal float, and then adds the dollar sign in front. This was important for us to keep because we wanted to work with numeric values for money, but display it in dollar format.

# build_market
This was an important function for us to create because we wanted to show users a random selection of cards every time they logged into their account. It takes one command that has two options (0, 1). Inputting a 0 builds a new market, while inputting a 1 prints the existing market. So every new login requires a command of 0, but within each login, we call it with the command of 1. As for writing the code, we first make sure that we clear our previous Market table in SQL so that we start fresh every time. Then we select 4 random, unowned cards from pitching and batting respectively via SQL queries. We then loop through those lists and fill the Market table with the relevant data that will then allow us to access those players' information when we need to use the buy function.

#
#
#
# HTML
Here is a list of all of our HTML pages apology.html, batter.html, buy.html, index.html, layout.html, login.html, mycards.html, pitcher.html, register.html, search.html, sell.html, and usersearch.html. Rather than go through each individual page's HTML and repeat ourselves over and over, we will explain the features that appear somewhere on one of our pages. We will explain how they work, and then also mention upon which HTML pages they appear. The one exception is layout.html.

# layout.html
In this file, we set up the Jinja that we use in the rest of our files. This saves us a ton of time and effort. In here, we access our Boostrap, our own CSS stylesheet, we layout the navigation bar on top of the screen, and include our footer. This saves us time and makes our code cleaner for all of our other pages.

# Cards (appears on batter.html, buy.html, mycards.html, pitcher.html, sell.html, usersearch.html)
For a website focused on playing cards, naturally, this was an important element of what we were doing. The general principle behind these cards was that we implemented the layout from Bootstrap. We then wanted to pass in the relevant statistics. We explained above how we created lists that we passed in from the app.py file. We then simply had to combine Bootstrap, our own text labeling each statistic, and then Jinja in which we indexed into our list to print the important information in a style that looked like a playing card.

# Forms and buttons (appear on batter.html, buy.html, login.html, pitcher.html, register.html, search.html, sell.html, usersearch.html)
Again, this was another absolutely ubiquitous and crucial component for an information-heavy website. We needed users to be able to input exactly what they were looking for. We used forms, within which had input options so that people could type in data and submit buttons to enter it. This was also very easy to then use in our app.py file, as we only had to use the syntax request.form.get("name_of_form") to compare the user inputs with our data tables.

# Dropdown menu (appears on buy.html, search.html)
Used the option syntax to create a unique option on the dropdown menu for all 8 players listed on buy.html, and all 3 options (batter, pitcher, user) on search.html.

# Various types of text (all files)
Forms and buttons were how we dealt with user input, cards were key for displaying information, but for the most part, a lot of HTML code simply required printing text, and so we used lots of different header and paragraph types to print what we wanted on the website.

# Note
On various pages, we had to utilize Jinja for-loops. This was essential because we couldn't hard code in data because so much of what we were displaying depended on the data we were working with. So we rarely knew how many cards we would be displaying or whose cards they would be. And so we very often had to for-loop through the lists we passed into the HTML to make sure that we printed all the information we needed to.


#
#
#
# CSS
We used Bootstrap pretty heavily, especially for the cards, and then made our own stylistic decisions on our own stylesheet mostly based on trial and error.


