# coding: utf8
#!/usr/bin/env python

from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://tipi:r2d2@localhost/geo_data'

import findahouse.views
