from datasette import hookimpl
from functools import wraps
from pyinstrument import Profiler


@hookimpl
def asgi_wrapper():
    def wrap_with_pyinstrument(app):
        @wraps(app)
        async def add_pyinstrument(scope, receive, send):
            query_string = scope.get("query_string", b"")
            should_instrument = query_string and b"_pyinstrument=1" in query_string
            if not should_instrument:
                await app(scope, receive, send)
            else:
                profiler = Profiler(interval=0.0001, async_mode="enabled")
                profiler.start()
                collected = []

                async def fake_send(event):
                    collected.append(event)

                await app(scope, receive, fake_send)
                profiler.stop()
                html = profiler.output_html()
                await send(
                    {
                        "type": "http.response.start",
                        "status": 200,
                        "headers": [
                            [b"content-type", b"text/html; charset=utf-8"],
                        ],
                    }
                )
                await send({"type": "http.response.body", "body": html.encode("utf-8")})

        return add_pyinstrument

    return wrap_with_pyinstrument
