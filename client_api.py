import requests
import os, json

server = os.environ["CQPARTS_SERVER"]
api_path = "/api/v0/"


class cqparts_api:
    def __init__(self, verbose=False):
        self.prefix = server + api_path
        self.verbose = verbose

    def req(self, verb, path):
        if path[0] != "/":
            path = "/" + path
        url = self.prefix + verb + path
        if self.verbose:
            print(url)
        response = requests.get(url)
        if response.status_code == 200:
            return json.loads(response.content.decode("utf-8"))
        else:
            return None

    def unbuilt(self):
        return self.req("stat", "unbuilt")

    def built(self):
        return self.req("stat", "built")

    def all(self):
        return self.req("stat", "all")

    def show(self, path):
        return self.req("show", path)

    def showcase(self):
        return self.req("stat", "showcase")
