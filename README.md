# WordAssoc

This is the beginnings of a simple web app game that will be used in a recruiting effort for collegel level software engineers.

The core of the game will be a word association game.  Small, instantly recognizable phrases will appear, along with several technology choices that might be associated with the phrase.  It's the user's job to select the technology most strongly associated with that phrase. This process continues for a fixed length time period, after which the user will receive a score based on the number of right and wrong answers.  The user at the end of the day with the highest score wins.

# Technologies
### TBD

# Setup
### TBD

# Interactivity
### TBD

# Dynamism
### TBD

# Responsiveness
### TBD

# A touch of data science
### TBD


# Running locally
1. source venv/bin/activate
1. python wordassoc.py OR foreman start
1. sass --watch static/css/game.css.scss:static/css/game.css
1. Navigate to localhost:5000

# Setting up herokupostgres
1. heroku addons:add heroku-postresql:dev
1. heroku pg:promote `heroku_postgresql_color_url`  _Note: replace this with whatever "color" url they give you_

That's it!  Getting Flask-SQLAlchemy set up was a much bigger pain.  For some reason foreman still doesn't like it :(
