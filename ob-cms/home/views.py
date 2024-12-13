from django.http import HttpResponse, HttpResponseNotFound, Http404,  HttpResponseRedirect

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .models import Signature
from .forms import SignatureForm
import re
import os
from django.conf import settings
from django.urls import path
from django.shortcuts import render
from django.http import JsonResponse
from googletrans import Translator
import speech_recognition as sr

from django.shortcuts import render, redirect

# Translator instance
translator = Translator()

#redirect to spanish if the url contains colombia.open.build
def index(req):
    sub, _ = req.META['HTTP_HOST'].split('.', 1)
    if sub == 'colombia':
        return HttpResponseRedirect("/inicio")
    else:
        return HttpResponseRedirect("/")


import sendgrid
from sendgrid.helpers.mail import Mail
from django.conf import settings

def send_notification_email(subject, message):
    sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
    from_email = "team@open.build"  # Your "from" email address
    to_email = "greg@open.build"      # Admin's email address

    mail = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=message
    )

    response = sg.send(mail)
    return response.status_code



class SignatureCreateView(CreateView):
    model = Signature
    template_name = 'home/signature.html'
    success_url = '/'  # Replace with the desired URL
    form_class = SignatureForm

    def form_valid(self, form):
        
        form.save()
        messages.success(self.request, 'Success, Your Signature has been Submitted!')
        
        # Send Email
        subject = "New Open Build Framework Form Submission" 
        message = "A new form has been submitted from " + str(form.cleaned_data['email'])
        send_notification_email(subject, message)
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


from django.shortcuts import render
from .forms import MentorApplicationForm, ProjectSubmissionForm

def apply_to_mentor(request):
    if request.method == 'POST':
        form = MentorApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'application_submitted.html')
    else:
        form = MentorApplicationForm()
    return render(request, 'home/apply_to_mentor.html', {'form': form})

def submit_project(request):
    if request.method == 'POST':
        form = ProjectSubmissionForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'submission_success.html')
    else:
        form = ProjectSubmissionForm()
    return render(request, 'home/submit_project.html', {'form': form})

def translate_audio(request):
    if request.method == 'POST' and 'audio' in request.FILES:
        recognizer = sr.Recognizer()
        audio_file = request.FILES['audio']
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            try:
                # Speech-to-text
                text = recognizer.recognize_google(audio_data)
                # Translate text
                translated_text = translator.translate(text, dest='en').text
                return JsonResponse({'success': True, 'text': text, 'translation': translated_text})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

def translate_chat(request):
    if request.method == 'POST':
        original_message = request.POST.get('message', '')
        target_language = request.POST.get('language', 'en')
        try:
            translated_message = translator.translate(original_message, dest=target_language).text
            return JsonResponse({'success': True, 'translation': translated_message})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})