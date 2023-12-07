from django.db import models

# Create your models here.

class Analysis:
    query : str

#TODO: Reconcile how to include a list in this model,  self.PIC_Array = PIC_Array
class Article(models.Model):
        # self.name = name TODO
        URL = models.CharField(max_length=100)
        Text = models.TextField()
        img = models.ImageField(upload_to='pics', default='tempString')
        #self.PIC_Array = PIC_Array

        AItext = models.CharField(max_length=100)
        QualityArticle = models.BooleanField(default=False)
    

