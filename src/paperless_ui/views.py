from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from documents.models import *

@login_required
def index(request):
    docs = Docuements.objects.all()
    context = {'docs': docs, }
    return render(request, 'paperless_ui/docs/index.html', context)
