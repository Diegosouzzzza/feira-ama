"""Training command line. Run with the training group:

uv run --group training python -m amazonvision.training sintetico --saida C:\\tmp\\ds
uv run --group training python -m amazonvision.training treinar \\
    --manifesto C:\\tmp\\ds\\manifest.csv --produto tucuma
"""

import argparse
from pathlib import Path

from amazonvision.config import Settings


def main() -> None:
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
        from amazonvision.training.train import train as run
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
