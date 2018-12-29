from flask import Flask, redirect, request
from mailmanclient import Client


app = Flask(__name__)

@app.route("/subscribe", methods = ['POST'])
def subscribe():
    email = request.form['email']
    l = request.form['list_name']
    name = request.form['name']
    success_url = request.form['success_redirect_url']
    error_url = request.form['error_redirect_url']

    client = Client('http://172.22.199.2:8001/3.1', 'restadmin', 'restpass')
    list = client.get_list(l)

    try:
        user = list.get_member(email)
        return redirect(success_url, code=302)
    except:
        # not a user
        try:
            # http://docs.mailman3.org/projects/mailmanclient/en/3.1.0/apiref.html#mailmanclient._client.MailingList.subscribe
            list.subscribe(email, name, True, True, True)
            return redirect(success_url, code=302)
        except:
            print('error subscribing')
            return redirect(error_url, code=302)

@app.route("/unsubscribe", methods = ['POST'])
def unsubscribe():
    email = request.form['email']
    l = request.form['list_name']
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
