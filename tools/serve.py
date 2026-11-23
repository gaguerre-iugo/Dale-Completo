# -*- coding: utf-8 -*-
"""Servidor local para revisar el libro sin cache del navegador.

`python -m http.server` no manda cabeceras de cache, asi que Chrome guarda los
mp3 y los sigue reproduciendo viejos aunque se regenere el archivo. Este
servidor agrega `Cache-Control: no-store` a todo.

Uso:
    python tools/serve.py [puerto]
"""
import http.server
import socketserver
import sys
from functools import partial


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def log_message(self, fmt, *args):
        pass


def main():
    puerto = int(sys.argv[1]) if len(sys.argv) > 1 else 8777
    handler = partial(Handler, directory=".")
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(("127.0.0.1", puerto), handler) as httpd:
        print(f"http://127.0.0.1:{puerto}/  (sin cache)")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
