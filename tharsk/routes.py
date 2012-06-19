from klein import route


@route("/")
def root(request):
    return "Hello, world!"
