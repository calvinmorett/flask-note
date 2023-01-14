from flask import Flask, request
import sqlite3
import nltk

app = Flask(__name__, static_url_path='/static')

def extract_keywords(text):
    nltk.download('punkt', quiet=True)
    tokens = nltk.word_tokenize(text)
    keywords = [token for token in tokens if token.isalnum()]
    return keywords

@app.route('/', methods=['GET', 'POST'])
def add_text():
    if request.method == 'POST':
        text = request.form.get('text')
        tags = request.form.get('tags')
        tags = tags.strip().split(",") if tags else []
        keywords = extract_keywords(text)
        conn = sqlite3.connect('texts.db')
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS texts (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT, added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, tags TEXT, keywords TEXT)")
        c.execute("INSERT INTO texts (text, tags, keywords) VALUES (?,?,?)", (text, ",".join(tags), ",".join(keywords)))
        conn.commit()
        return '''
                <link rel="stylesheet" type="text/css" href="static/style.css">
                                
                <div id="addtextform">
                <p>Text was just added.</p><BR>
                    <form method="POST">
                        Text: <input type="text" name="text" placeholder="Enter text" required><br>
                        Tags: <input type="text" name="tags" placeholder="Enter the tags (comma-separated)"><br>
                        <input type="submit" value="Submit"><br>
                    </form>
               </div>                       
               '''
    else:
        return '''
                <link rel="stylesheet" type="text/css" href="static/style.css">
                
                <div id="addtextform">
                    <form method="POST">
                        Text: <input type="text" name="text" placeholder="Enter text" required><br>
                        Tags: <input type="text" name="tags" placeholder="Enter the tags (comma-separated)"><br>
                        <input type="submit" value="Submit"><br>
                    </form>
               </div>
               '''
               
               
# if __name__ == '__main__':
#     app.run(debug=True)