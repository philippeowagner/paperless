from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required

from .forms import FileFieldForm


def handle_uploaded_file(f):
    """ """
    with open('{}/{}'.format(settings.CONSUMPTION_DIR, f.name), 'wb+') as dest:
        for chunk in f.chunks():
            dest.write(chunk)

@login_required
def upload_files(request):
    """ """
    if request.method == 'POST':
        form = FileFieldForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect(reverse('paperless_uploader_home'))
    else:
        form = FileFieldForm()

    context = {'form': form}
    return render(request, 'paperless_uploader/index.html', context)
