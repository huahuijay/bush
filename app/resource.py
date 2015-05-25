from django.conf.urls import url
from tastypie.resources import Resource
from tastypie.utils import trailing_slash

from staf_wrapper import wrapper_STAF
import time


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
        # return self.create_response(request, {"name":"value"})
        staf_obj = wrapper_STAF.STAFWrapper()
        staf_obj.register()
        staf_obj.execute()
        while True:
            time.sleep(5)
            # successful
            if staf_obj.query() == 0:
                print staf_obj.result
                break
            # unsuccessful
            else:
                print 'is on-going'

        return self.create_response(request, {"key": staf_obj.result})

    class Meta:
        resource_name = 'staf'
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
