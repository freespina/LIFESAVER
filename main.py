
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

items=[{'title':'PS5 PRO 750$$','SELLER':'seller:misho gatenashvili','img':'https://4kwallpapers.com/images/wallpapers/playstation-5-pro-3840x2160-19032.jpg'},
       {'title':'BIGA PC 1300$$','SELLER':'seller:giorgi lalize','img':'data:image/jpeg;base64,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'},
       {'title':'Xbox 650$$','SELLER':'seller:lasha gelashvili','img':'https://wallpapercat.com/w/full/6/7/e/1257900-3840x2160-desktop-4k-xbox-background-photo.jpg'},
       {'title':'Nintendo 250$$','SELLER':'seller:laura jixvaze','img':'https://assets.nintendo.com/image/upload/c_fill,w_1200/q_auto:best/f_auto/dpr_2.0/ncom/en_US/products/hardware/nintendo-switch-red-blue/110478-nintendo-switch-neon-blue-neon-red-front-screen-on-1200x675'},
       {'title':'PS4 PRO 450$$', 'SELLER': 'seller:nikoloz welize','img': 'https://m.media-amazon.com/images/I/51tbWVPtckL._AC_SL1500_.jpg'},
       {'title':'PC XMAX 950$$', 'SELLER': 'seller:fotola joraze','img': 'https://m.media-amazon.com/images/I/815P1vN3HpL.jpg'},
       {'title':'Xbox 350$$', 'SELLER': 'seller:sandro nozaze','img': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQaVwNRDt1eMvC7kfWJZ0cLHUlaILdNKPP3fQ&s'}
       ]


@app.route('/')
def register():
    return render_template('register.html')

@app.route('/index')
def index():
    return render_template('index.html', items=items)


@app.route('/add_question', methods=['POST'])
def add_question():
    name = request.form.get('name')
    mail = request.form.get('mail')
    question = request.form.get('question')

    # Create record to database
    conn = sqlite3.connect('GEOshop_blogs.db')
    c = conn.cursor()

    conn.execute('''
                 INSERT INTO contacts (name, email, question)
                 VALUES (?, ?, ?)
                 ''', (name, mail, question))
    conn.commit()
    conn.close()
    return render_template('contact.html')



@app.route('/about_us')
def about_us():
    return render_template('about_us.html', items=items)

@app.route('/buy')
def buy():
    return render_template('buy.html', items=items)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        user_email = request.form.get('email')
        user_password = request.form.get('password')
        conn = sqlite3.connect('GEOshop_blogs.db')
        c = conn.cursor()
        c.execute("SELECT email, password FROM users WHERE email = ?", (user_email,))
        rows = c.fetchall() # [('sandro@gmail.com', '12341234')]
        if rows:
            database_password = rows[0][1]

            if database_password == user_password:
                return redirect(url_for('admin'))
        conn.close()


    return render_template('sign_in.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/admin_contacts')
def admin_contacts():
    conn = sqlite3.connect('GEOshop_blogs.db')
    c = conn.cursor()
    c.execute('SELECT * FROM contacts')
    rows = c.fetchall()
    conn.close()

    questions = []
    for row in rows:
        questions.append({'id': row[0],'name': row[1], 'email': row[2], 'question': row[3]})

    print(questions)
    return render_template('admin_contacts.html', questions = questions)


if __name__ == '__main__':
    app.run(debug=True)