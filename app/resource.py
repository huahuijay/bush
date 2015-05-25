from django.conf.urls import url
from tastypie.resources import Resource
from tastypie.utils import trailing_slash


class ProjectStafResource(Resource):
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<fun>.+)%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('staf_api'), name='staf_api'),
        ]

    def staf_api(self, request, **kwargs):
        method = kwargs['fun']
        print kwargs
        #args = dict(map(lambda x: x, request.GET.items()))
        return self.create_response(request, {"name":"value"})


    class Meta:
        resource_name = 'staf'
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
