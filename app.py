# STARPS : The Social Arena (Re-Build)
# STP Development & Pruduction
# Developed By : Nageshwar Tripathi
# Contributors : Suyash Awasthi & Harsh Kain
# riskIndustries.2965

from flask import Flask, url_for, redirect, render_template, flash, session, g
from flask import request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import random
import smtplib as s
import os
import string
from time import sleep
from PIL import Image
import PIL
import os
import glob
from secret import server_mail, server_pass

# import pytz

# # get the standard UTC time  
# UTC = pytz.utc 

# # it will get the time zone  
# # of the specified location 
# IST = pytz.timezone('Asia/Kolkata') 


UPLOAD_FOLDER = 'static'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///maindata.db'
app.config['SQLALCHEMY_BINDS'] = { 'second' : 'sqlite:///newdata.db', 'third' : 'sqlite:///photodata.db', 'fourth' : 'sqlite:///privacyaccess.db', 'fifth' : 'sqlite:///storydata.db' }
app.config['SECRET_KEY'] = 'riskindus29651382'
app.permanent_session_lifetime = timedelta(days=3)

db = SQLAlchemy(app)

#--------------Database Classes (Tables)-----------------

class MasterData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

class PostCont(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    posted_by = db.Column(db.String(20), nullable=False)
    posted_on = db.Column(db.DateTime, nullable=False, default=datetime.now())
    post_content = db.Column(db.Text, nullable=False)
    post_image_id = db.Column(db.String(60), nullable=True)

    def __repr__(self):
        return '<post_by %r>' % self.posted_by

class AccountDetails(db.Model):
    detail_id = db.Column(db.Integer, primary_key=True)
    detail_username = db.Column(db.String(20), nullable=False)
    detail_fullname = db.Column(db.String(30), nullable=True)
    detail_gender = db.Column(db.String(10), nullable=True)
    detail_bio = db.Column(db.Text, nullable=True)
    detail_country = db.Column(db.String(20), nullable=True)
    detail_state = db.Column(db.String(20), nullable=True)
    detail_city = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return '<details_ %r>' % self.detail_username

class RepliesData(db.Model):
    reply_id = db.Column(db.Integer, primary_key=True)
    reply_of = db.Column(db.Integer, nullable=False)
    reply_content = db.Column(db.Text, nullable=False)
    reply_by = db.Column(db.String(20), nullable=False)
    reply_on = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return '<replieof_%r>' % self.reply_of

class MsgData(db.Model):
    msg_id = db.Column(db.Integer, primary_key=True)
    msg_from = db.Column(db.String(20), nullable=False)
    msg_to = db.Column(db.String(20), nullable=False)
    msg_content = db.Column(db.Text, nullable=False)
    msg_on = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return '<msg_from_%r>' % self.msg_from

class ReportData(db.Model):
    report_id = db.Column(db.Integer, primary_key=True)
    report_by = db.Column(db.String(20), nullable=False)
    report_of = db.Column(db.String(20), nullable=False)
    report_detail = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<report_of_%r>' % self.report_of

class BlockData(db.Model):
    block_id = db.Column(db.Integer, primary_key=True)
    block_by = db.Column(db.String(20), nullable=False)
    blocked = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<blocked_%r>' % self.blocked

class FollowerData(db.Model):
    __bind_key__ = 'second'
    followed_id = db.Column(db.Integer, primary_key=True)
    followed_by = db.Column(db.String(20), nullable=False)
    followed_to = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Follow_by_%r>' % self.followed_by

class PrivateAccount(db.Model):
    __bind_key__ = 'second'
    pa_id = db.Column(db.Integer, primary_key=True)
    pa_username = db.Column(db.String(20), nullable=False)
    pa_status = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return '<pa_of_%r>' % self.pa_username

class Notifications(db.Model):
    __bind_key__ = 'second'
    notification_id = db.Column(db.Integer, primary_key=True)
    notification_type = db.Column(db.String(20), nullable=False)
    notification_username = db.Column(db.String(20), nullable=False)
    notification_person = db.Column(db.String(20), nullable=True)
    notification_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    notification_text = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return '<notify_to_%r>' % self.notification_username

class FollowRequests(db.Model):
    __bind_key__ = 'second'
    follow_request_id = db.Column(db.Integer, primary_key=True)
    follow_request_by = db.Column(db.String(20), nullable=False)
    follow_request_to = db.Column(db.String(20), nullable=False)
    follow_request_date = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return '<follow_r_to_%r>' % self.follow_request_to

class PhotoPost(db.Model):
    __bind_key__ = 'third'
    photopost_id = db.Column(db.Integer, primary_key=True)
    photopost_username = db.Column(db.String(20), nullable=False)
    photopost_image = db.Column(db.String(255), nullable=False)
    photopost_text = db.Column(db.Text, nullable=True)
    photopost_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return '<_%r>' % self.photopost_image

class LikesPhotoPost(db.Model):
    __bind_key__ = 'third'
    likep_id = db.Column(db.Integer, primary_key=True)
    likep_post_id = db.Column(db.Integer, nullable=False)
    likep_by = db.Column(db.String(20), nullable=False)
    likep_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return '<likes_on_%r>' % self.likep_post_id

class LikesTextPost(db.Model):
    __bind_key__ = 'third'
    liket_id = db.Column(db.Integer, primary_key=True)
    liket_post_id = db.Column(db.Integer, nullable=False)
    liket_by = db.Column(db.String(20), nullable=False)
    liket_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return '<likes_on_t_%r>' % self.liket_post_id

class PhotoPostCommnets(db.Model):
    __bind_key__ = 'third'
    comment_pp_id = db.Column(db.Integer, primary_key=True)
    comment_pp_post_id = db.Column(db.Integer, nullable=False)
    comment_pp_content = db.Column(db.Text, nullable=False)
    comment_pp_username = db.Column(db.String(20), nullable=False)
    comment_pp_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return "Reply_pp_post_id %r" % self.reply_pp_post_id

class user_Access_Key(db.Model):
    __bind_key__ = 'fourth'
    user_private_id = db.Column(db.Integer, primary_key=True)
    user_private_username = db.Column(db.String(20), nullable=False)
    user_private_key = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return "Private Key %r" % self.user_private_username


class StoryData(db.Model):
    __bind_key__ = 'fifth'
    story_id = db.Column(db.Integer, primary_key=True)
    story_username = db.Column(db.String(20), nullable=False)
    story_photo = db.Column(db.String(255), nullable=False)
    story_text = db.Column(db.Text, nullable=True)
    story_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

class StoryViewers(db.Model):
    __bind_key__ = 'fifth'
    story_view_id = db.Column(db.Integer, primary_key=True)
    story_view_username = db.Column(db.String(20), nullable=False)
    story_view_photo_id = db.Column(db.Integer, nullable=False)
    story_view_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

#---------------Application Routes--------------------------------------------------------------

@app.route('/')
def index():
    return render_template('index.html')

# experimental ---------------------------------------
@app.route('/user/stories/show_story/<int:story_id>')
def show_story(story_id):
    username = session['username']
    get_story = StoryData.query.get(story_id)
    return render_template('show_story.html', story=get_story, username=username)
    sleep(10)
    return redirect(url_for('stories'))

@app.route('/user/stories/add_story', methods = ['GET', 'POST'])
def add_story():
    username = session['username']
    if request.method == 'POST':
        try:
            story_post_text = request.form['story_text']
        except:
            story_post_text = " "

        f = request.files['file']
        file_name, file_extension = os.path.splitext(f.filename)
        time_to_add = datetime.now()
        f.filename = f"story_{username}{time_to_add}" + ".jpg"
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))

        name_for_database = secure_filename(f.filename)

        #---saving to database--------------------------
        if os.path.exists(f"static/{secure_filename(f.filename)}"):
            add_story_database = StoryData(story_username=username, story_photo=name_for_database, story_text=story_post_text, story_time=datetime.now())
            db.session.add(add_story_database)
            db.session.commit()
        flash('Story Posted!')
        return redirect(url_for('stories'))
    else:
        return render_template('add_story.html')

@app.route('/user/stories')
def stories():
    username = session['username']
    all_stories = StoryData.query.order_by(StoryData.story_time).all()
    return render_template('stories.html',username=username, all_stories=all_stories)

@app.route('/user/follow_new_users')
def follow_new_users():
    username = session['username']
    all_users = AccountDetails.query.all()

    #--------------------get following and followers-------------------

    followers = []
    following = [username]

    all_followed = FollowerData.query.all()
    for follows in all_followed:
        if follows.followed_by == username:
            following.append(follows.followed_to)
        if follows.followed_to == username:
            followers.append(follows.followed_by)

    #------------get block list -------------------------
    system_data = MasterData.query.all()
    blocked_contact = BlockData.query.all()
    blocked_list = []
    for contact in blocked_contact:
        if contact.blocked == username:
            blocked_list.append(contact.block_by)
        if contact.block_by == username:
            blocked_list.append(contact.blocked)

    return render_template('follow_new_users.html', all_users=all_users, following=following, blocked_list=blocked_list)



@app.route('/user/notifications/single_photo_post/<int:photopost_id>/<int:private_key>/<int:notification_id>')
def single_photo_post(photopost_id, private_key, notification_id):
    username = session['username']
    notification_private_key = (123 + notification_id * 6730) * notification_id

    if private_key == notification_private_key:
        photopost_id = int(photopost_id)
        photopost = PhotoPost.query.filter(PhotoPost.photopost_id == photopost_id).first()

        #-------------------get photopost likes and likes number ----------------------
       
        all_post_likes = LikesPhotoPost.query.all()
        post_and_likes = {}
        number_of_likes = {}
        for likes in all_post_likes:
            photo_id = likes.likep_post_id

            if(post_and_likes.get(photo_id) == None):
                users = []
                user = likes.likep_by
                post_and_likes[photo_id] = users
                post_and_likes[photo_id].append(user)
            else:
                user = likes.likep_by
                post_and_likes[photo_id].append(user)

            if(number_of_likes.get(photo_id) == None):
                number = 0
                number_of_likes[photo_id] = number + 1
            else:
                number = number_of_likes.get(photo_id)
                number_of_likes[photo_id] = number + 1

        print(post_and_likes)
        print(number_of_likes)

        #-------------get all comments---------------------
        all_comments = PhotoPostCommnets.query.order_by(PhotoPostCommnets.comment_pp_time).all()

        return render_template('single_photo_post.html',all_comments=all_comments, username=username, photo=photopost, post_and_likes=post_and_likes, number_of_likes=number_of_likes)
    
    else:
        return redirect(url_for('user'))



@app.route('/user/notifications/single_text_post/<int:post_id>/<int:private_key>/<int:notification_id>')
def single_text_post(post_id, private_key, notification_id):
    username = session['username']
    notification_private_key = (123 + notification_id * 6730) * notification_id

    if private_key == notification_private_key:
        post_id = int(post_id)
        post = PostCont.query.filter(PostCont.post_id == post_id).first()

        #----------------get post likes and likes number ------------------------------
        all_post_likes = LikesTextPost.query.all()
        post_and_likes = {}
        number_of_likes = {}
        for likes in all_post_likes:
            post_id = likes.liket_post_id

            if(post_and_likes.get(post_id) == None):
                users = []
                user = likes.liket_by
                post_and_likes[post_id] = users
                post_and_likes[post_id].append(user)
            else:
                user = likes.liket_by
                post_and_likes[post_id].append(user)

            if(number_of_likes.get(post_id) == None):
                number = 0
                number_of_likes[post_id] = number + 1
            else:
                number = number_of_likes.get(post_id)
                number_of_likes[post_id] = number + 1

        print(post_and_likes)
        print(number_of_likes)

        #----------------get post replies -------------------------------
        all_replies = RepliesData.query.order_by(RepliesData.reply_on).all()


        return render_template('single_text_post.html',replies=all_replies, post_and_likes=post_and_likes, number_of_likes=number_of_likes, username=username, post=post)
    else:
        return redirect(url_for('user'))


@app.route('/user/show_photopost_likes_user/<int:photopost_id>')
def show_photopost_likes_user(photopost_id):
    username = session['username']

    like_user_list = []
    all_likes_data = LikesPhotoPost.query.filter(LikesPhotoPost.likep_post_id == photopost_id).all()
    for user in all_likes_data:
        like_user_list.append(user.likep_by)

    print(like_user_list)

    return render_template('show_photopost_likes_user.html', like_user_list=like_user_list)

@app.route('/user/show_post_likes_user/<int:post_id>')
def show_post_likes_user(post_id):
    username = session['username']

    like_user_list = []
    all_likes_data = LikesTextPost.query.filter(LikesTextPost.liket_post_id == post_id).all()
    for user in all_likes_data:
        like_user_list.append(user.liket_by)

    print(like_user_list)

    return render_template('show_post_likes_user.html', like_user_list=like_user_list)

@app.route('/user/view_photo_post/comment/delete/<int:comment_pp_id>')
def delete_comment(comment_pp_id):
    username = session['username']
    try:
        get_comment_data = PhotoPostCommnets.query.get(comment_pp_id)
        get_photopost_data = PhotoPost.query.get(get_comment_data.comment_pp_post_id)

        #----------------------reference-----------------------
        notification_type_ = f"Photo Post Comment {get_comment_data.comment_pp_post_id}"
        notification_username_ = get_photopost_data.photopost_username
        notification_person_ = username
        notification_text_ = f"{username} commented '{get_comment_data.comment_pp_content}' on your Photo Post."
        #----------------------reference------------------------

        comment = PhotoPostCommnets.query.get(comment_pp_id)
        db.session.delete(comment)
        db.session.commit()
        flash("Comment Deleted!")

        fetch_notification = Notifications.query.filter((Notifications.notification_type == notification_type_) & (Notifications.notification_username == notification_username_) & (Notifications.notification_person == notification_person_) & (Notifications.notification_text == notification_text_)).first()
        if fetch_notification != None:
            db.session.delete(fetch_notification)
            db.session.commit()


    except:
        pass
    return redirect(url_for('view_photo_posts'))

@app.route('/user/view_photo_posts/edit_comment/<int:photopost_comment_id>', methods=['GET', 'POST'])
def edit_photopost_comment(photopost_comment_id):
    comment = PhotoPostCommnets.query.get_or_404(photopost_comment_id)
    if request.method == 'POST':
        comment.comment_pp_content = request.form['comment-content']
        db.session.commit()
        return redirect('/user/view_photo_posts')
    else:
        return render_template('edit_comment.html', comment=comment)

@app.route('/user/view_photo_post/comment/<int:photopost_id>', methods = ['GET', 'POST'])
def photopost_comment(photopost_id):
    username = session['username']
    if request.method == 'POST':
        comment_content = request.form['comment-content']
        add_comment = PhotoPostCommnets(comment_pp_post_id=photopost_id, comment_pp_content=comment_content, comment_pp_username=username, comment_pp_time=datetime.now())
        db.session.add(add_comment)
        db.session.commit()
        _ppost = PhotoPost.query.filter(PhotoPost.photopost_id==photopost_id).first()
        name_ = _ppost.photopost_username

        #------------adding notification to the user-------------
        get_post = PhotoPost.query.filter(PhotoPost.photopost_id == photopost_id).first()
        if (get_post != None):
            user_of_post = get_post.photopost_username
            if user_of_post != username:
                notification_type_ = f"Photo Post Comment {photopost_id}"
                notification_username_ = user_of_post
                notification_person_ = username
                notification_text_ = f"{username} commented '{comment_content}' on your Photo Post."

                new_notification = Notifications(notification_type=notification_type_,
                                                 notification_username=notification_username_,
                                                 notification_person=notification_person_,
                                                 notification_text=notification_text_,
                                                 notification_time=datetime.now())

                db.session.add(new_notification)
                db.session.commit()


        flash(f"Commented on {name_}'s Post")
        return redirect(url_for('view_photo_posts'))
    else:
        return redirect(url_for('view_photo_posts'))

@app.route('/user/remove_like/<int:post_id>')
def remove_like_textpost(post_id):
    username = session['username']
    try:
        like_to_remove = LikesTextPost.query.filter((LikesTextPost.liket_post_id == post_id) & (LikesTextPost.liket_by == username)).first()
        db.session.delete(like_to_remove)
        db.session.commit()

        get_post_data = PostCont.query.filter(PostCont.post_id == post_id).first()

        #-----------------reference -----------------------------
        notification_type_ = f"Text Post Like {post_id}"
        notification_username_ = get_post_data.posted_by
        notification_person_ = username
        notification_text_ = f"{username} Liked your Text Post."
        #-----------------reference-----------------------------

        fetch_notification = Notifications.query.filter((Notifications.notification_type == notification_type_) & (Notifications.notification_username == notification_username_) & (Notifications.notification_person == notification_person_) & (Notifications.notification_text == notification_text_)).first()
        if fetch_notification != None:
            db.session.delete(fetch_notification)
            db.session.commit()

    except Exception as e:
        print(e)
        pass

    return redirect(url_for('user'))

@app.route('/user/like/<int:post_id>')
def like_text_post(post_id):
    username = session['username']
    #------------adding like ----------------
    add_new_like = LikesTextPost(liket_post_id=post_id, liket_by=username, liket_time=datetime.now())
    db.session.add(add_new_like)
    db.session.commit()

    #------------adding notification to the user-------------
    get_post = PostCont.query.filter(PostCont.post_id == post_id).first()
    if (get_post != None):
        user_of_post = get_post.posted_by
        if user_of_post != username:
            notification_type_ = f"Text Post Like {post_id}"
            notification_username_ = user_of_post
            notification_person_ = username
            notification_text_ = f"{username} Liked your Text Post."

            new_notification = Notifications(notification_type=notification_type_,
                                             notification_username=notification_username_,
                                             notification_person=notification_person_,
                                             notification_text=notification_text_,
                                             notification_time=datetime.now())

            db.session.add(new_notification)
            db.session.commit()

    return redirect(url_for('user'))


@app.route('/user/view_photo_posts')
def view_photo_posts():
    username = session['username']

    all_photo_posts = PhotoPost.query.order_by(PhotoPost.photopost_time.desc()).all()
    all_post_likes = LikesPhotoPost.query.all()
    post_and_likes = {}
    number_of_likes = {}
    for likes in all_post_likes:
        photo_id = likes.likep_post_id

        if(post_and_likes.get(photo_id) == None):
            users = []
            user = likes.likep_by
            post_and_likes[photo_id] = users
            post_and_likes[photo_id].append(user)
        else:
            user = likes.likep_by
            post_and_likes[photo_id].append(user)

        if(number_of_likes.get(photo_id) == None):
            number = 0
            number_of_likes[photo_id] = number + 1
        else:
            number = number_of_likes.get(photo_id)
            number_of_likes[photo_id] = number + 1

    print(post_and_likes)
    print(number_of_likes)

    #---get notification data to show on navbar-------------
    no_of_notifications = 0
    all_notifications = Notifications.query.all()
    for notification in all_notifications:
        if notification.notification_username == username:
            no_of_notifications += 1

    system_data = MasterData.query.all()
    blocked_contact = BlockData.query.all()
    blocked_list = []
    for contact in blocked_contact:
        if contact.blocked == username:
            blocked_list.append(contact.block_by)
        if contact.block_by == username:
            blocked_list.append(contact.blocked)

    #-------------get all comments---------------------
    all_comments = PhotoPostCommnets.query.order_by(PhotoPostCommnets.comment_pp_time).all()

    #-------------------get block list------------------
    system_data = MasterData.query.all()
    blocked_contact = BlockData.query.all()
    blocked_list = []
    for contact in blocked_contact:
        if contact.blocked == username:
            blocked_list.append(contact.block_by)
        if contact.block_by == username:
            blocked_list.append(contact.blocked)

    #--------------------get following and followers-------------------

    followers = []
    following = [username]

    all_followed = FollowerData.query.all()
    for follows in all_followed:
        if follows.followed_by == username:
            following.append(follows.followed_to)
        if follows.followed_to == username:
            followers.append(follows.followed_by)

    return render_template('view_photo_posts.html',following=following, blocked_list=blocked_list, all_comments=all_comments, no_of_notifications=no_of_notifications, number_of_likes=number_of_likes, post_and_likes=post_and_likes, likes_data=LikesPhotoPost, all_post_likes=all_post_likes, all_photo_posts=all_photo_posts, username=username)

@app.route('/user/view_photo_post/remove_like/<int:photopost_id>')
def remove_like_photopost(photopost_id):
    username = session['username']
    try:
        like_to_remove = LikesPhotoPost.query.filter((LikesPhotoPost.likep_post_id == photopost_id) & (LikesPhotoPost.likep_by == username)).first()
        db.session.delete(like_to_remove)
        db.session.commit()

        get_photopost_data = PhotoPost.query.filter(PhotoPost.photopost_id == photopost_id).first()

        #----------------------refrence-----------------------------------
        notification_type_ = f"Photo Post Like {photopost_id}"
        notification_username_ = get_photopost_data.photopost_username
        notification_person_ = username
        notification_text_ = f"{username} Liked your Photo Post."
        #----------------------refrence-----------------------------------

        fetch_notification = Notifications.query.filter((Notifications.notification_type == notification_type_) & (Notifications.notification_username == notification_username_) & (Notifications.notification_person == notification_person_) & (Notifications.notification_text == notification_text_)).first()
        if fetch_notification != None:
            db.session.delete(fetch_notification)
            db.session.commit()


    except Exception as e:
        print(e)
        pass

    return redirect(url_for('view_photo_posts'))



@app.route('/user/view_photo_post/like/<int:photopost_id>')
def like_photopost(photopost_id):
    username = session['username']
    add_new_like = LikesPhotoPost(likep_post_id=photopost_id, likep_by=username, likep_time=datetime.now())
    db.session.add(add_new_like)
    db.session.commit()

    #------------adding notification to the user-------------
    get_post = PhotoPost.query.filter(PhotoPost.photopost_id == photopost_id).first()
    if (get_post != None):
        user_of_post = get_post.photopost_username
        if user_of_post != username:
            notification_type_ = f"Photo Post Like {photopost_id}"
            notification_username_ = user_of_post
            notification_person_ = username
            notification_text_ = f"{username} Liked your Photo Post."

            new_notification = Notifications(notification_type=notification_type_,
                                             notification_username=notification_username_,
                                             notification_person=notification_person_,
                                             notification_text=notification_text_,
                                             notification_time=datetime.now())

            db.session.add(new_notification)
            db.session.commit()


    return redirect(url_for('view_photo_posts'))


@app.route('/user/view_photo_post/edit/<int:photopost_id>', methods = ['GET', 'POST'])
def edit_photopost(photopost_id):
    photopost_to_edit = PhotoPost.query.get(photopost_id)
    if request.method == 'POST':
        text_to_edit = request.form['text-to-edit']
        photopost_to_edit.photopost_text = text_to_edit
        db.session.commit()
        return redirect(url_for('view_photo_posts'))

    else:
        text = photopost_to_edit.photopost_text
        return render_template('edit_photopost.html', text=text, photopost_id=photopost_id)


@app.route('/user/view_photo_post/delete/<int:photopost_id>')
def delete_photopost(photopost_id):

    # deleting likes ------------------
    all_likes = LikesPhotoPost.query.all()
    for like in all_likes:
        if like.likep_post_id == photopost_id:
            like_remove = LikesPhotoPost.query.filter(LikesPhotoPost.likep_post_id == photopost_id).first()
            db.session.delete(like_remove)
            db.session.commit()

    photopost_to_delete = PhotoPost.query.get(photopost_id)

    #------------deleting from hosting
    filename_remove = PhotoPost.query.get(photopost_id).photopost_image
    if os.path.exists(f"static/{filename_remove}"):
        os.remove(f"static/{filename_remove}")
    else:
         print("The file does not exist")

    #-------------deleting from database

    db.session.delete(photopost_to_delete)
    db.session.commit()



    return redirect(url_for('view_photo_posts'))

@app.route('/user/post_photo', methods = ['GET', 'POST'])
def post_photo():
    username = session['username']
    time_to_upload = datetime.now()
    if request.method == 'POST':
        try:
            photo_post_text = request.form['photo_text']
        except:
            photo_post_text = " "

        f = request.files['file']
        file_name, file_extension = os.path.splitext(f.filename)
        f.filename = f"{username}{time_to_upload}" + ".jpg"
        print("___________________")
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))

        name_for_database = secure_filename(f.filename)

        try:
            # compressing image ------------------------
            file_name = f"static/{secure_filename(f.filename)}"

            im = Image.open(file_name)
            rgb_im = im.convert('RGB')
            rgb_im.save(file_name)


            picture = Image.open(file_name)
            dim = picture.size
            print(f"This is the current width and height of the image: {dim}")
            picture.save(file_name,optimize=True,quality=20)

            #---saving to database--------------------------
            if os.path.exists(f"static/{secure_filename(f.filename)}"):
                photo_to_post = PhotoPost(photopost_image=name_for_database, photopost_username=username, photopost_time=datetime.now(), photopost_text=photo_post_text)
                db.session.add(photo_to_post)
                db.session.commit()

            flash("Photo Posted!")
            return redirect(url_for('view_photo_posts'))
        except:
            filename_remove = secure_filename(f.filename)
            if os.path.exists(f"static/{filename_remove}"):
                os.remove(f"static/{filename_remove}")
            else:
                print("The file does not exist")

            flash("Unsupported Image")
            return redirect(url_for('post_photo'))
    else:
        return render_template("post_photo.html")

# experimental ends ---------------------------------------


@app.route('/user/notifications/delete/<int:notification_id>')
def delete_notification(notification_id):
    notification_to_delete = Notifications.query.get(notification_id)
    db.session.delete(notification_to_delete)
    db.session.commit()
    return redirect(url_for('notifications'))

@app.route('/user/notifications')
def notifications():
    username = session['username']
    all_notifications = Notifications.query.order_by(Notifications.notification_time.desc()).all()
    notification_no = 0
    for notification in all_notifications:
        if notification.notification_username == username:
            notification_no += 1

    return render_template('notifications.html',notification_no=notification_no, all_notifications=all_notifications, username=username)

@app.route('/user/account/eliminateFollower/<string:userToEliminate>')
def eliminate_user(userToEliminate):
    try:
        username = session['username']
        user_to_eliminate = FollowerData.query.filter((FollowerData.followed_by == userToEliminate) & (FollowerData.followed_to == username)).first()
        db.session.delete(user_to_eliminate)
        db.session.commit()

    except:
        pass

    all_followers = FollowerData.query.all()
    return render_template('show_followers.html', all_followers=all_followers, username=username, user=username)

@app.route('/user/account/follow_requests/decline/<string:userToDecline>')
def decline_request(userToDecline):
    username = session['username']

    try:
        already_sent_request = FollowRequests.query.filter((FollowRequests.follow_request_by==userToDecline) & (FollowRequests.follow_request_to==username)).first()
        db.session.delete(already_sent_request)
        db.session.commit()
    except:
        pass

    return redirect(url_for('follow_requests'))

@app.route('/user/account/follow_requests/accept/<string:userToAccept>')
def accept_request(userToAccept):
    username = session['username']

    get_follow_data = FollowerData.query.filter((FollowerData.followed_by == userToAccept ) & (FollowerData.followed_to == username)).first()
    if(get_follow_data == None or get_follow_data == ""):
        new_follow = FollowerData(followed_by=userToAccept, followed_to=username)
        db.session.add(new_follow)
        db.session.commit()

        # Adding Follow to notification ---------------------

        notification_type_ = "New Follow"
        notification_username_ = username
        notification_person_ = userToAccept
        notification_text_ = f"{userToAccept} starts Following you."

        new_notification = Notifications(notification_type=notification_type_, notification_username=notification_username_, notification_person=notification_person_, notification_text=notification_text_, notification_time=datetime.now())
        db.session.add(new_notification)
        db.session.commit()

        # Adding acceptance to notification ---------------------

        notification_type_ = "Follow Request Accepted"
        notification_username_ = userToAccept
        notification_person_ = username
        notification_text_ = f"{username} Accepted your Follow Request."

        new_notification = Notifications(notification_type=notification_type_, notification_username=notification_username_, notification_person=notification_person_, notification_text=notification_text_, notification_time=datetime.now())
        db.session.add(new_notification)
        db.session.commit()

    try:
        already_sent_request = FollowRequests.query.filter((FollowRequests.follow_request_by==userToAccept) & (FollowRequests.follow_request_to==username)).first()
        db.session.delete(already_sent_request)
        db.session.commit()
    except:
        pass

    return redirect(url_for('follow_requests'))


@app.route('/user/account/follow_requests')
def follow_requests():
    username = session['username']
    all_follow_requests = []
    requests_no = 0
    requests_data = FollowRequests.query.order_by(FollowRequests.follow_request_date.desc()).all()
    for request in requests_data:
        if(request.follow_request_to == username):
            requests_no += 1
            all_follow_requests.append(request.follow_request_by)

    return render_template('follow_requests.html', username=username, requests_no=requests_no, all_follow_requests=all_follow_requests)

@app.route('/user/account/settings/account_privacy/lock')
def lock_account():
    username = session['username']
    account_find = PrivateAccount.query.filter(PrivateAccount.pa_username==username).first()
    account_id = account_find.pa_id

    private_account = PrivateAccount.query.get_or_404(account_id)

    private_account.pa_status = 1
    db.session.commit()
    return redirect(url_for('account_privacy'))

@app.route('/user/account/settings/account_privacy/unlock')
def unlock_account():
    username = session['username']
    account_find = PrivateAccount.query.filter(PrivateAccount.pa_username==username).first()
    account_id = account_find.pa_id

    private_account = PrivateAccount.query.get_or_404(account_id)

    private_account.pa_status = 0
    db.session.commit()

    # accepting all pending follow requests ---------------------

    received_requests = FollowRequests.query.filter(FollowRequests.follow_request_to == username).all()
    for request in received_requests:
        userToAccept = request.follow_request_by
        get_follow_data = FollowerData.query.filter((FollowerData.followed_by == userToAccept ) & (FollowerData.followed_to == username)).first()
        if(get_follow_data == None or get_follow_data == ""):
            new_follow = FollowerData(followed_by=userToAccept, followed_to=username)
            db.session.add(new_follow)
            db.session.commit()
        try:
            already_sent_request = FollowRequests.query.filter((FollowRequests.follow_request_by==userToAccept) & (FollowRequests.follow_request_to==username)).first()
            db.session.delete(already_sent_request)
            db.session.commit()
        except:
            pass

    return redirect(url_for('account_privacy'))

@app.route('/user/account/settings/account_privacy')
def account_privacy():
    username = session['username']
    try:
        pa_user = PrivateAccount.query.filter(PrivateAccount.pa_username == username).first()
        private_status = pa_user.pa_status
    except:
        test_occurence = PrivateAccount.query.filter(PrivateAccount.pa_username == username).first()
        if(test_occurence == None or test_occurence == ""):
            add_private_account = PrivateAccount(pa_username=username)
            db.session.add(add_private_account)
            db.session.commit()

            pa_user = PrivateAccount.query.filter(PrivateAccount.pa_username == username).first()
            private_status = pa_user.pa_status
        else:
            private_status=False

    return render_template('account_privacy.html', username=username, private_status=private_status)

@app.route('/user/account/settings')
def settings():
    username = session['username']
    return render_template('settings.html', username=username)

@app.route('/user/show_user/following/<string:user>/<string:private_key>')
def show_following(user, private_key):
    username = session['username']
    user_private = user_Access_Key.query.filter(user_Access_Key.user_private_username==user).first()
    user_private_key = user_private.user_private_key
    print("PRIVATE KEY : ",user_private_key)

    #---------checking for private key -----------------
    if user_private_key == private_key:
        all_followers = FollowerData.query.all()
        return render_template('show_followings.html', all_followers=all_followers, username=username, user=user)
    else:
        return redirect(url_for('user'))

@app.route('/user/show_user/followers/<string:user>/<string:private_key>')
def show_followers(user, private_key):
    username = session['username']
    user_private = user_Access_Key.query.filter(user_Access_Key.user_private_username==user).first()
    user_private_key = user_private.user_private_key
    print("PRIVATE KEY : ",user_private_key)

    #---------checking for private key -----------------
    if user_private_key == private_key:
        all_followers = FollowerData.query.all()
        return render_template('show_followers.html', all_followers=all_followers, username=username, user=user)
    else:
        return redirect(url_for('user'))

@app.route('/user/show_user/unfollow/<string:userToUnfollow>')
def unfollow_user(userToUnfollow):
    username = session['username']
    try:
        print("------------------")
        do_unfollow = FollowerData.query.filter((FollowerData.followed_by == username) & (FollowerData.followed_to == userToUnfollow)).first()
        db.session.delete(do_unfollow)
        db.session.commit()
        print("-------------------dfd-")
        #----------------reference -------------------------
        notification_type_ = "New Follow"
        notification_username_ = userToUnfollow
        notification_person_ = username
        notification_text_ = f"{username} starts Following you."
        #----------------reference -------------------------
        print("-----------XXXX")
        fetch_notification = Notifications.query.filter((Notifications.notification_type == notification_type_) & (Notifications.notification_person == notification_person_) & (Notifications.notification_username == notification_username_) & (Notifications.notification_text == notification_text_)).first()
        print(fetch_notification)
        if fetch_notification != None:
            print("Done")
            db.session.delete(fetch_notification)
            db.session.commit()

    except Exception as e:
        print(e)
        pass
    return redirect(url_for('show_user', username_=userToUnfollow))

@app.route('/user/show_user/cancle/<string:userToCancle>')
def cancle_follow_request(userToCancle):
    username = session['username']

    try:
        already_sent_request = FollowRequests.query.filter((FollowRequests.follow_request_by==username) & (FollowRequests.follow_request_to==userToCancle)).first()
        db.session.delete(already_sent_request)
        db.session.commit()

        #--------------------reference ------------------------------
        notification_type_ = "Follow Request"
        notification_username_ = userToCancle
        notification_person_ = username
        notification_text_ = f"{username} sents you Follow Request."
        #--------------------reference ------------------------------
        fetch_notification = Notifications.query.filter((Notifications.notification_type == notification_type_) & (Notifications.notification_person == notification_person_) & (Notifications.notification_username == notification_username_) & (Notifications.notification_text == notification_text_)).first()
        print(fetch_notification)
        if fetch_notification != None:
            print("Done")
            db.session.delete(fetch_notification)
            db.session.commit()


    except Exception as e:
        print(e)
        pass

    return redirect(url_for('show_user', username_=userToCancle))


@app.route('/user/show_user/follow/<string:userToFollow>')
def follow_user(userToFollow):
    username = session['username']

    checking_private_user = PrivateAccount.query.filter(PrivateAccount.pa_username == userToFollow).first()
    if(checking_private_user != None and checking_private_user != ""):
        user_privacy_status = checking_private_user.pa_status
    else:
        add_user_privacy = PrivateAccount(pa_username=userToFollow)
        db.session.add(add_user_privacy)
        db.session.commit()

        checking_private_user = PrivateAccount.query.filter(PrivateAccount.pa_username == userToFollow).first()
        user_privacy_status = checking_private_user.pa_status

    if(user_privacy_status):
        get_follow_data = FollowerData.query.filter((FollowerData.followed_by == username) & (FollowerData.followed_to == userToFollow)).first()
        if(get_follow_data == None or get_follow_data == ""):
            new_follow_request = FollowRequests(follow_request_by=username, follow_request_to=userToFollow, follow_request_date=datetime.now())
            db.session.add(new_follow_request)
            db.session.commit()

            notification_type_ = "Follow Request"
            notification_username_ = userToFollow
            notification_person_ = username
            notification_text_ = f"{username} sents you Follow Request."

            new_notification = Notifications(notification_type=notification_type_, notification_username=notification_username_, notification_person=notification_person_, notification_text=notification_text_, notification_time=datetime.now())
            db.session.add(new_notification)
            db.session.commit()

    else:
        print("Username : ", username)
        print("User to follow", userToFollow)
        get_follow_data = FollowerData.query.filter((FollowerData.followed_by == username) & (FollowerData.followed_to == userToFollow)).first()
        # print(get_follow_data.followed_by, get_follow_data.followed_to)
        if(get_follow_data == None or get_follow_data == ""):
            new_follow = FollowerData(followed_by=username, followed_to=userToFollow)
            db.session.add(new_follow)
            db.session.commit()

            # Adding Follow to notification ---------------------

            notification_type_ = "New Follow"
            notification_username_ = userToFollow
            notification_person_ = username
            notification_text_ = f"{username} starts Following you."

            new_notification = Notifications(notification_type=notification_type_, notification_username=notification_username_, notification_person=notification_person_, notification_text=notification_text_, notification_time=datetime.now())
            db.session.add(new_notification)
            db.session.commit()
        else:
            print("XXXXXXXXXXXXXX")

    return redirect(url_for('show_user', username_=userToFollow))

@app.route('/user/account/block_list/unblock/<string:user>')
def unblock(user):
    username = session['username']
    try:
        all_blocked = BlockData.query.all()
        for name in all_blocked:
            if name.block_by == username and name.blocked == user:
                block_ = BlockData.query.filter((BlockData.block_by == username) & (BlockData.blocked == user)).first()
                db.session.delete(block_)
                db.session.commit()
    except Exception as e:
        print(e)
        pass
    return redirect(url_for('block_list'))


@app.route('/user/account/block_list')
def block_list():
    username = session['username']

    all_blocked = BlockData.query.all()

    blocked_users = []

    for user in all_blocked:
        if user.block_by == username:
            blocked_users.append(user.blocked)

    sorted_blocked = []
    for name in blocked_users:
        if name not in sorted_blocked:
            sorted_blocked.append(name)

    no_of_blocked_users = len(sorted_blocked)

    return render_template('block_list.html', username=username, blocked_users = sorted_blocked, blocked_count=no_of_blocked_users)


@app.route('/block_user/<string:user>')
def block_user(user):
    username = session['username']

    #-------------removing from following and followers----------------
    remove_user = FollowerData.query.filter((FollowerData.followed_by == username) & (FollowerData.followed_to == user)).first()
    if(remove_user != None and remove_user != ""):
        db.session.delete(remove_user)
        db.session.commit()

    remove_user = FollowerData.query.filter((FollowerData.followed_by == user) & (FollowerData.followed_to == username)).first()
    if(remove_user != None and remove_user != ""):
        db.session.delete(remove_user)
        db.session.commit()

    #---------blocking user ------------------------------
    block_user_add = BlockData(block_by=username, blocked=user)
    db.session.add(block_user_add)
    db.session.commit()

    flash(f"{user} Blocked!")
    return redirect(url_for('user'))


@app.route('/report_user_submit/<string:user>', methods = ['GET', 'POST'])
def report_user_submit(user):
    username = session['username']
    if request.method == 'POST':
        report_reason = request.form['report_reason']
        try:
            ob = s.SMTP("smtp.gmail.com",587)
            ob.starttls()
            ob.login("starps.stp@gmail.com","hikerposts")
            subject = "STARPS Report"
            body = f"""        
                    A New Report Recorded!

                    Reported By : {username}

                    Report Of : {user}

                    Report Reason : {report_reason}
            """
            message = "Subject:{}\n\n{}".format(subject,body)
            ob.sendmail("nagesh.risk@gmail.com",'stpandstp.martialstylus@gmail.com' ,message)
            print("send successfully")

            add_report_to_database = ReportData(report_by=username, report_of=user, report_detail=report_reason)
            db.session.add(add_report_to_database)
            db.session.commit()
            flash("Report Submitted !")
            return redirect(url_for('user'))
        except:
            flash("Something went Wrong!, please Try Again later")
            return redirect(url_for('user'))
    else:
         return render_template('report_user.html', username=username, user=user)


@app.route('/report_user/<string:user>', methods = ['GET', 'POST'])
def report_user(user):
    username = session['username']
    return render_template('report_user.html', username=username, user=user)



@app.route('/forgot_password/change_password/<string:forgot_username>', methods = ['GET', 'POST'])
def change_forgotten_password(forgot_username):
    if request.method == 'POST':
        try:
            get_forgot_otp = int(request.form['otp'])
        except:
            get_forgot_otp = 0000
            pass
        forgot_new_password = request.form['new-password']
        forgot_new_password2 = request.form['new-password2']
        valid_password = True
        password_invalidity = 0

        length_of_password = len(forgot_new_password)
        if(length_of_password < 6):
            password_invalidity+=1

        if(forgot_new_password != forgot_new_password2):
            valid_password = False
            flash("Password doesn't Matched! ")
            return render_template('change-forgotten-password.html')

        elif(password_invalidity!=0):
            valid_password = False
            flash("Password must be length of 6 or more!")
            return render_template('change-forgotten-password.html')

        global genrated_forgot_otp
        otp_validity = False
        if (genrated_forgot_otp == get_forgot_otp):
            otp_validity = True
        else:
            flash('Incorrect OTP, check email for a new ONE!')
            return render_template('')

        if (otp_validity == True and valid_password == True):
            updating_account_ = MasterData.query.filter(MasterData.username == forgot_username).first()
            updating_account_.password = forgot_new_password
            db.session.commit()
            return redirect('/')


    else:
        return render_template('change-forgotten-password.html')


@app.route('/forgot_password', methods = ['GET', 'POST'] )
def forgot_password():
    if request.method == 'POST':
        forgot_username = request.form['forgot-username']
        user_data = MasterData.query.all()
        user_exist = False
        for data in user_data:
            if data.username == forgot_username:
                user_exist = True

        if user_exist == False:
            flash("Username not found!")
            return render_template('forgot-password.html')

        if user_exist == True:
            all_account = MasterData.query.filter(MasterData.username == forgot_username).first()
            email_address = all_account.email
            otp_sent = False
            while otp_sent == False:
                global genrated_forgot_otp
                genrated_forgot_otp = random.randint(100000,999999)
                print(genrated_forgot_otp)
                ob = s.SMTP("smtp.gmail.com",587)
                ob.starttls()
                ob.login("starps.stp@gmail.com","hikerposts")
                subject = "Change Starps Password"
                body = f"Dear {forgot_username},\n\nYour Starps OTP for changing password is {genrated_forgot_otp}.\nDon't share this OTP with anyone.\n(if you're not requested for this, just ignore this Email)\n\n Thank you"
                message = "Subject:{}\n\n{}".format(subject,body)
                ob.sendmail("nagesh.risk@gmail.com",email_address ,message)
                print("send successfully")
                otp_sent = True
                ob.quit()

            return render_template('change-forgotten-password.html', forgot_username=forgot_username)


        return render_template('forgot-password.html')
    else:
        return render_template('forgot-password.html')



@app.route('/user/chat_room')
def chat_room():
    username = session['username']
    all_msgs = MsgData.query.order_by(MsgData.msg_on).all()
    all_users = MasterData.query.all()
    all_contacts = []
    for msg in all_msgs:
        if(msg.msg_to == username or msg.msg_from == username):
            if(msg.msg_from != username):
                all_contacts.append(msg.msg_from)
            if(msg.msg_to != username):
                all_contacts.append(msg.msg_to)
    sorted_contacts = []
    for i in all_contacts:
        if i not in sorted_contacts:
            sorted_contacts.append(i)

    sorted_contacts = sorted_contacts[::-1]
    no_of_chats = len(sorted_contacts)

    blocked_contact = BlockData.query.all()
    blocked_list = []
    for contact in blocked_contact:
        if contact.blocked == username:
            blocked_list.append(contact.block_by)
        if contact.block_by == username:
            blocked_list.append(contact.blocked)

    return render_template('chat_room.html', username=username, all_contacts = sorted_contacts, no_of_chats=no_of_chats, blocked_list=blocked_list)


@app.route('/user/show_user/send_message/<string:msg_with>', methods = ['GET', 'POST'])
def send_user_message(msg_with):
    username = session['username']
    if request.method == 'POST':
        msg_content = request.form['message-content']
        add_msg_to_database = MsgData(msg_from=username, msg_to=msg_with, msg_content=msg_content, msg_on=datetime.now())
        db.session.add(add_msg_to_database)
        db.session.commit()

        all_msgs = MsgData.query.order_by(MsgData.msg_on).all()
        return render_template('user_messages.html', all_msgs=all_msgs, username=username, msg_with=msg_with)
    else:
        all_msgs = MsgData.query.order_by(MsgData.msg_on).all()
        return render_template('user_messages.html', all_msgs=all_msgs, username=username, msg_with=msg_with)


@app.route('/user/show_user/message/<string:msg_with>/<string:private_key>')
def show_user_message(msg_with, private_key):
    session['Chat_username'] = msg_with
    msg_with = session['Chat_username']
    username = session['username']

    user_private = user_Access_Key.query.filter(user_Access_Key.user_private_username==msg_with).first()
    user_private_key = user_private.user_private_key
    print("PRIVATE KEY : ",user_private_key)

    #---------checking for private key -----------------
    if user_private_key == private_key:
        app.jinja_env.globals['profile_pic_user_msg'] = f'{msg_with}.jpg'

        all_msgs = MsgData.query.order_by(MsgData.msg_on).all()
        return render_template('user_messages.html', all_msgs=all_msgs, username=username, msg_with=msg_with)
    else:
        return redirect(url_for('user'))


@app.route('/user/edit_reply/<int:id>', methods=['GET', 'POST'])
def edit_reply(id):
    reply = RepliesData.query.get_or_404(id)
    if request.method == 'POST':
        reply.reply_content = request.form['reply-content']
        db.session.commit()
        return redirect('/user')
    else:
        return render_template('edit_reply.html', reply=reply)


@app.route('/user/delete_reply/<int:reply_id>')
def delete_reply(reply_id):
    username = session['username']
    try:
        get_reply_data = RepliesData.query.get(reply_id)
        get_post_data = PostCont.query.get(get_reply_data.reply_of)

        #------------------reference---------------------------
        notification_type_ = f"Text Post Reply {get_post_data.post_id}"
        notification_username_ = get_post_data.posted_by
        notification_person_ = username
        notification_text_ = f"{username} replied '{get_reply_data.reply_content}' on your Text Post."
        #------------------reference---------------------------
        
        fetch_notification = Notifications.query.filter((Notifications.notification_type == notification_type_) & (Notifications.notification_person == notification_person_) & (Notifications.notification_username == notification_username_) & (Notifications.notification_text == notification_text_)).first()
        if fetch_notification != None:
            print("Done")
            db.session.delete(fetch_notification)
            db.session.commit()

        reply = RepliesData.query.get_or_404(reply_id)
        db.session.delete(reply)
        db.session.commit()
        flash("Reply Deleted!")

    except Exception as e:
        print(e)
        pass

    return redirect('/user')



@app.route('/user/reply/<int:post_id>', methods = ['GET', 'POST'])
def reply(post_id):
    username = session['username']
    if request.method == 'POST':
        reply_content = request.form['replycontent']
        add_reply = RepliesData(reply_of=post_id, reply_content=reply_content, reply_by=username, reply_on=datetime.now())
        db.session.add(add_reply)
        db.session.commit()
        _post = PostCont.query.filter(PostCont.post_id==post_id).first()
        name_ = _post.posted_by
        
        #------------adding notification to the user-------------
        get_post = PostCont.query.filter(PostCont.post_id == post_id).first()
        if (get_post != None):
            user_of_post = get_post.posted_by
            if user_of_post != username:
                notification_type_ = f"Text Post Reply {post_id}"
                notification_username_ = user_of_post
                notification_person_ = username
                notification_text_ = f"{username} replied '{reply_content}' on your Text Post."

                new_notification = Notifications(notification_type=notification_type_,
                                                 notification_username=notification_username_,
                                                 notification_person=notification_person_,
                                                 notification_text=notification_text_,
                                                 notification_time=datetime.now())

                db.session.add(new_notification)
                db.session.commit()

        flash(f"Replied {name_}")
        return redirect('/user')
    else:
        return redirect('/user')


@app.route('/user/show_user/show_user_photoposts/<string:username>/<string:private_key>')
def show_user_photoposts(username, private_key):

    current_user = session['username']
    user_private = user_Access_Key.query.filter(user_Access_Key.user_private_username==username).first()
    user_private_key = user_private.user_private_key
    print("PRIVATE KEY : ",user_private_key)

    #---------checking for private key -----------------
    if user_private_key == private_key:

        # ------------get all photoposts and likes------------
        all_photo_posts = PhotoPost.query.order_by(PhotoPost.photopost_time.desc()).all()
        all_post_likes = LikesPhotoPost.query.all()

        post_and_likes = {}
        number_of_likes = {}

        for likes in all_post_likes:
            photo_id = likes.likep_post_id

            if(post_and_likes.get(photo_id) == None):
                users = []
                user = likes.likep_by
                post_and_likes[photo_id] = users
                post_and_likes[photo_id].append(user)
            else:
                user = likes.likep_by
                post_and_likes[photo_id].append(user)

            if(number_of_likes.get(photo_id) == None):
                number = 0
                number_of_likes[photo_id] = number + 1
            else:
                number = number_of_likes.get(photo_id)
                number_of_likes[photo_id] = number + 1

        print(post_and_likes)
        print(number_of_likes)


        return render_template('show_user_photoposts.html',user_private_key=private_key, username=username, number_of_likes=number_of_likes, post_and_likes=post_and_likes, all_photo_posts=all_photo_posts)

    else:
        return redirect(url_for('user'))




@app.route('/user/show_user/show_user_posts/<string:username>/<string:private_key>')
def show_user_posts(username, private_key):
    current_user = session['username']
    user_private = user_Access_Key.query.filter(user_Access_Key.user_private_username==username).first()
    user_private_key = user_private.user_private_key
    print("PRIVATE KEY : ",user_private_key)

    #---------checking for private key -----------------
    if user_private_key == private_key:
        all_posts = PostCont.query.order_by(PostCont.posted_on.desc()).all()
        all_replies = RepliesData.query.order_by(RepliesData.reply_on).all()

        #----------------get post likes and likes number ------------------------------
        all_post_likes = LikesTextPost.query.all()
        post_and_likes = {}
        number_of_likes = {}
        for likes in all_post_likes:
            post_id = likes.liket_post_id

            if(post_and_likes.get(post_id) == None):
                users = []
                user = likes.liket_by
                post_and_likes[post_id] = users
                post_and_likes[post_id].append(user)
            else:
                user = likes.liket_by
                post_and_likes[post_id].append(user)

            if(number_of_likes.get(post_id) == None):
                number = 0
                number_of_likes[post_id] = number + 1
            else:
                number = number_of_likes.get(post_id)
                number_of_likes[post_id] = number + 1

        print(post_and_likes)
        print(number_of_likes)

        return render_template('show_user_posts.html',user_private_key=private_key, number_of_likes=number_of_likes, post_and_likes=post_and_likes, posts=all_posts, username=username, replies=all_replies, current_user=current_user)
    else:
        return redirect(url_for('user'))

@app.route('/user/account/update/profile', methods = ['GET', 'POST'])
def change_profile():
    username = session['username']
    if request.method == 'POST':
        f = request.files['file']
        file_name, file_extension = os.path.splitext(f.filename)
        f.filename = f"{username}" + ".jpg"
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        flash("Profile Picture Updated, it may take some time to show.")
        return redirect(url_for('account'))

    return render_template('change_profile.html')

@app.route('/user/search_user', methods = ['GET', 'POST'])
def search_user():
    username = session['username']
    blocked_contact = BlockData.query.all()
    blocked_list = []
    for contact in blocked_contact:
        if contact.blocked == username:
            blocked_list.append(contact.block_by)
        if contact.block_by == username:
            blocked_list.append(contact.blocked)

    if request.method == 'POST':
        user_to_search = request.form['search_user']
        user_found = False
        user_found_list = []
        if(user_to_search):
            try:
                system_data = MasterData.query.all()
                for users in system_data:
                    if user_to_search in users.username and users.username not in blocked_list:
                        user_found_list.append(users.username)
                        user_found = True
            except:
                user_found = False
        if(user_found == True):
            user_found_list = user_found_list[::-1]
            print(user_found_list)
            system_data_detail = AccountDetails.query.all()
            return render_template('user_search_list.html', user_found=user_found_list, user_to_search=user_to_search, system_data=system_data_detail)
        else:
            flash(f"{user_to_search} Not Found!")
            return redirect(url_for('user'))
    else:
        return url_for('user')


@app.route('/user/show_user/<string:username_>')
def show_user(username_):
    curr_user = session['username']

    #-----------------checking for Block List ------------------------------
    curr_user_blocked = False
    show_user_blocked = False

    all_blocks = BlockData.query.all()
    for blocks in all_blocks:
        if(blocks.block_by == username_ and blocks.blocked == curr_user):
            curr_user_blocked = True
        if(blocks.block_by == curr_user and blocks.blocked == username_):
            show_user_blocked = True

    if(curr_user_blocked == False and show_user_blocked == False):

        #---------------------checking for private key existance ------------------------
        try_to_get_key = user_Access_Key.query.filter(user_Access_Key.user_private_username==username_).first()

        if try_to_get_key == None or try_to_get_key == "":

            #adding----private---key------------------------------------------------------------------

            private_key_length = 15

            private_key_characters = string.ascii_letters + string.digits
            private_key = []
            for x in range(private_key_length):
                private_key.append(random.choice(private_key_characters))

            private_key = "".join(private_key)

            print(private_key)

            add_private_key = user_Access_Key(user_private_username=username_, user_private_key=private_key)
            db.session.add(add_private_key)
            db.session.commit()

            user_private_key =  private_key
            #-----------------------------------------------------------------------------------------


        try:
            all_info = AccountDetails.query.filter(AccountDetails.detail_username == username_).first()
            bio_ = all_info.detail_bio
            gender_ = all_info.detail_gender
            city_ = all_info.detail_city
            state_ = all_info.detail_state
            country_ = all_info.detail_country
            fullname_ = all_info.detail_fullname

            followers_no = 0
            following_no = 0
            followers = []
            following = []

            logged_follow = False

            all_followed = FollowerData.query.all()
            for follows in all_followed:
                if follows.followed_by == curr_user and follows.followed_to == username_:
                    logged_follow = True
                if follows.followed_by == username_:
                    following_no += 1
                    following.append(follows.followed_to)
                if follows.followed_to == username_:
                    followers_no += 1
                    followers.append(follows.followed_by)

            private_account = False

            get_private_data = PrivateAccount.query.filter(PrivateAccount.pa_username ==  username_).first()
            if(get_private_data != None and get_private_data != ""):
                status_ = get_private_data.pa_status
                private_account = status_

            follow_request_data = FollowRequests.query.filter((FollowRequests.follow_request_by == curr_user) & (FollowRequests.follow_request_to == username_)).first()
            if(follow_request_data != None and follow_request_data != "" and follow_request_data.follow_request_to == username_):
                pending_f_request = True
                pending_request_of = follow_request_data.follow_request_to

            else:
                pending_f_request = False
                pending_request_of = "follow_request_data.follow_request_to"

            requests_data = FollowRequests.query.all()

            #--------------------get private keys-----------------------
            user_private = user_Access_Key.query.filter(user_Access_Key.user_private_username==username_).first()
            user_private_key = user_private.user_private_key
            print("PRIVATE KEY : ",user_private_key)
            app.jinja_env.globals['profile_pic_user'] = f'{username_}.jpg'

            return render_template('show_user.html',user_private_key=user_private_key, pending_f_request=pending_f_request, requests_data=requests_data, private_account=private_account, logged_follow=logged_follow, followers=followers, following=following, followers_no=followers_no, following_no=following_no, curr_user=curr_user ,bio=bio_, gender=gender_, country=country_, state=state_, fullname=fullname_, city=city_, username_=username_)
        except Exception as e:
            print(e)
            return url_for('user')

    else:
        return redirect(url_for('page_not_available'))


@app.route('/user/account/change_password', methods = ['GET', 'POST'])
def change_password():
    username = session['username']
    if request.method == 'POST':
        old_password = request.form['oldpassword']
        new_password = request.form['newpassword']
        new_password2 = request.form['newpassword2']

        user_pass_data = MasterData.query.filter(MasterData.username == username).first()
        user_password_ = user_pass_data.password

        new_matched = True
        old_matched = True

        if(new_password != new_password2):
            new_matched = False
            flash("New Password not Matched!")

        if(old_password != user_password_):
            old_matched = False
            flash("Wrong old Password!")



        valid_password = True
        password_invalidity = 0

        length_of_password = len(new_password)
        if(length_of_password < 6):
            password_invalidity+=1

        if(password_invalidity!=0):
            valid_password = False
            flash("Password must be length of 6 or more!")
            return render_template('change_password.html')


        if(new_matched == True and old_matched == True and valid_password == True):
            updating_account_ = MasterData.query.filter(MasterData.username == username).first()
            print(updating_account_)
            print(new_password)
            updating_account_.password = request.form['newpassword']

            db.session.commit()
            flash("Password Changed Successfully.")
            return redirect(url_for('account'))
        else:
            return render_template('change_password.html')

    else:
        return render_template('change_password.html')



@app.route('/user/account/update', methods = ['GET', 'POST'])
def account_update():
    username = session['username']

    updating_account = MasterData.query.filter(MasterData.username == username).first()
    up_email = updating_account.email
    up_password = updating_account.password

    updating_account = AccountDetails.query.filter(AccountDetails.detail_username == username).first()
    up_bio = updating_account.detail_bio
    up_fullname = updating_account.detail_fullname
    up_city = updating_account.detail_city
    up_state =  updating_account.detail_state
    up_country = updating_account.detail_country
    up_gender = updating_account.detail_gender

    if request.method == 'POST':
        new_fullname = request.form['fullname']
        new_bio = request.form['bio']
        new_gender = request.form['gender']
        new_city = request.form['city']
        new_state = request.form['state']
        new_country = request.form['country']
        new_email = request.form['email']

        updating_account = MasterData.query.filter(MasterData.username == username).first()
        updating_account.email = new_email

        db.session.commit()

        updating_account = AccountDetails.query.filter(AccountDetails.detail_username == username).first()
        updating_account.detail_fullname = new_fullname
        updating_account.detail_bio = new_bio
        updating_account.detail_gender = new_gender
        updating_account.detail_city = new_city
        updating_account.detail_state = new_state
        updating_account.detail_country = new_country

        db.session.commit()
        flash("Account details Updated!")
        return redirect(url_for('account'))

    else:
        return render_template('updateaccount.html', username=username, gender=up_gender, bio=up_bio, fullname=up_fullname, city=up_city, state=up_state, country=up_country, email=up_email)

@app.route('/account_deleteconfirm')
def confirm_delete():
    return render_template('deleteconfirm.html')


@app.route('/account_delete', methods=['POST', 'GET'])
def account_delete():

    if request.method == 'POST':
        passwd = request.form['password']
        username = session['username']

        main_data = MasterData.query.filter(MasterData.username == username).first()
        account_data = AccountDetails.query.filter(AccountDetails.detail_username == username).first()
        message_data = MsgData.query.all()
        post_data = PostCont.query.all()
        reply_data = RepliesData.query.all()

        date_time = datetime.now()
        filename = f"deleted_account/{username}_{date_time}.txt"

        content = f"Username : {main_data.username}\nEmail : {main_data.email}\nFullname : {account_data.detail_fullname}\nGender : {account_data.detail_gender}\nLocation : {account_data.detail_city},{account_data.detail_state},{account_data.detail_country}\nBio : {account_data.detail_bio}\nAccount Deleted on : {date_time}"

        post_user = ""

        for post in post_data:
            if(post.posted_by == username):
                cont = f"\nDate : {post.posted_on}\nPost ID : {post.post_id}\nPost Content : {post.post_content}\n\n"
                post_user += cont

        user_replied = ""

        for reply in reply_data:
            if(reply.reply_by == username):
                cont = f"\nDate : {reply.reply_on}\nReply ID : {reply.reply_id}\nReply of Post : {reply.reply_of}\nReply Content : {reply.reply_content}\n\n"
                user_replied += cont

        user_sends_msg = ""

        for msg in message_data:
            if(msg.msg_from == username):
                cont = f"\nDate : {msg.msg_on}\nMsg to : {msg.msg_to}\nMessage : {msg.msg_content}\n\n"
                user_sends_msg += cont

        user_receive_msg = ""

        for msg in message_data:
            if(msg.msg_to == username):
                cont = f"\nDate : {msg.msg_on}\nMsg from : {msg.msg_from}\nMessage : {msg.msg_content}\n\n"
                user_receive_msg += cont

        f = open(filename, 'a')
        f.write(content)
        f.write("\n\nPosts ------------")
        f.write(post_user)
        f.write("\n\nUser Replied on other Posts -----------------------")
        f.write(user_replied)
        f.write("\n\nUser sends Messages --------------------------------")
        f.write(user_sends_msg)
        f.write("\n\nUser receives Messages ---------------------------------")
        f.write(user_receive_msg)
        f.close()



        try:
            user_data_info = MasterData.query.filter(MasterData.username==username).first()
            if(passwd == user_data_info.password):
                try:
                    user_account = MasterData.query.filter(MasterData.username == username).first()
                    db.session.delete(user_account)
                    db.session.commit()
                except Exception as e:
                    print(e)
                    pass

                try:
                    user_account2 = AccountDetails.query.filter(AccountDetails.detail_username == username).first()
                    db.session.delete(user_account2)
                    db.session.commit()
                except Exception as e:
                    print(e)
                    pass

                #----------------deleting text post and their replies and likes-----------------------
                try:
                    post_data_user = PostCont.query.all()
                    for posts in post_data_user:
                        if(post.posted_by == username):

                            #-----------------------deleting replies ---------------
                            remove_replies = RepliesData.query.filter(RepliesData.reply_of == post.post_id ).first()
                            if(remove_replies != None):
                                db.session.delete(remove_replies)
                                db.session.commit()

                            #-------------------------deleting likes ---------------
                            remove_likes = LikesTextPost.query.filter(LikesTextPost.liket_post_id == post.post_id).first()
                            if(remove_likes != None):
                                db.session.delete(remove_likes)
                                db.session.commit()

                            remove_post = PostCont.query.filter(PostCont.posted_by == username).first()
                            db.session.delete(remove_post)
                            db.session.commit()

                except Exception as e:
                    print(e)
                    pass
                #----------------------deleting likes by user on text posts--------
                try:
                    all_likes = LikesTextPost.query.all()
                    for like in all_likes:
                        if(like.liket_by == username):
                            remove_likes = LikesTextPost.query.filter(LikesTextPost.liket_by == username).first()
                            db.session.delete(remove_likes)
                            db.session.commit()
                except Exception as e:
                    print(e)
                    pass

                #----------------------deleting replies by user on text Posts----------------
                try:
                    all_replies = RepliesData.query.order_by(RepliesData.reply_on).all()
                    for reply in all_replies:
                        if reply.reply_by == username:
                            reply = RepliesData.query.filter(RepliesData.reply_by == username).first()
                            db.session.delete(reply)
                            db.session.commit()
                except Exception as e:
                    print(e)
                    pass

                #----------------------deleting messages -----------------------------

                try:
                    all_msgs = MsgData.query.order_by(MsgData.msg_on).all()
                    for msg in all_msgs:
                        if msg.msg_from == username :
                            msg_ = MsgData.query.filter(MsgData.msg_from == username).first()
                            db.session.delete(msg_)
                            db.session.commit()
                        elif msg.msg_to == username:
                            msg_= MsgData.query.filter(MsgData.msg_to == username).first()
                            db.session.delete(msg_)
                            db.session.commit()

                except Exception as e:
                    print(e)
                    pass

                #----------------------------deleting block list-------------------
                try:
                    all_blocked = BlockData.query.all()
                    for name in all_blocked:
                        if name.block_by == username :
                            block_ = BlockData.query.filter(BlockData.block_by == username).first()
                            db.session.delete(block_)
                            db.session.commit()
                        elif name.blocked == username :
                            block_ = BlockData.query.filter(BlockData.blocked == username).first()
                            db.session.delete(block_)
                            db.session.commit()
                except Exception as e:
                    print(e)
                    pass
                 #------------------deleting followings and Followers-------------------------
                try:
                    user_follow_data = FollowerData.query.all()
                    for data in user_follow_data:
                        if data.followed_by == username:
                            data_delete = FollowerData.query.filter(FollowerData.followed_by == username).first()
                            db.session.delete(data_delete)
                            db.session.commit()
                        elif data.followed_to == username:
                            data_delete = FollowerData.query.filter(FollowerData.followed_to == username).first()
                            db.session.delete(data_delete)
                            db.session.commit()

                except:
                    print(e)
                    pass


                try:
                    filename = f"{username}.jpg"
                    if os.path.exists(f"static/{filename}"):
                        os.remove(f"static/{filename}")
                    else:
                        print("The file does not exist")
                except Exception as e:
                    print(e)
                    pass

                #-----------deleting notifications --------------------
                try:
                    all_notifications = Notifications.query.all()
                    for notification in all_notifications:
                        if notification.notification_username == username:
                            delete_notification = Notifications.query.filter(Notifications.notification_username == username).first()
                            db.session.delete(delete_notification)
                            db.session.commit()
                except Exception as e:
                    print(e)
                    pass

                #------------------------

                #-------------------deleting Private Account Status-----------------------
                try:
                    private_account = PrivateAccount.query.filter(PrivateAccount.pa_username).first()
                    if(private_account != None or private_account != ""):
                        db.session.delete(private_account)
                        db.session.commit()
                except Exception as e:
                    print(e)
                    pass

                #-----------------deleting follow Requests--------------------
                try:
                    all_follow_requests = FollowRequests.query.all()
                    for request in all_follow_requests:
                        if(request.follow_request_by == username):
                            delete_request = FollowRequests.query.filter(FollowRequests.follow_request_by == username).first()
                            db.session.delete(delete_request)
                            db.session.commit()
                        elif(request.follow_request_to == username):
                            delete_request = FollowRequests.query.filter(FollowRequests.follow_request_to == username).first()
                except Exception as e:
                    print(e)
                    pass

                #-------------deleting user Private Key ---------------
                try:
                    private_key = user_Access_Key.query.filter(user_Access_Key.user_private_username == username).first()
                    if private_key != None or private_key != "":
                        db.session.delete(private_key)
                        db.session.commit()
                except Exception as e:
                    print(e)
                    pass

                #-----------------deleting photopost and their comments and likes and Images--------------------
                try:
                    photopost_data_user = PhotoPost.query.all()
                    for photo in photopost_data_user:
                        if(photo.photopost_username == username):

                            #-----------------------deleting Comments ---------------
                            remove_comments = PhotoPostCommnets.query.filter(PhotoPostCommnets.comment_pp_post_id == photo.photopost_id ).first()
                            if(remove_comments != None):
                                db.session.delete(remove_comments)
                                db.session.commit()

                            #-------------------------deleting likes ---------------
                            remove_likes = LikesPhotoPost.query.filter(LikesPhotoPost.likep_post_id == photo.photopost_id).first()
                            if(remove_likes != None):
                                db.session.delete(remove_likes)
                                db.session.commit()
                            #------------------------delete photopost images -----------------------
                            photo_name = photo.photopost_image
                            try:
                                filename = photo_name
                                if os.path.exists(f"static/{filename}"):
                                    os.remove(f"static/{filename}")
                                else:
                                     print("The file does not exist")
                            except Exception as e:
                                print(e)
                                pass
                            #---------------deleting photopost from database ------------------
                            remove_photopost = PhotoPost.query.filter(PhotoPost.photopost_username == username).first()
                            db.session.delete(remove_photopost)
                            db.session.commit()

                except Exception as e:
                    print(e)
                    pass

                #-------------deleting likes on photoposts by user -----------------------------
                try:
                    all_likes = LikesPhotoPost.query.all()
                    for like in all_likes:
                        if(like.likep_by == username):
                            remove_like = LikesPhotoPost.query.filter(LikesPhotoPost.likep_by == username).first()
                            db.session.delete(remove_like)
                            db.session.commit()

                except Exception as e:
                    print(e)
                    pass

                #------------deleting photopost comments by user on Photo Posts---------------------
                try:
                    all_comments = PhotoPostCommnets.query.all()
                    for comment in all_comments:
                        if(comment.comment_pp_username == username):
                            comment_remove = PhotoPostCommnets.query.filter(PhotoPostCommnets.comment_pp_username == username).first()
                            db.session.delete(comment_remove)
                            db.session.commit()


                except Exception as e:
                    print(e)
                    pass

            else:
                return render_template(url_for('confirm_delete'))
        except Exception as e:
            print(e)
            return  redirect(url_for('index'))
        flash("Account deleted Successfully.")
        return render_template('index.html')
    else:
        return render_template('deleteconfirm.html')
        try:
            flash("Account deleted Successfully.")
            return redirect(url_for('index'))
        except Exception as e:
            print(e)
            return redirect(url_for('login'))




@app.route('/add_details', methods = ['GET', 'POST'])
def add_details():
    if request.method == 'POST':

        #----------------updating profile photo ----------------------------

        f = request.files['file']
        file_name, file_extension = os.path.splitext(f.filename)
        f.filename = f"{signin_username}" + ".jpg"
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))

        #----------------updating profile photo ----------------------------


        adddetail_username = request.form['username']
        if(len(request.form['fullname']) != 0 ):
            adddetail_fullname = request.form['fullname']
        else:
            adddetail_fullname = "N/A"

        adddetail_gender = request.form['gender']

        if(len(request.form['bio']) != 0 ):
            adddetail_bio = request.form['bio']
        else:
           adddetail_bio = "N/A"

        if(len(request.form['city']) != 0 ):
            adddetail_city = request.form['city']
        else:
           adddetail_city = "N/A"

        if(len(request.form['state']) != 0 ):
            adddetail_state = request.form['state']
        else:
           adddetail_state = "N/A"

        if(len(request.form['country']) != 0 ):
            adddetail_country = request.form['country']
        else:
           adddetail_country = "N/A"

        add_details_to_database = AccountDetails(detail_username=adddetail_username, detail_fullname=adddetail_fullname, detail_gender=adddetail_gender, detail_bio=adddetail_bio, detail_country=adddetail_country, detail_state=adddetail_state, detail_city=adddetail_city)
        db.session.add(add_details_to_database)
        db.session.commit()
        print("username : ", adddetail_username)
        flash("Account Created Successfully, please Login.")
        return redirect(url_for('login'))
    else:
        return render_template('add_details.html')


@app.route('/user/account')
def account():
    username = session['username']
    account_info = AccountDetails.query.filter(AccountDetails.detail_username==username).first()
    bio = account_info.detail_bio
    gender = account_info.detail_gender
    fullname = account_info.detail_fullname
    city = account_info.detail_city
    state = account_info.detail_state
    country = account_info.detail_country
    info = MasterData.query.filter(MasterData.username == username).first()
    email_data = info.email
    email = email_data

    app.jinja_env.globals['profile_pic'] = f'{username}.jpg'

    followers_no = 0
    following_no = 0

    all_followed = FollowerData.query.all()
    for follows in all_followed:
        if follows.followed_by == username:
            following_no += 1

        if follows.followed_to == username:
            followers_no += 1

    try:
        privacy_status_data = PrivateAccount.query.filter(PrivateAccount.pa_username == username).first()
        privacy_status = privacy_status_data.pa_status
    except:
        privacy_status = False
        pass

    #---------------get private_key----------------
    user_private = user_Access_Key.query.filter(user_Access_Key.user_private_username==username).first()
    user_private_key = user_private.user_private_key

    return render_template('myaccount.html',user_private_key=user_private_key, privacy_status=privacy_status, followers_no=followers_no, following_no=following_no, bio=bio, gender=gender, country=country, state=state, email=email, fullname=fullname, city=city, username=username)

@app.route('/user/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = PostCont.query.get_or_404(id)
    if request.method == 'POST':
        post.post_content = request.form['content']
        db.session.commit()
        flash("Post Edited!")
        return redirect('/user')
    else:
        return render_template('edit_post.html', post=post)

@app.route('/user/delete/<int:id>')
def delete(id):
    # deleting likes ------------------
    all_likes = LikesTextPost.query.all()
    for like in all_likes:
        if like.liket_post_id == id:
            like_remove = LikesTextPost.query.filter(LikesTextPost.liket_post_id == id).first()
            db.session.delete(like_remove)
            db.session.commit()

    #----------deleting post---------------

    post = PostCont.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash("Post Deleted!")
    return redirect('/user')

@app.route('/user/create_post', methods = ['GET', 'POST'])
def createPost():
    if request.method == 'POST':
        new_post_content = request.form['content']
        username = session['username']
        print(datetime.now())
        new_post = PostCont(posted_by=username, post_content=new_post_content, posted_on=datetime.now())
        db.session.add(new_post)
        db.session.commit()
        flash("Posted Successfully!")
        return redirect('/user')
    else:
        return render_template('create_post.html')


@app.route('/user')
def user():
    if 'username' in session:
        username = session['username']
        user__ = MasterData.query.filter(MasterData.username == username).first()
        user_id = user__.id
        user__ = MasterData.query.filter(MasterData.username == username).first()
        user_email = user__.email

        app.jinja_env.globals['image_name'] = '.jpg'

        all_posts = PostCont.query.order_by(PostCont.posted_on.desc()).all()
        all_replies = RepliesData.query.order_by(RepliesData.reply_on).all()

        no_of_notifications = 0
        all_notifications = Notifications.query.all()
        for notification in all_notifications:
            if notification.notification_username == username:
                no_of_notifications += 1

        #------------get block list -------------------------
        system_data = MasterData.query.all()
        blocked_contact = BlockData.query.all()
        blocked_list = []
        for contact in blocked_contact:
            if contact.blocked == username:
                blocked_list.append(contact.block_by)
            if contact.block_by == username:
                blocked_list.append(contact.blocked)

        #----------------get post likes and likes number ------------------------------
        all_post_likes = LikesTextPost.query.all()
        post_and_likes = {}
        number_of_likes = {}
        for likes in all_post_likes:
            post_id = likes.liket_post_id

            if(post_and_likes.get(post_id) == None):
                users = []
                user = likes.liket_by
                post_and_likes[post_id] = users
                post_and_likes[post_id].append(user)
            else:
                user = likes.liket_by
                post_and_likes[post_id].append(user)

            if(number_of_likes.get(post_id) == None):
                number = 0
                number_of_likes[post_id] = number + 1
            else:
                number = number_of_likes.get(post_id)
                number_of_likes[post_id] = number + 1

        print(post_and_likes)
        print(number_of_likes)

        #--------------------get following and followers-------------------

        followers = []
        following = [username]

        all_followed = FollowerData.query.all()
        for follows in all_followed:
            if follows.followed_by == username:
                following.append(follows.followed_to)
            if follows.followed_to == username:
                followers.append(follows.followed_by)

        return render_template('user.html',following=following, post_and_likes=post_and_likes, number_of_likes=number_of_likes, no_of_notifications=no_of_notifications, posts=all_posts, replies=all_replies, username=username, blocked_list=blocked_list, system_data=system_data)

    else:
        return redirect(url_for('login'))


@app.route('/user_logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_username = request.form['username']
        login_password = request.form['password']
        user_data = MasterData.query.all()
        user_exist = False
        for data in user_data:
            if data.username == login_username:
                user_exist = True

        if user_exist == False:
            flash("Username not found!")
            return render_template('login.html')

        if user_exist == True:
            info = MasterData.query.filter(MasterData.username == login_username).first()
            password_data = info.password
            if(login_password != password_data):
                flash("Incorrect Password!")
                return render_template('login.html')
            else:
                user__ = MasterData.query.filter(MasterData.username == login_username).first()
                user_id = user__.id
                user__ = MasterData.query.filter(MasterData.username == login_username).first()
                user_email = user__.email
                session['username'] = login_username
                user_data = ""
                info = ""
                return redirect('/user')
    else:
        return render_template('login.html')


@app.route('/verify-otp-final', methods = ['GET', 'POST'])
def verify_otp_final():
    if request.method == 'POST':
        try:
            get_otp = int(request.form['otp'])
        except Exception as e:
            print(e)
            get_otp = 0000
            pass
        print("Get OTP : ", get_otp)
        print('Generated OTP : ', genrated_otp)
        if get_otp == genrated_otp:
            add_user_to_database = MasterData(username=signin_username, email=signin_email, password=signin_password)
            db.session.add(add_user_to_database)
            db.session.commit()

            #adding----private---key------------------------------------------------------------------
            try:
                private_key_length = 15

                private_key_characters = ['1','2','8','5','f','g','z','v','6','p','l','q','c','4','d','x']
                private_key = []
                for x in range(private_key_length):
                    private_key.append(random.choice(private_key_characters))

                private_key = "".join(private_key)

                print(private_key)

                add_private_key = user_Access_Key(user_private_username=signin_username, user_private_key=private_key)
                db.session.add(add_private_key)
                db.session.commit()
            except:
                private_key = '3xqi903ml56splq'
                add_private_key = user_Access_Key(user_private_username=signin_username, user_private_key=private_key)
                db.session.add(add_private_key)
                db.session.commit()
            #-----------------------------------------------------------------------------------------


            date_time = datetime.now()
            cont = f"Username : {signin_username}\nEmail : {signin_email}\nDate : {date_time}\n\n"
            filename = "account_created/new_accounts.txt"

            f = open(filename, 'a')
            f.write(cont)
            f.close()

            return render_template('add_details.html', username=signin_username)
        else:
            flash("Incorrect OTP")
            return render_template('verify-otp.html')
    else:
        return render_template('verify-otp.html')


@app.route('/verify-otp', methods = ['GET', 'POST'])
def verify_otp():
    global genrated_otp
    genrated_otp = send_otp(signin_email)
    genrated_otp = int(genrated_otp)
    return render_template('verify-otp.html')

def send_otp(email_address):
    otp_sent = False
    while otp_sent == False:
        genrated_otp = random.randint(100000,999999)
        print(genrated_otp)
        ob = s.SMTP("smtp.gmail.com",587)
        ob.starttls()
        ob.login(server_mail,server_pass)
        subject = "STARPS OTP"
        body = f"""        
                Dear {signin_username},

                Your Starps verification OTP is {genrated_otp}.

                Don't share this OTP with anyone.

                Thank you
        """
        message = "Subject:{}\n\n{}".format(subject,body)
        ob.sendmail("nagesh.risk@gmail.com",email_address ,message)
        print("send successfully")
        otp_sent = True
        ob.quit()
    return genrated_otp




@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        global signin_email
        global signin_password
        global signin_username
        signin_username = request.form['username']
        signin_email = request.form['email']
        signin_password = request.form['password']
        signin_password2 = request.form['password2']

        valid_username = True
        invalid_characters = ".! #$%^&*()<>?/;:'=+-[]|\""

        for char in signin_username:
            if(char in invalid_characters):
                valid_username = False

        if valid_username == False:
            flash("Special Characters and space are not allowed in Username except underscore(_)")
            return render_template('signup.html')


        email_pre_exists = False
        username_pre_exists = False
        valid_password = True

        data_from_database = MasterData.query.all()

        for user in data_from_database:
            if(user.email == signin_email):
                email_pre_exists = True
                flash("Email already exists")
                return render_template('signup.html')

        for user in data_from_database:
            if(user.username == signin_username):
                username_pre_exists = True
                flash("Username already exists")
                return render_template('signup.html')

        password_invalidity = 0

        length_of_password = len(signin_password)
        if(length_of_password < 6):
            password_invalidity+=1

        if(signin_password != signin_password2):
            valid_password = False
            flash("Password doesn't Matched! ")
            return render_template('signup.html')

        elif(password_invalidity!=0):
            valid_password = False
            flash("Password must be length of 6 or more!")
            return render_template('signup.html')


        if(valid_username == True and email_pre_exists == False and valid_password == True and username_pre_exists == False):
            # add_user_to_database = MasterData(username=signin_username, email=signin_email, password=signin_password)
            # db.session.add(add_user_to_database)
            # db.session.commit()
            return redirect(url_for('verify_otp'))
    else:
        return render_template('signup.html')

@app.route('/user/page_not_available')
def page_not_available():
    return render_template('page_not_available.html')

@app.route('/starps/about')
def about_us():
    return render_template('about.html')

@app.route('/starps/privacy_policy')
def privacy_policy():
    return render_template('privacy_policy.html')

@app.route('/starps/term_and_conditions')
def term_and_conditions():
    return render_template('term_and_conditions.html')


if __name__ == "__main__":
    app.run(debug=True)
