COMPILING AND CONFIGURING:
Our website is available at the url https://wild-switch.herokuapp.com/. You can go here to view and test the site. Below are instructions on how to use the site and what to test for. Feel free to explore more if there is anything you are interested in or curious about. 

A BRIEF NOTE ABOUT PLAYER DATABASE:
First, credit to http://www.seanlahman.com/baseball-archive/statistics/ for the data. Second, we have trimmed the data as follows. We started with data going back to 1900. We excluded everybody before 1960 who is not in the Hall of Fame. We excluded everybody before 1980 who was not an all-star. Realistically, we believe that the farther we go back, non-elite players become less relevant. We then needed a way to sift through players who did not record meaningful statistics in a given season. Batters had to meet this standard: At-Bats ≥ 130 and Games ≥ 50. Pitchers had to meet this standard: Games ≥ 10 AND Batters Faced ≥ 100. Just in case you search for an obscure player from 1920 and wonder why he's not there.

USAGE AND TESTING:
The basic functions of our website are laid out on the homepage. However, we will give very explicit instructions on how to use and test every element of our website here. Those functions are the following: register, login, view page instructions and credits, buy cards from random market, buy from search, buy from users, search for batters, search for pitchers, search for users, sell to market, put for sale with new value, view collection and cash amount, and logout. Below are explanations of what each does.

# REGISTER
Function - The register page allows users to create an account by entering a username and password. 
Usage - When you go to the site, it will direct you to a login page. In the top right corner, there are two buttons, log in and register. Upon clicking the register button, you will be redirected to a register page. It will ask you to enter a username, a password, and a password confirmation. You will get an error meesage if any of the following are true: you leave a text box blank, your username is taken, or your passwords do not match. Otherwise, you will be allowed to register, meaning the app will store your username and password to allow for future login. You will then be redirected to the homepage.
Testing - 
don't enter username --> Sorry. Please enter username.
don't enter password --> Sorry. Please enter password.
don't enter password confirmation --> Sorry. Please enter confirmation.
enter taken username (e.g. Andrew) --> Sorry. Username taken.
enter different passwords --> Sorry. Passwords do not match.
enter unique username and matching passwords --> [redirected to homepage]

# LOG IN
Function - The log in page allows registered users to log in when they come to the site
Usage - Allows you to log in to your account to use the site. Users must enter correct username and password and submit to log in. You will get an error if either of the following are true: you leave a text box blank or the username and password haven't been registered. We also increase your cash by five every time you log-in to incentivize repeated usage of the site, and allows users to continue improving. 
Testing - 
don't enter username --> Sorry. Must provide username.
don't enter password --> Sorry. Must provide password.
incorrect username and/or password--> Sorry. Invalid username and/or password
correct username and password--> [redirected to homepage, and cash will be five greater than before]


note: all the following functions require log-in

# HOMEPAGE
Function - The homepage is the default page after login/register. It shows the user the site's functions, rules, and credits the data source.
Usage - Same as the function. 
Testing - 
register or log in --> redirects to homepage
click on WildSwitch in the top left corner from any page --> redirects to homepage

# BUY CARDS FROM MARKET
Function - Shows users 8 random cards, and gives them the option to buy any of them. 
Usage - Go to the buy page by clicking the "Buy" button on the top left of the screen. From there, you can select the name of any of the eight cards displayed on the page and hit the buy button. When you hit the buy button, you will be redirected to view your collection. Your cash will decrease by the price listed on the card. Note that these 8 cards will be the same until you logout and then log back in. 
Testing - 
click the "buy" option on the top left --> redirects to page, showing 8 cards
select name from dropdown menu and enter buy button --> redirects to collection page with card on it and less cash
click on card you already bought (still there in same session) --> error message: Sorry. Already purchased!
select name from menu where value is greater than your cash --> error message: "Sorry. Can't afford.

# SEARCH FOR BATTERS/PITCHERS/USERS
Function - The search function allows users to search database for any batter or pitcher and view cards of that player from every year of their career. You can also elect to search for users. That function allows you to view what cards another user owns, their price, and whether or not they're for sale.
Usage - Click on the search button on the navigation bar at the top of the page. If a user types in a valid player name and makes sure to select their position (batter or pitcher), they will be redirected to a page displaying cards from all of their seasons, including price and value. If you enter a valid username, you will be redirected to see their cards.
Testing - 
enter invalid player name (or at least not with the right position) --> Sorry. Not a valid full name or incorrect position.
enter invalid username with --> Sorry. Not a valid username.
enter valid batter name (e.g. Babe Ruth) with batter full name selected --> [redirects to page showing cards from every season]
enter valid pitcher name (e.g. Sandy Koufax) with pitcher full name selected --> [redirects to page showing cards from every season]
enter valid username (e.g. Nicole) with user selected--> redirects to page showing all of their cards

# BUY CARDS FROM SEARCH
Function - Allows users to buy cards after they've searched for a specific player
Usage - After entering a specific player name on the search function, users will see all of that player's seasons. They will then have the option to select which year's card they would like to purchase. That card will then be added to your collection, that cash value will be deducted from your account, and you will be redirected to view your cards.
Testing - 
enter a year that the player does not have a card for --> Sorry. Please enter a valid year.
enter a year that the player has a card for --> [redirects to "Collection" page, where your cards now include the player and you've lost that cash value]

# BUY FROM OTHER USERS
Function - When viewing another user's cards, if they are set with the status "for sale", you can enter a card name and year and buy it.
Usage - After searching for another user's cards via the search function, you will be able to see all of their cards. There are also two text fields at the top of the screen that allow you to enter a name and a year. If you enter a valid name and year for a card on the page that is marked for sale, it will be added to your collection, taken away from theirs, and both users' cash values will be updated.
Testing - 
go to another user's page (e.g. Andrew) and select a player that is not for sale (e.g. Mickey Mantle 1954) --> error message: Sorry. Card is not for sale.
go to another user's page (e.g. Andrew) and select a player that is for sale (e.g. Chase Utley 2008) --> [redirected to your collection, which now includes Chase Utley]
go to another user's page (e.g. Andrew) and enter a name that is not on the page --> error message: Sorry. Please enter a valid player name.


# SELL TO MARKET/CHANGE STATUS TO FOR SALE AND SET VALUE
Function - On the sell page, you will see all of your cards. There are then two options. You can sell your card for the market price, or you can making it available for sale at a price of your choosing.
Usage - On the sell page, there are two buttons. The one on the left is a sell button. If a user enters a valid player name and year of a card they own, that will sell the card back to the market and increase their cash by the market value. The right button is a little more complicated. When a user enters a valid player name and year of a card they own as well as a value, the card will then be listed as for sale when other people view the page so that they can buy it, and the price will be whatever you set the value to. Note that you cannot change the market value, however.
[If you are not familiar with playing cards, you may be wondering why anybody would be willing to buy a marked-up card. However, scarcity drives value. While there will initially be lots of great cards available, eventually, they would all be owned, and then people could set higher prices. See this link if you're curious about the market for rare playing cards. https://sidelinesources.com/culture-news/new-record-honus-wagner-t206-card-sells-for-6-6-million/. Yup, we just linked Andrew's own article.]
Testing - 
enter invalid player name or year for Sell button --> Sorry. You do not own this card.
enter valid player name and year for Sell button --> Redirected to your cards, without that one included, and with new cash.
enter invalid player name or year for Place for Sale button --> Sorry. You do not own this card.
enter  valid player name and year but no value for Place for Sale button --> Sorry. Must provide value.
enter valid player name, year, and value for Place for Sale button --> redirect to your collection page, but that card's price will be updated

# VIEW COLLECTION AND CASH 
Function - Allows users to see how many cards they own, how much money they have left, and view the cards they own.
Usage - When you click on the "Collection" button in the navigation bar or after purchasing a new card or selling a card, you should be able to view all of the cards that you have bought.
Testing - 
Click "Collection" button --> all cards that you own should appear, organized by batters and pitchers, as well as an accurate value of cash stores

# LOGOUT
Function - Logs users out of account.
Usage - When the user clicks on the logout button in the top right of the navigation bar, their session should end.
Testing - 
click log out button --> should be unable to accesss the functions that require log ins
