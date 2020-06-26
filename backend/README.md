# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### Pipenv Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
$pip install pipenv
$pipenv install
```

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## API Endpoints

Endpoints
- GET '/categories'
- GET '/questions'
- POST '/questions'
- DELETE '/question'
- POST '/questions/search'
- GET '/categories/<int:category>/questions'
- POST '/quizzed'



### GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a two keys, a success flag, and categories object that contains an integer category id, and a single value, a category type.
- Example:
{
  "categories": [
    {
      "id": 1, 
      "type": "Science"
    }, 
    {
      "id": 2, 
      "type": "Art"
    }, 
    {
      "id": 3, 
      "type": "Geography"
    }, 
    {
      "id": 4, 
      "type": "History"
    }, 
    {
      "id": 5, 
      "type": "Entertainment"
    }, 
    {
      "id": 6, 
      "type": "Sports"
    }
  ], 
  "success": true
}
 

### GET '/questions'
- Fetches a dictionary of questions which includes a slice of questions which are shown in one page, the total number of questions, the current category and all the categories.
- Request Arguments: int page (optional, 10 questions per page).
- Returns: An object with five keys, a success flag, questions, the total number of questions,the current category and all the categories.
- Example:
{
  "categories": [
    {
      "id": 1, 
      "type": "Science"
    }, 
    {
      "id": 2, 
      "type": "Art"
    }, 
    {
      "id": 3, 
      "type": "Geography"
    }, 
    {
      "id": 4, 
      "type": "History"
    }, 
    {
      "id": 5, 
      "type": "Entertainment"
    }, 
    {
      "id": 6, 
      "type": "Sports"
    }
  ], 
  "currentcategory": 5, 
  "questions": [
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }, 
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }
  ], 
  "success": true, 
  "total": 20
}



### POST '/questions'
- Post a dictionary of a question to create a new question entry.
- Request Arguments: An object with four keys, a question text, an answer text, a category id and a difficulty score.
- Returns: An object with six keys, which corresponds to the newly created question with a success flag and id.
- Example:
{
    "success" : true,
    '"d" : 5,
    "question" : "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?",
    "answer" : "Escher",
    "category" : 1,
    "difficulty" : 3
}

### DELETE '/questions/<int:question_id>'
- Delete a question specified given id.
- Request Arguments: None
- Returns: An object with two keys, which are a success flag and the deleted question id.
- Example:
{
    'success' : true,
    'delete_id' : 4,
}


### POST '/questions/search'
- Fetches questions which includes the given search term as a substring.
- Request Arguments: 
{
    'search_term': search term string
}
- Returns: An object with four keys, a success flag, questions, total, currentcategory.
- Example:
{
    "currentcategory": 1
    "questions": [
        {
        answer: "Bashayer",
        category: 1,
        difficulty: 3,
        id: 26,
        question: "Who is the developer?"
        }
    ]
    "success": true
    "total": 1
}

### GET '/categories/<int:category>/questions'
- Fetches questions which have the given category id.
- Request Arguments: None
- Returns: An object with four keys, which are a success flag, questions, total, category_id.
- Example:
{
  "category_id": 4, 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Scarab", 
      "category": 4, 
      "difficulty": 4, 
      "id": 23, 
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }
  ], 
  "success": true, 
  "total": 4
}

### POST '/quizzes'
- Fetches questions to play the quiz, which are fetched one by one from the questions specified by the given category id.
- Request Arguments: 
{
     "previous_questions": questions which are previously shown,
     "quiz_category": category object (type and id) which specifies the whole quiz set
}
- Returns: An object with two keys, success, question.
- Example:
{
    "question": 
    {
        "answer": "Blood",
        "category": 1,
        "difficulty": 4,
        "id": 22,
        "question": "Hematology is a branch of medicine involving the study of what?"
    }
    "success": true
}


## Testing
To run the tests, run
```
dropdb trivia
createdb trivia
psql trivia < trivia.psql
python test_flaskr.py
```
