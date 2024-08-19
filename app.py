from flask import Flask, render_template, request
import sqlite3,os

app = Flask(__name__)

def init_db():
    db_path = os.path.abspath("contact.db")
    print(f"Initializing database at: {db_path}")
    with sqlite3.connect(db_path) as conn:
        conn.execute('DROP TABLE IF EXISTS messages') 
        conn.execute('''CREATE TABLE messages
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         email TEXT NOT NULL,
                         message TEXT NOT NULL,
                         timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    print("Database initialized and table created")

    
@app.route('/')
def home():
    return render_template('homepage.htm')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/project1')
def project1():
    return render_template('project1.html')


@app.route('/about-me')
def about_me():
    return render_template('about-me.html')


@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    print("Request method:", request.method)  
    if request.method == 'POST':
        email = request.form.get('email')
        message = request.form.get('message')
        print(f"Received: email={email}, message={message}") 

        if not email or not message:
            print("Missing email or message")  
            return render_template('contacts.html', message="Please fill out both the email and message fields.")

        if '@' not in email:
            print("Invalid email")  
            return render_template('contacts.html', message="Please enter a valid email address.")

        with sqlite3.connect("contact.db") as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO messages (email, message) VALUES (?, ?)', (email, message))
                conn.commit()
                print("Data inserted successfully") 
        

        return render_template('contacts.html', message="Message sent and stored successfully!")
    
    return render_template('contacts.html')
 


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
