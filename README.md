# WordAssoc

This is the beginnings of a simple web app game that will be used in a recruiting effort for collegel level software engineers.

The core of the game will be a word association game.  Small, instantly recognizable phrases will appear, along with several technology choices that might be associated with the phrase.  It's the user's job to select the technology most strongly associated with that phrase. This process continues for a fixed length time period, after which the user will receive a score based on the number of right and wrong answers.  The user at the end of the day with the highest score wins.

# Technologies
The backend is written entirely in Python using the Flask web-framework with the SQLAlchemy extension for managing relational-based models.  The current setup uses SQLite for local development and switches over to Heroku Postgres for deployment.

The front end uses jQuery for DOM manipulation and AJAX calls, and the Foundation framework for CSS/Javascript components.

# Setup
##Prerequisites:
1. Python 2.7 (May work with other versions; untested)
2. virtualenv
3. setuptools
4. pip
5. Heroku toolbelt (for deploying to Heroku)

## Installation
1. Clone or download respository
2. source venv/bin/activate
3. python wordassoc.py

# Dynamism
Questions are pulled from a JSON file, mapped to an answer-generation scheme tailored to the current user (possibly adjusting for their technologic background), and are different for each game.

# Responsiveness
The site is designed to operate reasonably well on any modern device, from mobile phones up to desktops.  It is optimized, however, for medium sized touch screen devices; tablets.  Future efforts may include further optimizations on other platforms.

# A touch of data science
The primary goal of this application is to gether data about the user's background in technology.  This data may be used to help shape future interview processes with the user, to provide a high level, anonymous profile of the user in relation to their peers, and will be used to give away a sweet prize at the Virginia Tech CSRC career fair.

The game is silly and simple, but we hope the resulting data can help give both us and our users some perspective about the user base in general.


# Running locally for development
1. source venv/bin/activate
1. python wordassoc.py OR foreman start
1. sass --watch static/css/game.css.scss:static/css/game.css
1. Navigate to localhost:5000

# Setting up herokupostgres
1. heroku addons:add heroku-postresql:dev
1. heroku pg:promote `heroku_postgresql_color_url`  _Note: replace this with whatever "color" url they give you_

That's it!
