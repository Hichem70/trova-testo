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
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    

    def __init__(self, title, content, source, chapter_id):
        self.title = title
        self.content = content
        self.source = source
        self.chapter_id = chapter_id
    


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


@app.route('/')
def home():

    if "password" in session:
        chapters = Chapter.query.all()
        texts = Text.query.all()
        return render_template('index.html', chapters=chapters, texts=texts)

    else:
        return redirect(url_for('login'))

@app.route('/insert', methods=['POST', 'GET'])
def insert():
    chapters = Chapter.query.all()
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        source = request.form['source']
        related_chapter = request.form['chapter']

        data_to_insert = Text(title=title, content=content, source=source, chapter_id=related_chapter)
        db.session.add(data_to_insert)
        db.session.commit()

        flash('Testo aggiunto correttamente !', category='success')

        return redirect(url_for('home'))

    return render_template('add_text.html', chapters=chapters)

@app.route('/remove/<id>')
def remove(id):

    to_remove = Text.query.filter_by(id=id).first()

    db.session.delete(to_remove)
    db.session.commit()
    flash('Testo cancellato correttamente !', category='success')

    return redirect(url_for('home'))

@app.route('/edit/<id>', methods=['POST', 'GET'])
def edit(id):

    text = Text.query.filter_by(id=id).first()
    chapters = Chapter.query.all()

    if request.method == 'POST':

        if "password" in session:
            title = request.form['title']
            content = request.form['content']
            source = request.form['source']
            related_chapter = request.form['chapter']
        

            update_this = Text.query.filter_by(id=id).first()

            update_this.title=title
            update_this.content=content
            update_this.source=source
            update_this.chapter_id=related_chapter
        
        
            db.session.commit()
            flash('Aggiornamento andato a buon fine, Grazie!', category='success')
            return redirect(url_for('home'))

            else:
                return redirect(url_for('home'))

        


    

    return render_template('edit.html', text=text, chapters=chapters)

if __name__ == "__main__":
    app.run(debug=True)
