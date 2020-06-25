import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    '''This class represents the trivia test case'''

    def setUp(self):
        '''Define test variables and initialize app.'''
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'trivia'
        self.database_path = 'postgres://{}/{}'.format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()
    
    def tearDown(self):
        '''Executed after reach test'''
        pass


    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['categories']), 6)
    
    def test_error_get_categories(self):
        res = self.client().get('/categories/666666')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_questions_paginated(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(data['currentcategory'])
        self.assertTrue(data['total'])
        self.assertTrue(data['questions'])
        self.assertEqual(len(data['questions']), 10)

    def test_error_questions_paginated(self):
        res = self.client().get('/questions?page=10000000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_question(self):
        res = self.client().delete('/questions/14')
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['delete_id'])

    def test_error_delete_question(self):
        res = self.client().delete('/questions/62334')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_post_question(self):
        res = self.client().post('/questions', json={
            'question': 'First human heart transplant operation conducted by Dr. Christiaan Barnard on Louis Washkansky, was conducted in (Date)',
            'answer': '1967',
            'category': 1,
            'difficulty': 4
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(data['question'])

    def test_error_post_question(self):
        res = self.client().post('/questions', json={
            'question': '',
            'answer': '',
            'category': 1,
            'difficulty': 1
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_search_questions(self):
        data_json = {
            'searchTerm': 'Who is the developer?'
        }
        res = self.client().post('/questions/search', json=data_json)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(data['questions'])

    def test_error_search_questions_empty(self):
        res = self.client().post('/questions/search', json={'searchTerm': ''})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)

    def test_error_search_questions_wrong_data(self):
        res = self.client().post('/questions/search',
                                 json={'searchTerm': '123sdkd'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

    def test_get_questions_by_category_id(self):
        res = self.client().get('/categories/{}/questions'.format(2))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['category_id'], 'Art')
        self.assertTrue(data['category_id'])
        self.assertTrue(data['total'])
        self.assertTrue(data['questions'])

    def test_erorr_get_questions_by_category_id(self):
        res = self.client().get('/categories/{}/questions'.format(10))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_all_quizzes(self):
        data_json = {
            'previous_questions': [3, 4, 10, 12, 11, 5],
            'quiz_category': {'type': 'click'}
        }
        res = self.client().post('/quizzes', json=data_json)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['question'])
        self.assertNotEqual(data['question']['id'], 3)
        self.assertNotEqual(data['question']['id'], 12)

    def test_get_quizzes_by_category(self):
        data_json = {
            'previous_questions': [3, 4, 10, 12, 11, 5],
            'quiz_category': {'type': 'Art', 'id': 2}
        }
        res = self.client().post('/quizzes', json=data_json)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['question'])
        self.assertNotEqual(data['question']['id'], 3)
        self.assertNotEqual(data['question']['id'], 12)

    def test_error_quizzes_by_category(self):
        data_json = {
            'previous_questions': [3, 4, 10, 12, 11, 5],
            'quiz_category': None
        }
        res = self.client().post('/quizzes', json=data_json)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == '__main__':
    unittest.main()