import requests
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse

class IPCheckMiddleware(MiddlewareMixin):
    def process_request(self, request):
        trusted_ips = ['127.0.0.1']  # Доверенные IP-адреса
        client_ip = request.META['REMOTE_ADDR']

        if client_ip not in trusted_ips:
            ip_info = requests.get(f"https://ipinfo.io/{client_ip}/json").json()

            if 'bogon' in ip_info.get('bogon', ''):
                return JsonResponse({'error': 'IP address is not trusted'}, status=403)
