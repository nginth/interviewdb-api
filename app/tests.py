import unittest
import json
from flask_testing import TestCase
from app.app import create_app


class TestQuestionAPI(TestCase):
    def create_app(self):
        return create_app('test_config.json')

    def test_fail(self):
        assert False
