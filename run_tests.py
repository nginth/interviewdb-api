#!/usr/bin/env python3 -W ignore::DeprecationWarning
# Ignore DeprecationWarnings because of some werkzeug package
# that I can't seem to update on MacOS High Sierra.
import unittest
from app.tests import *

if __name__ == '__main__':
    unittest.main()
