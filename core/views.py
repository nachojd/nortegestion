from django.views.generic import TemplateView
from django.http import HttpResponse

# Views moved to specific apps:
# - Rubro, Marca, Product → productos/views.py
# - Cliente → clientes/views.py  
# - Quote, QuoteItem → cotizaciones/views.py

class FrontendView(TemplateView):
    template_name = 'core/index.html'

def api_info(request):
    """Vista de información de la API"""
    api_info = {
        'rubros': f"{request.build_absolute_uri('/api/rubros/')}",
        'marcas': f"{request.build_absolute_uri('/api/marcas/')}",
        'products': f"{request.build_absolute_uri('/api/products/')}",
        'clientes': f"{request.build_absolute_uri('/api/clientes/')}",
        'quotes': f"{request.build_absolute_uri('/api/quotes/')}"
    }
    
    import json
    return HttpResponse(
        json.dumps(api_info, indent=2), 
        content_type='application/json'
    )
