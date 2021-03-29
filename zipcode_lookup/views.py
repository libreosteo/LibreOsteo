from django.http import JsonResponse

from .models import ZipcodeMapping


def zipcode_lookup(request, zipcode):
    qs = ZipcodeMapping.objects.filter(
        zipcode=zipcode,
    )
    data = [
        {'city': i.city, 'zipcode': i.zipcode}
        for i in qs.all()
    ]
    return JsonResponse(data, safe=False)
