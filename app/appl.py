from cachetools import cached
from flask import Flask


@cached({})
def get_app():
    apd = Flask("app")

    return apd
