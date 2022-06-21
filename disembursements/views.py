from django.http import HttpResponse, JsonResponse
from django.core.serializers.python import Serializer
from django.views.decorators.http import require_GET
from .models import Disembursement

# Extends Django Serializer. It excludes the private key and the model in the serialized result.
class CustomSerialiser(Serializer):
    def end_object( self, obj ):
        self._current['id'] = obj._get_pk_val()
        self.objects.append( self._current )

# Define the serializer that will be used by the endpoints below.
serializer = CustomSerialiser()

# TODO: ADD DOCU
@require_GET
def get_all(request):
    query_set = Disembursement.objects.all()
    data = serializer.serialize(query_set)
    return HttpResponse(data, content_type='application/json')

# TODO: ADD DOCU
@require_GET
def get_by_merchant(request, merchant=None):
    query_set = Disembursement.objects.filter(merchant_id=merchant)
    data = serializer.serialize(query_set)
    return HttpResponse(data, content_type='application/json')

