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

app=Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# UPLOAD_FOLDER = 'static/img/uploads'
# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['SECRET_KEY'] = 'll91628bb0b13ce0c676d32e2vsba245'
app.config['UPLOADED_IMAGES_DEST'] = 'static/uploads/images'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///test.db'

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


@app.route('/',methods=['GET','POST'])
def home():
    limitpost = Posts.query.order_by(Posts.id.desc()).limit(3).all()
    print("The Posts" + str(limitpost)) 
    return render_template('index.html', limitpost=limitpost)

@app.route("/post/<int:id>")
def post(id):
    post = Posts.query.get_or_404(id)
    print(post)
    return render_template('post.html', post=post)

@app.route("/delete/<int:post_id>")
def delete(post_id):
    post = Posts.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash(f'Your post has been deleted','danger')
    print(post)
    return redirect(url_for('adminPosts'))


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

@app.route('/updates')
def updates(): 
    posts = Posts.query.all()
    return render_template('updates.html', posts=posts)


@app.route("/faceofcu")
def faceofcu():
    return render_template('faceOfCu.html')
    
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