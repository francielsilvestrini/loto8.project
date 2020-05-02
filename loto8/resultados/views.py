import logging
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Resultado
from .forms import UploadFileForm
from .functions import converter_para_json, carregar_concursos


@login_required()
def importar_resultados(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                json_data = converter_para_json(request.FILES['file'])
                carregar_concursos(json_data)
                # salvar no banco

                messages.success(request, 'Arquivo importado com sucesso!')
                return redirect('resultados:listar')
            except Exception as e:
                logging.getLogger("error_logger").error("Unable to upload file. " + repr(e))
                messages.error(request, "Unable to upload file. " + repr(e))
    else:
        form = UploadFileForm()
    return render(request, 'resultados/importar.html', {'form': form})


def listar_resultados(request):
    resultados = Resultado.objects.all().order_by('-concurso')
    return render(request, 'resultados/listar_resultados.html', {'resultados': resultados})