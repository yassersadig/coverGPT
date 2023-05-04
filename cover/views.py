from django.shortcuts import render
from django.http import HttpResponse
import openai
import os
from dotenv import load_dotenv

load_dotenv()



def index(request):
    return render(request, 'cover/index.html')


def result(request):
    title = request.POST.get('title')
    company = request.POST.get('company')
    resume = request.POST.get('resume')
    job = request.POST.get('job')

    openai.api_key = os.getenv('OPENAI_SECRET_KEY')

    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'user', 'content': "Write me a personalized cover letter explaining why I'm a great candidate for this job. the job title is %s, the company is %s." % (
                title, company)},
            {'role': 'user', 'content': "Update the cover letter to include examples and measurable outcomes from my resume. Here is my resume: %s" % resume},
            {'role': 'user', 'content': "Update and personalize this cover letter to the following job decription: %s" % job}
        ])
    response = completion.choices[0].get('message', {}).get('content')
    return HttpResponse(response)
