from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect


class ObjectDetailMixin:
    model = None
    template = None

    def get(self, request, slug):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        return render(request, self.template, context={self.model.__name__.lower(): obj})


class ObjectCreateMixin:
    form_model = None
    template = None

    def get(self, request):
        form = self.form_model()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = self.form_model(request.POST)
        if form.is_valid():
            new_obj = form.save()
            return redirect(new_obj)
        return render(request, self.template, {'form': form})
