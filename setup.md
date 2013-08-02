# Setup process
1. heroku login
1. virtualenv venv --distribute
1. pip install Flask gunicorn
1. source venv/bin/active
1. gem install sass



# Notes
Traditional grid systems will likely be inappropriate for the layout invisioned.  Grid systems are typically responsive-width based on screen size and their height is typically determined by the content.

What we'd like is a grid system where both the row heigh and column width are determined solely by screen size.  We will need to do some research to find a good candidate framework to use.

Would this be terribly difficult to do with javascript?  On resize/orientation change, calculate the block size as total height - topbar - topmargin * 1/2 - gutter -bottommargin and total width - side margins - gutter.  Optionally use media queries to not CONSTANTLY resize?

Until we figure this out, maybe just to a grid with 4 big, block style buttons in the grid.  Not as neat, but hey...
