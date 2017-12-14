import unittest
import json
from flask_testing import TestCase
from .app import create_app, db
from .models import Question


class TestQuestionAPI(TestCase):
    def create_app(self):
        return create_app('test_config.json')

    def setUp(self):
        db.drop_all()
        db.create_all()
        self.populate_db()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def populate_db(self):
        q1 = self.create_question(
            "trees are fun", "balance this tree", "recursion")
        q2 = self.create_question(
            "trees are not fun", "red black tree", "hard work")

        db.session.add_all((q1, q2))
        db.session.commit()

    def create_question(self, name, content, answer=None):
        q = Question()
        q.name = name
        q.content = content
        q.answer = answer
        return q

    def test_fail(self):
        assert False
