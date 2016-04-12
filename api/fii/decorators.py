import json

from functools import wraps

from flask import request, Response


def require(*dargs):
    def inner_require(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            for attr in dargs:
                value = request.form.get(attr, request.args.get(attr, None))
                if value is None:
                    message = json.dumps({'error': 'missing_' + attr})
                    return Response(message, mimetype='application/json')
            return func(*args, **kwargs)
        return decorated_function
    return inner_require
