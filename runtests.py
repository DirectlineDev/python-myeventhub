# -*- coding: utf-8 -*-

import os
from six import print_


# test environment variables
for k in os.environ.keys():
    print_(k)
