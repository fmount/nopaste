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
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, mapper, relation, sessionmaker
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask import Flask, abort, jsonify
from passlib.apps import custom_app_context as pwd_context
from config import CONF
import logging
import json
import sqlite_middleware

Base = declarative_base()

LOG = logging.getLogger(__name__)


class Link(Base):

    __tablename__ = "links"

    uuid = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    url = Column(String)
    timestamp = Column(String)


    def __init__(self, uuid, url, timestamp):
        self.uuid = uuid
        self.url = url
        self.timestamp = timestamp


    def __repr__(self):
        return str(dict({"uuid": self.uuid, "url": self.url, "timestamp": self.timestamp}))


    def __str__(self):
        return str({"uuid": self.uuid, "url": self.url, "timestamp": self.timestamp})


    def _tojson(self):
        return jsonify("link", dict({"uuid": self.uuid, "url": self.url, "timestamp": self.timestamp}))


class User(Base):

    __tablename__ = "users"

    uuid = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String(32), index=True)
    password_hash = Column(String(128))

    def __init__(self, uuid, username, password):
        self.uuid = uuid
        self.username = username
        self.password_hash = self.hash_password(password)


    def hash_password(self, password):
        return pwd_context.encrypt(password)


    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)


    def isadmin(self):
        if self.username == CONF.default.admin_user and \
                self.verify_password(CONF.default.admin_password):
            return True
        return False


    def __repr__(self):
        pass


    def __str__(self):
        pass


    def _tojson(self):
        return dict({"uuid": self.uuid, "name": self.username})
