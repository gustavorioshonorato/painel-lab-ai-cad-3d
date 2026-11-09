from __future__ import annotations

import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from generator import generate

APP_DIR = Path(__file__).resolve().parent
OUT_DIR = APP_DIR / "outputs"


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(APP_DIR), **kwargs)

    def do_POST(self):
        if urlparse(self.path).path != "/api/generate":
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length < 1 or length > 200_000:
                raise ValueError("Envie uma configuração JSON válida.")
            config = json.loads(self.rfile.read(length).decode("utf-8"))
            result = generate(config, OUT_DIR)
            payload = {"ok": True, "layout": result["layout"], "svg": result["svg"], "summary": result["summary"],
                       "downloads": {"json": "/outputs/panel_config.json", "svg": "/outputs/panel_layout.svg", "dxf": "/outputs/panel_layout.dxf"}, "drawings": ["/outputs/drawings/" + name for name in result["drawings"]]}
            data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
        except (ValueError, json.JSONDecodeError, UnicodeDecodeError) as exc:
            data = json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False).encode("utf-8")
            self.send_response(400)
        except Exception as exc:
            data = json.dumps({"ok": False, "error": f"Falha na geração: {exc}"}, ensure_ascii=False).encode("utf-8")
            self.send_response(500)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):
        print("%s - %s" % (self.address_string(), fmt % args))


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 8765), Handler)
    print("Painel Lab local: http://127.0.0.1:8765")
    print("Somente este computador; não exponha o servidor à rede.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
    finally:
        server.server_close()
