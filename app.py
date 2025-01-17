from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', active_page='home')

@app.route('/jak-to-dziala')
def jak_to_dziala():
    return render_template('how-it-works.html', active_page='how-it-works')

@app.route('/analizuj-kod')
def analizuj_kod():
    return render_template('analyze-code.html', active_page='analyze-code')

@app.route('/o-nas')
def o_nas():
    return render_template('about-us.html', active_page='about-us')

if __name__ == '__main__':
    app.run(debug=True)
