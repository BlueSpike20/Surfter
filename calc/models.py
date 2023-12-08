from django.db import models

# Create your models here.

class Analysis(models.Model):
        query = models.CharField(max_length=200)
        img = models.ImageField()
        analysis = models.CharField(max_length=500)
        semquad = models.CharField(max_length=256)


#TODO: Reconcile how to include a list in this model,  self.PIC_Array = PIC_Array
class Article(models.Model):
        # self.name = name TODO
        query = models.CharField(max_length=200)
        URL = models.CharField(max_length=200)
        Text = models.TextField()
        img = models.ImageField(upload_to='pics', default='tempString')
        #self.PIC_Array = PIC_Array
        AItext = models.CharField(max_length=100)
        QualityArticle = models.BooleanField(default=False)
    

