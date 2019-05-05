from django.shortcuts import render, redirect
from django.http import HttpResponse
import pandas as pd
import numpy as np
from base_class.amazon_comment import AmazonComment

# Create your views here.


def index(request):
    return render(request, 'index.html')


def result(request):
    comments = None
    url = request.POST.get('search_words', '')
    print('url', url)

    url = 'https://www.amazon.com/Kindle-Oasis-reader-High-Resolution-International/dp/B06XDFJJRS/ref=cm_cr_arp_d_product_top?ie=UTF8'

    ac = AmazonComment(url)
    df = ac.comments
    html = """<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Comments</title>
            <script src="/static/css/bootstrap.css"></script>
        </head>
        <body>
        <h1>SA</h1>
            <table id="table-div">""" + \
           df.to_html(escape=False)\
           + """
        </table>
        </body>
        </html>
        """
    return HttpResponse(html.encode('utf-8'))

