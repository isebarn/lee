# flask app

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)

# database model for a table called Clicks, has name, site, datetime
class Clicks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    site = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Clicks %r>' % self.id
    
# database model for a table called Sites, has name, url
class Sites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    url = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return '<Sites %r>' % self.id
    

# create all tables if not existing
with app.app_context():
    db.create_all()
    
# GET endpoint that accepts n (name), s(site) and saves to the Clicks table.
# Then it queries the Sites table for a site with the same name as the one passed in.
# If it exists, it redirects to the url of that site. If it doesn't exist, it redirects to the homepage.
@app.route('/click', methods=['GET'])
def click():
    name = request.args.get('n')
    site = request.args.get('s')
    click = Clicks(name=name, site=site)
    try:
        db.session.add(click)
        db.session.commit()        
    except:
        return 'There was an issue adding your click'
    
    site = Sites.query.filter_by(name=site).first()
    if site:
        # 301 to site.url
        return redirect(site.url, code=301)
    else:
        return render_template('not_found.html')


# GET endpoint that retrieves all clicks from the Clicks table, sorted by newest first and
# returns the template templates/index.html
@app.route('/', methods=['GET'])
def index():
    clicks = Clicks.query.order_by(Clicks.date_created.desc()).all()
    return render_template('index.html', clicks=clicks)

# POST endpoint that creates a new site in the Sites table
@app.route('/add_site', methods=['POST'])
def add_site():
    # get json from request
    body = request.get_json()

    site = Sites(name=body['name'], url=body['url'])
    try:
        db.session.add(site)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue adding your site'
    