from flask import Flask, render_template 


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    return render_template('login.html')

@app.route('/iregister', methods=['GET','POST'])
def iregister():
    return render_template('iregister.html')

@app.route('/sregister', methods=['GET','POST'])
def sregister():
    return render_template('sregister.html')







if __name__ == "__main__":
    app.run()