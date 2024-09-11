from django.db import models 

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=100, blank=True, null=True)
    sub_category = models.ForeignKey('SubCategory', on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return self.name
    

class SubCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name    

class AvilableUrl(models.Model):
    url = models.URLField(max_length=200)
    
    def __str__(self):
        return self.url
    

# class Job(models.Model):
class Job(models.Model):
    company = models.CharField(max_length=255)
    position = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    email= models.EmailField(max_length=255, blank=True, null=True)
    website = models.URLField(max_length=255, blank=True, null=True)
    # vacancy = models.CharField(max_length=255, blank=True, null=True)
    salary = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    job_type = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    job_posted = models.TextField(blank=True, null=True)
    job_link = models.URLField(max_length=255, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.company + " - " + self.position