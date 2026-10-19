import argparse
import json
import logging
from pathlib import Path

import uvicorn

from amazonvision.config import Settings


def main() -> None:
    parser = argparse.ArgumentParser(prog="amazonvision")
    parser.add_argument(
        "--reload", action="store_true", help="recarregar ao editar (desenvolvimento)"
    )
    parser.add_argument(
        "--dump-openapi", type=Path, metavar="ARQUIVO", help="gravar o esquema OpenAPI e sair"
    )
    args = parser.parse_args()

    if args.dump_openapi:
        from amazonvision.main import create_app

        schema = create_app().openapi()
        args.dump_openapi.write_text(
            json.dumps(schema, indent=2, ensure_ascii=False) + "\n", "utf-8"
        )
        return

    settings = Settings()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    uvicorn.run(
        "amazonvision.main:create_app",
        factory=True,
        host=settings.host,
        port=settings.port,
        reload=args.reload,
        workers=1,
    )


if __name__ == "__main__":
    main()
