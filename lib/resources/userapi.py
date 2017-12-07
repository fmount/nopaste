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

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import backref, mapper, relation, sessionmaker
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask import Flask, abort, jsonify, request, url_for
import logging
import json
import sqlite_middleware
from model import User

LOG = logging.getLogger(__name__)



class UserAPI(Resource):


    def get(self, uuid):
        #item = sqlite_middleware._get_object(uuid, Session())
        #if item is not None:
        #    return item._tojson()
        #abort(404)
        pass


    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')
        
        
        if username is None or password is None:
            abort(400)  # missing arguments
       
        engine = create_engine('sqlite:///weburl.db')
        Session = sessionmaker(bind=engine)
        
        print(password)
        if sqlite_middleware._get_user(username, Session()) is not None:
            print(username)
            abort(400)  # existing user

        cur_id = sqlite_middleware._get_last_object(Session(), User)
        user = User(cur_id, username, password)
        
        
        sqlite_middleware._insert_link(user, Session())
        return jsonify("user", user._tojson())


    def delete(self):
        pass
