from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from datetime import date


# Create your models here.

class Genre(models.Model):
    """Modelo representando um gênero de livro."""
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')
    
    def __str__(self):
        """String para representar o objeto."""
        return self.name

class Language(models.Model):
    """Modelo que representa um idioma (por exemplo, inglês, francês, japonês etc.)"""
    name = models.CharField(max_length=200,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def __str__(self):
        """String para representar o objeto (no site Admin etc.)"""
        return self.name

class Book(models.Model):
    """Modelo representando um livro (mas não uma cópia específica de um livro)."""
    title = models.CharField(max_length=200)

    # Chave estrangeira usada porque o livro pode ter apenas um autor, mas os autores podem ter vários livros
    # Cria como uma string em vez de um objeto, porque ainda não foi declarado no arquivo
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    
    summary = models.TextField(max_length=1000, help_text='Digite uma breve descrição do livro')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    
    # ManyToManyField usado porque o gênero pode conter muitos livros. Os livros podem abranger muitos gêneros.
    # A classe de gênero já foi definida para que possamos especificar o objeto acima.
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """String para representar o objeto."""
        return self.title
    
    def get_absolute_url(self):
        """Retorna o URL para acessar um registro detalhado deste livro."""
        return reverse('book-detail', args=[str(self.id)])


class BookInstance(models.Model):
    """Modelo representando uma cópia específica de um livro (ou seja, que pode ser emprestado da biblioteca)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='ID exclusivo para este livro em particular em toda a biblioteca')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True) 
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

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

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """String para representar o objeto."""
        return f'{self.id} ({self.book.title})'

class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return '{0}, {1}'.format(self.last_name, self.first_name)