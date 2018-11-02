from flask import Flask, jsonify, request, Response
from test import validBookObject
import json

app = Flask(__name__)

books = [
  {
    'name': 'How to get money',
    'price': 3000,
    'isbn': 978039400165
  },
  {
    'name': 'The enemy called Average',
    'price': 2500,
    'isbn': 978039400193
  },
]

# Get all books
@app.route('/books')
def get_books():
  return jsonify({'books': books})

# Add book
@app.route('/books', methods=['POST'])
def add_books():
  requests_data = request.get_json()
  if (validBookObject(requests_data)):
    new_book = {
      'name': requests_data["name"],
      'price': requests_data["price"],
      'isbn': requests_data['isbn']
    }
    books.insert(0, new_book)
    response = Response("", 201, mimetype='application/json')
    response.headers['Location'] = "/books/" + str(new_book['isbn'])
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
  return_value = {}
  for book in books:
    if book['isbn'] == isbn:
      return_value = {
        'name': book['name'],
        'price': book['price'],
        'isbn': isbn
      }
  return jsonify(return_value)

# Replace a book detail
@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
  requests_data = request.get_json()
  new_book = {
    'name': requests_data['name'],
    'price': int(requests_data['price']),
    'isbn': isbn
  }
  i = 0
  for book in books:
    if book['isbn'] == isbn:
      print(books[i])
      books[i] = new_book
    i += 1
  response = Response("", status=204)
  return response

# Update book
@app.route('/books/<int:isbn>', methods=['PATCH'])
def modify_book(isbn):
  requests_data = request.get_json()
  update_book = {}
  if ("name" in requests_data):
    update_book['name'] = requests_data['name']
  if ("price" in requests_data):
    update_book['price'] = requests_data['price']
  for book in books:
    if (book['isbn'] == isbn):
      book.update(update_book)
  response = Response("", status=204)
  response.headers['Location'] = "/books/" + str(isbn)
  return response

# Delete a book
@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
  print(isbn)
  i = 0
  for book in books:
    if book['isbn'] == isbn:
      books.pop(i)
      response = Response("", status=204)
      return response
    i += 1
  invalidResponse = {
    "error": "Book with the ISBN number that was provided was not found",
  }
  response = Response(json.dumps(invalidResponse), status=404, mimetype='application/json')
  return response

app.run(port=5000)
