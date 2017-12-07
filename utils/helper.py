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

from flask import render_template, make_response, Response
from bs4 import BeautifulSoup
from datetime import datetime as dt, timedelta
import logging

LOG = logging.getLogger(__name__)


def render(resource, ua):

    content = open(resource).read()

    if "curl" not in str(ua):
        LOG.info("[UA] Request rendering from %s " % str(ua))
        if bool(BeautifulSoup(content, "html.parser").find()):
            return Response(content, mimetype="text/html")

    return content


def is_expired(t1, expire_time):
    """
    Define the mode of setting link expired
    """
    LOG.info("Timedelta seconds: %d\n" % int(expire_time))
    now = dt.now()
    link_dt = dt.strptime(t1, "%Y-%m-%d %H:%M:%S")

    if abs(now - link_dt) > timedelta(seconds=expire_time):
        LOG.info("[EXPIRED] - TRUE")
        return True

    LOG.info("[EXPIRED] - FALSE")
    return False


# JUST FOR TEST PURPOSES ...
#print(is_expired("2017-12-01 20:32:00", 86400))
#print(is_expired("2017-12-06 15:32:00", 86400))
#print(is_expired("2017-12-07 20:32:00", 86400))
#print(is_expired("2017-12-05 20:32:00", 86400))
