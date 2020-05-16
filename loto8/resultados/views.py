import logging
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Resultado
from .forms import UploadFileForm
from .functions import converter_para_json, carregar_concursos, atualizar_novos_resultados


@login_required
def dashboard(request):
    context = {}
    template_name = 'resultados/dashboard.html'
    return render(request, template_name, context)


@login_required()
def importar_resultados(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                #converte o arquivo do padrão da loteria .htm para json
                json_data = converter_para_json(request.FILES['file'])
                
                # converte o json em um dicionario pythonico
                concursos = carregar_concursos(json_data)
                
                # salvar no banco
                atualizacoes_realizadas = atualizar_novos_resultados(concursos)

                mensagem = {
                    0: 'Nenhum resultado novo foi adicionado', 
                    1: 'Um resultado novo foi adicionado',
                }
                if atualizacoes_realizadas not in mensagem:
                    mensagem[atualizacoes_realizadas] = '{0} resultados novos foram adicionado'.format(atualizacoes_realizadas)
                messages.success(request, mensagem[atualizacoes_realizadas])
                
                return redirect('resultados:listar')
            except Exception as e:
                logging.getLogger("error_logger").error("Unable to upload file. " + repr(e))
                messages.error(request, "Unable to upload file. " + repr(e))
    else:
        form = UploadFileForm()
    return render(request, 'resultados/importar.html', {'form': form})


def listar_resultados(request):
    try:
        q = int(request.GET.get('q'))
    except:
        q = None
    if q:
        resultados = Resultado.objects.filter(concurso=q)
    else:
        resultados = Resultado.objects.all().order_by('-concurso')

    paginator = Paginator(resultados, 12)
    page = request.GET.get('page')

    resultados = paginator.get_page(page)

    return render(request, 'resultados/listar_resultados.html', {'resultados': resultados})