# -*- coding: utf-8 -*-

from flask import jsonify, request
from flask._compat import text_type, string_types
import json


# 自动识别字典，转换成json
def make_response(self, rv):
    """Converts the return value from a view function to a real
    response object that is an instance of :attr:`response_class`.

    The following types are allowed for `rv`:

    .. tabularcolumns:: |p{3.5cm}|p{9.5cm}|

    ======================= ===========================================
    :attr:`response_class`  the object is returned unchanged
    :class:`str`            a response object is created with the
                            string as body
    :class:`unicode`        a response object is created with the
                            string encoded to utf-8 as body
    a WSGI function         the function is called as WSGI application
                            and buffered as response object
    :class:`tuple`          A tuple in the form ``(response, status,
                            headers)`` where `response` is any of the
                            types defined here, `status` is a string
                            or an integer and `headers` is a list of
                            a dictionary with header values.
    ======================= ===========================================

    :param rv: the return value from the view function

    .. versionchanged:: 0.9
       Previously a tuple was interpreted as the arguments for the
       response object.
    """
    status = headers = None
    if isinstance(rv, tuple):
        rv, status, headers = rv + (None,) * (3 - len(rv))

    if rv is None:
        raise ValueError('View function did not return a response')

    if not isinstance(rv, self.response_class):
        # When we create a response object directly, we let the constructor
        # set the headers and status.  We do this because there can be
        # some extra logic involved when creating these objects with
        # specific values (like default content type selection).
        if isinstance(rv, (text_type, bytes, bytearray)):
            rv = self.response_class(rv, headers=headers, status=status)
            headers = status = None
        elif isinstance(rv, dict):
            rv = jsonify(rv)
        else:
            rv = self.response_class.force_type(rv, request.environ)

    if status is not None:
        if isinstance(status, string_types):
            rv.status = status
        else:
            rv.status_code = status
    if headers:
        rv.headers.extend(headers)

    return rv

def extends_db(db):
    class JsonBlob(db.TypeDecorator):
        impl = db.Text

        def process_bind_param(self, value, dialect):
            if isinstance(value, str):
                return value
            return json.dumps(value)

        def process_result_value(self, value, dialect):
            if value is not None:
                return json.loads(value)
            return None

    class MoneyBlob(db.TypeDecorator):
        impl = db.Integer

        def process_bind_param(self, value, dialect):
            return float(value) * 100

        def process_result_value(self, value, dialect):
            return value / 100

    db.JsonBlob = JsonBlob
    db.MoneyBlob = MoneyBlob