import json

from server.server_main import app

if __name__ == "__main__":
    with open('./../../docs/openapi.json', 'w') as f:
        openapi = app.openapi()
        version = openapi.get("openapi", "unknown version")

        print(f"writing openapi spec v{version}")
        json.dump(openapi, f, indent=2)
