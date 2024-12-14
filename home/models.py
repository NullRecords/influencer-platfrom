from django.db import models
from django.contrib import admin

from wagtail.models import Page


class HomePage(Page):
    pass

class AboutPage(Page):
    pass

class Portfolio(Page):
    pass


class Influencer(models.Model):
    name = models.CharField(max_length=255)
    platform = models.CharField(max_length=50, choices=[
        ('instagram', 'Instagram'),
        ('tiktok', 'TikTok'),
        ('youtube', 'YouTube'),
    ])
    followers = models.IntegerField()
    engagement_rate = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class Campaign(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    influencers = models.ManyToManyField(Influencer, related_name='campaigns')
    created_at = models.DateTimeField(auto_now_add=True)

class PerformanceMetric(models.Model):
    influencer = models.ForeignKey(Influencer, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    impressions = models.IntegerField()
    clicks = models.IntegerField()
    conversions = models.IntegerField()
    date = models.DateField()


class Signature(models.Model):
    FRAMEWORK_CHOICES = [
        ('Radical', 'Radical'),
        ('Ethical', 'Ethical'),
        ('All', 'All'),
    ]

    linkedin_url = models.URLField(null=True, blank=True, help_text="Share your LinkedIn Profile")
    twitter_url = models.URLField(null=True, blank=True, help_text="Share your Twitter Profile")
    github_url = models.URLField(null=True, blank=True, help_text="Share your Github Profile")
    framework = models.CharField(max_length=10, choices=FRAMEWORK_CHOICES)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    company = models.CharField(max_length=255,null=True, blank=True)
    is_collaborator = models.BooleanField(default=False,help_text="Check here if you would like to collaborate via GitHub")
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class SignatureAdmin(admin.ModelAdmin):
    list_display = ('company','name','email','framework')
    search_fields = ('company','name','email','framework')
    list_filter = ('company','name','email','framework')
    display = 'User Submitted Signature'


class MentorApplication(models.Model):
    APPLICATION_CHOICES = [
        ('mentor', 'Mentor'),
        ('intern', 'Intern/Junior Developer'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    linkedin_profile = models.URLField(blank=True)
    resume = models.FileField(upload_to='resumes/')
    application_type = models.CharField(max_length=6, choices=APPLICATION_CHOICES)
    experience = models.TextField()


class ProjectSubmission(models.Model):
    submitter_name = models.CharField(max_length=100)
    submitter_email = models.EmailField()
    project_title = models.CharField(max_length=200)
    project_description = models.TextField()
