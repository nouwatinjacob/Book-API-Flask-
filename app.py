from flask import Flask, jsonify, request, Response
from BookModel import *
from test import validBookObject
import json
from settings import *

# Get all books
@app.route('/books')
def get_books():
  return jsonify({'books': Book.get_all_books()})

# Add book
@app.route('/books', methods=['POST'])
def add_books():
  requests_data = request.get_json()
  if (validBookObject(requests_data)):
    Book.add_book(requests_data['name'], requests_data['price'], requests_data['isbn'])
    response = Response("", 201, mimetype='application/json')
    response.headers['Location'] = "/books/" + str(requests_data['isbn'])
    return response
  else:
    invalidResponse = {
      "error": "Invalid book object passed in request",
      "helpString": "Data passed in similar to this {'name': 'bookname', 'price': 1000, 'isbn': 99808089878}"
    }
    response = Response(json.dumps(invalidResponse), status=400, mimetype='application/json')
    return response

# get a book by isbn
@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
  return_value = Book.get_book(isbn)
  return jsonify(return_value)

# Replace a book detail
@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
  requests_data = request.get_json()
  Book.replace_book(isbn, requests_data['name'], requests_data['price'])
  response = Response("", status=204)
  return response

# Update book
@app.route('/books/<int:isbn>', methods=['PATCH'])
def modify_book(isbn):
  requests_data = request.get_json()
  if ("name" in requests_data):
    Book.update_book_name(isbn, requests_data['name'])
  if ("price" in requests_data):
    Book.update_book_price(isbn, requests_data['price'])
  response = Response("", status=204)
  response.headers['Location'] = "/books/" + str(isbn)
  return response

# Delete a book
@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
  if (Book.delete_book(isbn)):
    response = Response("", status=204)
    return response
  invalidResponse = {
    "error": "Book with the ISBN number that was provided was not found",
  }
  response = Response(json.dumps(invalidResponse), status=404, mimetype='application/json')
  return response

app.run(port=5000)
