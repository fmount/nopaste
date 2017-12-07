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

from flask import Flask, jsonify, abort, make_response, request
from flask_restful import Api, Resource, reqparse, fields, marshal
from werkzeug import secure_filename, FileStorage
from time import gmtime, strftime
from utils.short_url import Shorturl
from model import Link, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import sqlite_middleware
from config import CONF
from flask_httpauth import HTTPBasicAuth

import logging
import json
import os

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

"""

LOG = logging.getLogger(__name__)
auth = HTTPBasicAuth()

engine = create_engine(CONF.database.sql_engine_prefix + CONF.database.dbname)


class Links(Resource):
 

    # Make an authorization model to print all the links
    # present on the database, else return the helper

    @auth.login_required
    def get(self):
        Session = sessionmaker(bind=engine)
        items = sqlite_middleware._get_all_objects(Session(), Link)
        return jsonify("links", str(items))


    def put(self):
        pass


    def post(self):
        f = request.files['file']
        Session = sessionmaker(bind=engine)
        try:
            cur_id = sqlite_middleware._get_last_object(Session(), Link) + 1
            es = Shorturl.toBase62(cur_id)
            f.save(CONF.default.upload_folder + "/" + secure_filename(es))

            l = Link(cur_id, CONF.default.uri + "/" + secure_filename(es), strftime("%Y-%m-%d %H:%M:%S", gmtime()))
            sqlite_middleware._insert_link(l, Session())
            LOG.info("[POST] - Generating tinyUrl: %s\n" % (CONF.default.uri + es))

            return l._tojson()
        except:
            return "DB Operational Error"

    # Drop the entire db and delete all the created files

    @auth.login_required
    def delete(self):
        Session = sessionmaker(bind=engine)
        sqlite_middleware._clear_table_by_name(Base, Session(), "links")
        filelist = [f for f in os.listdir(CONF.default.upload_folder)]

        for f in filelist:
            LOG.info("[DELETE] - %s" % str(CONF.default.upload_folder + "/" + f))
            os.remove(CONF.default.upload_folder + "/" + f)

        return "Cleaning db.."


    @auth.verify_password
    def verify_password(username, password):
        Session = sessionmaker(bind=engine)
        user = sqlite_middleware._get_user(username, Session())
        if not user or not user.verify_password(password):
            return False
        return True


class LinkAPI(Resource):


    def get(self, uuid):
        Session = sessionmaker(bind=engine)
        item = sqlite_middleware._get_object(uuid, Session())
        if item is not None:
            LOG.info("[GET] - %s\n" % str(item._tojson()))
            return item._tojson()
        abort(404)

    def put(self):
        pass


    @auth.login_required
    def delete(self, uuid):
        Session = sessionmaker(bind=engine)
        link = sqlite_middleware._delete_object(uuid, Session(), Link)
        LOG.info("[DELETE] - %s" % str(CONF.default.upload_folder + "/" + Shorturl.toBase62(uuid)))
        os.remove(CONF.default.upload_folder + "/" + Shorturl.toBase62(uuid))
        return link._tojson()
