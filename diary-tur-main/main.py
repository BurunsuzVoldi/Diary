from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SQLite ile bağlantı kurma 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# DB oluşturma
db = SQLAlchemy(app)

# Card tablosu
class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(100), nullable=False)
    text = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Card {self.id}>'

# User tablosu
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

# Giriş sayfası
@app.route('/', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        form_login = request.form['email']
        form_password = request.form['password']
        
        # Kullanıcıları veritabanından al
        users_db = User.query.all()
        
        # Kullanıcı bilgilerini kontrol et
        for user in users_db:
            if form_login == user.email and form_password == user.password:
                return redirect('/index')
        
        # Hatalı giriş
        error = 'Geçersiz e-posta veya şifre. Lütfen tekrar deneyin.'
        
    return render_template('login.html', error=error)

# Kayıt sayfası
@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        login = request.form['email']
        password = request.form['password']
        
        # Yeni kullanıcıyı veri tabanına ekle
        new_user = User(email=login, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect('/')
    else:
        return render_template('registration.html')

# İçerik sayfası
@app.route('/index')
def index():
    cards = Card.query.order_by(Card.id).all()
    return render_template('index.html', cards=cards)

# Kart sayfası
@app.route('/card/<int:id>')
def card(id):
    card = Card.query.get(id)
    return render_template('card.html', card=card)

# Kart oluşturma sayfası
@app.route('/create')
def create():
    return render_template('create_card.html')

# Kart oluşturma formu
@app.route('/form_create', methods=['GET', 'POST'])
def form_create():
    if request.method == 'POST':
        title = request.form['title']
        subtitle = request.form['subtitle']
        text = request.form['text']

        card = Card(title=title, subtitle=subtitle, text=text)
        db.session.add(card)
        db.session.commit()
        return redirect('/index')
    else:
        return render_template('create_card.html')

if __name__ == "__main__":
    app.run(debug=True)
