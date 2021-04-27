
* To distribute
  * degit into new repo (in new a/c in GH)
    * Remove unwanted files (e.g. this one)
  * Try checking out on other laptop and running (tests and app)  
  * Removed unwanted files (e.g. this TODO)    
  * Add to new GH account (so public)
  * Check readme looks ok on github
  * Check live demo ok but then reset counter

Scripts
git push heroku master
heroku open

rm -r instance
flask db init
flask db migrate -m "initial"
flask db upgrade


remember to keep reverting to SQLAlchemy==1.3.23

#input = [4, 7, 13, 16]
#input = [10e8 + 4, 10e8 + 7, 10e8 + 13, 10e8 + 16]
input = [10000000004.0, 10000000007.0, 10000000013.0, 10000000016.0]
