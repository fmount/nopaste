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
import uuid

import os
import sys
import json
import string
from math import floor


class Shorturl(object):
    def __init__(self):
        pass

    # Base62 Encoder and Decoder
    @classmethod
    def toBase62(self, num, b=62):
        if b <= 0 or b > 62:
            print("Exiting")
            return 0
        base = string.digits + string.lowercase + string.uppercase
        r = num % b
        res = base[r]
        q = floor(num / b)
        while q:
            r = q % b
            q = floor(q / b)
            res = base[int(r)] + res
        return res

    @classmethod
    def toBase10(self, msg, b=62):
        basecode = string.digits + string.lowercase + string.uppercase
        limit = len(msg)
        res = 0
        for i in range(0, limit):
            res = b * res + basecode.find(msg[i], 0)
        return res
            

#Make some tests
#for i in range(0, pow(10, 7)):
#   print(Shorturl.toBase62(i))
#h = uuid.uuid4().int
#print(h)
#a = Shorturl.toBase62(h)
#print(Shorturl.toBase10(a))
