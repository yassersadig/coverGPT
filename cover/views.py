from django.shortcuts import render
import openai
import os
from dotenv import load_dotenv
import PyPDF2

load_dotenv()


def index(request):
    return render(request, 'cover/index.html')


def result(request):
    title = request.POST.get('title')
    company = request.POST.get('company')
    resume_text = get_resume_from_file(request)
    job = request.POST.get('job')

    response = resume_text

    if os.getenv('DEBUG', 'True') == 'False':

        openai.api_key = os.getenv('OPENAI_SECRET_KEY')

        completion = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'user', 'content': "Write me a personalized cover letter explaining why I'm a great candidate for this job. the job title is %s, the company is %s." % (
                    title, company)},
                {'role': 'user', 'content': "Update the cover letter to include examples and measurable outcomes from my resume. Here is my resume: %s" % resume_text},
                {'role': 'user', 'content': "Update and personalize this cover letter to the following job decription: %s" % job}
            ])
        response = completion.choices[0].get('message', {}).get('content')
    return render(request, 'cover/result.html', {'result': response})

def get_resume_from_file(request):
    resume_file = request.FILES.get('resume')
    resume_pdf = PyPDF2.PdfFileReader(resume_file)
    resume_text = ''
    for page in resume_pdf.pages:
        resume_text += '\n%s' % page.extractText()
    return resume_text
