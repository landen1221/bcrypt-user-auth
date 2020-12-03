from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import RegistrationForm, LoginForm, FeedbackForm


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///project_24"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)

toolbar = DebugToolbarExtension(app)

@app.route('/')
def home_page():
    return redirect('/register')

@app.route('/register', methods=["GET","POST"])
def registration():
    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password, email, first_name, last_name)
        db.session.add(new_user)
        db.session.commit()

        session['userID'] = username
        flash(f"Welcome {username}!", 'success')

        return redirect('/secret')

    return render_template('/register.html', form=form)


@app.route('/login', methods=["GET","POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        auth_user = User.authenticate(username, password)

        session['userID'] = username
        flash(f"Welcome back: {username}", 'success')

        return redirect(f'/user/{username}')

    return render_template('/login.html', form=form)

@app.route('/user/<username>')
def user_details(username):
    if confirm_login():
        return redirect('/login')
    
    user = User.query.filter_by(username = username).first()
    feedback = Feedback.query.filter_by(feedback_about = username).all()

    return render_template('user.html', user=user, feedback=feedback)

@app.route('/users')
def secret_route():
    users = User.query.all()
    
    return render_template('users.html', users=users)

@app.route('/logout')
def logout_user():
    session.pop('userID')
    flash("Successfully logged out -- Goodbye!", "success")
    return redirect('/login')

# @app.route('/users/<username>/delete')
# def delete_user(username):
#     return

@app.route('/users/<username>/feedback/add', methods=["GET", "POST"])
def add_feedback(username):
    form = FeedbackForm()

    if form.validate_on_submit():
        print('made it to the post stage!!!')
        title = form.title.data
        content = form.content.data
        feedback_about = username
        feedback_from = session['userID']

        new_fb = Feedback(title=title, content=content, feedback_about=feedback_about, feedback_from=feedback_from)
        db.session.add(new_fb)
        db.session.commit()
        
        flash(f"Post added", 'success')
        
        return redirect(f'/user/{username}')

    return render_template('feedback.html', form=form, username=username)

@app.route('/feedback/<feedbackID>/update', methods=["GET", "POST"])
def update_feedback(feedbackID):
    feedback = Feedback.query.get(feedbackID)
    username = feedback.feedback_about
    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        
        db.session.commit()
        
        flash(f"Post updated", 'success')
        
        return redirect(f'/user/{username}')

    

    return render_template('feedback.html', form=form, username=username)


@app.route('/feedback/<feedbackID>/delete')
def delete_feedback(feedbackID):
        
    feedback = Feedback.query.get_or_404(feedbackID)
    if feedback.feedback_from == session['userID']:
        db.session.delete(feedback)
        db.session.commit()
        flash('feedback deleted')
        
        return redirect('/users')

    flash("You don't have permission to do that!", "danger")
    return


def confirm_login():
    if "userID" not in session:
        flash("Please login to view that page", "danger")
        return True

