from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from dotenv import load_dotenv
import sqlite3

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Configuração do banco de dados com caminho absoluto
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'urban_reports.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuração de upload
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Criar diretórios necessários
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'profiles'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'reports'), exist_ok=True)

# Models (mantenha os mesmos modelos do código anterior)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date)
    gender = db.Column(db.String(10))
    race = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    cpf = db.Column(db.String(14))
    city = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    profile_image = db.Column(db.String(200))
    is_dark_mode = db.Column(db.Boolean, default=False)
    notifications_enabled = db.Column(db.Boolean, default=True)
    
    reports = db.relationship('Report', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)
    votes = db.relationship('Vote', backref='voter', lazy=True)  # Adicione esta linha

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    address = db.Column(db.String(200))
    status = db.Column(db.String(20), default='pendente')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    photos = db.relationship('ReportPhoto', backref='report', lazy=True)
    comments = db.relationship('Comment', backref='report', lazy=True)
    votes = db.relationship('Vote', backref='voted_report', lazy=True)  # Adicione esta linha

class ReportPhoto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'), nullable=False)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'), nullable=False)

# Adicione esta classe depois do modelo Comment
class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10), nullable=False)  # upvote, downvote
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'), nullable=False)

# Adicione estas relações aos modelos User e Report
# Na classe User, adicione:
# votes = db.relationship('Vote', backref='voter', lazy=True)

# Na classe Report, adicione:
# votes = db.relationship('Vote', backref='voted_report', lazy=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Routes
@app.route('/')
def index():
    reports = Report.query.order_by(Report.created_at.desc()).limit(10).all()
    return render_template('index.html', reports=reports)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = 'remember' in request.form
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user, remember=remember)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Email ou senha incorretos.', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')
        surname = request.form.get('surname')
        birth_date_str = request.form.get('birth_date')
        gender = request.form.get('gender')
        race = request.form.get('race')
        phone = request.form.get('phone')
        cpf = request.form.get('cpf')
        city = request.form.get('city')
        
        # Check if user exists
        if User.query.filter_by(email=email).first():
            flash('Email já cadastrado.', 'error')
            return redirect(url_for('register'))
        
        if User.query.filter_by(username=username).first():
            flash('Nome de usuário já existe.', 'error')
            return redirect(url_for('register'))
        
        # Create new user
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d') if birth_date_str else None
        
        new_user = User(
            email=email,
            username=username,
            password=generate_password_hash(password),
            name=name,
            surname=surname,
            birth_date=birth_date,
            gender=gender,
            race=race,
            phone=phone,
            cpf=cpf,
            city=city
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Conta criada com sucesso! Faça login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    user_reports = Report.query.filter_by(user_id=current_user.id).order_by(Report.created_at.desc()).all()
    all_reports = Report.query.order_by(Report.created_at.desc()).limit(20).all()
    
    return render_template('dashboard.html', 
                         user_reports=user_reports, 
                         all_reports=all_reports)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        current_user.name = request.form.get('name', current_user.name)
        current_user.surname = request.form.get('surname', current_user.surname)
        current_user.email = request.form.get('email', current_user.email)
        current_user.phone = request.form.get('phone', current_user.phone)
        current_user.city = request.form.get('city', current_user.city)
        
        # Handle profile image upload
        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file and allowed_file(file.filename):
                filename = secure_filename(f"{current_user.id}_{datetime.now().timestamp()}.{file.filename.rsplit('.', 1)[1].lower()}")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'profiles', filename))
                current_user.profile_image = filename
        
        db.session.commit()
        flash('Perfil atualizado com sucesso!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('edit_profile.html')

@app.route('/new-report', methods=['GET', 'POST'])
@login_required
def new_report():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        address = request.form.get('address')
        
        report = Report(
            title=title,
            description=description,
            category=category,
            latitude=float(latitude) if latitude else None,
            longitude=float(longitude) if longitude else None,
            address=address,
            user_id=current_user.id
        )
        
        db.session.add(report)
        db.session.commit()
        
        # Handle multiple photo uploads
        photos = request.files.getlist('photos')
        for photo in photos:
            if photo and allowed_file(photo.filename):
                filename = secure_filename(f"{report.id}_{datetime.now().timestamp()}_{photo.filename}")
                photo.save(os.path.join(app.config['UPLOAD_FOLDER'], 'reports', filename))
                
                report_photo = ReportPhoto(
                    filename=filename,
                    report_id=report.id
                )
                db.session.add(report_photo)
        
        db.session.commit()
        flash('Reporte criado com sucesso!', 'success')
        return redirect(url_for('report_detail', report_id=report.id))
    
    return render_template('new_report.html')

@app.route('/report/<int:report_id>')
def report_detail(report_id):
    report = Report.query.get_or_404(report_id)
    return render_template('report_detail.html', report=report)

@app.route('/report/<int:report_id>/comment', methods=['POST'])
@login_required
def add_comment(report_id):
    content = request.form.get('content')
    
    comment = Comment(
        content=content,
        user_id=current_user.id,
        report_id=report_id
    )
    
    db.session.add(comment)
    db.session.commit()
    
    flash('Comentário adicionado!', 'success')
    return redirect(url_for('report_detail', report_id=report_id))

@app.route('/report/<int:report_id>/vote', methods=['POST'])
@login_required
def vote_report(report_id):
    vote_type = request.form.get('type')
    
    # Check if user already voted
    existing_vote = Vote.query.filter_by(
        user_id=current_user.id,
        report_id=report_id
    ).first()
    
    if existing_vote:
        if existing_vote.type == vote_type:
            db.session.delete(existing_vote)  # Remove vote if same type clicked
        else:
            existing_vote.type = vote_type  # Change vote type
    else:
        new_vote = Vote(
            type=vote_type,
            user_id=current_user.id,
            report_id=report_id
        )
        db.session.add(new_vote)
    
    db.session.commit()
    return jsonify({'success': True})

@app.route('/toggle-dark-mode', methods=['POST'])
@login_required
def toggle_dark_mode():
    current_user.is_dark_mode = not current_user.is_dark_mode
    db.session.commit()
    return jsonify({'dark_mode': current_user.is_dark_mode})

@app.route('/toggle-notifications', methods=['POST'])
@login_required
def toggle_notifications():
    current_user.notifications_enabled = not current_user.notifications_enabled
    db.session.commit()
    return jsonify({'notifications': current_user.notifications_enabled})

@app.route('/search')
def search():
    query = request.args.get('q', '')
    city = request.args.get('city', '')
    category = request.args.get('category', '')
    
    reports_query = Report.query
    
    if query:
        reports_query = reports_query.filter(
            (Report.title.contains(query)) | 
            (Report.description.contains(query))
        )
    
    if city:
        reports_query = reports_query.filter(Report.address.contains(city))
    
    if category:
        reports_query = reports_query.filter_by(category=category)
    
    reports = reports_query.order_by(Report.created_at.desc()).all()
    
    return render_template('search.html', reports=reports, query=query)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('index'))

# API Routes
@app.route('/api/reports')
def api_reports():
    reports = Report.query.order_by(Report.created_at.desc()).limit(50).all()
    
    reports_data = []
    for report in reports:
        reports_data.append({
            'id': report.id,
            'title': report.title,
            'description': report.description[:100] + '...',
            'category': report.category,
            'latitude': report.latitude,
            'longitude': report.longitude,
            'address': report.address,
            'status': report.status,
            'created_at': report.created_at.isoformat(),
            'author': report.author.username,
            'photo_count': len(report.photos)
        })
    
    return jsonify(reports_data)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create uploads directories if they don't exist
        os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'profiles'), exist_ok=True)
        os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'reports'), exist_ok=True)
    
    app.run(debug=True, port=5000)