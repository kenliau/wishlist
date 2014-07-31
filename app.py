from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import os
import admin
import MySQLdb as mdb

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = admin.secret_key


@app.route("/")
def index():
  return render_template('index.html')


@app.route("/<string:userid>/", methods=['GET', 'POST'])
def display_wishlist(userid):
  if not session.get('logged_in'):
    return redirect(url_for('login'))

  if request.method == 'POST':
    add_to_wishlist(userid, request.form)
    wishlist_array = display_user_wishlist(userid)
    return render_template('wishlist.html', wishlist_array=wishlist_array, userid=userid.capitalize())

  elif request.method == 'GET':
    wishlist_array = display_user_wishlist(userid)
    return render_template('wishlist.html', wishlist_array=wishlist_array, userid=userid.capitalize())

@app.route('/login/', methods=['GET', 'POST'])
def login():
  error = None
  if request.method == 'POST':
      if request.form['username'] != admin.username:#os.environ['username']:
          error = 'Invalid username'
      elif request.form['password'] != admin.password:#os.environ['password']:
          error = 'Invalid password'
      else:
          session['logged_in'] = True
          return redirect(url_for('display_wishlist', userid=request.form['username']))
  return render_template('login.html', error=error)


@app.route('/logout/')
def logout():
  session.pop('logged_in', None)
  return redirect(url_for('index'))


def add_to_wishlist(userid, form): 
  item = form['item']
  url = form['url'] if form['url'] else ""
  imageUrl = form['imageUrl']
  try:
    form['priority']
    priority = 1
  except:
    priority = 0

  #fix url format
  if url and (not url.startswith('http://') and not url.startswith('https://')):
    url = 'http://' + url
  ADD_WISHLIST = "INSERT INTO wishlist (userid, item, url, imageUrl, priority) VALUES ('%s', '%s', '%s', '%s', %d) ;" % (userid, item, url, imageUrl, int(priority))
  db = mdb.connect(host="localhost", user="kenliau", db="kenliau")
  cursor = db.cursor()
  print ADD_WISHLIST
  cursor.execute(ADD_WISHLIST)
  db.commit()

  cursor.close()
  db.close()


def display_user_wishlist(userid):
  # find if user exists
  FIND_USER = "SELECT * FROM wishlist WHERE userid='%s' ORDER BY priority DESC ;" % userid 
  db = mdb.connect(host="localhost", user="kenliau", db="kenliau")
  cursor = db.cursor()
  cursor.execute(FIND_USER)
  result = cursor.fetchone()

  if result == None:
    abort(404)

  # list all wishlist by this user
  wishlist_array = []
  while True:
    if not result: 
      break

    item = {}
    item['userid'] = result[1]
    item['itemName'] = result[2]
    item['url'] = result[3]
    item['imageUrl'] = result[4]
    item['priority'] = result[5]
    
    wishlist_array.append(item)

    result = cursor.fetchone()

  cursor.close()
  db.close()

  return wishlist_array


if __name__ == "__main__":
    app.run(debug=True)
