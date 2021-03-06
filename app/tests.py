import unittest
import json
from flask_testing import TestCase
from .app import create_app, db
from .models import Question, Hint, Category, Answer


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
        self.assertEqual(2, len(Question.query.all()))
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
        self.assertEqual(3, len(Question.query.all()))

    def test_update(self):
        response = self.client.put('/question/1', data=json.dumps(
            dict(content='updated content', name='updated name')), content_type='application/json')
        body = json.loads(response.data.decode('utf-8'))
        expected = {
            'message': 'Updated.',
            'question': {
                "answers": [],
                "categories": [],
                "content": "updated content",
                "hints": [],
                "id": 1,
                "name": "updated name"
            }
        }
        self.assertEqual(expected, body)
        self.assertEqual(200, response.status_code)
        q1 = Question.query.filter(Question.id == 1).first()
        self.assertEqual(q1.content, 'updated content')
        self.assertEqual(q1.name, 'updated name')

    def test_update_fail_id(self):
        response = self.client.put('/question/1', data=json.dumps(
            dict(id=7, name='updated name')), content_type='application/json')
        body = json.loads(response.data.decode('utf-8'))
        expected = {
            'message': 'Cannot update id.'
        }
        self.assertEqual(expected, body)
        self.assertEqual(400, response.status_code)

    def test_update_fail_unimplemented(self):
        for key in ('answers', 'categories', 'hints'):
            response = self.client.put('/question/1',
                                       data=json.dumps(
                                           {key: ['a', 'b'], 'content': 'asdfs'}),
                                       content_type='application/json')
            body = json.loads(response.data.decode('utf-8'))
            expected = {
                'message': 'Update of ' +
                key +
                'not implemented. Use the endpoints respective to ' +
                key +
                ' to perform this operation.'
            }
            self.assertEqual(expected, body)
            self.assertEqual(400, response.status_code)


class TestHintAPI(TestCase):
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
        q1 = Question()
        q1.name = 'question'
        q1.content = 'its a question'

        q2 = Question()
        q2.name = 'question 2'
        q2.content = 'its a question 2'

        h1 = Hint()
        h1.order = 0
        h1.content = 'hint'
        h1.question_id = 1

        db.session.add_all((q1, q2, h1))
        db.session.commit()

        self.preexisting_hints = 1

    def test_post(self):
        self.assertEqual(self.preexisting_hints, len(Hint.query.all()))
        response = self.client.post('/hint',
                                    data=json.dumps(
                                        dict(order=1,
                                             content='use a tree',
                                             questionId=1)),
                                    content_type='application/json')
        body = json.loads(response.data.decode('utf-8'))
        expected = {
            'message': 'Created.'
        }
        self.assertEqual(expected, body)
        self.assertEqual(201, response.status_code)
        self.assertEqual(self.preexisting_hints + 1, len(Hint.query.all()))

    def test_update(self):
        prev_hints = Question.query.filter(Question.id == 2).first().hints
        update = {
            'content': 'updated content',
            'order': 2,
            'questionId': 2
        }
        response = self.client.put(
            '/hint/1', data=json.dumps(update), content_type='application/json')
        body = json.loads(response.data.decode('utf-8'))
        expected = {
            'message': 'Updated.',
            'hint': {
                'content': 'updated content',
                'order': 2,
                'questionId': 2,
                'id': 1
            }
        }
        self.assertEqual(expected, body)
        self.assertEqual(200, response.status_code)
        hint_question = Question.query.filter(Question.id == 2).first()
        self.assertEqual(len(prev_hints) + 1, len(hint_question.hints))


class TestCategoryAPI(TestCase):
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
        q1 = Question()
        q1.name = 'question'
        q1.content = 'its a question'
        db.session.add(q1)

        c1 = self.create_category('trees')
        c2 = self.create_category('recursion')
        db.session.add_all((c1, c2))
        db.session.commit()

        self.preexisting_categories = 2

    def create_category(self, name):
        c = Category()
        c.name = name
        return c

    def test_get_all(self):
        response = self.client.get('/category')
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(
            len(json_response['categories']), self.preexisting_categories)
        expected = {
            "next": None,
            "page": 1,
            "pages": 1,
            "per_page": 20,
            "prev": None,
            "categories": [
                {
                    "name": "trees"
                },
                {
                    "name": "recursion"
                }
            ]
        }
        self.assertEqual(expected, json_response)

    def test_get_specific(self):
        response = self.client.get('/category/trees')
        category = json.loads(response.data.decode('utf-8'))
        expected = {
            "name": "trees"
        }
        self.assertEqual(expected, category)

        response = self.client.get('/category/recursion')
        category = json.loads(response.data.decode('utf-8'))
        expected = {
            "name": "recursion"
        }
        self.assertEqual(expected, category)

    def test_post(self):
        self.assertEqual(self.preexisting_categories,
                         len(Category.query.all()))
        response = self.client.post('/category',
                                    data=json.dumps(dict(name='graphs')),
                                    content_type='application/json')
        body = json.loads(response.data.decode('utf-8'))
        expected = {
            'message': 'Created.'
        }
        self.assertEqual(expected, body)
        self.assertEqual(201, response.status_code)
        self.assertEqual(self.preexisting_categories + 1,
                         len(Category.query.all()))


class TestAnswerAPI(TestCase):
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
        q1 = Question()
        q1.name = 'question'
        q1.content = 'its a question'
        db.session.add(q1)
        db.session.commit()

        self.preexisting_answers = 0

    def test_post(self):
        self.assertEqual(self.preexisting_answers, len(Answer.query.all()))
        response = self.client.post('/answer',
                                    data=json.dumps(
                                        dict(content='this is how you use the tree: return 1 + solve_question(tree)',
                                             questionId=1)),
                                    content_type='application/json')
        body = json.loads(response.data.decode('utf-8'))
        expected = {
            'message': 'Created.'
        }
        self.assertEqual(expected, body)
        self.assertEqual(201, response.status_code)
        self.assertEqual(self.preexisting_answers +
                         1, len(Answer.query.all()))
