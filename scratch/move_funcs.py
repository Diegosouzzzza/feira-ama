import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("Manual_Montagem_Esteira_70cm.html", "r", encoding="utf-8") as f:
    text = f.read()

# Remove the ones inside init3D
target_remove = '''      // Helper para alternância de tema no cenário da feira
      function updateFairTheme(theme) {
        if (typeof fairFloorMesh !== 'undefined' && fairFloorMesh && fairFloorMesh.material) {
          const floorCol = (theme === 'blueprint') ? 0x0f223d : (theme === 'dark' ? 0x1a202c : 0xcbd5e1);
          fairFloorMesh.material.color.setHex(floorCol);
        }
      }

      // Efeito de acionamento visual da Botoeira S0 NR-12
      function triggerEmergencyButtonEffect() {
        const statusEl = document.getElementById('actionStatus');
        if (statusEl) {
          statusEl.innerHTML = '<span style="color: #dc2626; font-weight: 800;">[PARADA DE EMERGÊNCIA NR-12]</span> Botoeira S0 acionada na borda frontal da bancada (&le; 60 cm). Bobina K1 desenergizada em 32 ms. Esteira e atuadores parados com segurança.';
        }
        if (typeof isBeltRunning !== 'undefined') isBeltRunning = false;
        if (typeof simCycle !== 'undefined' && simCycle.active) simCycle.active = false;
        if (typeof s0Cap !== 'undefined' && s0Cap) {
          s0Cap.position.y = 38;
          setTimeout(() => { if (s0Cap) s0Cap.position.y = 45; }, 400);
        }
      }'''

assert target_remove in text, "target_remove not found!"
text = text.replace(target_remove, "", 1)

# Add them right before selectComponent in the outer scope
outer_funcs = '''    // Helper para alternância de tema no cenário da feira
    function updateFairTheme(theme) {
      if (typeof fairFloorMesh !== 'undefined' && fairFloorMesh && fairFloorMesh.material) {
        const floorCol = (theme === 'blueprint') ? 0x0f223d : (theme === 'dark' ? 0x1a202c : 0xcbd5e1);
        fairFloorMesh.material.color.setHex(floorCol);
      }
    }

    // Efeito de acionamento visual da Botoeira S0 NR-12
    function triggerEmergencyButtonEffect() {
      const statusEl = document.getElementById('actionStatus');
      if (statusEl) {
        statusEl.innerHTML = '<span style="color: #dc2626; font-weight: 800;">[PARADA DE EMERGÊNCIA NR-12]</span> Botoeira S0 acionada na borda frontal da bancada (&le; 60 cm). Bobina K1 desenergizada em 32 ms. Esteira e atuadores parados com segurança.';
      }
      if (typeof isBeltRunning !== 'undefined') isBeltRunning = false;
      if (typeof simCycle !== 'undefined' && simCycle.active) simCycle.active = false;
      if (typeof s0Cap !== 'undefined' && s0Cap) {
        s0Cap.position.y = 38;
        setTimeout(() => { if (s0Cap) s0Cap.position.y = 45; }, 400);
      }
    }

    // Seleção Interativa de Componente'''

assert '// Seleção Interativa de Componente' in text, "selectComponent marker not found!"
text = text.replace('// Seleção Interativa de Componente', outer_funcs, 1)

with open("Manual_Montagem_Esteira_70cm.html", "w", encoding="utf-8") as f:
    f.write(text)

print("Moved updateFairTheme and triggerEmergencyButtonEffect to outer scope successfully!")
