from django.db import models
from django.urls import reverse
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
import uuid

#name model
class MyModelName(models.Model):

    my_field_name = models.CharField(max_length=20, help_text = "enter a field document")

    class Meta:
        ordering = ['-my_field_name']

    def get_absolute_url(self):
        return reverse('model-detail-view' , args=[str(self.id)])
    
    def __str__(self):
        return self.my_field_name
    
#genre model
class Genre(models.Model):
    name = models.CharField(
        max_length = 200,
        unique = True,
        help_text = "enter a genre"
    )

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('genre' , args=[str(self.id)])
    
    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name= 'genre_name_case_insensitive_unique',
                violation_error_message = 'genre already exists'
            ),
        ]

#book model
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.RESTRICT, null=True)
    summary = models.TextField(
        max_length=1000, help_text="Enter a brief description of the book")
   
    isbn = models.CharField('ISBN', max_length=13,
                            unique=True,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn'
                                      '">ISBN number</a>')


    genre = models.ManyToManyField(
        Genre, help_text="Select a genre for this book")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

#book instance model
class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f'{self.id} ({self.book.title})'
    
    #author model
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

