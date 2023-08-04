from django.db import models

# books(id, isbn, title, description, (release_year), price_cents, cover, (recommended, )
#    publisher_id, private_download_url)
# publishers(id, name, base, phone. email, established)
# topics(id, name)
# book_topics(book_id, topic_id)
# book_contributors(ebook_id, contributor_id)
# contributors(id, name, born, ethnicity, job)

class Book(models.Model):
    isbn = models.CharField(max_length=13)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price_cents = models.PositiveIntegerField()
    cover = models.FileField(upload_to='covers/')

    # Relationships
    publisher = models.ForeignKey('Publisher', null=True, on_delete=models.CASCADE)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    topics = models.ManyToManyField('Topic')

class Author(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

class Publisher(models.Model):
    name = models.CharField(max_length=255)

class Topic(models.Model):
    name = models.CharField(max_length=255)
