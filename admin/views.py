from django.http import HttpResponse
from django.shortcuts import render
import yaml
from pathlib import Path
from rest_framework.request import Request as DRFRequest
from drf_spectacular.views import SpectacularAPIView

BASE_DIR = Path(__file__).resolve().parent.parent

def home(request):
    context = {}
    return render(request, BASE_DIR / 'templates/admin/home.html', context)
    

def custom_swagger_ui(request):
    return render(request, 'custom_swagger_ui.html')

    
def custom_yaml(request, prefix):
    drf_request = DRFRequest(request)
    if not hasattr(drf_request, 'version'):
        drf_request.version = 'default'

    spectacular_api_view = SpectacularAPIView()
    response = spectacular_api_view.get(drf_request)
    
    if response.status_code != 200:
        return HttpResponse("Error generating the schema", status=500)

    schema = response.data
    filtered_paths = {}
    for path, detail in schema['paths'].items():
        if path.startswith(f'/{prefix}/'):
            # Maintain the correct endpoint structure without additional transformations
            filtered_paths[path] = detail

    if not filtered_paths:
        return HttpResponse("No paths found for this prefix", status=404)

    # Format the title appropriately for display purposes
    formatted_title = ' '.join(word.capitalize() for word in prefix.replace('-', ' ').replace('_', ' ').split())
    formatted_title = formatted_title.replace('Api', '').strip()

    new_schema = {
        'openapi': schema['openapi'],
        'info': {
            'title': f"{formatted_title}",
            'version': schema['info']['version'],
            'description': f"{formatted_title} related endpoints"
        },
        'paths': filtered_paths,
        'components': schema['components']
    }

    yaml_content = yaml.dump(new_schema, sort_keys=False, allow_unicode=True)
    response = HttpResponse(yaml_content, content_type="application/x-yaml")
    response['Content-Disposition'] = f'attachment; filename="{prefix}.yaml"'
    return response
