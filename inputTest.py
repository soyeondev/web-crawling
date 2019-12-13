from flask import Flask, render_template, redirect, request, url_for, json

app = Flask(__name__)
 

@app.route("/hello")
def test():
    return render_template('hello.html')

if __name__ == '__main__':
    app.run()
