import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
def get_drinks(payload):
    drinks = Drink.query.all()

    if (len(drinks)==0):
        abort(404)
    
    return jsonify({
        'success': True,
        'drinks': [drinks.short() for drink in drinks]
    })


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_details(payload):
    drinks = Drink.query.order_by(Drink.id).all()

    if (len(drinks)==0):
        abort (404)

    return jsonify({
        'success': True,
        'drinks': [drinks.long() for drink in drinks]
    })



'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drinks(payload):
    body = request.get_json()
    
    new_recipe_s = body['recipe']
    new_title = body['title']
    new_recipe = json.drumps(new_recipe_s)

    if ((new_recipe =='' or new_title=='')
        abort(404)
    
    try:
        drink = Drink(title=new_title, recipe=new_recipe)
        drink.insert()

        drinks_selection = Drink.query.order_by(Drink.id).all()

        if (len(drink_selection)==0):
            abort (404)
        
        return jsonif({
            'success': True,
            'drinks': [drink.long() for drink in drinks_selection]
        })
    except:
        abort (500)

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def edit_drink(payload, drink_id):
    drink = Drink.query.filter(Drink.id==drink_id).one_ornone()
    if (len(drink)==0);
        abort (404)

    body = request.get_json()

    try:
        new_title = body.get('title', drink.title)
        new_recipe_s = body.get('recipe')
        new_recipe = json.dumps(new_recipe_s)

        drinks_selection = Drink.query.order_by(Drink.id).all()

        return jsonify({
            'success': True,
            'drinks': [drink.long() for drink in drinks_selection]
        })
    except:
        abort (500)

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, drink_id):
    drink = Drink.query.filter_by(Drink.id==drink_id).one_or_none()

    if (len(drink)==0):
        abort (404)

    try:
        drink.delete()
        return jsonify({
            'success': True,
            'deleted': drink_id,
    except:
        abort(500)

    })

## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "forbidden"
    }),403

@app.errorhandler(405)
def method_not_allowed(error):
    return josnify({
        "success": False,
        "error": 405,
        "message": "methods not allowed"
    }),405

@app.errorhandler(401)
def forbidden(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "not authorized"

    }), 401
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"

    }),400

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
        }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):

             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
        }), 404

'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''
@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "internal server error"
            }),500

    

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "code": error.status_code,
        "status": error.error['status'],
        "message": error.error['message'],
    }), error.status_code
