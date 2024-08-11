from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SESSION_TYPE"] = "filesystem"
db = SQLAlchemy(app)
Session(app)

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
    name = db.Column(db.String(50), primary_key=True)
    desc = db.Column(db.String(200))
    startdate = db.Column(db.Date)
    enddate = db.Column(db.Date)
    visibility = db.Column(db.Boolean)
    flag = db.Column(db.Boolean,default=False)
    goals = db.Column(db.String(50))
    sponsor_name = db.Column(db.String(50), db.ForeignKey('sponsor.name'), nullable = False)

class adreqs(db.Model):
    
    name = db.Column(db.String(50),primary_key=True)
    desc = db.Column(db.String(200))
    campaign_name = db.Column(db.Integer, db.ForeignKey('campaign.name'))
    influencer_name = db.Column(db.String(50), db.ForeignKey('influencer.name'), nullable = True)
    amount = db.Column(db.Integer)
    requirements = db.Column(db.String(200))
    status = db.Column(db.String(50))
    


with app.app_context():
    db.create_all()
    if not admin.query.filter_by(name='admin').first():
        admin = admin(name='admin', passwd= 'admin')
        db.session.add(admin)
        db.session.commit()





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
    session['username']=username
    
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

    

@app.route('/Already_exists')
def already_exists():
    return render_template('already_exists.html')

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
    if influencer.query.filter_by(name=username).first():
        return redirect('/already_exists')
    else:
        user = influencer(name=username,passwd=password,category=category,niche=niche,reach=reach)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')

@app.route('/influencer')
def influencer_main():
    return render_template('influencer.html')

@app.route('/influencer/stats')
def influencer_stats():
    pass



##sponsor
@app.route('/sregister')
def sregister():
    return render_template('sregister.html')

@app.route('/sregister',methods=['POST'])
def sregister_to():
    username=request.form.get('susername')
    password=request.form.get('spassword')
    industry=request.form.get('industry')
    if sponsor.query.filter_by(name=username).first():
        return redirect('/already_exists')
    else: 
        user = sponsor(name=username,passwd=password,industry=industry)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')




@app.route('/sponsor')
def sponsor_main():
    campaigns=campaign.query.filter_by(sponsor_name=session.get('username')).all()
    adrequests = adreqs.query.all()

    


    return render_template('sponsor.html')

@app.route('/sponsor/create_campaign')
def create_campaign():
    return render_template('create_campaign.html')

@app.route('/sponsor/create_campaign', methods=['POST'])
def create_campaign_post():
    
    name = request.form.get('name')
    desc = request.form.get('desc')
    startdate = datetime.datetime(int(request.form.get('start').split('-')[0]),int(request.form.get('start').split('-')[1]),int(request.form.get('start').split('-')[2]))
    enddate = datetime.datetime(int(request.form.get('end').split('-')[0]),int(request.form.get('end').split('-')[1]),int(request.form.get('end').split('-')[2]))
    visibility = True
    goals = request.form.get('goal')
    sponsor_name = session.get('username')
    campaignn = campaign(name=name,desc=desc,startdate=startdate,enddate=enddate,visibility=visibility,goals=goals,sponsor_name=sponsor_name)
    db.session.add(campaignn)
    db.session.commit()
    return redirect('/sponsor')

@app.route('/sponsor/create_ad_request')
def create_ad_requests():
    return render_template('create_ad_requests.html')

@app.route('/sponsor/create_ad_request',methods=['POST'])
def create_ad_requests_post():
    campaign_list = campaign.query.all()
    

    name = request.form.get('name')
    desc = request.form.get('desc')
    campaign_name = request.form.get('campaigni')
    influencer_name = None
    amount = request.form.get('amount')
    requirements = request.form.get('requires')
    status = 'Pending'
    adreq = adreqs(name=name,desc=desc,campaign_name=campaign_name,influencer_name=influencer_name,amount=amount,requirements=requirements,status=status)
    db.session.add(adreq)
    db.session.commit()
    return redirect('/sponsor')
    

@app.route('/sponsor/find_influencer')
def find_inf():
    infs=influencer.query.all()

    return render_template('sponsor_find_inf.html')

@app.route('/sponsor/stats')
def sponsor_stats():
    campaign_list = campaign.query.filter_by(sponsor_name=session.get('username')).all()
    total_cams= len(campaign_list)
    return render_template('sponsor_stats.html')

@app.route('/admin')
def admin_main():
    return render_template('admin.html')

@app.route('/admin',methods=['POST'])
def flag():
    pass



if __name__ == "__main__":
    
    app.run(debug=True)