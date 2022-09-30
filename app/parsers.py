from flask_restful import reqparse, inputs


event_parser = reqparse.RequestParser()
event_parser.add_argument(
    'date',
    type=inputs.date,
    help="The event date with the correct format is required! The correct format is YYYY-MM-DD!",
    required=True,
)
event_parser.add_argument(
    'event',
    type=str,
    help="The event name is required!",
    required=True,
)

date_parser = reqparse.RequestParser()
date_parser.add_argument(
    'start_time',
    type=inputs.date
)
date_parser.add_argument(
    'end_time',
    type=inputs.date
)