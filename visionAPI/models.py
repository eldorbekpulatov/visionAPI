from django.db import models

class Architect(models.Model):
    name = models.CharField(max_length=50)
    path = models.URLField(max_length=150)

    def __str__(self):
        return self.name
    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)

class Sample(models.Model):
    sampleID = models.PositiveSmallIntegerField()
    page = models.PositiveSmallIntegerField()
    architect = models.ForeignKey('Architect', on_delete=models.CASCADE )
    
    def __str__(self):
        return str(self.sampleID)
    
    def __unicode__(self):
        return str(self.sampleID)

    class Meta:
        ordering = ("sampleID",)

class Phrase(models.Model):
    phrase = models.CharField(max_length=50)
    architect = models.ForeignKey('Architect', on_delete=models.CASCADE )
    
    def __str__(self):
        return str(self.phrase)
    
    def __unicode__(self):
        return str(self.phrase)
    
    class Meta:
        ordering = ("phrase",)