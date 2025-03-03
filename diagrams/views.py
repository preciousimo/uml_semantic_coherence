from django.shortcuts import render, redirect
from .forms import UseCaseDiagramForm, ClassDiagramForm
from .utils import validate_semantic_coherence

def upload_diagrams(request):
    if request.method == 'POST':
        use_case_form = UseCaseDiagramForm(request.POST, request.FILES)
        class_diagram_form = ClassDiagramForm(request.POST, request.FILES)
        if use_case_form.is_valid() and class_diagram_form.is_valid():
            use_case_diagram = use_case_form.save()
            class_diagram = class_diagram_form.save()
            results = validate_semantic_coherence(use_case_diagram, class_diagram)
            return render(request, 'results.html', {'results': results})
    else:
        use_case_form = UseCaseDiagramForm()
        class_diagram_form = ClassDiagramForm()
    return render(request, 'upload.html', {'use_case_form': use_case_form, 'class_diagram_form': class_diagram_form})