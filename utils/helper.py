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
from config import CONF
import logging

LOG = logging.getLogger(__name__)


def render(resource, ua):

    content = open(resource).read()

    if "curl" not in str(ua):
        LOG.info("[UA] Request rendering from %s " % str(ua))
        if bool(BeautifulSoup(content, "html.parser").find()):
            return Response(content, mimetype="text/html")

    return content


def isexpired(t1):
    """
    TBD: Define the mode of setting link expired
    """
    print("The expire time is set to: %d\n" % int(CONF.default.expire_time))
    pass
