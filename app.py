from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)


# tables 

class influencer(db.Model):
    name = db.Column(db.String(50), primary_key=True)
    passwd = db.Column(db.String(50))
    flag = db.Column(db.Boolean, default=False)
    category = db.Column(db.String(50))
    niche = db.Column(db.String(50))
    reach = db.Column(db.Integer)

class admin(db.Model):
    name = db.Column(db.String(50), primary_key=True)
    passwd = db.Column(db.String(50))

class sponsor(db.Model):
    name = db.Column(db.String(50), primary_key=True)
    passwd = db.Column(db.String(50))
    industry = db.Column(db.String(50))
    flag = db.Column(db.Boolean, default=False)

class campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    desc = db.Column(db.String(50))
    startdate = db.Column(db.Date)
    enddate = db.Column(db.Date)
    visibility = db.Column(db.Boolean)
    flag = db.Column(db.Boolean,default=False)
    goals = db.Column(db.String(50))
    sponsor_name = db.Column(db.String(50), db.ForeignKey('sponsor.name'), nullable = False)

class adreqs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    desc = db.Column(db.String(50))
    campaign_id = db.Column(db.Integer)
    influencer_name = db.Column(db.String(50))
    amount = db.Column(db.Integer)
    requirements = db.Column(db.String(50))
    status = db.Column(db.String(50))
    


with app.app_context():
    db.create_all()

#add admin

# controllers
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_to():
    username = request.form.get('username')
    password = request.form.get('upassword')
    category = request.form.get('role')
    if category == 'Influencer':
        user = influencer.query.filter_by(name=username, passwd=password).first()
        if user:
            return redirect("/influencer")
    elif category == 'Sponsor':
        user = sponsor.query.filter_by(name=username, passwd=password).first()
        if user:
            return redirect("/sponsor")
    elif category == 'Admin':
        user = admin.query.filter_by(name=username, passwd=password).first()
        if user:
            return redirect("/admin")
    
    return render_template('error_login.html')

    



@app.route('/iregister')
def iregister():
    return render_template('iregister.html')
    
@app.route('/iregister',methods=['POST'])
def iregister_to():
    username = request.form.get('iusername')
    password = request.form.get('iupassword')
    category = request.form.get('icategory')
    niche = request.form.get('iniche')
    reach = request.form.get('ireach')
    user = influencer(name=username,passwd=password,category=category,niche=niche,reach=reach)
    db.session.add(user)
    db.session.commit()
    return redirect('/login')




@app.route('/sregister')
def sregister():
    username=request.form.get('susername')
    password=request.form.get('spassword')
    industry=request.form.get('sindustry')
    user = sponsor(name=username,passwd=password,industry=industry)
    db.session.add(user)
    db.session.commit()
    return redirect('/login')


@app.route('/influencer')
def influencer_main():
    return render_template('influencer.html')

@app.route('/sponsor')
def sponsor_main():
    return render_template('sponsor.html')

@app.route('/admin')
def admin_main():
    return render_template('admin.html')



if __name__ == "__main__":
    
    app.run(debug=True)