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

from oslo_config import cfg


# Register the stanza
opt_default_group = cfg.OptGroup(name='default', \
                                title='Default Options')

opt_database_group = cfg.OptGroup(name='database', \
                                title='Database options')

# Register the options

default_opts = [

    cfg.StrOpt('upload_folder', default='uploads',
            help=('Where store/retrieve files')),
    
    cfg.StrOpt('templates_folder', default='templates',
            help=('Templates\' location')),
    
    cfg.StrOpt('uri', default='http://localhost:5000',
            help=('Endpoint of the flask webserver')),
    
    cfg.BoolOpt('debug', default=False, \
            help=('True enables, False disables debug mode')),

    cfg.IntOpt('expire_time', default=86400, \
            help=('Expiring time of a link')),
    
    cfg.StrOpt('admin_user', default='admin', \
            help=('admin user to manage private resources')),

    cfg.StrOpt('admin_password', default='password', \
            help=('Admin password related to the admin user'))
]

database_opts = [

    cfg.StrOpt('dbname', default='weburl.db',
            help=('The sqlalchemy database name')),

    cfg.StrOpt('sql_engine_prefix', default='sqlite:///',
            help=('Prefix of the connection stub for the db')),
]


CONF = cfg.CONF
CONF(default_config_files=['config/nopaste.conf'])
CONF.register_group(opt_default_group)
CONF.register_opts(default_opts, opt_default_group)

CONF.register_group(opt_database_group)
CONF.register_opts(database_opts, opt_database_group)

CONF.default.host = CONF.default.uri.split(":")[1].split("//")[1]
CONF.default.port = CONF.default.uri.split(":")[2]


#if __name__ == '__main__':
#print(CONF.default.upload_folder)
#print(CONF.default.upload_folder)
#print(CONF.default.uri)
#print(CONF.default.debug)
#print(CONF.database.dbname)
#print(CONF.database.sql_engine_prefix)
