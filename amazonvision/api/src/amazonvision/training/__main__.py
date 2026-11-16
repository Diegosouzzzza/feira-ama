"""Training command line. Run with the training group:

uv run --group training python -m amazonvision.training sintetico --saida C:\\tmp\\ds
uv run --group training python -m amazonvision.training treinar \\
    --manifesto C:\\tmp\\ds\\manifest.csv --produto tucuma
uv run --group training python -m amazonvision.training anomalia \\
    --manifesto C:\\tmp\\ds\\manifest.csv --produto castanha
"""

import argparse
import sys
from pathlib import Path

from amazonvision.config import Settings


def main() -> None:
    # torch.onnx prints emoji; a redirected Windows console (cp1252) would crash on them.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    parser = argparse.ArgumentParser(prog="amazonvision.training")
    sub = parser.add_subparsers(dest="command", required=True)

    synth = sub.add_parser("sintetico", help="gera fotos de teste a partir do simulador")
    synth.add_argument("--saida", type=Path, required=True)
    synth.add_argument("--produto", default="tucuma")
    synth.add_argument("--pecas-por-classe", type=int, default=20)
    synth.add_argument("--fotos-por-peca", type=int, default=4)

    split = sub.add_parser("dividir", help="divide o manifesto por peça física")
    split.add_argument("--manifesto", type=Path, required=True)
    split.add_argument("--semente", type=int, default=7)

    train = sub.add_parser("treinar", help="treina, exporta ONNX e gera o relatório")
    train.add_argument("--manifesto", type=Path, required=True)
    train.add_argument("--produto", required=True)
    train.add_argument("--saida", type=Path, default=None, help="padrão: <dados>/modelos-treinados")
    train.add_argument("--epocas", type=int, default=12)
    train.add_argument("--lote", type=int, default=16)
    train.add_argument("--sem-pre-treino", action="store_true")
    train.add_argument("--dispositivo", default="auto", help="auto, cpu ou cuda")
    train.add_argument("--meta-falsa-aprovacao", type=float, default=0.05)
    train.add_argument(
        "--roi",
        default=None,
        help="janela de inspeção x,y,largura,altura em frações 0..1 (ex.: 0.2,0.1,0.6,0.8); "
        "padrão: quadro inteiro. Use o valor mostrado na tela Configuração",
    )
    anomaly = sub.add_parser(
        "anomalia", help="aprende só com peças boas (classe A) e marca o que foge do padrão"
    )
    anomaly.add_argument("--manifesto", type=Path, required=True)
    anomaly.add_argument("--produto", required=True)
    anomaly.add_argument(
        "--saida", type=Path, default=None, help="padrão: <dados>/modelos-treinados"
    )
    anomaly.add_argument("--banco", type=int, default=4000, help="retalhos no banco de memória")
    anomaly.add_argument("--limiar", type=float, default=0.80)
    anomaly.add_argument("--sem-pre-treino", action="store_true")
    anomaly.add_argument("--roi", default=None, help="igual ao do comando treinar")
    args = parser.parse_args()

    if args.command == "sintetico":
        from amazonvision.training.synthetic import generate

        manifest = generate(
            args.saida,
            product_id=args.produto,
            pieces_per_class=args.pecas_por_classe,
            photos_per_piece=args.fotos_por_peca,
        )
        print(f"manifesto: {manifest}")
    elif args.command == "dividir":
        from amazonvision.training.dataset import (
            read_manifest,
            split_by_physical_sample,
            write_manifest,
        )

        samples = split_by_physical_sample(read_manifest(args.manifesto), seed=args.semente)
        write_manifest(args.manifesto, samples)
        print(f"partições gravadas em {args.manifesto}")
    else:
        from amazonvision.vision.preprocess import RoiSpec

        roi = None
        if args.roi:
            try:
                x, y, width, height = (float(v) for v in args.roi.split(","))
                roi = RoiSpec(x=x, y=y, width=width, height=height)
            except ValueError as exc:
                parser.error(
                    f"--roi inválido ({exc}); use x,y,largura,altura, ex.: 0.2,0.1,0.6,0.8"
                )

        out = args.saida or Settings().data_root / "modelos-treinados"
        if args.command == "anomalia":
            from amazonvision.training.anomaly import train_anomaly

            package = train_anomaly(
                args.manifesto,
                product_id=args.produto,
                out_dir=out,
                pretrained=not args.sem_pre_treino,
                bank_size=args.banco,
                threshold=args.limiar,
                roi=roi,
            )
            print(f"pacote do modelo: {package}")
            print(f"relatório: {package / 'relatorio.md'}")
            return

        from amazonvision.training.train import train as run

        package = run(
            args.manifesto,
            product_id=args.produto,
            out_dir=out,
            epochs=args.epocas,
            batch_size=args.lote,
            pretrained=not args.sem_pre_treino,
            device=args.dispositivo,
            max_false_approval=args.meta_falsa_aprovacao,
            roi=roi,
        )
        print(f"pacote do modelo: {package}")
        print(f"relatório: {package / 'relatorio.md'}")


if __name__ == "__main__":
    main()
