from django.db import models

# Database schema:
# books(id, isbn, title, description, (release_year), price_cents, cover, recommended, 
#    publisher_id, private_download_url)
# publishers(id, name, base, phone. email, established)
# topics(id, name)
# book_topics(book_id, topic_id)
# book_contributors(ebook_id, contributor_id)
# contributors(id, name, born, ethnicity, job)


# Create your models here.

class Book(models.Model):
    isbn = models.CharField(max_length=13)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price_cents = models.PositiveIntegerField(null=True) # Free ebooks can exist.
    cover = models.ImageField(upload_to='covers/') # Inherits all attributes and methods from FileField, but also validates that the uploaded object is a valid image.
    release_year = models.PositiveIntegerField(null=False) # Need release year for filter menu

    #Relationships with rest of db
    publisher = models.ForeignKey('Publisher', null=True, on_delete=models.DO_NOTHING)
    author = models.ForeignKey('Author', on_delete=models.DO_NOTHING)
    topics = models.ManyToManyField('Topic')

class Author(models.Model):
    JOB_CHOICES = [
        ("AU", "Author"),
        ("GH", "Ghostwriter"),
        ("TR", "Translator"),
        ("RE", "Researches"),
        ("IL", "Illustrator")
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    born = models.PositiveIntegerField(null=True)
    ethnicity = models.CharField(max_length=255, editable=False, default="Unknown")
    job = models.CharField(max_length=2, choices=JOB_CHOICES, null=True)

class Publisher(models.Model):
    name = models.CharField(max_length=255)

class Topic(models.Model):
    name = models.CharField(max_length=255)


