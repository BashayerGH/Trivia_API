import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  db = setup_db(app)
  
  # Set up CORS. Allow '*' for origins.
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


  # Use the after_request decorator to set Access-Control-Allow
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response

  # Create an endpoint to handle GET requests for all available categories
  @app.route('/categories')
  def Get_categories():
    categories = [category.format() for category in Category.query.all()]
    
    if len(categories) == 0:
      abort(404)
    else:
      return jsonify({
        "categories": categories,
        "success": True
        })


  # Create an endpoint to handle GET requests for questions, 
  # including pagination (every 10 questions). 
  # This endpoint should return a list of questions, 
  # number of total questions, current category, categories. 

  @app.route('/questions')
  def Get_questions():
    try:
        questions = Question.query.order_by(Question.id).all()
        total_questions = len(questions)
        categories = [category.format() for category in Category.query.all()]
        

        # pagination
        page = request.args.get('page', 1, type=int)
        start =  (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions  = [question.format() for question in questions]
        questions  = questions [start:end]
        current_category = questions[0]['category']

        return jsonify({
            'questions': questions,
            'total': total_questions,
            'categories': categories,
            'currentcategory': current_category,
            'success': True,
        })

    except Exception:
      if len(questions) == 0:
            abort(404)
      else:
        abort(422)


  # Create an endpoint to DELETE question using a question ID
  @app.route('/questions/<int:id>', methods=['DELETE'])
  def Remove_question(id):
        try:
          question = Question.query.filter(Question.id == id).one_or_none()
          if question is None:
            abort(404)
          else:
            question.delete()
            return jsonify({
              'delete_id': id,
              'success': True
              })
        except Exception:
          abort(422)


  # Create an endpoint to POST a new question, 
  # which will require the question and answer text, 
  # category, and difficulty score.

  @app.route('/questions', methods=['POST'])
  def Post_question():

        try:
            data = request.json
            category = int(data['category'])
            difficulty = int(data['difficulty'])
            question = data['question']
            answer = data['answer']

            if (question == '' or answer == ''):
              abort(422)

            Question(question=question, answer=answer,difficulty=difficulty,category=category).insert()
            return jsonify({
              'question': question,
              'answer': answer,
              'difficulty': difficulty,
              'category': category,
              'success': True     
            })

        except Exception:
            abort(422)


  # Create a POST endpoint to get questions based on a search term. 
  # It should return any questions for whom the search term 
  # is a substring of the question. 

  @app.route('/questions/search', methods=['POST'])
  def Search():
        data = request.json
        key = data['searchTerm']
        if (key == ''):
          abort(404)
        else:
          data = Question.query.filter(Question.question.ilike('%{}%'.format(key))).all()


          try:
            questions = [i.format() for i in data]
            total = len(questions)
            category = questions[0]['category']
            return jsonify({
                'questions': questions,
                'total': total,
                'currentcategory': category,
                'success': True
                })
          except Exception:
            abort(422)


  # Create a GET endpoint to get questions based on category

  @app.route('/categories/<int:category>/questions')
  def Get_questions_by_category_id(category):
      data = Question.query.filter(Question.category == category).all()
      questions = [i.format() for i in data]
      total = len(questions)

      if total == 0:
        abort(404)

      else:
        return jsonify({
          'questions': questions,
          'total': total,
          'category_id': category,
          'success': True
          })

   # Create a POST endpoint to get questions to play the quiz. 
   # This endpoint should take category and previous question parameters 
   # and return a random questions within the given category, 
   # if provided, and that is not one of the previous questions

  @app.route('/quizzes', methods=['POST'])
  def Post_quizzes():
        try:
            searched_data = request.get_json()

            if ("click" == searched_data['quiz_category']):
                questions = Question.query.order_by(Question.id).all()
            else :
                questions = Question.query.filter_by(category=searched_data['quiz_category']['id']).filter(
                            Question.id.notin_(searched_data['previous_questions'])).all()
            
          
            question_length = len(questions)
            if question_length > 0:
                return jsonify({
                    'success': True,
                    'question': Question.format(
                        questions[random.randrange(0, question_length)]
                    )
                })
            else:
              abort(404)
        except:
            abort(422)



  # Create error handlers for all expected errors 404 and 422
  @app.errorhandler(404)
  def not_found(error):
        return (
            jsonify({
              'error': 404,
              'message': 'resource not found',
              'success': False }),
            404,
        )

  @app.errorhandler(422)
  def unprocessable(error):
      return (
            jsonify({
              'error': 422,
              'message': 'unprocessable',
              'success': False }),
            422,
        )
  
  return app

    