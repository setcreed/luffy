from rest_framework.throttling import SimpleRateThrottle

class SMSRateThrottle(SimpleRateThrottle):
    scope = 'sms'
    def get_cache_key(self, request, view):
        mobile = request.query_params.get('mobile') or request.data.get('mobile')
        if not mobile:
            return None
        return self.cache_format % {
            'scope': self.scope,
            'ident': mobile
        }

