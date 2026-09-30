#!/usr/bin/env python3
"""Serve public/ on 127.0.0.1:5656, rebuilding on every page load.

Edit a tool in tools/*.md, refresh the browser, see it. A content error prints here
and serves the error as text instead of a stale page.
"""
import functools, http.server, importlib, os, sys, traceback

import build

PORT = int(os.environ.get("SCAFFOLD_PORT", "5656"))


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.split("?")[0] in ("/", "/index.html"):
            try:
                importlib.reload(build)  # an edit to build.py counts too, not just content
                build.main()
            except Exception:
                body = traceback.format_exc().encode()
                self.send_response(500)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
        super().do_GET()

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


if __name__ == "__main__":
    build.main()
    handler = functools.partial(Handler, directory=str(build.PUB))
    print(f"http://127.0.0.1:{PORT}")
    try:
        http.server.ThreadingHTTPServer(("127.0.0.1", PORT), handler).serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
