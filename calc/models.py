from django.db import models

# Create your models here.

class Analysis(models.Model):
        query = models.CharField(max_length=256)
        img = models.CharField(max_length=256)
        analysis = models.TextField()
        semquad = models.CharField(max_length=256)


#TODO: Reconcile how to include a list in this model,  self.PIC_Array = PIC_Array
class Article(models.Model):
        # self.name = name TODO
        query = models.CharField(max_length=256)
        URL = models.CharField(max_length=256)
        Text = models.TextField()
        img = models.TextField(max_length=256)
        #self.PIC_Array = PIC_Array
        AItext = models.TextField()
        QualityArticle = models.BooleanField(default=False)


class SurftStatus(models.Model):
    is_running = models.BooleanField(default=False)
    

