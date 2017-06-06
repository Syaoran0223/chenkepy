from .errors import forbidden

@api.befor_request
@auth.login_required
def before_request():
    if not g.current_user.is_anonymous and not g.current_user.confirmed:
        return forbidden(u"请登录");