# -*- coding: utf-8 -*-
"""
Regera SOMENTE as mesas corrigidas pelo laudo LT-3D-002 (06/11/2026) e o STL mestre,
sem apagar nada. NAO use main() do gerador: ele apaga todas as STL das pastas 01-07,
inclusive a Mesa 14 e as buchas avulsas, que nao saem deste gerador.

Uso:  python regerar_mesas_corrigidas.py
"""
import os
import shutil
import sys
import warnings

warnings.filterwarnings('ignore')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gerar_kit_3d_amazonvision as g  # noqa: E402

CORRIGIDAS = {
    'Mesa_01_Chassi_4x_Cabeceiras_e_2x_Mancais.stl': [('ricley', '01_Mesa_01_Chassi_4x_Cabeceiras_e_2x_Mancais.stl')],
    'Mesa_02_Chassi_6x_Extensoes_e_6x_Guias_Laterais.stl': [('diego', '01_Mesa_02_Chassi_6x_Extensoes_e_6x_Guias.stl')],
    'Mesa_05_Tambores_Motriz_Livre_Central_e_Polias_GT2.stl': [('ricley', '03_Mesa_05_Tambores_Motriz_Livre_e_Polias_GT2.stl')],
    'Mesa_07_Acionamento_Motor_GA37_e_Empurrador_MG996R_Completo.stl': [('diego', '05_Mesa_07_Acionamento_GA37_e_Empurrador_MG996R.stl')],
}
PROJ = os.path.abspath(os.path.join(g.KIT_ROOT, '..'))


def main():
    plates = []
    for group, filename, func, expected in g.MESAS_REGISTRY:
        tm = func()
        plates.append(tm)
        if filename not in CORRIGIDAS:
            continue
        bodies = len(tm.split(only_watertight=False))
        status = 'OK' if bodies == expected else 'ERRO'
        print(f"[{status}] {filename}: {bodies}/{expected} corpos, extents={tm.extents.round(1).tolist()}, "
              f"watertight={tm.is_watertight}")
        if bodies != expected:
            raise SystemExit("Contagem de corpos errada (pecas se tocando?) - nada foi gravado para esta mesa.")
        out = os.path.join(g.SUBDIRS[group[:2]], filename)
        g.export_binary_stl(tm, out, f"AmazonVision 4.0 - {filename} - rev LT-3D-002")
        for pasta, nome in CORRIGIDAS[filename]:
            shutil.copy2(out, os.path.join(PROJ, pasta, nome))
            print(f"      copiado para {pasta}/{nome}")
    g.generate_master_build_plates_stl(plates)


if __name__ == '__main__':
    main()
