from django.contrib import admin
from .models import Architect, Sample, Phrase

# Register your models here.
class ArchitectAdmin(admin.ModelAdmin):
	list_display = ['name',]
	list_display_links = ['name']
	search_fields = ['name'] 
	list_filter = ["name"]
	class Meta:
		architect=Architect
admin.site.register(Architect, ArchitectAdmin)


class SampleAdmin(admin.ModelAdmin):
	list_display = ["sampleID"]
	list_display_links = ["sampleID"]
	list_filter = ['architect']
	search_fields = ["architect", 'sampleID']
	class Meta:
		sample=Sample
admin.site.register(Sample, SampleAdmin)

class PhraseAdmin(admin.ModelAdmin):
	list_display = ["phrase"]
	list_display_links = ["phrase"]
	list_filter = ['architect']
	search_fields = ["architect", 'phrase']
	class Meta:
		phrase=Phrase
admin.site.register(Phrase, PhraseAdmin)