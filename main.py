from flask import Flask, render_template, request, url_for, flash, redirect, session
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

app.config['SECRET_KEY'] = '@ajaxAmstemax!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chapter = db.Column(db.String(250), nullable=False)
    texts = db.relationship('Text', backref='chapter', lazy=True)

    def __init__(self, chapter):
        self.chapter = chapter
    
class Text(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    content = db.Column(db.String(20000), nullable=False)
    source = db.Column(db.String(250), nullable=False)
    level = db.Column(db.String(250), nullable=False)
    contribuente = db.Column(db.String(250), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    

    def __init__(self, title, content, source, level , contribuente ,chapter_id):
        self.title = title
        self.content = content
        self.source = source
        self.level = level
        self.contribuente = contribuente
        self.chapter_id = chapter_id

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    

    if request.method == 'POST':
        
        username = request.form['username']
        password = request.form['password']

        

        if password == "docenti2021" and username != "":
            session['password'] = password
            flash(f'Ciao {username} !', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Password errata! Riprova', 'error')






    return render_template('login.html')

@app.route('/logout')
def logout():

    session.clear()
    return redirect(url_for('login'))

@app.route('/admin@1986rades@foret')
def home():

    chapters = Chapter.query.all()
    texts = Text.query.all()
    return render_template('index.html', chapters=chapters, texts=texts)

@app.route('/insert', methods=['POST', 'GET'])
def insert():
    chapters = Chapter.query.all()
    if request.method == 'POST':
        contrib = request.form['contrib']
        title = request.form['title']
        content = request.form['content']
        source = request.form['source']
        level = request.form['level']
        related_chapter = request.form['chapter']

        data_to_insert = Text(title=title, content=content, source=source, level=level, contribuente=contrib ,chapter_id=related_chapter)
        db.session.add(data_to_insert)
        db.session.commit() 

        flash('Testo aggiunto correttamente !', category='success')

        return redirect(url_for('index'))

    return render_template('add_text.html', chapters=chapters)

@app.route('/remove/<id>')
def remove(id):

    to_remove = Text.query.filter_by(id=id).first()

    db.session.delete(to_remove)
    db.session.commit()
    flash('Testo cancellato correttamente !', category='success')

    return redirect(url_for('home'))

@app.route('/edit@admin@1986/<id>', methods=['POST', 'GET'])
def edit(id):

    text = Text.query.filter_by(id=id).first()
    chapters = Chapter.query.all()

    if request.method == 'POST':

        ## GETTING INFORMATIONS FROM INPUT VIA POST METHOD
        title = request.form['title']
        content = request.form['content']
        source = request.form['source']
        contrib = request.form['contrib']
        level = request.form['level']
        related_chapter = request.form['chapter']
        
        ## GETTING INFORMATIONS FROM DATABASE

        update_this = Text.query.filter_by(id=id).first()

        ## AND THEN APPLY MODIFICATIONS ON THEM
        update_this.title=title
        update_this.content=content
        update_this.source=source
        update_this.contrib=contrib
        update_this.level=level
        update_this.chapter_id=related_chapter
        
        
        db.session.commit()

        flash('Aggiornamento andato a buon fine, Grazie!', category='success')

        return redirect(url_for('index'))

        


    

    return render_template('edit.html', text=text, chapters=chapters)

@app.route('/home', methods=['POST', 'GET'])
def index():

    chapters = Chapter.query.all()
    all_texts = Text.query.all()

    if request.method == 'POST':
        chapter_id = request.form['chapterId']

        texts = Text.query.filter_by(chapter_id=chapter_id).all()

        chapters = Chapter.query.all()


        return render_template('home.html', texts=texts, chapters=chapters)

    
    return render_template('home.html', chapters=chapters, all_texts=all_texts)

if __name__ == "__main__":
    app.run(debug=True)

