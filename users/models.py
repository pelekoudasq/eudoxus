from django.contrib.auth.models import User, Group
from django.db import models

class Publisher(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	title = models.CharField(max_length=100, unique=True, blank=False)

	def __str__(self):
		return self.title

class Distributor(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	title = models.CharField(max_length=100, unique=True, blank=False)

	def __str__(self):
		return self.title

class Secretary(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
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
	title = models.CharField(max_length=100, blank=True, null=True)
	author = models.CharField(max_length=100, blank=True, null=True)
	total_pages = models.IntegerField(blank=True, null=True)
	isbn = models.IntegerField(unique=True, blank=True, null=True)
	first_published = models.IntegerField(blank=True, null=True)
	pub = models.ForeignKey(Publisher, on_delete=models.CASCADE, blank=True, null=True)
	dist = models.ForeignKey(Distributor, on_delete=models.CASCADE, blank=True, null=True)
	avail = models.IntegerField(blank=True, null=True)

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
	user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
	books = models.ManyToManyField(Book)

class Student(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	uni = models.ForeignKey(University, on_delete=models.CASCADE, blank=False)
	dept = models.ForeignKey(Department, on_delete=models.CASCADE, blank=False)
