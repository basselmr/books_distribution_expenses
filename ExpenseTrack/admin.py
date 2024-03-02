from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.categoryModel)
admin.site.register(models.publisherModel)
admin.site.register(models.bookModel)
admin.site.register(models.distributionExpenseModel)
