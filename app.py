from flask import Flask, render_template, url_for, redirect, request,flash
from models import db, User,Subjects,Sessions
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'psecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:jntuhucej%40507@localhost/studytracker'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---------------- HOME ----------------
@app.route('/')
def home():
    return redirect(url_for('login'))


# ---------------- LOGIN ----------------
@app.route('/login', methods=["GET", "POST"])
def login():
     if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()

        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!', 'danger')
     return render_template("login.html")


# ---------------- REGISTER ----------------
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'error')
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration Successful. Please login!', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')
#-----------dashboard--------#
@app.route('/dashboard')
@login_required
def dashboard():

    sessions = Sessions.query.filter_by(user_id=current_user.id).all()

    subject_totals = {}

    for s in sessions:
        subject_name = s.subjects.name if s.subjects else "Unknown"
        subject_totals[subject_name] = subject_totals.get(subject_name, 0) + float(s.hours)

    subjects = list(subject_totals.keys())
    hours = list(subject_totals.values())

    return render_template(
        'dashboard.html',
        username=current_user.username,
        subjects=subjects,
        hours=hours
    )
#-----------adding add session------------#
@app.route('/add', methods=['GET','POST'])
@login_required
def add_session():
    subjects=Subjects.query.all()
    if request.method=='POST':
        title=request.form['title']
        hours=float(request.form['hours'])
        date=request.form['date']
        subjects_id= int(request.form['subjects_id'])

        new_session = Sessions(
            title=title,
            hours=hours,
            date=date,
            user_id=current_user.id,
            subjects_id=subjects_id 
        )
        db.session.add(new_session)
        db.session.commit()
        flash('SEssion is Added !', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_session.html',subjects=subjects)
#------add subjects-------------------------#
@app.route('/subjects',methods=["GET","POST"])
@login_required
def list_subjects():
    subjects = Subjects.query.all()
    return render_template('list_subjects.html',subjects=subjects)


#--------adding categories------------------#
@app.route('/subjects/add',methods=['GET','POST'])
@login_required
def add_categories():
    if request.method =='POST':
        name=request.form['name']
        description=request.form['description']
        
        if Subjects.query.filter_by(name=name).first():
            flash('subject already exist','danger')
        else:
            new_sub=Subjects(name=name,description=description)
            db.session.add(new_sub)
            db.session.commit()
            flash('Subject is added!','succcess')
            return redirect(url_for('list_subjects'))
    return render_template('add_categories.html')

#-------lOGOUT-#
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

#-------------Edit option----#
@app.route('/subjects/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_category(id):
    category = Subjects.query.get_or_404(id)

    if request.method == 'POST':
        category.name = request.form['name']
        category.description = request.form['description']
        db.session.commit()
        flash('Subjects updated!', 'success')
        return redirect(url_for('list_subjects'))

    return render_template('edit_category.html', category=category)

#-------------Delete option------------#
@app.route('/categories/delete/<int:id>')
@login_required
def delete_category(id):
    category = Subjects.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    flash('subjects deleted!', 'success')
    return redirect(url_for('list_subjects'))
    
# ---------------- CREATE TABLES ----------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)