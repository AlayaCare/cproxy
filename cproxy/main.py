from blinker import signal
import Cookie
import httplib
import logging
import requests
from werkzeug.wrappers import Headers, Request, Response


request_received = signal('request-received')
response_received = signal('response-received')


httplib.HTTPConnection.debuglevel = 0

logging.basicConfig() # you need to initialize logging, otherwise you will not see anything from requests
logging.getLogger().setLevel(logging.INFO)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


def massage_request_headers(headers):
    # Strip response-like heafers from the request environ
    headers = Headers(headers.items())
    for key in ('Content-Type', 'Content-Length'):
        headers.remove(key)
    return headers


def massage_response_headers(headers):
    headers = Headers(headers.items())
    for key in ('Transfer-Encoding',):
        headers.remove(key)
    if headers.get('Content-Encoding') == 'gzip':
        headers.remove('Content-Encoding')
        headers.remove('Content-Length')
    headers.remove('Set-Cookie')
    return headers


def set_cookies(response, cookies, host):
    for c in cookies:
        domain = c.domain if c.domain != host else None
        response.set_cookie(c.name, value=c.value, expires=c.expires,
                            path=c.path, domain=domain, secure=c.secure)


def app(environ, start_response):
    req_in = Request(environ)
    request_received.send('cproxy', request=req_in)

    req_headers = massage_request_headers(req_in.headers)
    resp_in = requests.request(method=req_in.method.lower(),
                               url=req_in.url,
                               params=req_in.args,
                               data=req_in.form,
                               headers=req_headers,
                               cookies=req_in.cookies,
                               files=req_in.files)
    response_received.send('cproxy', request=req_in, response=resp_in)

    resp_headers = massage_response_headers(resp_in.headers)
    resp_out = Response(resp_in.iter_content(), status=resp_in.status_code,
                        headers=resp_headers)
    set_cookies(resp_out, resp_in.cookies, req_in.host)
    return resp_out(environ, start_response)
