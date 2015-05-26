from django.conf.urls import url
from tastypie.resources import Resource
from tastypie.utils import trailing_slash

from staf_wrapper import wrapper_STAF
import time


class ProjectStafResource(Resource):
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/?$" % self._meta.resource_name, self.wrap_view('staf_api'), name='staf_api'),
            url(r"^(?P<resource_name>%s)/?$" % 'non_blocking_trigger', self.wrap_view('non_blocking_trigger'), name='non_blocking_trigger'),
            url(r"^(?P<resource_name>%s)/(?P<fun>.+)%s$" % ('query', trailing_slash()), self.wrap_view('query'), name='query'),
            url(r"^initialize$", self.wrap_view('initialize'), name='initialize'),
            url(r"^unregister$", self.wrap_view('unregister'), name='unregister'),
        ]

    def initialize(self, request, **kwargs):
        self._num = 0
        self._map_str_obj = dict()
        return self.create_response(request, {"key": 'value'})


    def non_blocking_trigger(self, request, **kwargs):
        staf_obj = wrapper_STAF.STAFWrapper()
        staf_obj.register()
        staf_handle = staf_obj.execute()
        # self._map_str_obj[staf_handle] = staf_obj
        self._num += 1
        self._map_str_obj[self._num] = staf_obj
        return self.create_response(request, {"key": self._num})


    def query(self, request, **kwargs):
        key = int(kwargs['fun'])
        staf_obj = self._map_str_obj.get(key)
        if staf_obj.query() == 0:
            return self.create_response(request, {"key": staf_obj.result})
        else:
            return self.create_response(request, {"key": 'on-going'})


    def unregister(self, request, **kwargs):
        if staf_obj.unregister() == 0:
            return self.create_response(request, {"key": 'successful'})
        else:
            return self.create_response(request, {"key": 'unsuccessful'})


    def staf_api(self, request, **kwargs):
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
        staf_obj.unregister()

        return self.create_response(request, {"key": staf_obj.result})


    class Meta:
        resource_name = 'staf'
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
