from django.db import models

from decimal import Decimal

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
    release_year = models.PositiveIntegerField(null=True) # Need release year for filter menu

    #Relationships with rest of db
    publisher = models.ForeignKey('Publisher', null=True, on_delete=models.DO_NOTHING)
    author = models.ForeignKey('Author', on_delete=models.DO_NOTHING)
    topics = models.ManyToManyField('Topic')

    def price(self):
        # return f"€{'{:,.2f}'.format(self.price_cents/100)}"
        return Decimal(self.price_cents) / Decimal(100)

    def price_with_currency(self):
        return f"€{self.price()}"

class Author(models.Model):
    class JobChoices(models.TextChoices):
        AUTHOR = "AU", "Author"
        GHOSTWRITER = "GH", "Ghostwriter"
        TRANSLATOR = "TR", "Translator"
        RESEARCHER = "RE", "Researcher"
        ILLUSTRATOR = "IL", "Illustrator"

    def name(self):
        return f"{self.first_name} {self.last_name}"

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    born = models.PositiveIntegerField(null=True)
    ethnicity = models.CharField(max_length=255, editable=False, default="Unknown")
    job = models.CharField(max_length=2, choices=JobChoices.choices, null=False, default=JobChoices.AUTHOR)

class Publisher(models.Model):
    name = models.CharField(max_length=255)

class Topic(models.Model):
    name = models.CharField(max_length=255)

class Cart(models.Model):
    items = models.ManyToManyField('Book')

    def __len__(self):
        if self.id:
            return self.items.count()
        else:
            return 0

    def __iter__(self):
        if self.id:
            return iter(self.items.all())
        else:
            return iter([])

    def isempty(self):
            return len(self) == 0

    def price(self):
        return sum([item.price() for item in self])


    def price_with_currency(self):
        return f"€{self.price()}"
