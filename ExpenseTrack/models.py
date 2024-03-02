from django.db import models

# Create your models here.
class categoryModel(models.Model):
    category = models.CharField(max_length=150)
    def __str__(self):
        return self.category

class publisherModel(models.Model):
    publisher = models.CharField(max_length=255)
    def __str__(self):
        return self.publisher

class bookModel(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.TextField()
    author = models.CharField(max_length=255)
    category = models.ForeignKey(categoryModel,on_delete = models.CASCADE)
    publisher = models.ForeignKey(publisherModel,on_delete = models.CASCADE)
    def __str__(self):
        return self.title

class distributionExpenseModel(models.Model):
    book = models.ForeignKey(bookModel,on_delete = models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.book + ' ' + self.amount




