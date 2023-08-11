from django.core.management.base import BaseCommand

from django.core.files.images import ImageFile
from django.db import transaction
from store.models import *

from xml.etree import ElementTree
from urllib.request import urlopen
import random
import logging
import json
import io
import os

GOOGLE_BOOKS_API_KEY = os.environ.get('GOOGLE_BOOKS_API_KEY') or ""

logging.getLogger().setLevel(logging.INFO)
# Import single book by id
def import_book(book_id):
    book_data = retrieve_google_book_data(book_id)
    import_book_data(book_id, book_data)
    # print(f'Imported book {book_data["title"]}')

def get_book_ids_from_xml(xml_file):
    tree = ElementTree.parse(xml_file)
    book_ids = [elem.text for elem in tree.iterfind('books/book/id')]
    return book_ids

# Safe access to nested dictionary values, similar to ruby's Hash#dig
# https://ruby-doc.org/core-3.1.1/Hash.html#method-i-dig
def dig(self, *keys):
    try:
        for key in keys:
            self = self[key]
        return self
    except:
        return None

# Retrieve book data for book id from Google Books API
def retrieve_google_book_data(book_id):
    response = urlopen(f'https://www.googleapis.com/books/v1/volumes/{book_id}?key={GOOGLE_BOOKS_API_KEY}')
    if response.code == 200:
        response_data = json.loads(response.read())
        return {
            'isbn': dig(response_data, 'volumeInfo', 'industryIdentifiers', 0, 'identifier'),
            'title': dig(response_data, 'volumeInfo', 'title'),
            'description': dig(response_data, 'volumeInfo', 'description'),
            'price': dig(response_data, 'saleInfo', 'retailPrice', 'amount'),
            'cover_url': dig(response_data, 'volumeInfo', 'imageLinks', 'small'),
            'release_date': dig(response_data, 'volumeInfo', 'publishedDate'),
            'author_name': dig(response_data, 'volumeInfo', 'authors', 0),
            'publisher_name': dig(response_data, 'volumeInfo', 'publisher'),
            'categories': dig(response_data, 'volumeInfo', 'categories'),
        }
    else:
        logging.error(f'Error retrieving book {book_id}: {response.code}')

# Download cover image from url and return image bytes
def cover_file(cover_url, filename):
    if cover_url is None:
        logging.warn("No cover url for book")
        return None

    response = urlopen(cover_url)
    if response.code == 200:
        cover_file_bytes = io.BytesIO(response.read())
        return ImageFile(cover_file_bytes, name=f'{filename}.jpg')
    else:
        logging.error(f'Error ({response.code}) retrieving cover from {cover_url}')
        return None

def author_split_name(author_name):
    if ' ' in author_name:
        return list(reversed(author_name.rsplit(" ", 1)))
    else:
        return author_name, ""

# Convert google books categories to topic names
def topic_names(categories):
    topic_names = set()
    for category in categories:
        for topic_name in category.split('/'):
            topic_names.add(topic_name.strip())
    return topic_names

# Save book and related models to database
@transaction.atomic
def import_book_data(book_id, book_data):
    logging.info(f'Importing book {book_id}: {book_data["title"]}')

    if book_data['author_name']:
        last_name, first_name = author_split_name(book_data['author_name'])
        author, _ = Author.objects.get_or_create(
            first_name=first_name,
            last_name=last_name,
        )
    else:
        author = None

    if book_data['publisher_name']:
        publisher, _ = Publisher.objects.get_or_create(
            name=book_data['publisher_name'],
        )
    else:
        publisher = None

    book = Book(
        isbn=book_data['isbn'],
        title=book_data['title'],
        description=book_data['description'] or "",
        price_cents=int(book_data['price'] * 100) if book_data['price'] else random.randint(100, 1000),
        cover=cover_file(book_data['cover_url'], filename=book_data["isbn"]),
        release_year=int(book_data['release_date'][:4]) if book_data['release_date'] else None,
        publisher=publisher,
        author=author,
    )

    book.save()

    if book_data['categories']:
        for name in topic_names(book_data['categories']):
            topic, _ = Topic.objects.get_or_create(name=name)
            book.topics.add(topic)

class Command(BaseCommand):
    help = 'Import books from Google Books XML files'

    def add_arguments(self, parser):
        parser.add_argument("book_id", nargs="*", help="Google Books ID to import")
        parser.add_argument( "--xml", nargs="*", default=[], help="Path to exported Google Books xml")

    def handle(self, *args, **options):
        book_ids = set(options['book_id'])

        for xml_filename in options['xml']:
            with open(xml_filename, 'r') as xml_file:
                book_ids.update(get_book_ids_from_xml(xml_file))

        for book_id in book_ids:
            import_book(book_id)
