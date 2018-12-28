from flask import Flask, redirect, request

app = Flask(__name__)

@app.route("/subscribe", methods = ['POST'])
def subscribe(links=None):
    print(request.form)
    url = request.form['success_redirect_url']
    return redirect(url, code=302)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)
