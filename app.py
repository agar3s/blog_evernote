from flask import Flask, render_template, url_for

from evernote.api.client import EvernoteClient

#put your development token below
dev_token = "your development token"

client = EvernoteClient(token=dev_token)
user_store = client.get_user_store()

app = Flask(__name__)

@app.route("/")
def index():
    user = user_store.getUser()
    return render_template('index.html', user=user.username)

if __name__ == "__main__":
    app.debug = True
    app.run()