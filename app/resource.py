from django.conf.urls import url
from tastypie.resources import Resource
from tastypie.utils import trailing_slash

from staf_wrapper import wrapper_STAF
import time


class ProjectStafResource(Resource):
    def __init__(self):
        Resource.__init__(self)
        self.staf_obj = wrapper_STAF.STAFWrapper()
        self.staf_obj.register()

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/?$" % self._meta.resource_name, self.wrap_view('staf_api'), name='staf_api'),
            # following is new APIs
            url(r"^trigger_deb/(?P<mode>.+)/(?P<suite_name>.+?/?)$", self.wrap_view('trigger_deb'), name='trigger_deb'),
            url(r"^trigger_iso/(?P<mode>.+)/(?P<suite_name>.+?/?)$", self.wrap_view('trigger_iso'), name='trigger_iso'),
            url(r"^get_result/(?P<staf_handle_key>.+/?)$", self.wrap_view('get_result'), name='get_result'),
        ]

    def trigger_deb(self, request, **kwargs):
        if kwargs['mode'] == u'non-blocking':
            exec_handle = self.staf_obj.execute(kwargs['suite_name'])
            return self.create_response(request, {"key": exec_handle})
        else:
            raise

    def trigger_iso(self, request, **kwargs):
        pass

    def get_result(self, request, **kwargs):
        if self._query(kwargs['staf_handle_key']) == 'on-going':
            return self.create_response(request, {"key": 'on-going'})
        else:
            return self.create_response(request, {"key": self.staf_obj.result})

    def _query(self, exec_handle):
        if self.staf_obj.query(job_id=exec_handle) == 0:
            return 'has-done'
        else:
            return 'on-going'

    def _unregister(self):
        if self.staf_obj.unregister() == 0:
            return 'successful'
        else:
            return 'unsuccessful'

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
