from flask import Blueprint, Response

renderbp = Blueprint("render", __name__)

import json, time

event = []


@renderbp.route("/render")
def render():
    def eventStream():
        while True:
            # wait for source data to be available, then push it
            if len(event) > 0:
                yield event.pop(0)
            else:
                time.sleep(1)

    return Response(eventStream(), mimetype="text/event-stream")


# get posted image
@renderbp.route("/image", methods=["POST"])
def image():
    pass


# get zipped gltf
@renderbp.route("/zipped/<modelname>")
def zipped(modelname):
    return
