from flask import Blueprint, Response

renderbp = Blueprint('render',__name__)

import time 

event = ['one','two','three']

@renderbp.route('/render')
def render():
    def eventStream():
        while True:
            # wait for source data to be available, then push it
            if len(event) > 0:
                yield 'data: {}\n\n'.format(event.pop())
    return Response(eventStream(), mimetype="text/event-stream")

