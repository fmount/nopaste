#!/usr/bin/env python

# -*- coding: utf-8 -*-

############################################################################
#
#       Licensed under the MIT License (the "License"); you may not use this file
#       except in compliance with the License.  You may obtain a copy of the License
#       in the LICENSE file or at
#
#       https://opensource.org/licenses/MIT
#
#       Unless required by applicable law or agreed to in writing, software
#       distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#       WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#       See the License for the specific language governing permissions and
#       limitations under the License.
#
#       author: fmount <fmount9@autistici.org>
#       version: 0.1
#       company: --
#
#############################################################################

from flask import Flask, Response, jsonify, abort, render_template, make_response, request
from flask_restful import Api, Resource, reqparse, fields, marshal
import logging
import os
import sqlite_middleware
from lib.resources.linksapi import Links, LinkAPI
from model import Link, User, Base
from lib.resources.userapi import UsersAPI, UserAPI
import jinja2
import json
import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils.short_url import Shorturl
from utils import helper
from config import CONF

"""
Datamodel is made like this:

    links: [
    {
        id: [ID],
        url: [URL],
        timestamp: [timestamp]
    },
    {
        id: [ID],
        url: [URL],
        timestamp: [timestamp]
    } ]

The main flask resource is implemented on the linksv2 and remaind to
the more generic model called Link (you can find it on the model.py)

"""

LOG = logging.getLogger(__name__)
#logging.basicConfig(filename='/tmp/nopaste.log', level=logging.DEBUG)

app = Flask(__name__, static_folder=CONF.default.upload_folder, static_url_path="")
api = Api(app)


my_loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader(CONF.default.templates_folder),
])

app.jinja_loader = my_loader
engine = sqlite_middleware._init_engine(Base)


@app.errorhandler(400)
def bad_request(error):
    LOG.warn(jsonify({'error': 'Bad request'}))
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    LOG.warn(jsonify({'error': 'Not found'}))
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/', methods=['GET'])
def home():
    LOG.info("request for home.html")
    return make_response(render_template('home.html'))


@app.route('/<url>')
def show_me_thefile(url):
    identifier = Shorturl.toBase10(url)
    LOG.info("Resolved identifier: %s\n" % str(identifier))
    
    Session = sessionmaker(bind=engine)
    if sqlite_middleware._get_object(identifier, Session(), Link) is None or not \
            os.path.exists(CONF.default.upload_folder + "/" + url) or \
            helper.is_expired(sqlite_middleware._get_object(\
                identifier, Session(), Link).timestamp, CONF.default.expire_time):
        abort(404)

    LOG.info("[Rendering] %s\n" % str(CONF.default.upload_folder + "/" + url))
    return helper.render((CONF.default.upload_folder + "/" + url), request.user_agent)


api.add_resource(Links, "/api/links")
api.add_resource(LinkAPI, "/api/link/<int:uuid>", endpoint="link")
api.add_resource(UsersAPI, "/api/users")
api.add_resource(UserAPI, "/api/user/<int:uuid>", endpoint="user")


def run():
    app.run(host='127.0.0.1', debug=CONF.default.debug)


if __name__ == '__main__':
    run()
