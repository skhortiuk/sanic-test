from functools import wraps

from sanic.response import json


def username_required():
    def decorator(f):
        @wraps(f)
        async def decorated(instance, request, *args, **kwargs):
            if "username" not in request.headers:
                return json(
                    {
                        "status": "ERROR",
                        "error_code": 403,
                        "error": "Please provide `username` in headers!"
                    },
                    status=403
                )
            return await f(instance, request, *args, **kwargs)

        return decorated

    return decorator
