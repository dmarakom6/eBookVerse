# Google books importer

CLI tool to import books from Google Books into the eBookVerse store. It can:
- fetch book metadata and save it to the database
- download book covers

## Using an api key

The importer can be used without an api key, but to avoid getting rate-limited by google it is advisable to create a [Google Books API Key](https://console.cloud.google.com/marketplace/product/google/books.googleapis.com).

The importer looks for an api key to use in environment variable `GOOGLE_BOOKS_API_KEY`. To set the environment variable, run:

```bash
export GOOGLE_BOOKS_API_KEY=yourkeyhere
```

## Import books one by one

1. Find the book you want to import on [Google Books](https://books.google.com/).
2. Copy the book's id from the url, e.g. [https://www.google.gr/books/edition/The_Pragmatic_Programmer/**5wBQEp6ruIAC**](https://www.google.gr/books/edition/The_Pragmatic_Programmer/5wBQEp6ruIAC)
3. Run the importer with the book id as an argument:

```bash
python manage.py importgooglebooks 5wBQEp6ruIAC
```

## Bulk import books from a Google Books shelf

1. Go to [Google Books](https://books.google.com/). Sign in with your account.
2. Go to [My Library](https://books.google.com/books) and create a new shelf.
3. Start adding books to the shelf.
4. Export the shelf to an XML file, e.g. `google_books_library_shelf.xml`
5. Import the shelf's books into ebookverse by running

```bash
python manage.py importgooglebooks --xml path/to/google_books_library_shelf.xml
```

The command accepts multiple arguments in any combination, e.g.

```bash
python manage.py importgooglebooks book_id_1 book_id_2 --xml file1.xml file2.xml
```
