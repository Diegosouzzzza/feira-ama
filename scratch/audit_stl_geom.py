import struct
import os

kit_dir = r'c:\Users\ponto\OneDrive\Desktop\FEIRA - AMA\Kit_Impressao_3D_Esteira_AmazonVision'

def analyze_stl(filepath):
    filename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)
    with open(filepath, 'rb') as f:
        header = f.read(80)
        num_triangles_bytes = f.read(4)
        if len(num_triangles_bytes) < 4:
            return filename, 0, (0,0,0), (0,0,0), "Arquivo vazio/corrompido"
        num_triangles = struct.unpack('<I', num_triangles_bytes)[0]
        
        # Check expected size
        expected_size = 84 + num_triangles * 50
        if filesize != expected_size:
            # might be ascii stl or size mismatch
            return filename, num_triangles, (0,0,0), (0,0,0), f"Tamanho inesperado: {filesize} != {expected_size}"
        
        # Read vertices to get bounding box
        min_x = min_y = min_z = float('inf')
        max_x = max_y = max_z = float('-inf')
        
        # Sample or stream
        # read chunks of 5000 triangles
        chunk_size = 5000
        bytes_per_chunk = chunk_size * 50
        
        for _ in range(0, num_triangles, chunk_size):
            chunk = f.read(bytes_per_chunk)
            n_in_chunk = len(chunk) // 50
            for i in range(n_in_chunk):
                offset = i * 50
                # normal: 12 bytes, v1: 12, v2: 12, v3: 12, attr: 2
                v_data = chunk[offset+12 : offset+48]
                x1, y1, z1, x2, y2, z2, x3, y3, z3 = struct.unpack('<9f', v_data)
                min_x = min(min_x, x1, x2, x3)
                max_x = max(max_x, x1, x2, x3)
                min_y = min(min_y, y1, y2, y3)
                max_y = max(max_y, y1, y2, y3)
                min_z = min(min_z, z1, z2, z3)
                max_z = max(max_z, z1, z2, z3)
                
        dim_x = max_x - min_x
        dim_y = max_y - min_y
        dim_z = max_z - min_z
        
        return filename, num_triangles, (min_x, min_y, min_z), (dim_x, dim_y, dim_z), "OK"

print("=== AUDITORIA DIMENSIONAL E ESTRUTURAL DAS MESAS DE IMPRESSÃO 3D ===")
mesas = []
for root, dirs, files in os.walk(kit_dir):
    for file in sorted(files):
        if file.lower().startswith('mesa_') and file.lower().endswith('.stl'):
            mesas.append(os.path.join(root, file))

for mp in sorted(mesas):
    fn, tri, mins, dims, status = analyze_stl(mp)
    fit_p2s = dims[0] <= 256 and dims[1] <= 256 and dims[2] <= 256
    z0 = abs(mins[2]) < 0.05
    print(f"{fn[:35]:<35} | Tris: {tri:<7} | Zmin: {mins[2]:5.2f} | Dims: {dims[0]:5.1f}x{dims[1]:5.1f}x{dims[2]:5.1f} mm | P2S Fit: {'SIM' if fit_p2s else 'NÃO'} | Z=0: {'SIM' if z0 else 'NÃO'}")

# Check master STL
master_path = os.path.join(kit_dir, '00_Montagem_Geral_e_Fontes_CAD', 'TODAS_AS_MESAS_DE_IMPRESSAO_BAMBU_P2S.stl')
if os.path.exists(master_path):
    fn, tri, mins, dims, status = analyze_stl(master_path)
    print(f"\nMASTER STL: {fn} | Tris: {tri} | Dims: {dims[0]:.1f}x{dims[1]:.1f}x{dims[2]:.1f} mm | Status: {status}")
