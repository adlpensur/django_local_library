from django.db import models
from datetime import date

# Create your models here.
class Genre(models.Model):
    """
    Modelo que representa un género literario (p. ej. ciencia ficción, poesía, etc.).
    """
    name = models.CharField(max_length=200, help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)")
    
    def __str__(self):
        """
        Cadena que representa a la instancia particular del modelo (p. ej en el sitio de Administración)
        """
        return self.name

from django.urls import reverse #Used to generate URLs by reversing the URL patterns

class Book(models.Model):
    """
    Modelo que representa un libro (pero no un Ejemplar específico).
    """

    title = models.CharField(max_length=200)

    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    # ForeignKey, ya que un libro tiene un solo autor, pero el mismo autor puede haber escrito muchos libros.
    # 'Author' es un string, en vez de un objeto, porque la clase Author aún no ha sido declarada.

    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    
    isbn = models.CharField('ISBN',max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    # ManyToManyField, porque un género puede contener muchos libros y un libro puede cubrir varios géneros.
    # La clase Genre ya ha sido definida, entonces podemos especificar el objeto arriba.
    
    def __str__(self):
        """
        String que representa al objeto Book
        """
        return self.title
    
    
    def get_absolute_url(self):
        """
        Devuelve el URL a una instancia particular de Book
        """
        return reverse('book-detail', args=[str(self.id)]) 

import uuid # Requerida para las instancias de libros únicos

from django.contrib.auth.models import User #Required to assign User as a borrower

class BookInstance(models.Model):
    """
    Model representing a specific copy of a book (i.e. that can be borrowed from the library).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True) 
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False
        

    LOAN_STATUS = (
        ('d', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status= models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='d', help_text='Book availability')


    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"),) 
        

    def __str__(self):
        """
        String para representar el Objeto del Modelo
        """
        return '%s (%s)' % (self.id,self.book.title)

class Author(models.Model):
    """
    Modelo que representa un autor
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)
    
    def get_absolute_url(self):
        """
        Retorna la url para acceder a una instancia particular de un autor.
        """
        return reverse('author-detail', args=[str(self.id)])
    

    def __str__(self):
        """
        String para representar el Objeto Modelo
        """
        return '%s, %s' % (self.last_name, self.first_name)

from django.views import generic

class BookListView(generic.ListView):
    model = Book
    context_object_name = 'my_book_list'   # your own name for the list as a template variable
    queryset = Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
    template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location
