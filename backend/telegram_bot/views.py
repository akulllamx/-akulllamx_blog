from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from telegram import Update
from .bot import get_application

application = get_application()


@csrf_exempt
@require_http_methods(["POST"])
async def telegram_webhook(request):
    """Webhook для получения обновлений от Telegram"""
    try:
        data = json.loads(request.body)
        update = Update.de_json(data, application.bot)

        # Передаем update в очередь приложения
        await application.update_queue.put(update)

        return JsonResponse({'status': 'ok'})
    except Exception as e:
        print(f"Ошибка webhook: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
