from flask_restful import fields, marshal_with, Resource, reqparse, inputs
from datetime import date

from database import db, Event
from parsers import event_parser, date_parser


resource_fields = {
    'id': fields.Integer,
    'event': fields.String,
    'date': fields.DateTime(dt_format='iso8601')
}


class EventResource(Resource):
    @staticmethod
    def post():
        data = event_parser.parse_args()
        if "message" in data:
            return data
        db.session.add(Event(event=data['event'], date=data["date"].date()))
        db.session.commit()
        return {
            "message": "The event has been added!",
            "event": data["event"],
            "date": str(data["date"].date())}

    @staticmethod
    @marshal_with(resource_fields)
    def get():
        data = date_parser.parse_args()
        if data['start_time'] is None and data['end_time'] is None:
            return Event.query.all()
        elif data['start_time'] is None:
            return Event.query.filter(Event.date <= data['end_time'].date()).all()
        elif data['end_time'] is None:
            return Event.query.filter(Event.date >= data['start_time'].date()).all()
        return Event.query.filter(Event.date.between(data['start_time'].date(), data['end_time'].date())).all()


class TodayEventResource(Resource):
    @staticmethod
    @marshal_with(resource_fields)
    def get():
        return Event.query.filter(Event.date == date.today()).all()


class IdEventResource(Resource):
    @staticmethod
    @marshal_with(resource_fields)
    def get(id):
        return Event.query.filter_by(id=id).first_or_404(description="The event doesn't exist!")

    @staticmethod
    def delete(id):
        event = Event.query.filter_by(id=id).first_or_404(description="The event doesn't exist!")
        db.session.delete(event)
        db.session.commit()
        return {"message": "The event has been deleted!"}
