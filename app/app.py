from flask import Flask, render_template
import os
app = Flask(__name__)

@app.route('/')
def hello_world():  # put application's code here
    return render_template('project.html')

if __name__ == '__main__':
    app.run()
