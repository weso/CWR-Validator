#!/usr/bin/python
import sys
import logging
from cwr_validator import create_app
logging.basicConfig(stream=sys.stderr)

sys.path.insert(0,"/var/www/cwr_validator/")
#os.chdir("/var/www/cwr_validator")

application = create_app()