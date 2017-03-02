from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from documents.models import *

@login_required
def index(request):
    docs = Document.objects.all()
    context = {'docs': docs, }
    return render(request, 'paperless_ui/docs/index.html', context)


@login_required
def doc_viewer(request, checksum):
    doc = Document.objects.get(checksum=checksum)

    from markdownx.settings import MARKDOWNX_MARKDOWNIFY_FUNCTION
    from django.utils.module_loading import import_string
    markdownify = import_string(MARKDOWNX_MARKDOWNIFY_FUNCTION)
    md_content = markdownify(doc.content)

    context = {'doc': doc, 'md_content': md_content,}
    return render(request, 'paperless_ui/docs/doc_viewer.html', context)
