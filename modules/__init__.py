from flask import Flask


app = Flask(__name__)


from modules import *
from .api import *
