# -*- coding: utf-8 -*-

import requests

r = requests.get('https://api.github.com/repos/vmg/redcarpet/pulls?state=closed')
