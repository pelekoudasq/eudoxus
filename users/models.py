from django.db import models

# Create your models here.
class Publisher(models.Model):
	title = models.CharField(max_length=100, unique=True, blank=False)

	def __str__(self):
		return self.title

class University(models.Model):
	title = models.CharField(max_length=100, unique=True, blank=False)

	def __str__(self):
		return self.title

class Department(models.Model):
	title = models.CharField(max_length=100, blank=False)
	uni = models.ForeignKey(University, on_delete=models.CASCADE, blank=False)

	def __str__(self):
		return self.title

class Book(models.Model):
	title = models.CharField(max_length=100, blank=False)
	author = models.CharField(max_length=100, blank=False)
	total_pages = models.IntegerField()
	isbn = models.IntegerField(unique=True, blank=False)
	first_published = models.IntegerField(blank=False)
	uni = models.ForeignKey(Publisher, on_delete=models.CASCADE, blank=False)

	def __str__(self):
		return self.title

class Class(models.Model):
	title = models.CharField(max_length=100, blank=False)
	dept = models.ForeignKey(Department, on_delete=models.CASCADE, blank=False)
	semester = models.IntegerField(blank=True)
	books = models.ManyToManyField(Book)

	def __str__(self):
		return self.title

class Order(models.Model):
	uni = models.ForeignKey(University, on_delete=models.CASCADE, blank=False)
	dept = models.ForeignKey(Department, on_delete=models.CASCADE, blank=False)



