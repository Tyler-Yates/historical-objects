import logging
import os

from flask import Flask, render_template, request, redirect

from data_loader import load_data

application = Flask(__name__)

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

# Load data for objects
application.medals = {}
application.books = {}
application.plates = {}
load_data(application)

DEV_MODE = False
if os.environ.get('DEV') == '1':
    DEV_MODE = True
    print("Running in dev mode")


@application.before_request
def before_request():
    if DEV_MODE:
        return

    if request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)


@application.route('/debug')
def debug_page():
    problematic_medals = {}
    for medal in application.medals.values():
        if medal.sort_year == -1:
            problematic_medals[medal.id] = 'No sort_year'

    problematic_books = {}
    for book in application.books.values():
        if book.sort_year == -1:
            problematic_books[book.id] = 'No sort_year'

    problematic_plates = {}
    for plate in application.plates.values():
        if plate.sort_year == -1:
            problematic_plates[plate.id] = 'No sort_year'

    return render_template('debug.html',
                           medals=application.medals,
                           problematic_medals=problematic_medals,
                           books=application.books,
                           problematic_books=problematic_books,
                           plates=application.plates,
                           problematic_plates=problematic_plates)


@application.route('/')
def home_page():
    return render_template('index.html')


@application.route('/medals')
def medals_page():
    return render_template('medals.html', medals=application.medals.values())


@application.route('/medals/<medal_id>')
def medal_page(medal_id):
    return render_template('medal.html', medal=application.medals[medal_id])


@application.route('/books')
def books_page():
    return render_template('books.html', books=application.books.values())


@application.route('/books/<book_id>')
def book_page(book_id):
    book = application.books[book_id]
    return render_template('book.html', book=book, gallery=book.gallery_images)


@application.route('/plates')
def plates_page():
    return render_template('plates.html', plates=application.plates.values())


@application.route('/plates/<plate_id>')
def plate_page(plate_id):
    return render_template('plate.html', plate=application.plates[plate_id])


@application.route('/references')
def references_page():
    return render_template('references.html')


@application.route('/about')
def about_page():
    return render_template('about.html')


if __name__ == '__main__':
    if DEV_MODE:
        application.run(ssl_context='adhoc')
    else:
        application.run()
