def get_user_by_context(context):
    request = context.get("request", None)
    if request and not request.user.is_anonymous:
        return request.user
    return None


def get_user_by_request(request):
    if request and not request.user.is_anonymous:
        return request.user
    return None


def get_referrer_origin(req):
    request = req.get("request", None)
    if request and request.headers.get("Referer") is not None:
        return request.headers.get("Referer")
    return request.headers.get("origin")
