import unittest
import json
from flask_testing import TestCase
from .app import create_app, db
from .models import Question


def dict_in(d1, d2):
    all(item in d2.items() for item in d1.items())


class TestQuestionAPI(TestCase):
    def create_app(self):
        return create_app('test_config.json')

    def setUp(self):
        db.drop_all()
        db.create_all()
        self.maxDiff = 1000
        self.populate_db()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def populate_db(self):
        q1 = self.create_question(
            "trees are fun", "balance this tree")
        q2 = self.create_question(
            "trees are not fun", "red black tree")

        db.session.add_all((q1, q2))
        db.session.commit()

    def create_question(self, name, content):
        q = Question()
        q.name = name
        q.content = content
        return q

    def test_all_response(self):
        response = self.client.get('/question')
        questions = json.loads(response.data.decode('utf-8'))
        self.assertEqual(len(questions['questions']), 2)
        expected = {
            "next": None,
            "page": 1,
            "pages": 1,
            "per_page": 20,
            "prev": None,
            "questions": [
                {
                    "answers": [],
                    "categories": [],
                    "content": "balance this tree",
                    "hints": [],
                    "id": 1,
                    "name": "trees are fun"
                },
                {
                    "answers": [],
                    "categories": [],
                    "content": "red black tree",
                    "hints": [],
                    "id": 2,
                    "name": "trees are not fun"
                }
            ]
        }
        self.assertEqual(expected, questions)

    def test_specific_response(self):
        response = self.client.get('/question/1')
        question = json.loads(response.data.decode('utf-8'))
        expected = {
            "answers": [],
            "categories": [],
            "content": "balance this tree",
            "hints": [],
            "id": 1,
            "name": "trees are fun"
        }
        self.assertEqual(expected, question)

        response = self.client.get('/question/2')
        question = json.loads(response.data.decode('utf-8'))
        expected = {
            "answers": [],
            "categories": [],
            "content": "red black tree",
            "hints": [],
            "id": 2,
            "name": "trees are not fun"
        }
        self.assertEqual(expected, question)

    def test_specific_404(self):
        response = self.client.get('/question/100')
        question = json.loads(response.data.decode('utf-8'))
        expected = {
            "message": "Not found."
        }
        self.assertEqual(expected, question)
        self.assertEqual(404, response.status_code)

    def test_post(self):
        response = self.client.post('/question',
                                    data=json.dumps(
                                        dict(name='another graph question?',
                                             content='just make a tree or something',
                                             categories=['graphs'])),
                                    content_type='application/json')
        body = json.loads(response.data.decode('utf-8'))
        expected = {
            'message': 'Created.'
        }
        self.assertEqual(expected, body)
        self.assertEqual(201, response.status_code)
