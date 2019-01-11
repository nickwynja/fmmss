from flask import Flask, redirect, request
from mailmanclient import Client


app = Flask(__name__)

@app.route("/")
def index():
    # For site uptime checks
    return ('', 200)

@app.route("/1.0/subscribe", methods = ['POST'])
def subscribe():
    lists = []
    for r in request.form:
        if r.startswith('list-'):
            lists.append(request.form[r])
    email = request.form['email']
    name = request.form['name']
    success_url = request.form['success_redirect_url']
    error_url = request.form['error_redirect_url']

    client = Client('http://172.22.199.2:8001/3.1', 'restadmin', 'restpass')

    for l in lists:
        try:
            list = client.get_list(l)
            user = list.get_member(email)
            return redirect(success_url, code=302)
        except:
            # not a user
            try:
                # http://docs.mailman3.org/projects/mailmanclient/en/3.1.0/apiref.html#mailmanclient._client.MailingList.subscribe
                list.subscribe(email, name, True, True, True)
                return redirect(success_url, code=302)
            except:
                return redirect(error_url, code=302)
            return redirect(error_url, code=302)


@app.route("/1.0/unsubscribe", methods = ['POST'])
def unsubscribe():
    email = request.form['email']
    l = request.form['list']
    success_url = request.form['success_redirect_url']
    error_url = request.form['error_redirect_url']

    client = Client('http://172.22.199.2:8001/3.1', 'restadmin', 'restpass')
    list = client.get_list(l)

    try:
        list.unsubscribe(email)
        return redirect(success_url, code=302)
    except:
        return redirect(error_url, code=302)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)
