# from _typeshed import NoneType
from flask import Flask,redirect,url_for,render_template,request
from flask.helpers import flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import *
# from werkzeug.utils import secure_filename
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from flask_uploads import configure_uploads, IMAGES, UploadSet
from PIL import Image
import os
from flask_migrate import Migrate
import urllib.request, urllib.parse
import urllib
import secrets
import os
import psycopg2

app=Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# UPLOAD_FOLDER = 'static/img/uploads'
# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['SECRET_KEY'] = 'll91628bb0b13ce0c676d32e2vsba245'
app.config['UPLOADED_IMAGES_DEST'] = 'static/uploads/images'
# app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///test.db'
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://xxmrmthiiqypir:ae1d1b9e0b95be54c56da2db6f4477dcaadd6b9b057f64062865165d49e0190f@ec2-54-90-211-192.compute-1.amazonaws.com:5432/dc26jivb9kblu3'
# postgres://xxmrmthiiqypir:ae1d1b9e0b95be54c56da2db6f4477dcaadd6b9b057f64062865165d49e0190f@ec2-54-90-211-192.compute-1.amazonaws.com:5432/dc26jivb9kblu3

# app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://brseclrcjduofa:67eeffeaac88d1f6427e5857d31ff197571bd041dc71c54c2896e56fd5a8f74a@ec2-54-227-246-76.compute-1.amazonaws.com:5432/d74p8vghnkk2d7'

# Takes the name of the file and the extensions
images = UploadSet('images', IMAGES)
configure_uploads(app, images)

class Posts(db.Model):
    tablename = ['Posts']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.Column(db.String)
    image_file = db.Column(db.String(200), default='default.png')
    
    def __repr__(self):
        return f"Posts('{self.id}', '{self.title}')"

class Candidates(db.Model):
    tablename = ['Posts']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    age = db.Column(db.String)
    votes = db.Column(db.Integer, default = 0)
    image_file = db.Column(db.String(200), default='default.png')
    
    def __repr__(self):
        return f"Candidates('{self.id}', '{self.name}')"



class Issue(db.Model):
    tablename = ['Posts']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.Column(db.String)
    
    def __repr__(self):
        return f"Issue('{self.id}', '{self.title}')"

class Feedback(db.Model):
    tablename = ['Posts']

    id = db.Column(db.Integer, primary_key=True)
    feedback = db.Column(db.String, nullable=False)
    phone = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Feedback('{self.id}', '{self.title}')"


# functions
# 1856913067:AAF6ZpmhgQ8BcTZASwlyaeELB0V5CaXVZZs

def sendtelegram(params):
    url = "https://api.telegram.org/bot1856913067:AAF6ZpmhgQ8BcTZASwlyaeELB0V5CaXVZZs/sendMessage?chat_id=-594997151&text=" + urllib.parse.quote(params)
    content = urllib.request.urlopen(url).read()
    print(content)
    return content

@app.route('/',methods=['GET','POST'])
def home():
    candidates = Candidates.query.all()
    return render_template('faceofcu.html', candidates=candidates)
# Default Config
# @app.route('/',methods=['GET','POST'])
# def home():
#     limitpost = Posts.query.order_by(Posts.id.desc()).limit(3).all()
#     print("The Posts" + str(limitpost)) 
#     return render_template('index.html', limitpost=limitpost)

@app.route("/post/<int:id>")
def post(id):
    post = Posts.query.get_or_404(id)
    print(post)
    return render_template('post.html', post=post)

@app.route("/addcontestant", methods=['POST','GET'])    
def addcontestant():
    form = AddContestant()
    if form.validate_on_submit():
        newForm = Candidates(name=form.name.data, age=form.age.data, description=form.description.data, image_file=form.picture.data, votes=form.votes.data)
        db.session.add(newForm)
        db.session.commit()
        flash(f' ' + form.name.data + 'has been added successsfully', 'success')
        return redirect(url_for('adminCandidates'))
    return render_template('addcontestant.html', form=form)


@app.route("/delete/<int:post_id>")
def delete(post_id):
    post = Posts.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash(f'Your post has been deleted','danger')
    print(post)
    return redirect(url_for('adminPosts'))

@app.route("/deletecandidate/<int:candidate_id>")
def deleteCandidate(candidate_id):
    candidate = Candidates.query.get_or_404(candidate_id)
    db.session.delete(candidate)
    db.session.commit()
    flash(f'Your post has been deleted','danger')
    print(candidate)
    return redirect(url_for('adminCandidates'))


@app.route("/edit/<int:post_id>", methods=['GET','POST'])
def edit(post_id):
    form = AddPostForm()
    post = Posts.query.get_or_404(post_id)
    print(post.id)
    if request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.author.data = post.author
    elif request.method == 'POST':
        print("Post ")
        if form.validate_on_submit(): 
            post.title = form.title.data
            post.content = form.content.data
            db.session.commit()
            flash(f'Your post has been editted succesfully','success')
            return redirect(url_for('adminPosts'))
            print(post)
    return render_template('editpost.html', form=form, title=post.id, post=post)

# Candidate Edit
@app.route("/editCandidate/<int:candidate_id>", methods=['GET','POST'])
def editCandidate(candidate_id):
    form = AddContestant()
    candidate = Candidates.query.get_or_404(candidate_id)
    print(candidate_id)
    if request.method == 'GET':
        form.name.data = candidate.name
        form.description.data = candidate.description
        form.age.data = candidate.age
        form.votes.data = candidate.votes
    elif request.method == 'POST':
        print("Post ")
        if form.validate_on_submit(): 
            candidate.name = form.name.data
            candidate.description = form.description.data
            candidate.votes = form.votes.data
            db.session.commit()
            flash(f'Your post has been editted succesfully','success')
            return redirect(url_for('adminCandidates'))
    return render_template('editcandidate.html', form=form, candidate=candidate, post=post)

@app.route('/updates')
def updates(): 
    posts = Posts.query.all()
    return render_template('updates.html', posts=posts)


@app.route("/faceofcu")
def faceofcu():
    return render_template('faceOfCu.html')

@app.route("/fpreview/<int:id>")
def fpreview(id):
    candidate = Candidates.query.get_or_404(id)
    return render_template('faceofcupreview.html', candidate=candidate)


@app.route("/payment")
def payment():
    return render_template('payment.html')

@app.route("/votes")
def votes():
    return render_template('votes.html')
    
@app.route("/thanks/<int:id>/<int:amount>")
def thanks(id, amount):
    user = Candidates.query.get_or_404(id)
    print(user.votes)
    user.votes = user.votes + amount
    db.session.commit()
    print("User Votes = " + str(user.votes))
    api_key = "aniXLCfDJ2S0F1joBHuM0FcmH" #Remember to put your own API Key here
    phone = "0545977791, 0544588320" #SMS recepient"s phone number
    message = str(amount) + ' votes(s) have been cast for ' + user.name
    sender_id = "PrestoSl" #11 Characters maximum
    # send_sms(api_key,phone,message,sender_id)
    amount = round(amount / 0.5)
    sendtelegram(message)
    flash(f'' + str(amount) + ' votes(s) have been cast for ' + user.name,'success')
    return redirect(url_for('home'))
    # return render_template('thankyou.html')
       
@app.route("/nothanks/<int:id>/<int:amount>")
def nothanks(id, amount):
    user = Candidates.query.get_or_404(id) 
    print(user.votes)
    print("User Votes = " + str(user.votes))
    api_key = "aniXLCfDJ2S0F1joBHuM0FcmH" #Remember to put your own API Key here
    phone = "0545977791" #SMS recepient"s phone number
    message = str(amount) + ' votes(s) was being attempted to cast for ' + user.name
    sender_id = "PrestoSl" #11 Characters maximum
    send_sms(api_key,phone,message,sender_id)
    flash(f'' + str(amount) + ' votes(s) was being attempted to cast for ' + user.name,'danger')
    return redirect(url_for('home'))
    # return render_template('thankyou.html')
    
     
def send_sms(api_key,phone,message,sender_id):
    params = {"key":api_key,"to":phone,"msg":message,"sender_id":sender_id}
    url = 'https://apps.mnotify.net/smsapi?'+ urllib.parse.urlencode(params)
    content = urllib.request.urlopen(url).read()
    print (content)
    print (url)
# @app.route('/msgtry', methods=['POST','GET'])
def next():
    api_key = "aniXLCfDJ2S0F1joBHuM0FcmH" #Remember to put your own API Key here
    phone = "0545977791" #SMS recepient"s phone number
    message = "Your payment was successful?"
    sender_id = "PrestoSl" #11 Characters maximum
    send_sms(api_key,phone,message,sender_id)
    return render_template('menu.html')


@app.route('/admin')
def admin():    
    return render_template('admin.html')


@app.route("/profile/<int:id>")
def profile(id):
    return render_template('profile.html')

@app.route("/update/<int:id>")
def update(id):
    return render_template('update.html')

@app.route("/feedback",methods=['GET','POST'])
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        print("Done")
        newFeedback = Feedback(phone=form.phone.data, feedback=form.feedback.data)
        db.session.add(newFeedback)
        db.session.commit()
        flash(f'Your feedback has been submitted successfully','success')
        return redirect(url_for('home'))
    return render_template('feedback.html', form=form)

@app.route("/admin/posts")
def adminPosts():
    posts = Posts.query.all()
    return render_template('posts.html', posts=posts)

@app.route("/admin/candidates")
def adminCandidates():
    candidates = Candidates.query.all()
    return render_template('candidates.html', candidates=candidates)


@app.route("/admin/votes")
def adminvotes():
    candidates = Candidates.query.all()
    return render_template('adminvotes.html', candidates=candidates)


@app.route("/public/votes")
def publicvotes():
    candidates = Candidates.query.all()
    return render_template('publicvotes.html', candidates=candidates)


@app.route("/addpost", methods=['GET','POST'])
def addpost():
    form = AddPostForm()
    if form.validate_on_submit():
        # print(form.picture.data)
        if form.picture.data:
            filename = images.save(form.picture.data)
        else:
            filename = 'IneruuTrade.png'
        print(filename)
        newPost = Posts(title=form.title.data, content=form.content.data, author=form.author.data, image_file = filename)
        db.session.add(newPost)
        db.session.commit()
        print("Form has been submitted successfully")
        flash(f'Your post has been uploaded successfully', 'success')

        return redirect(url_for('admin'))
    return render_template('addpost.html', form=form)


@app.route("/raiseissue", methods=['GET','POST'])
def raiseissue():
    form = RaiseIssue()
    if form.validate_on_submit():
        newIssue = Issue(title=form.title.data, content=form.content.data, author=form.author.data, image_file=form.picture.data)
        db.session.add(newIssue)
        db.session.commit()
        print("Form has been submitted successfully")
        flash(f'Your post has been uploaded successfully', 'success')

        return redirect(url_for('admin'))
    return render_template('addpost.html', form=form)

@app.route("/team")
def team():
    return render_template('team.html')
if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000,debug=True)