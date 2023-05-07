from django.shortcuts import render
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

    response = 'Dear Hiring Manager, I am thrilled to submit my application for the Software Engineer position at Odoo. With my strong background in software development, I believe that I am an ideal candidate for this role. As a software engineer at my previous company, I demonstrated proficiency in developing and implementing software solutions to meet client needs, collaborating with teammates on large-scale projects, and continually improving my programming skills. These accomplishments led to receiving a promotion within my first year of employment. I have a passion for software development and thrive in collaborative team environments. I believe in a user-centric approach and consistently strive to develop intuitive and effective software for clients. As a team player, I am able to work collaboratively with people from all different backgrounds and skillsets to deliver high-quality software. Through my experience, I have developed expertise in a range of programming languages and toolkits such as Python, C++, and Git. Additionally, I have experience with web application development, database technologies, and agile project management. Specifically, at my previous company, I led the development of a new web application for a client which resulted in a 25% increase in user engagement and a 15% increase in revenue. I pride myself on my ability to use data to inform development decisions, resulting in measurable improvements for clients. I am excited about the opportunity to join the dynamic team at Odoo and contribute my skills and experience to create innovative and effective software solutions. I look forward to the opportunity to meet with you to discuss my application further. Thank you for your time and consideration. Sincerely, [Your Name]'

    if os.getenv('DEBUG', 'True') == 'False':

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
    return render(request, 'cover/result.html', {'result': response})
