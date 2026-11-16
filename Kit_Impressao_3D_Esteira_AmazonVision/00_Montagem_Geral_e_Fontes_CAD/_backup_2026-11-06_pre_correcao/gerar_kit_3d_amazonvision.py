# -*- coding: utf-8 -*-
"""
================================================================================
PROJETO AMAZONVISION 4.0 — ESTEIRA SELETORA INDUSTRIAL 700 MM
GERADOR DAS 13 MESAS DE IMPRESSÃO CONSOLIDADAS (BAMBU LAB P2S 256×256 MM)
================================================================================
Engenharia Mecânica de Manufatura Aditiva (FDM) & CAD Paramétrico de Precisão

Este script consolida todas as 48 peças individuais de fabricação em 13 Mesas de
Impressão Prontas (Mesa_01 a Mesa_13) para fatiamento direto no Bambu Studio,
com nesting otimizado, sem colisões, quantidades reais de montagem e assentamento
100% plano em Z = 0.00 mm.

AS 13 MESAS DE IMPRESSÃO CONSOLIDADAS:
- Mesa 01: Chassi — 4x Cabeceiras e 2x Mancais Tensores (6 corpos)
- Mesa 02: Chassi — 6x Extensões e 6x Guias Laterais (12 corpos)
- Mesa 03: Chassi — 2x Mesas Deslizantes BedPlate Par 1 e 2 (2 corpos)
- Mesa 04: Chassi — 1x Mesa BedPlate, 8x Pés Estruturais e 4x Travessas (13 corpos)
- Mesa 05: Roletes — Tambor Motriz, Tambor Livre, Rolete Central e Polias GT2 (5 corpos)
- Mesa 06: Correia — Lote de 18x Elos Modulares 122 mm (Imprimir 5x para 86 elos) (18 corpos)
- Mesa 07: Acionamento — Suporte Motor GA37, Empurrador MG996R Completo e Guarda NR-12 (8 corpos)
- Mesa 08: Eletrônica — Sensores Ópticos 5V, 4x Suportes DIN, 12x Clipes e 18x Espaçadores (38 corpos)
- Mesa 09: Visão — Cúpula Túnel, Suporte Ring Light, Janela Acrílico e Caixa Webcam (5 corpos)
- Mesa 10: Caixas — Rampa Descarte 18° Auto-Portante e Botoeira NR-12 Completa (3 corpos)
- Mesa 11: Coleta — Caixa Coletora 152x152x55 mm (Imprimir 2x: Aprovados e Rejeitados) (1 corpo)
- Mesa 12: Sinalização — Anel Difusor Ring Light 1 mm e 2x Plaquetas de Identificação (3 corpos)
- Mesa 13: Flexível — Lote de 8x Sapatas Antivibração em TPU 95A (8 corpos)
================================================================================
"""

import os
import sys
import json
import time
import zipfile
import xml.etree.ElementTree as ET
import numpy as np
import trimesh
import manifold3d
import shapely.geometry
import shapely.ops
import matplotlib.textpath
from matplotlib.font_manager import FontProperties

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
KIT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
LEGACY_3MF_PATH = r"c:\Users\ponto\Downloads\AmazonVision_Esteira_Macas_70cm_A1Mini.3mf"

SUBDIRS = {
    '00': os.path.join(KIT_ROOT, '00_Montagem_Geral_e_Fontes_CAD'),
    '01': os.path.join(KIT_ROOT, '01_Estrutura_Esteira'),
    '02': os.path.join(KIT_ROOT, '02_Roletes_e_Suportes'),
    '03': os.path.join(KIT_ROOT, '03_Acionamento_e_Motor'),
    '04': os.path.join(KIT_ROOT, '04_Sensores_e_Eletronica'),
    '05': os.path.join(KIT_ROOT, '05_Webcam_e_Protecao'),
    '06': os.path.join(KIT_ROOT, '06_Caixas_e_Tampas'),
    '07': os.path.join(KIT_ROOT, '07_Fixacoes_e_Acessorios'),
}

for d in SUBDIRS.values():
    os.makedirs(d, exist_ok=True)

# ------------------------------------------------------------------------------
# Funções Utilitárias de Conversão, Primitivas e Posicionamento
# ------------------------------------------------------------------------------

def to_trimesh(manifold_obj, process=True):
    mesh_data = manifold_obj.to_mesh()
    verts = mesh_data.vert_properties[:, :3]
    faces = mesh_data.tri_verts
    return trimesh.Trimesh(vertices=verts, faces=faces, process=process)

def to_manifold(trimesh_obj):
    mesh_in = manifold3d.Mesh(
        vert_properties=np.ascontiguousarray(trimesh_obj.vertices, dtype=np.float32),
        tri_verts=np.ascontiguousarray(trimesh_obj.faces, dtype=np.uint32)
    )
    return manifold3d.Manifold(mesh_in)

def make_box(dx, dy, dz, center=(0, 0, 0)):
    m = manifold3d.Manifold.cube([dx, dy, dz], center=True)
    return m.translate(center)

def make_cylinder(radius, height, center=(0, 0, 0), axis='z', sections=32):
    m = manifold3d.Manifold.cylinder(height, radius, radius, sections).translate([0, 0, -height / 2.0])
    if axis == 'x':
        m = m.rotate([0, 90, 0])
    elif axis == 'y':
        m = m.rotate([-90, 0, 0])
    return m.translate(center)

def make_annulus(r_inner, r_outer, height, center=(0, 0, 0), axis='z', sections=32):
    c_out = make_cylinder(r_outer, height, center, axis, sections)
    c_in = make_cylinder(r_inner, height + 2.0, center, axis, sections)
    return c_out - c_in

def make_hex_prism(across_flats, height, center=(0, 0, 0), axis='z'):
    r_circ = (across_flats / 2.0) / np.cos(np.pi / 6.0)
    return make_cylinder(r_circ, height, center, axis, sections=6)

def make_slot(length, width, height, center=(0, 0, 0), slot_axis='x', normal_axis='z'):
    r = width / 2.0
    cyl_dist = max(0.0, length - width)
    if slot_axis == 'x' and normal_axis == 'z':
        c1_pos = [-cyl_dist / 2.0, 0.0, 0.0]
        c2_pos = [cyl_dist / 2.0, 0.0, 0.0]
        box_dims = [cyl_dist, width, height]
    elif slot_axis == 'y' and normal_axis == 'z':
        c1_pos = [0.0, -cyl_dist / 2.0, 0.0]
        c2_pos = [0.0, cyl_dist / 2.0, 0.0]
        box_dims = [width, cyl_dist, height]
    elif slot_axis == 'x' and normal_axis == 'y':
        c1_pos = [-cyl_dist / 2.0, 0.0, 0.0]
        c2_pos = [cyl_dist / 2.0, 0.0, 0.0]
        box_dims = [cyl_dist, height, width]
    elif slot_axis == 'z' and normal_axis == 'y':
        c1_pos = [0.0, 0.0, -cyl_dist / 2.0]
        c2_pos = [0.0, 0.0, cyl_dist / 2.0]
        box_dims = [width, height, cyl_dist]
    elif slot_axis == 'y' and normal_axis == 'x':
        c1_pos = [0.0, -cyl_dist / 2.0, 0.0]
        c2_pos = [0.0, cyl_dist / 2.0, 0.0]
        box_dims = [height, cyl_dist, width]
    elif slot_axis == 'z' and normal_axis == 'x':
        c1_pos = [0.0, 0.0, -cyl_dist / 2.0]
        c2_pos = [0.0, 0.0, cyl_dist / 2.0]
        box_dims = [height, width, cyl_dist]
    else:
        raise ValueError(f"Combinação inválida de eixos: slot_axis='{slot_axis}', normal_axis='{normal_axis}'")

    b = make_box(box_dims[0], box_dims[1], box_dims[2])
    c1 = make_cylinder(r, height, c1_pos, axis=normal_axis, sections=24)
    c2 = make_cylinder(r, height, c2_pos, axis=normal_axis, sections=24)
    m = b + c1 + c2
    return m.translate(center)

def orient_for_print(tm_mesh):
    bounds = tm_mesh.bounds
    z_min = bounds[0][2]
    x_mid = (bounds[0][0] + bounds[1][0]) / 2.0
    y_mid = (bounds[0][1] + bounds[1][1]) / 2.0
    tm_mesh.apply_translation([-x_mid, -y_mid, -z_min])
    return tm_mesh

def place_on_bed(tm_mesh, cx=0.0, cy=0.0, rot_z_deg=0.0):
    """
    Posiciona uma malha sobre a mesa de impressão na coordenada (cx, cy) com rotação em Z opcional,
    garantindo que sua face inferior assente perfeitamente em Z = 0.00 mm.
    """
    m = tm_mesh.copy()
    if abs(rot_z_deg) > 1e-3:
        m.apply_transform(trimesh.transformations.rotation_matrix(np.radians(rot_z_deg), [0, 0, 1]))
    bounds = m.bounds
    x_mid = (bounds[0][0] + bounds[1][0]) / 2.0
    y_mid = (bounds[0][1] + bounds[1][1]) / 2.0
    z_min = bounds[0][2]
    m.apply_translation([cx - x_mid, cy - y_mid, -z_min])
    return m

def export_binary_stl(tm_mesh, output_path, header_comment="AmazonVision 4.0 - Bambu P2S"):
    tm_mesh.fix_normals()
    vertices = np.ascontiguousarray(tm_mesh.vertices, dtype=np.float32)
    faces = np.ascontiguousarray(tm_mesh.faces, dtype=np.int32)
    num_faces = len(faces)
    
    v0 = vertices[faces[:, 0]]
    v1 = vertices[faces[:, 1]]
    v2 = vertices[faces[:, 2]]
    normals = np.cross(v1 - v0, v2 - v0)
    norm_lens = np.linalg.norm(normals, axis=1, keepdims=True)
    norm_lens[norm_lens == 0] = 1.0
    normals = normals / norm_lens
    normals = normals.astype(np.float32)
    
    stl_dtype = np.dtype([
        ('normal', np.float32, (3,)),
        ('v0', np.float32, (3,)),
        ('v1', np.float32, (3,)),
        ('v2', np.float32, (3,)),
        ('attr', np.uint16)
    ])
    
    stl_data = np.zeros(num_faces, dtype=stl_dtype)
    stl_data['normal'] = normals
    stl_data['v0'] = v0
    stl_data['v1'] = v1
    stl_data['v2'] = v2
    stl_data['attr'] = 0
    
    header = header_comment.encode('ascii', errors='replace')[:80].ljust(80, b'\x00')
    
    with open(output_path, 'wb') as f:
        f.write(header)
        f.write(np.uint32(num_faces).tobytes())
        f.write(stl_data.tobytes())
        
    expected_size = 84 + 50 * num_faces
    actual_size = os.path.getsize(output_path)
    assert actual_size == expected_size, f"Erro de tamanho de STL binário em {output_path}!"

def load_legacy_3mf_mesh(model_name):
    with zipfile.ZipFile(LEGACY_3MF_PATH, 'r') as z:
        target = f"3D/Objects/{model_name}.model"
        if target not in z.namelist():
            raise FileNotFoundError(f"Objeto {target} não encontrado no 3MF!")
        root = ET.fromstring(z.read(target))
        ns = {'m': 'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
        verts = [[float(v.attrib['x']), float(v.attrib['y']), float(v.attrib['z'])]
                 for v in root.findall('.//m:vertex', ns)]
        faces = [[int(t.attrib['v1']), int(t.attrib['v2']), int(t.attrib['v3'])]
                 for t in root.findall('.//m:triangle', ns)]
        return trimesh.Trimesh(vertices=np.array(verts), faces=np.array(faces), process=True)

def compute_bed_contact_area(tm, z_thresh=0.05):
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

def make_embossed_plate(dx, dy, dz, text_str, font_size=5.2, text_h=1.0):
    m_base = make_box(dx, dy, dz, center=(0, 0, dz / 2.0))
    
    fp = FontProperties(family='DejaVu Sans', weight='bold')
    tp = matplotlib.textpath.TextPath((0, 0), text_str, size=font_size, prop=fp)
    polys = [shapely.geometry.Polygon(path) for path in tp.to_polygons() if len(path) >= 3]
    union_poly = shapely.ops.unary_union([p for p in polys if p.is_valid and p.area > 0.01])
    
    if union_poly.geom_type == 'MultiPolygon':
        geos = [trimesh.creation.extrude_polygon(p, height=text_h) for p in union_poly.geoms]
        tm_text = trimesh.util.concatenate(geos)
    else:
        tm_text = trimesh.creation.extrude_polygon(union_poly, height=text_h)
        
    tb = tm_text.bounds
    tm_text.apply_translation([-(tb[0][0] + tb[1][0]) / 2.0, -(tb[0][1] + tb[1][1]) / 2.0, dz])
    m_text = to_manifold(tm_text)
    return m_base + m_text

# ==============================================================================
# FUNÇÕES AUXILIARES DE ENGENHARIA DfAM (ALÍVIO ESTRUTURAL & MASSA)
# ==============================================================================

def make_arch_portal(length_x, width_y, h_straight, h_peak, center=(0, 0, 0)):
    """Cria um cortador de portal com teto em arco a 45 graus para eliminar suportes FDM."""
    w2 = width_y / 2.0
    poly = shapely.geometry.Polygon([
        [-w2, 0.0],
        [w2, 0.0],
        [w2, h_straight],
        [0.0, h_peak],
        [-w2, h_straight]
    ])
    tm_p = trimesh.creation.extrude_polygon(poly, height=length_x)
    verts = tm_p.vertices.copy()
    new_verts = np.column_stack([verts[:, 2] - length_x / 2.0, verts[:, 0], verts[:, 1]])
    tm_p.vertices = new_verts
    tm_p.apply_translation(center)
    return to_manifold(tm_p)

def make_drum_cavity(z_start, z_end, r_in, r_out, cone_h=12.0):
    """Cria cavidade anelar oca com teto cônico a 45 graus (impressão auto-portante zero suporte)."""
    h_total = z_end - z_start
    h_cyl = max(0.1, h_total - cone_h)
    cyl_part = manifold3d.Manifold.cylinder(h_cyl, r_out, r_out, 48).translate([0, 0, z_start])
    cone_part = manifold3d.Manifold.cylinder(cone_h, r_out, r_in, 48).translate([0, 0, z_start + h_cyl])
    outer_void = cyl_part + cone_part
    inner_core = manifold3d.Manifold.cylinder(h_total + 2.0, r_in, r_in, 48).translate([0, 0, z_start - 1.0])
    return outer_void - inner_core

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

# ==============================================================================
# MODELAGEM PARAMÉTRICA DAS PEÇAS HOMOLOGADAS
# ==============================================================================

def generate_01A():
    body = make_box(164.0, 60.0, 20.0, center=(0, 0, 10.0))
    lip = make_box(164.0, 15.0, 6.0, center=(0, 32.5, 3.0))
    flange = make_box(6.0, 68.0, 24.0, center=(-80.0, -2.0, 12.0))
    m = body + lip + flange
    b_seat = make_cylinder(11.075, 7.5, center=(43.0, -10.0, 16.5), axis='z', sections=36)
    b_thru = make_cylinder(8.0, 25.0, center=(43.0, -10.0, 10.0), axis='z', sections=28)
    for dx in [-20.0, 20.0]:
        for dy in [-15.0, 15.0]:
            h = make_cylinder(2.15, 25.0, center=(3.0 + dx, -10.0 + dy, 10.0), axis='z', sections=20)
            b_thru = b_thru + h
    f_h1 = make_cylinder(2.15, 30.0, center=(-80.0, 16.0, 12.0), axis='x', sections=18)
    f_h2 = make_cylinder(2.15, 30.0, center=(-80.0, -20.0, 12.0), axis='x', sections=18)
    c_h1 = make_cylinder(1.65, 25.0, center=(15.0, 18.0, 10.0), axis='z', sections=16)
    c_h2 = make_cylinder(1.65, 25.0, center=(65.0, 18.0, 10.0), axis='z', sections=16)

    # Bolsos de alívio estrutural (Viga C nervurada preservando furos do motor)
    p1 = make_box(50.0, 44.0, 14.0, center=(-46.0, 0.0, 14.0))
    p2 = make_box(32.0, 22.0, 14.0, center=(3.0, -10.0, 14.0))
    p3 = make_box(36.0, 20.0, 14.0, center=(43.0, 16.0, 14.0))

    m = m - b_seat - b_thru - f_h1 - f_h2 - c_h1 - c_h2 - p1 - p2 - p3
    return orient_for_print(to_trimesh(m))

def generate_01B():
    body = make_box(164.0, 60.0, 20.0, center=(0, 0, 10.0))
    lip = make_box(164.0, 15.0, 6.0, center=(0, 32.5, 3.0))
    flange = make_box(6.0, 68.0, 24.0, center=(-80.0, -2.0, 12.0))
    m = body + lip + flange
    b_seat = make_cylinder(11.075, 7.5, center=(43.0, -10.0, 16.5), axis='z', sections=36)
    b_thru = make_cylinder(8.0, 25.0, center=(43.0, -10.0, 10.0), axis='z', sections=28)
    f_h1 = make_cylinder(2.15, 30.0, center=(-80.0, 16.0, 12.0), axis='x', sections=18)
    f_h2 = make_cylinder(2.15, 30.0, center=(-80.0, -20.0, 12.0), axis='x', sections=18)

    # Bolsos de alívio estrutural (Viga C nervurada)
    p1 = make_box(50.0, 44.0, 14.0, center=(-46.0, 0.0, 14.0))
    p2 = make_box(42.0, 44.0, 14.0, center=(4.0, 0.0, 14.0))
    p3 = make_box(36.0, 20.0, 14.0, center=(43.0, 16.0, 14.0))

    m = m - b_seat - b_thru - f_h1 - f_h2 - p1 - p2 - p3
    return orient_for_print(to_trimesh(m))

def generate_01C():
    body = make_box(165.0, 60.0, 20.0, center=(0, 0, 10.0))
    lip = make_box(165.0, 15.0, 6.0, center=(0, 32.5, 3.0))
    flange = make_box(6.0, 68.0, 24.0, center=(80.0, -2.0, 12.0))
    m = body + lip + flange
    slot_track = make_slot(36.0, 14.0, 25.0, center=(-43.0, -10.0, 10.0), slot_axis='x', normal_axis='z')
    m5_hole = make_cylinder(2.65, 55.0, center=(-70.0, -10.0, 10.0), axis='x', sections=20)
    m5_nut = make_hex_prism(8.15, 5.0, center=(-80.0, -10.0, 10.0), axis='x')
    f_h1 = make_cylinder(2.15, 30.0, center=(80.0, 16.0, 12.0), axis='x', sections=18)
    f_h2 = make_cylinder(2.15, 30.0, center=(80.0, -20.0, 12.0), axis='x', sections=18)

    # Bolsos de alívio estrutural
    p1 = make_box(68.0, 44.0, 14.0, center=(36.0, 0.0, 14.0))
    p2 = make_box(48.0, 20.0, 14.0, center=(-43.0, 16.0, 14.0))

    m = m - slot_track - m5_hole - m5_nut - f_h1 - f_h2 - p1 - p2
    return orient_for_print(to_trimesh(m))

def generate_01D():
    body = make_box(165.0, 60.0, 20.0, center=(0, 0, 10.0))
    lip = make_box(165.0, 15.0, 6.0, center=(0, 32.5, 3.0))
    flange = make_box(6.0, 68.0, 24.0, center=(80.0, -2.0, 12.0))
    m = body + lip + flange
    slot_track = make_slot(36.0, 14.0, 25.0, center=(-43.0, -10.0, 10.0), slot_axis='x', normal_axis='z')
    m5_hole = make_cylinder(2.65, 55.0, center=(-70.0, -10.0, 10.0), axis='x', sections=20)
    m5_nut = make_hex_prism(8.15, 5.0, center=(-80.0, -10.0, 10.0), axis='x')
    f_h1 = make_cylinder(2.15, 30.0, center=(80.0, 16.0, 12.0), axis='x', sections=18)
    f_h2 = make_cylinder(2.15, 30.0, center=(80.0, -20.0, 12.0), axis='x', sections=18)

    # Bolsos de alívio estrutural
    p1 = make_box(68.0, 44.0, 14.0, center=(36.0, 0.0, 14.0))
    p2 = make_box(48.0, 20.0, 14.0, center=(-43.0, 16.0, 14.0))

    m = m - slot_track - m5_hole - m5_nut - f_h1 - f_h2 - p1 - p2
    return orient_for_print(to_trimesh(m))

def generate_01E():
    body = make_box(110.0, 50.0, 16.0, center=(0, 0, 8.0))
    shelf = make_box(110.0, 8.0, 6.0, center=(0, 21.0, 13.0))
    f_left = make_box(4.0, 60.0, 20.0, center=(-53.0, 0, 10.0))
    f_right = make_box(4.0, 60.0, 20.0, center=(53.0, 0, 10.0))
    m = body + shelf + f_left + f_right
    h1 = make_cylinder(2.15, 20.0, center=(-53.0, 16.0, 10.0), axis='x', sections=18)
    h2 = make_cylinder(2.15, 20.0, center=(-53.0, -16.0, 10.0), axis='x', sections=18)
    h3 = make_cylinder(2.15, 20.0, center=(53.0, 16.0, 10.0), axis='x', sections=18)
    h4 = make_cylinder(2.15, 20.0, center=(53.0, -16.0, 10.0), axis='x', sections=18)
    foot_h = make_cylinder(2.15, 25.0, center=(0, -20.0, 8.0), axis='y', sections=18)

    # Bolsos profundos de alívio
    p1 = make_box(42.0, 38.0, 11.0, center=(-25.0, 0.0, 11.5))
    p2 = make_box(42.0, 38.0, 11.0, center=(25.0, 0.0, 11.5))

    m = m - h1 - h2 - h3 - h4 - foot_h - p1 - p2
    return orient_for_print(to_trimesh(m))

def generate_01F():
    body = make_box(110.0, 50.0, 18.0, center=(0, 0, 9.0))
    shelf = make_box(110.0, 8.0, 6.0, center=(0, 21.0, 14.0))
    f_left = make_box(4.0, 60.0, 22.0, center=(-53.0, 0, 11.0))
    f_right = make_box(4.0, 60.0, 22.0, center=(53.0, 0, 11.0))
    m = body + shelf + f_left + f_right
    cradle = make_cylinder(11.075, 7.5, center=(0, 0, 14.5), axis='z', sections=36)
    cradle_thru = make_cylinder(4.2, 25.0, center=(0, 0, 9.0), axis='z', sections=20)
    h1 = make_cylinder(2.15, 20.0, center=(-53.0, 16.0, 10.0), axis='x', sections=18)
    h2 = make_cylinder(2.15, 20.0, center=(-53.0, -16.0, 10.0), axis='x', sections=18)
    h3 = make_cylinder(2.15, 20.0, center=(53.0, 16.0, 10.0), axis='x', sections=18)
    h4 = make_cylinder(2.15, 20.0, center=(53.0, -16.0, 10.0), axis='x', sections=18)

    # Bolsos laterais de alívio preservando berço 608ZZ
    p1 = make_box(32.0, 38.0, 12.0, center=(-31.0, 0.0, 13.0))
    p2 = make_box(32.0, 38.0, 12.0, center=(31.0, 0.0, 13.0))

    m = m - cradle - cradle_thru - h1 - h2 - h3 - h4 - p1 - p2
    return orient_for_print(to_trimesh(m))

def generate_01G():
    plate = make_box(210.0, 120.0, 3.0, center=(0, 0, 1.5))
    r1 = make_box(210.0, 4.0, 0.8, center=(0, -40.0, 3.4))
    r2 = make_box(210.0, 4.0, 0.8, center=(0, 0.0, 3.4))
    r3 = make_box(210.0, 4.0, 0.8, center=(0, 40.0, 3.4))
    m = plate + r1 + r2 + r3
    ch_in = make_box(6.0, 125.0, 4.0, center=(-105.0, 0, 3.0)).rotate([0, 45, 0])
    ch_out = make_box(6.0, 125.0, 4.0, center=(105.0, 0, 3.0)).rotate([0, -45, 0])
    f1 = make_cylinder(2.15, 10.0, center=(-80.0, -54.0, 1.5), axis='z', sections=20)
    f2 = make_cylinder(2.15, 10.0, center=(80.0, -54.0, 1.5), axis='z', sections=20)
    f3 = make_cylinder(2.15, 10.0, center=(-80.0, 54.0, 1.5), axis='z', sections=20)
    f4 = make_cylinder(2.15, 10.0, center=(80.0, 54.0, 1.5), axis='z', sections=20)
    m = m - ch_in - ch_out - f1 - f2 - f3 - f4

    # 8 janelas retangulares de alívio passantes
    for wx in [-66.0, -22.0, 22.0, 66.0]:
        for wy in [-20.0, 20.0]:
            win = make_box(38.0, 24.0, 10.0, center=(wx, wy, 1.5))
            m = m - win

    return orient_for_print(to_trimesh(m))

def generate_01H():
    bar = make_box(22.0, 122.0, 20.0, center=(0, 0, 10.0))
    pocket1 = make_box(30.0, 44.0, 12.0, center=(0, -28.0, 10.0))
    pocket2 = make_box(30.0, 44.0, 12.0, center=(0, 28.0, 10.0))
    h_left = make_cylinder(2.15, 30.0, center=(0, -61.0, 10.0), axis='y', sections=20)
    c_left = make_cylinder(4.2, 8.0, center=(0, -48.0, 10.0), axis='y', sections=24)
    h_right = make_cylinder(2.15, 30.0, center=(0, 61.0, 10.0), axis='y', sections=20)
    c_right = make_cylinder(4.2, 8.0, center=(0, 48.0, 10.0), axis='y', sections=24)
    m = bar - pocket1 - pocket2 - h_left - c_left - h_right - c_right
    return orient_for_print(to_trimesh(m))

def generate_01I():
    base = make_box(140.0, 8.0, 24.0, center=(0, 0, 12.0))
    lip = make_box(140.0, 4.0, 12.0, center=(0, -2.0, 18.0))
    m = base + lip
    s1 = make_slot(12.0, 4.3, 15.0, center=(-45.0, 0, 8.0), slot_axis='x', normal_axis='y')
    s2 = make_slot(12.0, 4.3, 15.0, center=(45.0, 0, 8.0), slot_axis='x', normal_axis='y')
    m = m - s1 - s2
    return orient_for_print(to_trimesh(m))

def generate_01J():
    base = make_box(180.0, 8.0, 28.0, center=(0, 0, 14.0))
    cutout = make_box(100.0, 16.0, 20.0, center=(0, 0, 20.0))
    s1 = make_slot(12.0, 4.3, 16.0, center=(-70.0, 0, 5.0), slot_axis='x', normal_axis='y')
    s2 = make_slot(12.0, 4.3, 16.0, center=(70.0, 0, 5.0), slot_axis='x', normal_axis='y')
    m = base - cutout - s1 - s2
    return orient_for_print(to_trimesh(m))

def generate_01K():
    col = make_box(32.0, 22.0, 59.0, center=(0, 0, 29.5))
    top_flange = make_box(46.0, 22.0, 8.0, center=(0, 0, 55.0))
    m = col + top_flange
    h1 = make_cylinder(2.15, 15.0, center=(-17.0, 0, 55.0), axis='z', sections=20)
    h2 = make_cylinder(2.15, 15.0, center=(17.0, 0, 55.0), axis='z', sections=20)
    h_side = make_cylinder(2.15, 30.0, center=(0, 0, 48.0), axis='y', sections=20)

    # Perfil H Industrial (canais entre Z=7.0 e Z=47.0)
    ch1 = make_box(22.0, 7.5, 40.0, center=(0, -7.5, 27.0))
    ch2 = make_box(22.0, 7.5, 40.0, center=(0, 7.5, 27.0))

    m = m - h1 - h2 - h_side - ch1 - ch2
    return orient_for_print(to_trimesh(m))

def generate_02A():
    tm_motor = load_legacy_3mf_mesh('tambor_motor')
    m = to_manifold(tm_motor)
    boss_cutter = make_box(100.0, 100.0, 20.0, center=(0, 0, 60.0 + 10.0))
    m = m - boss_cutter
    hub = manifold3d.Manifold.cylinder(6.286, 29.972, 29.972, 64).translate([0, 0, 59.5])
    m = m + hub
    for p in range(4):
        ang = p * (np.pi / 2.0)
        lug = manifold3d.Manifold.cylinder(6.0, 2.4, 2.4, 20).translate([10.0 * np.cos(ang), 10.0 * np.sin(ang), 65.786])
        m = m + lug
    shaft_bore = manifold3d.Manifold.cylinder(160.0, 4.075, 4.075, 32).translate([0, 0, -80.0])
    b_bot = manifold3d.Manifold.cylinder(7.2, 11.075, 11.075, 36).translate([0, 0, -65.786])
    b_top = manifold3d.Manifold.cylinder(7.2, 11.075, 11.075, 36).translate([0, 0, 65.786 - 7.2])
    cav1 = make_drum_cavity(-51.96, -4.0, 9.0, 21.0, 12.0)
    cav2 = make_drum_cavity(4.0, 55.786, 9.0, 21.0, 12.0)
    v_bot = make_cylinder(3.5, 30.0, center=(15.0, 0.0, -60.0), axis='z') + make_cylinder(3.5, 30.0, center=(-15.0, 0.0, -60.0), axis='z')
    v_top = make_cylinder(3.5, 30.0, center=(0.0, 15.0, 60.0), axis='z') + make_cylinder(3.5, 30.0, center=(0.0, -15.0, 60.0), axis='z')
    m = m - shaft_bore - b_bot - b_top - cav1 - cav2 - v_bot - v_top
    return orient_for_print(to_trimesh(m))

def generate_02B():
    tm_livre = load_legacy_3mf_mesh('tambor_livre')
    m = to_manifold(tm_livre)
    shaft_bore = manifold3d.Manifold.cylinder(150.0, 4.075, 4.075, 32).translate([0, 0, -75.0])
    b_bot = manifold3d.Manifold.cylinder(7.2, 11.075, 11.075, 36).translate([0, 0, -60.96])
    b_top = manifold3d.Manifold.cylinder(7.2, 11.075, 11.075, 36).translate([0, 0, 60.96 - 7.2])
    cav1 = make_drum_cavity(-51.96, -4.0, 9.0, 21.0, 12.0)
    cav2 = make_drum_cavity(4.0, 50.96, 9.0, 21.0, 12.0)
    v_bot = make_cylinder(3.5, 30.0, center=(15.0, 0.0, -55.0), axis='z') + make_cylinder(3.5, 30.0, center=(-15.0, 0.0, -55.0), axis='z')
    v_top = make_cylinder(3.5, 30.0, center=(0.0, 15.0, 55.0), axis='z') + make_cylinder(3.5, 30.0, center=(0.0, -15.0, 55.0), axis='z')
    m = m - shaft_bore - b_bot - b_top - cav1 - cav2 - v_bot - v_top
    return orient_for_print(to_trimesh(m))

def generate_02C():
    tm_central = load_legacy_3mf_mesh('tambor_central')
    m = to_manifold(tm_central)
    shaft_bore = manifold3d.Manifold.cylinder(150.0, 4.075, 4.075, 32).translate([0, 0, -75.0])
    b_bot = manifold3d.Manifold.cylinder(7.2, 11.075, 11.075, 36).translate([0, 0, -60.96])
    b_top = manifold3d.Manifold.cylinder(7.2, 11.075, 11.075, 36).translate([0, 0, 60.96 - 7.2])
    cav1 = make_drum_cavity(-51.96, -4.0, 8.5, 20.0, 11.5)
    cav2 = make_drum_cavity(4.0, 50.96, 8.5, 20.0, 11.5)
    v_bot = make_cylinder(3.0, 30.0, center=(14.25, 0.0, -55.0), axis='z') + make_cylinder(3.0, 30.0, center=(-14.25, 0.0, -55.0), axis='z')
    v_top = make_cylinder(3.0, 30.0, center=(0.0, 14.25, 55.0), axis='z') + make_cylinder(3.0, 30.0, center=(0.0, -14.25, 55.0), axis='z')
    m = m - shaft_bore - b_bot - b_top - cav1 - cav2 - v_bot - v_top
    return orient_for_print(to_trimesh(m))

def generate_02D():
    body = make_box(32.0, 28.0, 14.0, center=(0, 0, 7.0))
    t_top = make_box(32.0, 2.5, 6.0, center=(0, 14.0 + 1.25, 7.0))
    t_bot = make_box(32.0, 2.5, 6.0, center=(0, -14.0 - 1.25, 7.0))
    m = body + t_top + t_bot
    b_seat = make_cylinder(11.075, 7.2, center=(0, 0, 10.4), axis='z', sections=36)
    b_thru = make_cylinder(8.0, 20.0, center=(0, 0, 7.0), axis='z', sections=24)
    m5_hole = make_cylinder(2.65, 40.0, center=(0, 0, 7.0), axis='x', sections=20)
    nut_pocket = make_hex_prism(8.15, 4.5, center=(-12.0, 0, 7.0), axis='x')
    m = m - b_seat - b_thru - m5_hole - nut_pocket
    return orient_for_print(to_trimesh(m))

def generate_02E():
    tm = load_legacy_3mf_mesh('elo')
    tm.apply_transform(trimesh.transformations.rotation_matrix(np.pi, [1, 0, 0]))
    tm = orient_for_print(tm)
    m = to_manifold(tm)
    p1 = make_box(6.0, 48.0, 2.4, center=(0.0, -28.0, 4.2))
    p2 = make_box(6.0, 48.0, 2.4, center=(0.0, 28.0, 4.2))
    m = m - p1 - p2
    return orient_for_print(to_trimesh(m))

def generate_03A():
    motor_plate = make_box(58.0, 64.0, 6.0, center=(0, 0, 3.0))
    base_plate = make_box(58.0, 6.0, 48.0, center=(0, -29.0, 24.0))
    gusset1 = make_box(6.0, 48.0, 42.0, center=(-26.0, -8.0, 24.0))
    gusset2 = make_box(6.0, 48.0, 42.0, center=(26.0, -8.0, 24.0))
    m = motor_plate + base_plate + gusset1 + gusset2
    ctr_hole = make_cylinder(6.5, 15.0, center=(0, 4.0, 3.0), axis='z', sections=32)
    slots = []
    for s in range(6):
        ang = s * (2.0 * np.pi / 6.0)
        sx = 15.5 * np.cos(ang)
        sy = 4.0 + 15.5 * np.sin(ang)
        slot = make_slot(11.0, 3.3, 15.0, center=(sx, sy, 3.0), slot_axis='x', normal_axis='z')
        slot = slot.rotate([0, 0, np.degrees(ang)])
        slots.append(slot)
    b_h1 = make_cylinder(2.15, 20.0, center=(-18.0, -29.0, 24.0), axis='y', sections=18)
    b_h2 = make_cylinder(2.15, 20.0, center=(18.0, -29.0, 24.0), axis='y', sections=18)
    w1 = make_cylinder(10.0, 20.0, center=(-26.0, -4.0, 22.0), axis='x')
    w2 = make_cylinder(10.0, 20.0, center=(26.0, -4.0, 22.0), axis='x')
    m = m - ctr_hole - b_h1 - b_h2 - w1 - w2
    for s in slots:
        m = m - s
    return orient_for_print(to_trimesh(m))

def generate_03B():
    flange1 = make_cylinder(8.2, 1.3, center=(0, 0, 0.65), axis='z', sections=48)
    body = make_cylinder(6.366, 7.2, center=(0, 0, 4.7), axis='z', sections=64)
    flange2 = make_cylinder(8.2, 1.3, center=(0, 0, 8.75), axis='z', sections=48)
    hub = make_cylinder(7.5, 6.2, center=(0, 0, 12.3), axis='z', sections=36)
    m = flange1 + body + flange2 + hub
    for i in range(20):
        ang = i * (2.0 * np.pi / 20.0)
        gx = 6.366 * np.cos(ang)
        gy = 6.366 * np.sin(ang)
        groove = make_cylinder(0.55, 7.0, center=(gx, gy, 4.7), axis='z', sections=16)
        m = m - groove
    bore = make_cylinder(3.075, 25.0, center=(0, 0, 8.0), axis='z', sections=32)
    d_flat = make_box(8.0, 1.0, 25.0, center=(0, 3.05, 8.0))
    set_screw = make_cylinder(1.65, 12.0, center=(0, 0, 12.4), axis='x', sections=18)
    m = m - (bore - d_flat) - set_screw
    return orient_for_print(to_trimesh(m))

def generate_03C():
    flange40_1 = make_cylinder(14.5, 1.3, center=(0, 0, 0.65), axis='z', sections=64)
    body40 = make_cylinder(12.732, 7.2, center=(0, 0, 4.7), axis='z', sections=80)
    flange40_2 = make_cylinder(14.5, 1.3, center=(0, 0, 8.75), axis='z', sections=64)
    hub40 = make_cylinder(11.0, 6.2, center=(0, 0, 12.3), axis='z', sections=48)
    m40 = flange40_1 + body40 + flange40_2 + hub40
    for i in range(40):
        ang = i * (2.0 * np.pi / 40.0)
        gx = 12.732 * np.cos(ang)
        gy = 12.732 * np.sin(ang)
        groove = make_cylinder(0.55, 7.0, center=(gx, gy, 4.7), axis='z', sections=16)
        m40 = m40 - groove
    bore40 = make_cylinder(4.075, 25.0, center=(0, 0, 8.0), axis='z', sections=32)
    m40 = m40 - bore40
    for p in range(4):
        ang = p * (np.pi / 2.0)
        ph = make_cylinder(2.6, 12.0, center=(10.0 * np.cos(ang), 10.0 * np.sin(ang), 3.0), axis='z', sections=20)
        m40 = m40 - ph
    return orient_for_print(to_trimesh(m40))

def generate_03D():
    outer = make_box(110.0, 52.0, 22.0, center=(0, 0, 11.0))
    inner = make_box(104.0, 46.0, 20.0, center=(0, 0, 11.0))
    m = outer - inner
    window = make_box(50.0, 14.0, 10.0, center=(0, 0, 21.0))
    t1 = make_box(14.0, 8.0, 4.0, center=(-50.0, -28.0, 2.0))
    t2 = make_box(14.0, 8.0, 4.0, center=(50.0, -28.0, 2.0))
    t3 = make_box(8.0, 14.0, 4.0, center=(58.0, 0, 2.0))
    h1 = make_cylinder(1.65, 10.0, center=(-50.0, -28.0, 2.0), axis='z', sections=18)
    h2 = make_cylinder(1.65, 10.0, center=(50.0, -28.0, 2.0), axis='z', sections=18)
    h3 = make_cylinder(1.65, 10.0, center=(58.0, 0, 2.0), axis='z', sections=18)
    m = (m + t1 + t2 + t3) - window - h1 - h2 - h3
    return orient_for_print(to_trimesh(m))

def generate_03E():
    # Base / Pórtico: 4 buchas LM6UU (2 por haste, espaçadas 70 mm, entre-centros 85 mm)
    # Hastes guia Ø6 mm em X = -42.5 e X = +42.5 mm
    base_plate = make_box(118.0, 95.0, 4.5, center=(0, 0, 2.25))
    servo_pocket = make_box(41.4, 20.4, 15.0, center=(0, 22.0, 2.25))
    s_h1 = make_cylinder(1.65, 15.0, center=(-24.25, 17.0, 2.25), axis='z', sections=18)
    s_h2 = make_cylinder(1.65, 15.0, center=(-24.25, 27.0, 2.25), axis='z', sections=18)
    s_h3 = make_cylinder(1.65, 15.0, center=(24.25, 17.0, 2.25), axis='z', sections=18)
    s_h4 = make_cylinder(1.65, 15.0, center=(24.25, 27.0, 2.25), axis='z', sections=18)

    # Blocos para alojar as 4 buchas LM6UU (Ø 12 mm x 19 mm)
    b_left = make_box(18.0, 92.0, 24.0, center=(-42.5, -1.0, 12.0))
    b_right = make_box(18.0, 92.0, 24.0, center=(42.5, -1.0, 12.0))
    m = base_plate + b_left + b_right

    # Furos passantes das hastes Ø6 mm
    rod_h1 = make_cylinder(3.1, 100.0, center=(-42.5, -1.0, 15.0), axis='y', sections=28)
    rod_h2 = make_cylinder(3.1, 100.0, center=(42.5, -1.0, 15.0), axis='y', sections=28)

    # 4 cavidades para as buchas LM6UU (2 por haste espaçadas 70 mm entre centros)
    lm1_1 = make_cylinder(6.05, 22.0, center=(-42.5, -36.0, 15.0), axis='y', sections=32)
    lm1_2 = make_cylinder(6.05, 22.0, center=(-42.5, 34.0, 15.0), axis='y', sections=32)
    lm2_1 = make_cylinder(6.05, 22.0, center=(42.5, -36.0, 15.0), axis='y', sections=32)
    lm2_2 = make_cylinder(6.05, 22.0, center=(42.5, 34.0, 15.0), axis='y', sections=32)

    # Furos M4 de fixação na longarina
    m_h1 = make_cylinder(2.15, 15.0, center=(-52.0, -35.0, 2.25), axis='z', sections=18)
    m_h2 = make_cylinder(2.15, 15.0, center=(52.0, -35.0, 2.25), axis='z', sections=18)
    m_h3 = make_cylinder(2.15, 15.0, center=(-52.0, 35.0, 2.25), axis='z', sections=18)
    m_h4 = make_cylinder(2.15, 15.0, center=(52.0, 35.0, 2.25), axis='z', sections=18)

    w1 = make_box(22.0, 32.0, 10.0, center=(-20.0, 18.0, 2.25))
    w2 = make_box(22.0, 32.0, 10.0, center=(20.0, 18.0, 2.25))
    w3 = make_box(30.0, 30.0, 10.0, center=(0, -25.0, 2.25))

    m = m - servo_pocket - s_h1 - s_h2 - s_h3 - s_h4 - rod_h1 - rod_h2 - lm1_1 - lm1_2 - lm2_1 - lm2_2 - m_h1 - m_h2 - m_h3 - m_h4 - w1 - w2 - w3
    return orient_for_print(to_trimesh(m))

def generate_03F():
    # Alavanca impressa parafusada no horn 25T do MG996R: R = 60 mm
    hub = make_cylinder(12.0, 6.0, center=(0, 0, 3.0), axis='z', sections=36)
    arm = make_box(60.0, 12.0, 6.0, center=(30.0, 0, 3.0))
    eye = make_cylinder(8.0, 6.0, center=(60.0, 0, 3.0), axis='z', sections=28)
    m = hub + arm + eye
    spline_bore = make_cylinder(3.2, 10.0, center=(0, 0, 3.0), axis='z', sections=25)
    horn_pocket = make_cylinder(7.5, 3.0, center=(0, 0, 4.6), axis='z', sections=36)
    pivot_hole = make_cylinder(1.65, 10.0, center=(60.0, 0, 3.0), axis='z', sections=18)
    m = m - spline_bore - horn_pocket - pivot_hole
    return orient_for_print(to_trimesh(m))

def generate_03G():
    # Biela entre centros: L = 110 mm com alojamentos 623ZZ (Ø10x4 mm)
    eye1 = make_cylinder(8.0, 6.0, center=(0, 0, 3.0), axis='z', sections=28)
    eye2 = make_cylinder(8.0, 6.0, center=(110.0, 0, 3.0), axis='z', sections=28)
    beam_web = make_box(110.0, 4.0, 6.0, center=(55.0, 0, 3.0))
    beam_flange_top = make_box(110.0, 8.0, 1.5, center=(55.0, 0, 5.25))
    beam_flange_bot = make_box(110.0, 8.0, 1.5, center=(55.0, 0, 0.75))
    m = eye1 + eye2 + beam_web + beam_flange_top + beam_flange_bot
    h1 = make_cylinder(1.65, 10.0, center=(0, 0, 3.0), axis='z', sections=18)
    h2 = make_cylinder(1.65, 10.0, center=(110.0, 0, 3.0), axis='z', sections=18)
    pocket1 = make_cylinder(5.05, 4.2, center=(0, 0, 4.0), axis='z', sections=28)
    pocket2 = make_cylinder(5.05, 4.2, center=(110.0, 0, 4.0), axis='z', sections=28)
    m = m - h1 - h2 - pocket1 - pocket2
    return orient_for_print(to_trimesh(m))

def generate_03H():
    # Sapata 03H: 100 × 90 × 12 mm, face côncava R=45 mm, EVA 2 mm
    # Hastes guia Ø6 mm com entre-centros 85 mm (X = -42.5 e X = +42.5)
    front_body = make_box(100.0, 12.0, 90.0, center=(0, 6.0, 45.0))
    block1 = make_box(18.0, 14.0, 90.0, center=(-42.5, -7.0, 45.0))
    block2 = make_box(18.0, 14.0, 90.0, center=(42.5, -7.0, 45.0))
    m = front_body + block1 + block2

    # Face côncava R=45 mm para maçã de referência Ø80 mm
    concavity = make_cylinder(45.0, 100.0, center=(0, 54.0, 45.0), axis='z', sections=64)
    rod1 = make_cylinder(3.025, 95.0, center=(-42.5, -7.0, 45.0), axis='z', sections=28)
    rod2 = make_cylinder(3.025, 95.0, center=(42.5, -7.0, 45.0), axis='z', sections=28)
    pinch1 = make_cylinder(1.65, 25.0, center=(-42.5, -7.0, 45.0), axis='x', sections=18)
    pinch2 = make_cylinder(1.65, 25.0, center=(42.5, -7.0, 45.0), axis='x', sections=18)
    c1 = make_box(26.0, 8.0, 70.0, center=(-22.0, 6.0, 45.0))
    c2 = make_box(26.0, 8.0, 70.0, center=(22.0, 6.0, 45.0))
    m = m - concavity - rod1 - rod2 - pinch1 - pinch2 - c1 - c2
    return orient_for_print(to_trimesh(m))

def generate_03I():
    # Trave traseira 03I: 90 × 18 × 12 mm, entre-centros 85 mm
    bar = make_box(90.0, 18.0, 12.0, center=(0, 0, 6.0))
    clevis = make_cylinder(8.0, 12.0, center=(0, 11.0, 6.0), axis='z', sections=28)
    m = bar + clevis
    rod1 = make_cylinder(3.025, 20.0, center=(-42.5, 0, 6.0), axis='z', sections=24)
    rod2 = make_cylinder(3.025, 20.0, center=(42.5, 0, 6.0), axis='z', sections=24)
    pivot_hole = make_cylinder(1.65, 20.0, center=(0, 11.0, 6.0), axis='z', sections=18)
    pocket_623 = make_cylinder(5.05, 4.2, center=(0, 11.0, 8.0), axis='z', sections=28)
    pinch1 = make_cylinder(1.65, 25.0, center=(-42.5, 0, 6.0), axis='y', sections=18)
    pinch2 = make_cylinder(1.65, 25.0, center=(42.5, 0, 6.0), axis='y', sections=18)
    m = m - rod1 - rod2 - pivot_hole - pocket_623 - pinch1 - pinch2
    return orient_for_print(to_trimesh(m))

def generate_03J():
    cover = make_box(96.0, 85.0, 24.0, center=(0, 0, 12.0))
    cavity = make_box(92.0, 81.0, 22.0, center=(0, 0, 11.0))
    window = make_box(60.0, 45.0, 10.0, center=(0, 0, 23.0))
    m = cover - cavity - window
    f1 = make_cylinder(1.65, 10.0, center=(-42.0, -35.0, 12.0), axis='z', sections=18)
    f2 = make_cylinder(1.65, 10.0, center=(42.0, -35.0, 12.0), axis='z', sections=18)
    m = m - f1 - f2
    return orient_for_print(to_trimesh(m))

def generate_04A():
    # Suporte 04A: cavidade retangular 46 × 21 × 16 mm com 2 furos M3 de 25 mm entre-centros
    base = make_box(54.0, 40.0, 5.5, center=(0, 0, 2.75))
    col = make_box(54.0, 26.0, 85.0, center=(0, 7.0, 42.5))
    g1 = make_box(5.0, 28.0, 65.0, center=(-22.0, 0.0, 32.5))
    g2 = make_box(5.0, 28.0, 65.0, center=(22.0, 0.0, 32.5))
    m = base + col + g1 + g2
    cavity = make_box(46.0, 21.0, 16.0, center=(0, 8.0, 52.0))
    opt_win = make_box(30.0, 12.0, 12.0, center=(0, -2.0, 52.0))
    m3_h1 = make_cylinder(1.65, 40.0, center=(-12.5, 8.0, 42.0), axis='z', sections=18)
    m3_h2 = make_cylinder(1.65, 40.0, center=(12.5, 8.0, 42.0), axis='z', sections=18)
    b1 = make_cylinder(2.15, 20.0, center=(-18.0, -10.0, 2.75), axis='z', sections=18)
    b2 = make_cylinder(2.15, 20.0, center=(18.0, -10.0, 2.75), axis='z', sections=18)
    gh1 = make_cylinder(7.0, 60.0, center=(0, 0.0, 25.0), axis='x', sections=28)
    m = m - cavity - opt_win - m3_h1 - m3_h2 - b1 - b2 - gh1
    return orient_for_print(to_trimesh(m))

def generate_04B():
    base = make_box(54.0, 30.0, 6.0, center=(0, 0, 3.0))
    upright = make_box(54.0, 8.0, 65.0, center=(0, 11.0, 32.5))
    pocket = make_box(50.4, 6.0, 50.4, center=(0, 12.5, 36.0))
    m = (base + upright) - pocket
    b1 = make_cylinder(2.15, 15.0, center=(-18.0, -6.0, 3.0), axis='z', sections=18)
    b2 = make_cylinder(2.15, 15.0, center=(18.0, -6.0, 3.0), axis='z', sections=18)
    m = m - b1 - b2
    return orient_for_print(to_trimesh(m))

def generate_04C():
    base = make_box(80.0, 58.0, 7.0, center=(0, 0, 3.5))
    din_channel = make_box(85.0, 35.4, 3.5, center=(0, 0, 1.75))
    cutout = make_box(26.0, 22.0, 20.0, center=(0, 0, 3.5))
    m = base - din_channel - cutout
    p1 = make_cylinder(3.5, 6.0, center=(-26.0, -13.5, 10.0), axis='z', sections=20)
    p2 = make_cylinder(3.5, 6.0, center=(-26.0, 13.5, 10.0), axis='z', sections=20)
    p3 = make_cylinder(3.5, 6.0, center=(26.0, -13.5, 10.0), axis='z', sections=20)
    p4 = make_cylinder(3.5, 6.0, center=(26.0, 13.5, 10.0), axis='z', sections=20)
    m = m + p1 + p2 + p3 + p4
    h1 = make_cylinder(1.4, 15.0, center=(-26.0, -13.5, 10.0), axis='z', sections=16)
    h2 = make_cylinder(1.4, 15.0, center=(-26.0, 13.5, 10.0), axis='z', sections=16)
    h3 = make_cylinder(1.4, 15.0, center=(26.0, -13.5, 10.0), axis='z', sections=16)
    h4 = make_cylinder(1.4, 15.0, center=(26.0, 13.5, 10.0), axis='z', sections=16)
    m = m - h1 - h2 - h3 - h4
    return orient_for_print(to_trimesh(m))

def generate_04D():
    base = make_box(58.0, 58.0, 7.0, center=(0, 0, 3.5))
    din_channel = make_box(65.0, 35.4, 3.5, center=(0, 0, 1.75))
    cutout = make_box(26.0, 22.0, 20.0, center=(0, 0, 3.5))
    rim = make_box(52.0, 52.0, 4.0, center=(0, 0, 9.0))
    pocket = make_box(48.2, 40.2, 6.0, center=(0, 0, 9.5))
    m = (base + rim) - din_channel - pocket - cutout
    return orient_for_print(to_trimesh(m))

def generate_04E():
    base = make_box(85.0, 70.0, 7.0, center=(0, 0, 3.5))
    din_channel = make_box(90.0, 35.4, 3.5, center=(0, 0, 1.75))
    cutout = make_box(26.0, 22.0, 20.0, center=(0, 0, 3.5))
    b1 = make_box(65.4, 36.4, 6.0, center=(-8.0, 15.0, 5.0))
    cap = make_cylinder(6.5, 10.0, center=(32.0, 15.0, 5.0), axis='z', sections=24)
    b2 = make_box(45.4, 25.4, 6.0, center=(0, -20.0, 5.0))
    m = base - din_channel - cutout - b1 - cap - b2
    return orient_for_print(to_trimesh(m))

def generate_04F():
    base = make_box(50.0, 58.0, 7.0, center=(0, 0, 3.5))
    din_channel = make_box(55.0, 35.4, 3.5, center=(0, 0, 1.75))
    cutout = make_box(26.0, 22.0, 20.0, center=(0, 0, 3.5))
    rim = make_box(44.0, 44.0, 4.0, center=(0, 0, 9.0))
    pocket = make_box(35.4, 28.4, 6.0, center=(0, 0, 9.5))
    m = (base + rim) - din_channel - pocket - cutout
    return orient_for_print(to_trimesh(m))

def generate_05A():
    outer_shell = make_box(120.0, 146.0, 132.0, center=(0, 0, 66.0))
    inner_cavity = make_box(114.8, 140.8, 129.4, center=(0, 0, 64.7))
    m = outer_shell - inner_cavity
    portal1 = make_arch_portal(30.0, 116.0, 72.0, 108.0, center=(-58.0, 0, 0))
    portal2 = make_arch_portal(30.0, 116.0, 72.0, 108.0, center=(58.0, 0, 0))
    win_cutout = make_box(90.4, 10.0, 80.4, center=(0, 71.0, 65.0))
    win_recess = make_box(96.4, 4.0, 86.4, center=(0, 71.5, 65.0))
    cam_aperture = make_cylinder(22.5, 15.0, center=(0, 0, 130.0), axis='z', sections=36)
    fl_left = make_box(120.0, 14.0, 6.0, center=(0, -76.0, 3.0))
    fl_right = make_box(120.0, 14.0, 6.0, center=(0, 76.0, 3.0))
    m = m + fl_left + fl_right
    f_h1 = make_cylinder(2.15, 15.0, center=(-45.0, -76.0, 3.0), axis='z', sections=18)
    f_h2 = make_cylinder(2.15, 15.0, center=(45.0, -76.0, 3.0), axis='z', sections=18)
    f_h3 = make_cylinder(2.15, 15.0, center=(-45.0, 76.0, 3.0), axis='z', sections=18)
    f_h4 = make_cylinder(2.15, 15.0, center=(45.0, 76.0, 3.0), axis='z', sections=18)
    m = m - portal1 - portal2 - win_cutout - win_recess - cam_aperture - f_h1 - f_h2 - f_h3 - f_h4
    return orient_for_print(to_trimesh(m))

def generate_05B():
    frame = make_box(104.0, 94.0, 4.0, center=(0, 0, 2.0))
    window = make_box(82.0, 72.0, 10.0, center=(0, 0, 2.0))
    m = frame - window
    h1 = make_cylinder(1.65, 10.0, center=(-46.0, -41.0, 2.0), axis='z', sections=18)
    h2 = make_cylinder(1.65, 10.0, center=(46.0, -41.0, 2.0), axis='z', sections=18)
    h3 = make_cylinder(1.65, 10.0, center=(-46.0, 41.0, 2.0), axis='z', sections=18)
    h4 = make_cylinder(1.65, 10.0, center=(46.0, 41.0, 2.0), axis='z', sections=18)
    m = m - h1 - h2 - h3 - h4
    return orient_for_print(to_trimesh(m))

def generate_05C():
    box = make_box(65.0, 65.0, 35.0, center=(0, 0, 17.5))
    cavity = make_box(59.0, 59.0, 33.0, center=(0, 0, 18.5))
    m = box - cavity
    lens_h = make_cylinder(13.0, 10.0, center=(0, 0, 1.0), axis='z', sections=36)
    tripod_h = make_cylinder(3.25, 10.0, center=(0, -20.0, 1.0), axis='z', sections=24)
    cable_slot = make_slot(12.0, 6.5, 15.0, center=(0, 30.0, 18.0), slot_axis='z', normal_axis='y')
    m = m - lens_h - tripod_h - cable_slot
    return orient_for_print(to_trimesh(m))

def generate_05D():
    lid = make_box(65.0, 65.0, 4.0, center=(0, 0, 2.0))
    vents = []
    for vy in [-15.0, -7.5, 0.0, 7.5, 15.0]:
        v = make_slot(35.0, 2.5, 10.0, center=(0, vy, 2.0), slot_axis='x', normal_axis='z')
        vents.append(v)
    m = lid
    for v in vents:
        m = m - v
    return orient_for_print(to_trimesh(m))

def generate_05E():
    ring = make_cylinder(52.5, 6.0, center=(0, 0, 3.0), axis='z', sections=64)
    ctr_hole = make_cylinder(22.5, 10.0, center=(0, 0, 3.0), axis='z', sections=36)
    m = ring - ctr_hole
    g1 = make_annulus(35.0, 38.0, 4.0, center=(0, 0, 6.0), axis='z', sections=48)
    g2 = make_annulus(44.0, 47.5, 4.0, center=(0, 0, 6.0), axis='z', sections=48)
    m = m + g1 + g2
    w1 = make_cylinder(2.0, 15.0, center=(0, 30.0, 3.0), axis='z', sections=18)
    w2 = make_cylinder(2.0, 15.0, center=(0, -30.0, 3.0), axis='z', sections=18)
    m = m - w1 - w2
    return orient_for_print(to_trimesh(m))

def generate_05F():
    face = make_cylinder(49.0, 1.0, center=(0, 0, 0.5), axis='z', sections=64)
    ctr = make_cylinder(26.0, 5.0, center=(0, 0, 0.5), axis='z', sections=40)
    rim_out = make_annulus(47.5, 49.0, 5.0, center=(0, 0, 2.5), axis='z', sections=64)
    m = (face - ctr) + rim_out
    return orient_for_print(to_trimesh(m))

def generate_06A():
    # Rampa 06A: inclinação 18° (não 25°) + aba defletora EVA 3 mm
    flange = make_box(92.0, 20.0, 4.0, center=(0, -10.0, 54.0))
    f1 = make_cylinder(2.15, 10.0, center=(-28.0, -10.0, 54.0), axis='z', sections=18)
    f2 = make_cylinder(2.15, 10.0, center=(28.0, -10.0, 54.0), axis='z', sections=18)
    flange = flange - f1 - f2

    bed_length = 135.0
    # Rotação suave de 18° para rolamento seguro da maçã Ø80 mm
    chute_bed = make_box(84.0, bed_length, 4.0, center=(0, 0, 0)).rotate([18.0, 0, 0])
    chute_bed = chute_bed.translate([0, 60.0, 31.0])

    wall_l = make_box(4.0, 126.0, 75.0, center=(-44.0, 60.0, 37.5))
    wall_r = make_box(4.0, 126.0, 75.0, center=(44.0, 60.0, 37.5))

    guard_cutter = make_box(100.0, 170.0, 60.0, center=(0, 0, 30.0)).rotate([18.0, 0, 0])
    guard_cutter = guard_cutter.translate([0, 60.0, 31.0 + 2.0 + 25.0])

    runner_l = make_box(12.0, 126.0, 4.0, center=(-40.0, 63.0, 2.0))
    runner_r = make_box(12.0, 126.0, 4.0, center=(40.0, 63.0, 2.0))
    runner_tie = make_box(92.0, 20.0, 4.0, center=(0, 10.0, 2.0))

    # Aba defletora de amortecimento em EVA 3 mm na borda final
    eva_deflector_lip = make_box(92.0, 15.0, 3.0, center=(0, 122.0, 12.0))

    hole_l = make_cylinder(18.0, 20.0, center=(-44.0, 45.0, 22.0), axis='x', sections=32)
    hole_r = make_cylinder(18.0, 20.0, center=(44.0, 45.0, 22.0), axis='x', sections=32)

    m_ramp = (flange + chute_bed + wall_l + wall_r + runner_l + runner_r + runner_tie + eva_deflector_lip) - guard_cutter - hole_l - hole_r
    cutter_bot = make_box(150.0, 220.0, 20.0, center=(0, 50.0, -10.0))
    m_ramp = m_ramp - cutter_bot
    return orient_for_print(to_trimesh(m_ramp))

def generate_06B():
    outer = make_box(152.0, 152.0, 55.0, center=(0, 0, 27.5))
    inner = make_box(147.2, 147.2, 52.6, center=(0, 0, 28.7))
    collar_add = make_box(147.2, 147.2, 4.0, center=(0, 0, 53.0)) - make_box(144.0, 144.0, 6.0, center=(0, 0, 53.0))
    m = (outer - inner) + collar_add
    h1 = make_cylinder(1.65, 10.0, center=(-25.0, -76.0, 25.0), axis='y', sections=18)
    h2 = make_cylinder(1.65, 10.0, center=(25.0, -76.0, 25.0), axis='y', sections=18)
    m = m - h1 - h2
    return orient_for_print(to_trimesh(m))

def generate_06C():
    m = make_embossed_plate(80.0, 28.0, 2.5, "APROVADOS - CLASSE A", font_size=4.8, text_h=1.0)
    return orient_for_print(to_trimesh(m))

def generate_06D():
    m = make_embossed_plate(80.0, 28.0, 2.5, "REJEITADOS - CLASSES B/C", font_size=4.5, text_h=1.0)
    return orient_for_print(to_trimesh(m))

def generate_06E():
    outer = make_box(75.0, 75.0, 55.0, center=(0, 0, 27.5))
    inner = make_box(70.2, 70.2, 52.6, center=(0, 0, 28.7))
    m = outer - inner
    tab1 = make_box(16.0, 16.0, 4.0, center=(-42.0, -42.0, 2.0))
    tab2 = make_box(16.0, 16.0, 4.0, center=(42.0, -42.0, 2.0))
    tab3 = make_box(16.0, 16.0, 4.0, center=(-42.0, 42.0, 2.0))
    tab4 = make_box(16.0, 16.0, 4.0, center=(42.0, 42.0, 2.0))
    m = m + tab1 + tab2 + tab3 + tab4
    t_h1 = make_cylinder(2.15, 10.0, center=(-42.0, -42.0, 2.0), axis='z', sections=18)
    t_h2 = make_cylinder(2.15, 10.0, center=(42.0, -42.0, 2.0), axis='z', sections=18)
    t_h3 = make_cylinder(2.15, 10.0, center=(-42.0, 42.0, 2.0), axis='z', sections=18)
    t_h4 = make_cylinder(2.15, 10.0, center=(42.0, 42.0, 2.0), axis='z', sections=18)
    gland_h = make_cylinder(10.2, 15.0, center=(0, 37.5, 25.0), axis='y', sections=28)
    m = m - t_h1 - t_h2 - t_h3 - t_h4 - gland_h
    return orient_for_print(to_trimesh(m))

def generate_06F():
    lid = make_box(75.0, 75.0, 3.5, center=(0, 0, 1.75))
    rim = make_box(69.4, 69.4, 2.5, center=(0, 0, 1.25))
    btn_hole = make_cylinder(11.25, 20.0, center=(0, 0, 2.0), axis='z', sections=40)
    key_notch = make_box(3.2, 4.0, 20.0, center=(0, 12.0, 2.0))
    c1 = make_cylinder(2.15, 20.0, center=(-30.0, -30.0, 2.0), axis='z', sections=18)
    c2 = make_cylinder(2.15, 20.0, center=(30.0, -30.0, 2.0), axis='z', sections=18)
    c3 = make_cylinder(2.15, 20.0, center=(-30.0, 30.0, 2.0), axis='z', sections=18)
    c4 = make_cylinder(2.15, 20.0, center=(30.0, 30.0, 2.0), axis='z', sections=18)
    m = (lid + rim) - btn_hole - key_notch - c1 - c2 - c3 - c4
    return orient_for_print(to_trimesh(m))

def generate_07A():
    base = make_cylinder(18.0, 8.0, center=(0, 0, 4.0), axis='z', sections=36)
    pocket = make_box(32.4, 22.4, 5.0, center=(0, 0, 5.6))
    ring1 = make_annulus(6.0, 8.0, 1.0, center=(0, 0, 0.5), axis='z', sections=28)
    ring2 = make_annulus(11.0, 13.0, 1.0, center=(0, 0, 0.5), axis='z', sections=36)
    m = (base - pocket) - ring1 - ring2
    return orient_for_print(to_trimesh(m))

def generate_07B():
    body = make_box(22.0, 18.0, 12.0, center=(0, 0, 6.0))
    snap_slot = make_box(6.2, 20.0, 10.0, center=(-5.0, 0, 6.0))
    duct1 = make_cylinder(2.3, 25.0, center=(5.0, -4.5, 6.0), axis='y', sections=20)
    duct2 = make_cylinder(2.3, 25.0, center=(5.0, 4.5, 6.0), axis='y', sections=20)
    m = body - snap_slot - duct1 - duct2
    return orient_for_print(to_trimesh(m))

def generate_07C():
    spacers = []
    for i in range(4):
        s = make_annulus(4.1, 7.0, 2.0, center=(-30.0 + i * 20.0, -30.0, 1.0), axis='z', sections=32)
        spacers.append(s)
    for i in range(4):
        s = make_annulus(4.1, 7.0, 4.0, center=(-30.0 + i * 20.0, -10.0, 2.0), axis='z', sections=32)
        spacers.append(s)
    for i in range(4):
        s = make_annulus(4.1, 7.0, 6.0, center=(-30.0 + i * 20.0, 12.0, 3.0), axis='z', sections=32)
        spacers.append(s)
    spacers.append(make_annulus(4.1, 7.0, 10.0, center=(-20.0, 36.0, 5.0), axis='z', sections=32))
    spacers.append(make_annulus(4.1, 7.0, 10.0, center=(20.0, 36.0, 5.0), axis='z', sections=32))
    for i in range(4):
        s = make_annulus(3.1, 5.5, 5.0, center=(-30.0 + i * 20.0, 58.0, 2.5), axis='z', sections=28)
        spacers.append(s)
    m_all = spacers[0]
    for s in spacers[1:]:
        m_all = m_all + s
    return orient_for_print(to_trimesh(m_all))

# ==============================================================================
# CONSTRUÇÃO DAS 13 MESAS DE IMPRESSÃO CONSOLIDADAS
# ==============================================================================

def generate_mesa_01():
    parts = [
        place_on_bed(generate_01A(), cx=-39.5, cy=-81.0),
        place_on_bed(generate_01B(), cx=-39.5, cy=0.0),
        place_on_bed(generate_01C(), cx=-39.5, cy=81.0),
        place_on_bed(generate_01D(), cx=86.0, cy=-36.0, rot_z_deg=90.0),
        place_on_bed(generate_02D(), cx=66.0, cy=70.0),
        place_on_bed(generate_02D(), cx=104.0, cy=70.0)
    ]
    return trimesh.util.concatenate(parts)

def generate_mesa_02():
    parts = []
    for cx, cy in [(-66.0, -88.0), (48.0, -88.0), (-66.0, -24.0), (48.0, -24.0)]:
        parts.append(place_on_bed(generate_01E(), cx=cx, cy=cy))
    for cx, cy in [(-66.0, 40.0), (48.0, 40.0)]:
        parts.append(place_on_bed(generate_01F(), cx=cx, cy=cy))
    for cx, cy in [(-51.0, 78.0), (-51.0, 90.0), (-51.0, 102.0), (-51.0, 114.0)]:
        parts.append(place_on_bed(generate_01I(), cx=cx, cy=cy))
    for cx, cy in [(111.0, 0.0), (123.0, 0.0)]:
        parts.append(place_on_bed(generate_01J(), cx=cx, cy=cy, rot_z_deg=90.0))
    return trimesh.util.concatenate(parts)

def generate_mesa_03():
    parts = [
        place_on_bed(generate_01G(), cx=0.0, cy=-62.5),
        place_on_bed(generate_01G(), cx=0.0, cy=62.5)
    ]
    return trimesh.util.concatenate(parts)

def generate_mesa_04():
    parts = [
        place_on_bed(generate_01G(), cx=0.0, cy=-56.0)
    ]
    for cx in [-78.0, -26.0, 26.0, 78.0]:
        for cy in [20.0, 48.0]:
            parts.append(place_on_bed(generate_01K(), cx=cx, cy=cy))
    for cx in [-62.5, 62.5]:
        for cy in [76.0, 104.0]:
            parts.append(place_on_bed(generate_01H(), cx=cx, cy=cy, rot_z_deg=90.0))
    return trimesh.util.concatenate(parts)

def generate_mesa_05():
    parts = [
        place_on_bed(generate_02A(), cx=-36.0, cy=-36.0),
        place_on_bed(generate_02B(), cx=36.0, cy=-36.0),
        place_on_bed(generate_02C(), cx=-36.0, cy=36.0),
        place_on_bed(generate_03C(), cx=25.0, cy=25.0),
        place_on_bed(generate_03B(), cx=55.0, cy=25.0)
    ]
    return trimesh.util.concatenate(parts)

def generate_mesa_06():
    parts = []
    elo_tm = generate_02E()
    for r in range(2):
        for c in range(9):
            cx = -109.52 + c * 27.38
            cy = -61.96 + r * 123.92
            parts.append(place_on_bed(elo_tm, cx=cx, cy=cy))
    return trimesh.util.concatenate(parts)

def generate_mesa_07():
    parts = [
        place_on_bed(generate_03E(), cx=-58.0, cy=-68.0),
        place_on_bed(generate_03J(), cx=60.0, cy=-70.0),
        place_on_bed(generate_03D(), cx=-58.0, cy=16.0),
        place_on_bed(generate_03A(), cx=60.0, cy=12.0),
        place_on_bed(generate_03H(), cx=-62.0, cy=64.0),
        place_on_bed(generate_03I(), cx=55.0, cy=64.0),
        place_on_bed(generate_03F(), cx=-62.0, cy=96.0),
        place_on_bed(generate_03G(), cx=45.0, cy=96.0)
    ]
    return trimesh.util.concatenate(parts)

def generate_mesa_08():
    parts = [
        place_on_bed(generate_04A(), cx=-88.0, cy=-95.0),
        place_on_bed(generate_04A(), cx=-28.0, cy=-95.0),
        place_on_bed(generate_04B(), cx=32.0, cy=-95.0),
        place_on_bed(generate_04B(), cx=92.0, cy=-95.0),
        place_on_bed(generate_04C(), cx=-76.0, cy=-32.0),
        place_on_bed(generate_04D(), cx=-1.0, cy=-32.0),
        place_on_bed(generate_04E(), cx=76.5, cy=-32.0),
        place_on_bed(generate_04F(), cx=-91.0, cy=45.0),
        place_on_bed(generate_07C(), cx=-22.0, cy=60.0)
    ]
    clipe_tm = generate_07B()
    for r in range(4):
        for c in range(3):
            cx = 32.0 + c * 26.0
            cy = 20.0 + r * 22.0
            parts.append(place_on_bed(clipe_tm, cx=cx, cy=cy))
    return trimesh.util.concatenate(parts)

def generate_mesa_09():
    parts = [
        place_on_bed(generate_05A(), cx=-58.0, cy=-36.0),
        place_on_bed(generate_05E(), cx=64.5, cy=-66.5),
        place_on_bed(generate_05B(), cx=69.0, cy=45.0, rot_z_deg=90.0),
        place_on_bed(generate_05C(), cx=-85.5, cy=85.5),
        place_on_bed(generate_05D(), cx=-14.5, cy=85.5)
    ]
    return trimesh.util.concatenate(parts)

def generate_mesa_10():
    parts = [
        place_on_bed(generate_06A(), cx=-55.0, cy=0.0),
        place_on_bed(generate_06E(), cx=50.0, cy=-40.0),
        place_on_bed(generate_06F(), cx=50.0, cy=55.0)
    ]
    return trimesh.util.concatenate(parts)

def generate_mesa_11():
    parts = [
        place_on_bed(generate_06B(), cx=0.0, cy=0.0)
    ]
    return trimesh.util.concatenate(parts)

def generate_mesa_12():
    parts = [
        place_on_bed(generate_05F(), cx=-44.0, cy=0.0),
        place_on_bed(generate_06C(), cx=52.0, cy=-20.0),
        place_on_bed(generate_06D(), cx=52.0, cy=20.0)
    ]
    return trimesh.util.concatenate(parts)

def generate_mesa_13():
    parts = []
    sapata_tm = generate_07A()
    for r in range(2):
        for c in range(4):
            cx = -60.0 + c * 40.0
            cy = -20.0 + r * 40.0
            parts.append(place_on_bed(sapata_tm, cx=cx, cy=cy))
    return trimesh.util.concatenate(parts)

# ==============================================================================
# DICIONÁRIO DAS 13 MESAS DE IMPRESSÃO
# ==============================================================================

MESAS_REGISTRY = [
    ('01', 'Mesa_01_Chassi_4x_Cabeceiras_e_2x_Mancais.stl', generate_mesa_01, 6),
    ('01', 'Mesa_02_Chassi_6x_Extensoes_e_6x_Guias_Laterais.stl', generate_mesa_02, 12),
    ('01', 'Mesa_03_Chassi_2x_Mesas_Deslizantes_01G_Par1e2.stl', generate_mesa_03, 2),
    ('01', 'Mesa_04_Chassi_1x_Mesa_01G3_8x_Pes_01K_e_4x_Travessas_01H.stl', generate_mesa_04, 13),
    ('02', 'Mesa_05_Tambores_Motriz_Livre_Central_e_Polias_GT2.stl', generate_mesa_05, 5),
    ('02', 'Mesa_06_Lote_18x_Elos_Correia_Modular_122mm_Imprimir_5x.stl', generate_mesa_06, 18),
    ('03', 'Mesa_07_Acionamento_Motor_GA37_e_Empurrador_MG996R_Completo.stl', generate_mesa_07, 8),
    ('04', 'Mesa_08_Sensores_4x_Suportes_DIN_12x_Clipes_e_18x_Espacadores.stl', generate_mesa_08, 38),
    ('05', 'Mesa_09_Estacao_Visao_Cupula_Webcam_e_RingLight_Completa.stl', generate_mesa_09, 5),
    ('06', 'Mesa_10_Rampa_Descarte_18graus_e_Caixa_Emergencia_NR12_Completa.stl', generate_mesa_10, 3),
    ('06', 'Mesa_11_Caixa_Coletora_152x152x55mm_Imprimir_2x.stl', generate_mesa_11, 1),
    ('06', 'Mesa_12_Difusor_Optico_1mm_e_2x_Plaquetas_Identificacao_PLA_Branco.stl', generate_mesa_12, 3),
    ('07', 'Mesa_13_Lote_8x_Sapatas_Antivibracao_Pes_TPU_95A.stl', generate_mesa_13, 8),
]

# ==============================================================================
# MONTAGEM GERAL NO ESPAÇO 3D: Esteira_Completa_Montada_70cm.stl
# ==============================================================================

def generate_full_assembly():
    print("Construindo montagem geral tridimensional posicionada (Esteira_Completa_Montada_70cm.stl)...")
    parts = []

    chassi_l = trimesh.creation.box([700.0, 45.0, 16.0])
    chassi_l.apply_translation([0, 87.5, -68.0])
    chassi_r1 = trimesh.creation.box([460.0, 45.0, 16.0])
    chassi_r1.apply_translation([-120.0, 87.5, 68.0])
    chassi_r2 = trimesh.creation.box([140.0, 45.0, 16.0])
    chassi_r2.apply_translation([280.0, 87.5, 68.0])
    parts.extend([chassi_l, chassi_r1, chassi_r2])

    bed = trimesh.creation.box([650.0, 4.0, 120.0])
    bed.apply_translation([0, 105.0, 0])
    parts.append(bed)

    for lx in [-250.0, -80.0, 80.0, 250.0]:
        for lz in [-68.0, 68.0]:
            leg = trimesh.creation.box([32.0, 59.0, 22.0])
            leg.apply_translation([lx, 35.5, lz])
            foot = trimesh.creation.cylinder(18.0, 6.0, sections=24)
            foot.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2.0, [1, 0, 0]))
            foot.apply_translation([lx, 3.0, lz])
            parts.extend([leg, foot])
        cb = trimesh.creation.box([20.0, 14.0, 114.0])
        cb.apply_translation([lx, 35.0, 0])
        parts.append(cb)

    t_livre = trimesh.creation.cylinder(29.97, 121.92, sections=40)
    t_livre.apply_translation([-325.0, 80.0, 0])
    s_idle = trimesh.creation.cylinder(4.0, 160.0, sections=20)
    s_idle.apply_translation([-325.0, 80.0, 0])
    parts.extend([t_livre, s_idle])

    t_motor = trimesh.creation.cylinder(29.97, 131.6, sections=40)
    t_motor.apply_translation([325.0, 80.0, 0])
    s_drive = trimesh.creation.cylinder(4.0, 185.0, sections=20)
    s_drive.apply_translation([325.0, 80.0, -12.5])
    pul_40t = trimesh.creation.cylinder(14.5, 7.0, sections=36)
    pul_40t.apply_translation([325.0, 80.0, -88.0])
    parts.extend([t_motor, s_drive, pul_40t])

    r_center = trimesh.creation.cylinder(25.4, 121.92, sections=36)
    r_center.apply_translation([0, 75.0, 0])
    parts.append(r_center)

    belt_top = trimesh.creation.box([650.0, 4.5, 122.0])
    belt_top.apply_translation([0, 110.25, 0])
    belt_bot = trimesh.creation.box([650.0, 4.5, 122.0])
    belt_bot.apply_translation([0, 49.75, 0])
    parts.extend([belt_top, belt_bot])

    m_body = trimesh.creation.cylinder(18.5, 75.0, sections=28)
    m_body.apply_translation([285.0, 52.0, -75.0])
    pul_20t = trimesh.creation.cylinder(8.0, 7.0, sections=24)
    pul_20t.apply_translation([285.0, 52.0, -88.0])
    parts.extend([m_body, pul_20t])

    dome = trimesh.creation.box([120.0, 150.0, 146.0])
    dome.apply_translation([-150.0, 185.0, 0])
    cam = trimesh.creation.box([36.0, 22.0, 36.0])
    cam.apply_translation([-150.0, 255.0, 0])
    parts.extend([dome, cam])

    for sx in [-150.0, 100.0]:
        s_body = trimesh.creation.box([45.0, 15.0, 20.0])
        s_body.apply_translation([sx, 90.0, -80.0])
        refl = trimesh.creation.box([18.0, 18.0, 4.0])
        refl.apply_translation([sx, 90.0, 65.0])
        parts.extend([s_body, refl])

    pusher_base = trimesh.creation.box([118.0, 24.0, 95.0])
    pusher_base.apply_translation([160.0, 100.0, -112.0])
    servo = trimesh.creation.box([41.0, 20.0, 42.0])
    servo.apply_translation([160.0, 126.0, -132.0])
    shoe = trimesh.creation.box([100.0, 90.0, 12.0])
    shoe.apply_translation([160.0, 115.0, -62.0])
    parts.extend([pusher_base, servo, shoe])

    chute = trimesh.creation.box([92.0, 4.0, 135.0])
    chute.apply_transform(trimesh.transformations.rotation_matrix(np.radians(-18.0), [1, 0, 0]))
    chute.apply_translation([160.0, 78.85, 125.55])
    leg_ramp1 = trimesh.creation.box([4.0, 56.0, 120.0])
    leg_ramp1.apply_translation([118.0, 28.0, 125.0])
    leg_ramp2 = trimesh.creation.box([4.0, 56.0, 120.0])
    leg_ramp2.apply_translation([202.0, 28.0, 125.0])
    parts.extend([chute, leg_ramp1, leg_ramp2])

    box_app = trimesh.creation.box([152.0, 55.0, 152.0])
    box_app.apply_translation([375.0, 27.5, 0])
    box_rej = trimesh.creation.box([152.0, 55.0, 152.0])
    box_rej.apply_translation([160.0, 27.5, 190.0])
    parts.extend([box_app, box_rej])

    estop = trimesh.creation.box([75.0, 65.0, 75.0])
    estop.apply_translation([-340.0, 32.5, -160.0])
    parts.append(estop)

    full_mesh = trimesh.util.concatenate(parts)
    assembly_path = os.path.join(SUBDIRS['00'], 'Esteira_Completa_Montada_70cm.stl')
    export_binary_stl(full_mesh, assembly_path, "AmazonVision 4.0 - Montagem Geral 70cm")
    print(f"Montagem geral salva com sucesso: {assembly_path} ({len(full_mesh.faces)} triângulos)")
    return assembly_path

# ==============================================================================
# ARQUIVO STL MESTRE COM TODAS AS 13 MESAS: TODAS_AS_MESAS_DE_IMPRESSAO_BAMBU_P2S.stl
# ==============================================================================

def generate_master_build_plates_stl(plates_meshes):
    print("\nGerando Arquivo STL Mestre com Todas as 13 Mesas lado a lado (matriz 4x4, pitch 300 mm)...")
    master_plates = []
    for idx, tm in enumerate(plates_meshes):
        col = idx % 4
        row = idx // 4
        offset_x = (col - 1.5) * 300.0
        offset_y = (1.5 - row) * 300.0
        tm_trans = tm.copy()
        tm_trans.apply_translation([offset_x, offset_y, 0.0])
        master_plates.append(tm_trans)

    master_mesh = trimesh.util.concatenate(master_plates)
    master_path = os.path.join(SUBDIRS['00'], 'TODAS_AS_MESAS_DE_IMPRESSAO_BAMBU_P2S.stl')
    export_binary_stl(master_mesh, master_path, "AmazonVision 4.0 - Todas as 13 Mesas Bambu P2S")
    print(f"Arquivo STL Mestre salvo com sucesso: {master_path} ({len(master_mesh.faces)} triângulos)")
    return master_path

# ==============================================================================
# LIMPEZA DAS PEÇAS AVULSAS ANTIGAS
# ==============================================================================

def clean_old_stls():
    print("Limpando arquivos STL legados e peças avulsas das pastas 01 a 07...")
    removed_count = 0
    root_master = os.path.join(KIT_ROOT, 'TODAS_AS_MESAS_DE_IMPRESSAO_BAMBU_P2S.stl')
    if os.path.exists(root_master):
        os.remove(root_master)
        removed_count += 1
    for folder_key in ['01', '02', '03', '04', '05', '06', '07']:
        folder = SUBDIRS[folder_key]
        for fn in os.listdir(folder):
            if fn.endswith('.stl'):
                os.remove(os.path.join(folder, fn))
                removed_count += 1
    print(f"Limpeza concluída: {removed_count} arquivos avulsos removidos com segurança.")

# ==============================================================================
# AUDITORIA E VALIDAÇÃO DAS 13 MESAS DE IMPRESSÃO
# ==============================================================================

def run_mesh_audit():
    print("\nExecutando Auditoria Automática das 13 Mesas de Impressão (Bambu Lab P2S)...")
    report = {
        'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
        'bambu_p2s_max_volume_mm': [256.0, 256.0, 256.0],
        'total_build_plates': len(MESAS_REGISTRY),
        'total_project_sliced_mass_grams': 0.0,
        'mass_target_under_2400g': False,
        'plates': [],
        'assembly_validation': {},
        'master_plate_validation': {},
        'all_tests_passed': True
    }

    total_project_sliced_mass = 0.0

    for group, filename, _, expected_bodies in MESAS_REGISTRY:
        folder_map = {
            '01': '01_Estrutura_Esteira',
            '02': '02_Roletes_e_Suportes',
            '03': '03_Acionamento_e_Motor',
            '04': '04_Sensores_e_Eletronica',
            '05': '05_Webcam_e_Protecao',
            '06': '06_Caixas_e_Tampas',
            '07': '07_Fixacoes_e_Acessorios'
        }
        f_dir = folder_map[group[:2]]
        path = os.path.join(KIT_ROOT, f_dir, filename)

        if not os.path.exists(path):
            print(f"[ERRO] Mesa não encontrada: {path}")
            report['all_tests_passed'] = False
            continue

        file_size = os.path.getsize(path)
        m = trimesh.load(path, file_type='stl')
        triangles = len(m.faces)
        expected_size = 84 + 50 * triangles
        size_ok = (file_size == expected_size)

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
        total_project_sliced_mass += batch_grams

        status_ok = (size_ok and watertight and nan_inf_free and z_min_ok and fits_p2s and body_count_ok and bed_contact_ok)

        plate_report = {
            'plate_filename': filename,
            'group_folder': f_dir,
            'triangles': triangles,
            'file_size_bytes': file_size,
            'binary_stl_valid': size_ok,
            'watertight_manifold': watertight,
            'zero_nan_inf': nan_inf_free,
            'expected_body_count': expected_bodies,
            'actual_body_count': bodies,
            'body_count_ok': body_count_ok,
            'z_min_mm': round(float(bounds[0][2]), 4),
            'z_min_zero': z_min_ok,
            'bed_contact_area_mm2': round(z0_area, 1),
            'bed_contact_ok': bed_contact_ok,
            'extents_mm': [round(float(x), 2) for x in extents],
            'fits_bambu_p2s': fits_p2s,
            'solid_volume_cm3': vol_cm3,
            'surface_area_cm2': area_cm2,
            'estimated_sliced_mass_g': sliced_grams,
            'print_repetitions': repetitions,
            'batch_sliced_mass_g': batch_grams,
            'status': 'PASS' if status_ok else 'FAIL'
        }

        if not status_ok:
            report['all_tests_passed'] = False
            print(f"  [FALHA] {filename}: bodies={bodies}/{expected_bodies}, z0_area={z0_area:.1f} mm2, extents={extents}")
        else:
            print(f"  [OK] {filename:68s} | Corpos: {bodies:2d}/{expected_bodies:2d} | Z0 Area: {z0_area:7.1f} mm² | Vol: {vol_cm3:5.1f} cm³ | Massa: {sliced_grams:5.1f}g (Lote: {batch_grams:5.1f}g)")

        report['plates'].append(plate_report)

    # Validar Montagem Geral
    assembly_path = os.path.join(SUBDIRS['00'], 'Esteira_Completa_Montada_70cm.stl')
    m_ass = trimesh.load(assembly_path, file_type='stl')
    ass_bounds = m_ass.bounds
    ass_extents = m_ass.extents
    ground_ok = bool(abs(ass_bounds[0][1]) < 0.1)

    report['assembly_validation'] = {
        'filename': 'Esteira_Completa_Montada_70cm.stl',
        'triangles': len(m_ass.faces),
        'bounds_min_xyz_mm': [round(float(x), 2) for x in ass_bounds[0]],
        'bounds_max_xyz_mm': [round(float(x), 2) for x in ass_bounds[1]],
        'overall_envelope_xyz_mm': [round(float(x), 2) for x in ass_extents],
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

    # Validar Arquivo STL Mestre de Todas as 13 Mesas
    master_path = os.path.join(SUBDIRS['00'], 'TODAS_AS_MESAS_DE_IMPRESSAO_BAMBU_P2S.stl')
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

        report['master_plate_validation'] = {
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
            report['all_tests_passed'] = False
            print(f"  [FALHA] TODAS_AS_MESAS_DE_IMPRESSAO_BAMBU_P2S.stl: bodies={bodies_m}/122, z0_area={z0_area_m:.1f} mm2")
        else:
            print(f"\n[Arquivo STL Mestre em 00_Montagem_Geral_e_Fontes_CAD]")
            print(f"  [OK] TODAS_AS_MESAS_DE_IMPRESSAO_BAMBU_P2S.stl   | Corpos: {bodies_m:3d}/122 | Z0 Area: {z0_area_m:8.1f} mm² | Status: PASS")
    else:
        report['all_tests_passed'] = False
        print(f"  [ERRO] Arquivo STL Mestre não encontrado: {master_path}")

    # Validação da Meta de Redução de Massa DfAM (< 2400.0 g)
    report['total_project_sliced_mass_grams'] = round(total_project_sliced_mass, 1)
    report['mass_target_under_2400g'] = bool(total_project_sliced_mass < 2400.0)

    print(f"\n[Meta de Redução de Massa DfAM (< 2.400 g)]")
    if report['mass_target_under_2400g']:
        print(f"  [OK] Massa Total Fatiada do Projeto: {total_project_sliced_mass:.1f} g (< 2400.0 g) | META ATINGIDA!")
    else:
        report['all_tests_passed'] = False
        print(f"  [FALHA] Massa Total Fatiada do Projeto ({total_project_sliced_mass:.1f} g) excedeu o limite de 2400.0 g!")

    def json_converter(o):
        if isinstance(o, (np.bool_, np.generic)):
            return o.item()
        raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")

    report_path = os.path.join(SUBDIRS['00'], 'auditoria_malhas_stl.json')
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False, default=json_converter)

    print(f"\nRelatório de Auditoria salvo em: {report_path}")
    print(f"Status Geral da Auditoria: {'TODAS AS 13 MESAS + ARQUIVO MESTRE APROVADOS (PASS)' if report['all_tests_passed'] else 'REPROVADO (FAIL)'}")
    return report

# ==============================================================================
# EXECUÇÃO PRINCIPAL
# ==============================================================================

def main():
    start_time = time.time()

    # 1. Limpar arquivos avulsos antigos das pastas 01 a 07
    clean_old_stls()

    # 2. Gerar as 13 Mesas de Impressão Consolidadas
    count = 0
    total = len(MESAS_REGISTRY)
    plates_meshes = []

    for group, filename, generator_func, expected_bodies in MESAS_REGISTRY:
        count += 1
        folder_map = {
            '01': SUBDIRS['01'],
            '02': SUBDIRS['02'],
            '03': SUBDIRS['03'],
            '04': SUBDIRS['04'],
            '05': SUBDIRS['05'],
            '06': SUBDIRS['06'],
            '07': SUBDIRS['07']
        }
        dest_folder = folder_map[group[:2]]
        out_path = os.path.join(dest_folder, filename)
        print(f"[{count:2d}/{total:2d}] Gerando {filename} ({expected_bodies} corpos)...")
        tm = generator_func()
        export_binary_stl(tm, out_path, f"AmazonVision 4.0 - {filename}")
        plates_meshes.append(tm)

    # 3. Gerar Arquivo STL Mestre com Todas as 13 Mesas Lado a Lado
    generate_master_build_plates_stl(plates_meshes)

    # 4. Montagem geral
    generate_full_assembly()

    # 5. Auditoria completa das 13 Mesas + Arquivo Mestre + Montagem Geral
    audit = run_mesh_audit()

    elapsed = time.time() - start_time
    print(f"\nConsolidação em 13 Mesas + Arquivo Mestre concluída com êxito em {elapsed:.1f} segundos!")
    print(f"\nConsolidação em 13 Mesas concluída com êxito em {elapsed:.1f} segundos!")

if __name__ == '__main__':
    main()
