"""Ponto de entrada: `python3 main.py`."""

import os

from game.server import create_server

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    server = create_server("0.0.0.0", port)
    print(f"Brain Training Hub a correr em http://0.0.0.0:{port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor terminado.")
    finally:
        server.server_close()
