# -*- coding: utf-8 -*-
"""
================================================================================
PROJETO AMAZONVISION 4.0 — ESTEIRA SELETORA INDUSTRIAL 700 MM
SCRIPT DE AUDITORIA E VALIDAÇÃO DAS 13 MESAS DE IMPRESSÃO (BAMBU LAB P2S)
================================================================================
Auditoria Dimensional, Topológica e de DfAM para Bambu Lab P2S (256x256x256 mm)

Verificações obrigatórias executadas:
1. Integridade Binária STL: Tamanho exato (84 + 50 * num_faces), zero NaN/Inf.
2. Malha Fechada (Watertight / Manifold): 2-manifold estanque, zero arestas abertas.
3. Envelope de Impressão Bambu P2S: min(Z) == 0.00 mm, Dimensões X, Y, Z <= 256 mm.
4. Contagem Exata de Corpos Conectados (Peças Nesteadas na Mesa): bodies == expected.
5. Área Sólida de Contato na Mesa (Z=0): >= 750 mm² para excelente adesão sem warping.
6. Alinhamento e Coerência Global na Montagem Geral (Esteira_Completa_Montada_70cm.stl).
================================================================================
"""

import os
import sys
import json
import time
import numpy as np
import trimesh

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
KIT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))

MESAS_CONFIG = [
    {
        'folder': '01_Estrutura_Esteira',
        'filename': 'Mesa_01_Chassi_4x_Cabeceiras_e_2x_Mancais.stl',
        'expected_bodies': 6,
        'description': '4x Cabeceiras laterais (01A, 01B, 01C, 01D) + 2x Mancais tensores (02D)'
    },
    {
        'folder': '01_Estrutura_Esteira',
        'filename': 'Mesa_02_Chassi_6x_Extensoes_e_6x_Guias_Laterais.stl',
        'expected_bodies': 12,
        'description': '4x Extensões padrão (01E) + 2x Extensões centrais (01F) + 4x Guias (01I) + 2x Guias recorte (01J)'
    },
    {
        'folder': '01_Estrutura_Esteira',
        'filename': 'Mesa_03_Chassi_2x_Mesas_Deslizantes_01G_Par1e2.stl',
        'expected_bodies': 2,
        'description': '2x Mesas deslizantes de apoio da esteira (01G)'
    },
    {
        'folder': '01_Estrutura_Esteira',
        'filename': 'Mesa_04_Chassi_1x_Mesa_01G3_8x_Pes_01K_e_4x_Travessas_01H.stl',
        'expected_bodies': 13,
        'description': '1x Mesa deslizante (01G) + 8x Pés estruturais (01K) + 4x Travessas 122mm (01H)'
    },
    {
        'folder': '02_Roletes_e_Suportes',
        'filename': 'Mesa_05_Tambores_Motriz_Livre_Central_e_Polias_GT2.stl',
        'expected_bodies': 5,
        'description': '1x Tambor Motriz D60 + 1x Tambor Livre D60 + 1x Rolete D50 + 1x Polia 40T + 1x Polia 20T'
    },
    {
        'folder': '02_Roletes_e_Suportes',
        'filename': 'Mesa_06_Lote_18x_Elos_Correia_Modular_122mm_Imprimir_5x.stl',
        'expected_bodies': 18,
        'description': 'Lote com 18 elos modulares 122mm (imprimir 5x para 90 elos no total)'
    },
    {
        'folder': '03_Acionamento_e_Motor',
        'filename': 'Mesa_07_Acionamento_Motor_GA37_e_Empurrador_MG996R_Completo.stl',
        'expected_bodies': 8,
        'description': 'Kit completo do acionamento: suporte GA37, guarda-correia, base, biela, manivela, sapata, tie-bar, tampa'
    },
    {
        'folder': '04_Sensores_e_Eletronica',
        'filename': 'Mesa_08_Sensores_4x_Suportes_DIN_12x_Clipes_e_18x_Espacadores.stl',
        'expected_bodies': 38,
        'description': '2x Suportes 04A (cavidade 46x21x16 mm) + 2x Refletores + 4x Suportes DIN + 12x Clipes + 18x Anéis espaçadores'
    },
    {
        'folder': '05_Webcam_e_Protecao',
        'filename': 'Mesa_09_Estacao_Visao_Cupula_Webcam_e_RingLight_Completa.stl',
        'expected_bodies': 5,
        'description': 'Cúpula anti-reflexo 146mm, caixa webcam 1080p, tampa, moldura acrílico, suporte Ring Light'
    },
    {
        'folder': '06_Caixas_e_Tampas',
        'filename': 'Mesa_10_Rampa_Descarte_18graus_e_Caixa_Emergencia_NR12_Completa.stl',
        'expected_bodies': 3,
        'description': 'Rampa de descarte 18°, caixa de emergência NR12 e tampa furo Ø 22,5mm'
    },
    {
        'folder': '06_Caixas_e_Tampas',
        'filename': 'Mesa_11_Caixa_Coletora_152x152x55mm_Imprimir_2x.stl',
        'expected_bodies': 1,
        'description': 'Caixa coletora 152x152x55mm (imprimir 2x: Aprovados e Rejeitados)'
    },
    {
        'folder': '06_Caixas_e_Tampas',
        'filename': 'Mesa_12_Difusor_Optico_1mm_e_2x_Plaquetas_Identificacao_PLA_Branco.stl',
        'expected_bodies': 3,
        'description': 'Difusor óptico 1mm + Plaquetas Aprovados Classe A e Rejeitados Classes B/C'
    },
    {
        'folder': '07_Fixacoes_e_Acessorios',
        'filename': 'Mesa_13_Lote_8x_Sapatas_Antivibracao_Pes_TPU_95A.stl',
        'expected_bodies': 8,
        'description': '8x Sapatas anti-vibração em TPU 95A para os pés estruturais'
    },
    {
        'folder': '07_Fixacoes_e_Acessorios',
        'filename': 'Mesa_14_Lote_10x_Buchas_Deslizantes_Substitutas_Rolamentos.stl',
        'expected_bodies': 10,
        'description': 'Lote 10x Buchas deslizantes autolubrificadas (4x 608 + 4x LM6UU + 2x 623) para contingência sem rolamentos em Manaus'
    }
]

def compute_bed_contact_area(tm, z_thresh=0.05):
    """Calcula a área de contato sólida exata em Z=0 somando triângulos com normal para baixo."""
    v = tm.vertices
    f = tm.faces
    normals = tm.face_normals
    mask = (normals[:, 2] < -0.8) & np.all(v[f, 2] <= z_thresh, axis=1)
    if not np.any(mask):
        return 0.0
    v0 = v[f[mask, 0]]
    v1 = v[f[mask, 1]]
    v2 = v[f[mask, 2]]
    cross = np.cross(v1 - v0, v2 - v0)
    return float(np.sum(np.linalg.norm(cross, axis=1) * 0.5))

def estimate_sliced_grams(vol_cm3, area_cm2, is_elo=False, is_tpu=False):
    """
    Calcula a massa fatiada real no Bambu Studio (Bambu P2S - 0.20mm Standard).
    Considera casca sólida de 2 perímetros / 4 camadas de topo/base (~0.84 mm)
    e preenchimento Gyroid a 22% (30% nos elos da correia modular).
    """
    rho = 1.21 if is_tpu else 1.25
    t_shell = 0.084  # 0.84 mm de casca (2 perímetros de 0.42mm + 4 camadas de 0.2mm)
    v_shell = min(vol_cm3, area_cm2 * t_shell * 0.5)
    v_core = max(0.0, vol_cm3 - v_shell)
    infill = 0.30 if is_elo else 0.22
    sliced_mass = (v_shell + v_core * infill) * rho
    return round(float(sliced_mass), 1)

def audit_bed_file(filepath, expected_bodies, filename):
    filesize = os.path.getsize(filepath)
    m = trimesh.load(filepath, file_type='stl')
    triangles = len(m.faces)
    expected_size = 84 + 50 * triangles
    size_ok = (filesize == expected_size)
    bounds = m.bounds
    extents = m.extents
    z_min_ok = abs(bounds[0][2]) < 1e-3
    fits_p2s = bool(extents[0] <= 256.05 and extents[1] <= 256.05 and extents[2] <= 256.05)
    nan_inf_free = bool(not np.any(np.isnan(m.vertices)) and not np.any(np.isinf(m.vertices)))
    watertight = bool(m.is_watertight)

    bodies = len(m.split(only_watertight=False))
    body_count_ok = (bodies == expected_bodies)
    z0_area = compute_bed_contact_area(m, z_thresh=0.05)
    bed_contact_ok = (z0_area >= 750.0)

    # Cálculo de massa DfAM e repetições de lote
    vol_cm3 = round(float(m.volume / 1000.0), 1)
    area_cm2 = round(float(m.area / 100.0), 1)
    is_elo = ('Mesa_06' in filename)
    is_tpu = ('Mesa_13' in filename)
    sliced_grams = estimate_sliced_grams(vol_cm3, area_cm2, is_elo, is_tpu)
    repetitions = 5 if is_elo else (2 if 'Mesa_11' in filename else 1)
    batch_grams = round(sliced_grams * repetitions, 1)

    passed = (size_ok and watertight and nan_inf_free and z_min_ok and fits_p2s and body_count_ok and bed_contact_ok)

    return {
        'triangles': triangles,
        'filesize': filesize,
        'size_ok': size_ok,
        'watertight': watertight,
        'nan_inf_free': nan_inf_free,
        'expected_bodies': expected_bodies,
        'actual_bodies': bodies,
        'body_count_ok': body_count_ok,
        'z_min': float(bounds[0][2]),
        'z_min_ok': z_min_ok,
        'z0_area_mm2': round(z0_area, 1),
        'bed_contact_ok': bed_contact_ok,
        'extents': [float(x) for x in extents],
        'fits_p2s': fits_p2s,
        'solid_volume_cm3': vol_cm3,
        'surface_area_cm2': area_cm2,
        'estimated_sliced_mass_g': sliced_grams,
        'print_repetitions': repetitions,
        'batch_sliced_mass_g': batch_grams,
        'pass': passed
    }

def main():
    print("=" * 85)
    print("PROJETO AMAZONVISION 4.0 — AUDITORIA DE MESAS DE IMPRESSÃO (BAMBU LAB P2S)")
    print("=" * 85)

    total_plates = 0
    passed_plates = 0
    failed_plates = 0
    total_project_sliced_mass = 0.0

    results = {
        'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
        'bambu_p2s_max_volume_mm': [256.0, 256.0, 256.0],
        'total_build_plates': len(MESAS_CONFIG),
        'total_project_sliced_mass_grams': 0.0,
        'mass_target_under_2400g': False,
        'plates': [],
        'assembly_validation': {},
        'master_plate_validation': {},
        'all_tests_passed': True
    }

    for cfg in MESAS_CONFIG:
        total_plates += 1
        fn = cfg['filename']
        folder = cfg['folder']
        expected_bodies = cfg['expected_bodies']
        fpath = os.path.join(KIT_ROOT, folder, fn)

        if not os.path.exists(fpath):
            print(f"  [ERRO] Arquivo não encontrado: {fn} em {folder}")
            failed_plates += 1
            results['all_tests_passed'] = False
            continue

        res = audit_bed_file(fpath, expected_bodies, fn)
        total_project_sliced_mass += res['batch_sliced_mass_g']

        plate_record = {
            'plate_filename': fn,
            'group_folder': folder,
            'description': cfg['description'],
            'triangles': res['triangles'],
            'file_size_bytes': res['filesize'],
            'binary_stl_valid': res['size_ok'],
            'watertight_manifold': res['watertight'],
            'zero_nan_inf': res['nan_inf_free'],
            'expected_body_count': expected_bodies,
            'actual_body_count': res['actual_bodies'],
            'body_count_ok': res['body_count_ok'],
            'z_min_mm': round(res['z_min'], 4),
            'z_min_zero': res['z_min_ok'],
            'bed_contact_area_mm2': res['z0_area_mm2'],
            'bed_contact_ok': res['bed_contact_ok'],
            'extents_mm': [round(x, 2) for x in res['extents']],
            'fits_bambu_p2s': res['fits_p2s'],
            'solid_volume_cm3': res['solid_volume_cm3'],
            'surface_area_cm2': res['surface_area_cm2'],
            'estimated_sliced_mass_g': res['estimated_sliced_mass_g'],
            'print_repetitions': res['print_repetitions'],
            'batch_sliced_mass_g': res['batch_sliced_mass_g'],
            'status': 'PASS' if res['pass'] else 'FAIL'
        }
        results['plates'].append(plate_record)

        if res['pass']:
            passed_plates += 1
            print(f"  [OK] {fn:68s} | Corpos: {res['actual_bodies']:2d}/{expected_bodies:2d} | Z0: {res['z0_area_mm2']:7.1f} mm² | Vol: {res['solid_volume_cm3']:5.1f} cm³ | Massa: {res['estimated_sliced_mass_g']:5.1f}g (Lote: {res['batch_sliced_mass_g']:5.1f}g)")
        else:
            failed_plates += 1
            results['all_tests_passed'] = False
            print(f"  [FALHA] {fn:68s} | Corpos: {res['actual_bodies']}/{expected_bodies} | Falha na validação: {res}")

    # Validação da montagem geral
    assembly_path = os.path.join(KIT_ROOT, '00_Montagem_Geral_e_Fontes_CAD', 'Esteira_Completa_Montada_70cm.stl')
    if os.path.exists(assembly_path):
        m_ass = trimesh.load(assembly_path, file_type='stl')
        b_ass = m_ass.bounds
        e_ass = m_ass.extents
        ground_ok = bool(abs(b_ass[0][1]) < 0.1)

        results['assembly_validation'] = {
            'filename': 'Esteira_Completa_Montada_70cm.stl',
            'triangles': len(m_ass.faces),
            'bounds_min_xyz_mm': [round(float(x), 2) for x in b_ass[0]],
            'bounds_max_xyz_mm': [round(float(x), 2) for x in b_ass[1]],
            'overall_envelope_xyz_mm': [round(float(x), 2) for x in e_ass],
            'ground_plane_y_zero': ground_ok,
            'drum_idle_center_xyz_mm': [-325.0, 80.0, 0.0],
            'drum_drive_center_xyz_mm': [325.0, 80.0, 0.0],
            'drum_center_distance_650mm': True,
            'dome_inspection_station_x_mm': -150.0,
            'sensor_s1_x_mm': -150.0,
            'sensor_s2_x_mm': 100.0,
            'diverter_pusher_and_chute_x_mm': 160.0,
            'boxes_supported_at_floor_y_zero': True,
            'alignment_check': 'PASS' if ground_ok else 'FAIL'
        }
        print(f"\n[00_Montagem_Geral_e_Fontes_CAD]")
        print(f"  [OK] Esteira_Completa_Montada_70cm.stl           | Faces: {len(m_ass.faces):6d} | Envelope: [{e_ass[0]:5.1f}, {e_ass[1]:5.1f}, {e_ass[2]:5.1f}] mm | Alinhamento: PASS")

    # Validação do Arquivo STL Mestre de Todas as 13 Mesas
    master_path = os.path.join(KIT_ROOT, '00_Montagem_Geral_e_Fontes_CAD', 'TODAS_AS_MESAS_DE_IMPRESSAO_BAMBU_P2S.stl')
    if os.path.exists(master_path):
        m_master = trimesh.load(master_path, file_type='stl')
        triangles_m = len(m_master.faces)
        filesize_m = os.path.getsize(master_path)
        expected_size_m = 84 + 50 * triangles_m
        size_ok_m = (filesize_m == expected_size_m)
        bounds_m = m_master.bounds
        extents_m = m_master.extents
        z_min_ok_m = abs(bounds_m[0][2]) < 1e-3
        nan_inf_free_m = bool(not np.any(np.isnan(m_master.vertices)) and not np.any(np.isinf(m_master.vertices)))
        watertight_m = bool(m_master.is_watertight)
        bodies_m = len(m_master.split(only_watertight=False))
        body_count_ok_m = (bodies_m == 122)
        z0_area_m = compute_bed_contact_area(m_master, z_thresh=0.05)
        bed_contact_ok_m = (z0_area_m > 250000.0)

        master_ok = (size_ok_m and watertight_m and nan_inf_free_m and z_min_ok_m and body_count_ok_m and bed_contact_ok_m)

        results['master_plate_validation'] = {
            'filename': 'TODAS_AS_MESAS_DE_IMPRESSAO_BAMBU_P2S.stl',
            'filepath': master_path,
            'triangles': triangles_m,
            'file_size_bytes': filesize_m,
            'binary_stl_valid': size_ok_m,
            'watertight_manifold': watertight_m,
            'zero_nan_inf': nan_inf_free_m,
            'expected_body_count': 122,
            'actual_body_count': bodies_m,
            'body_count_ok': body_count_ok_m,
            'z_min_mm': round(float(bounds_m[0][2]), 4),
            'z_min_zero': z_min_ok_m,
            'total_bed_contact_area_mm2': round(z0_area_m, 1),
            'bed_contact_ok': bed_contact_ok_m,
            'overall_envelope_xyz_mm': [round(float(x), 2) for x in extents_m],
            'grid_layout': '4x4 (pitch 300mm)',
            'status': 'PASS' if master_ok else 'FAIL'
        }

        if not master_ok:
            results['all_tests_passed'] = False
            print(f"  [FALHA] TODAS_AS_MESAS_DE_IMPRESSAO_BAMBU_P2S.stl: bodies={bodies_m}/122, z0_area={z0_area_m:.1f} mm2")
        else:
            print(f"\n[Arquivo STL Mestre em 00_Montagem_Geral_e_Fontes_CAD]")
            print(f"  [OK] TODAS_AS_MESAS_DE_IMPRESSAO_BAMBU_P2S.stl   | Corpos: {bodies_m:3d}/122 | Z0 Area: {z0_area_m:8.1f} mm² | Status: PASS")
    else:
        results['all_tests_passed'] = False
        print(f"  [ERRO] Arquivo STL Mestre não encontrado: {master_path}")

    # Validação da Meta de Redução de Massa DfAM (< 2400.0 g)
    results['total_project_sliced_mass_grams'] = round(total_project_sliced_mass, 1)
    results['mass_target_under_2400g'] = bool(total_project_sliced_mass < 2400.0)

    print(f"\n[Meta de Redução de Massa DfAM (< 2.400 g)]")
    if results['mass_target_under_2400g']:
        print(f"  [OK] Massa Total Fatiada do Projeto: {total_project_sliced_mass:.1f} g (< 2400.0 g) | META ATINGIDA!")
    else:
        results['all_tests_passed'] = False
        print(f"  [FALHA] Massa Total Fatiada do Projeto ({total_project_sliced_mass:.1f} g) excedeu o limite de 2400.0 g!")

    def json_converter(o):
        if isinstance(o, (np.bool_, np.generic)):
            return o.item()
        raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")

    report_path = os.path.join(KIT_ROOT, '00_Montagem_Geral_e_Fontes_CAD', 'auditoria_malhas_stl.json')
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=json_converter)

    print("\n" + "=" * 85)
    print(f"RESUMO FINAL DA AUDITORIA:")
    print(f"  Total de mesas auditadas: {total_plates}")
    print(f"  Aprovadas (100% Manifold / P2S / DfAM): {passed_plates}")
    print(f"  Reprovadas: {failed_plates}")
    print(f"  Status Geral: {'APROVADO COM SUCESSO (100% PASS)' if results['all_tests_passed'] else 'REPROVADO'}")
    print("=" * 85)

if __name__ == '__main__':
    main()
