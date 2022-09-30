from flask import Flask
from flask_restful import Api
import sys

from app.resources import EventResource, TodayEventResource, IdEventResource
from app.database import db


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'


@app.before_first_request
def create_table():
    db.init_app(app)
    db.create_all()


api.add_resource(EventResource, '/event')
api.add_resource(TodayEventResource, '/event/today')
api.add_resource(IdEventResource, '/event/<int:id>')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run(port=8080)