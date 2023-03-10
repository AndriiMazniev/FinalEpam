from flask import Flask

app = Flask(__name__)
app.config.from_object('application.config.DebugConfig')
# app.config.from_object('application.config.TestingConfig')

from application import routes


