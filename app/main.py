from flask import Flask, redirect, request, abort
from mailmanclient import Client
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

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

    # First, check honeypot for bot activity
  #  abort(404)
    if 'bottle_of_mead' in request.form and request.form['bottle_of_mead'] is not "":
        app.logger.error('SPAM from %s' % email)
        return redirect(error_url, code=302)

    client = Client('http://172.22.199.2:8001/3.1', 'restadmin', 'restpass')

    for l in lists:
        try:
            list = client.get_list(l)
            user = list.get_member(email)
            app.logger.info('Successfully registered %s' % email)
            return redirect(success_url, code=302)
        except:
            # not a user
            try:
                # http://docs.mailman3.org/projects/mailmanclient/en/3.1.0/apiref.html#mailmanclient._client.MailingList.subscribe
                sub_policy = list.settings['subscription_policy']
                if sub_policy == "open":
                    list.subscribe(email, name, True, True)
                else:
                    list.subscribe(email, name)

                app.logger.info('Successfully registered %s' % email)
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
