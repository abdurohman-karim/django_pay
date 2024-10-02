import requests
import logging
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse

logger = logging.getLogger(__name__)

class IPCheckMiddleware(MiddlewareMixin):
    def process_request(self, request):
        trusted_ips = ['127.0.0.1']
        client_ip = request.META.get('REMOTE_ADDR')

        # Логируем входящий IP
        logger.info(f"Incoming request from IP: {client_ip}")

        if client_ip not in trusted_ips:
            try:
                ip_info = requests.get(f"https://ipinfo.io/{client_ip}/json")
                ip_info.raise_for_status()
                ip_info_json = ip_info.json()

                logger.info(f"IP info: {ip_info_json}")

                if isinstance(ip_info_json, dict) and 'bogon' in ip_info_json and ip_info_json['bogon']:
                    logger.warning(f"Bogon IP detected: {client_ip}")
                    return JsonResponse({'error': 'IP address is not trusted'}, status=403)

            except requests.RequestException as e:
                logger.error(f"Could not retrieve IP information for {client_ip}: {e}")
                return JsonResponse({'error': 'Could not retrieve IP information'}, status=503)

            except ValueError:
                logger.error(f"Invalid response from IP service for {client_ip}")
                return JsonResponse({'error': 'Invalid response from IP service'}, status=502)
