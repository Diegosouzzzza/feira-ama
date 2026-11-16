import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open("Manual_Montagem_Esteira_70cm.html", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Tab Button
tab_marker = '<button class="tab-btn" id="tabAssembly" onclick="setViewMode(\'assembly\')">'
assert tab_marker in text, "tabAssembly not found!"
pos = text.find(tab_marker)
pos_end = text.find('</button>', pos) + len('</button>')

new_tab = '''      <button class="tab-btn" id="tabFair" onclick="setViewMode('fair')">
        🎪 Banca Completa Feira
      </button>'''

text = text[:pos_end] + '\n' + new_tab + text[pos_end:]

# 2. Sidebar Cards 11 to 16
cards_marker = '<!-- Component 10 -->'
assert cards_marker in text, "cards_marker not found!"
pos_c10 = text.find(cards_marker)
pos_c10_end = text.find('</div>', text.find('card-spec', pos_c10)) + len('</div>')

new_cards = '''

        <!-- Component 11 -->
        <div class="component-card" id="card-11" onclick="selectComponent(11)">
          <div class="card-top">
            <span class="card-num">11</span>
            <span class="card-title">Painel Elétrico DIN & Automação</span>
            <span class="card-tag">Painel</span>
          </div>
          <p class="card-desc">Armário DIN 300 × 400 × 150 mm em tripé metálico com porta em policarbonato translúcido. Acomoda o disjuntor bipolar Q0 (10A), fonte industrial PS1 (12V 10A mono-fonte chaveada), relé de segurança K1 (40A NR-12), regulador Buck XL4015 (5V 5A para servo MG996R), Buck MP1584 (3,3V para sensores), módulo de potência MOSFET D4184 (controle PWM motor GA37) e microcontrolador ESP32 montado em protoboard MB-102 azul-neve com duplo circuito de proteção clamp BAT54S + R=1kΩ para os canais S1 e S2. Saída para eletrocalha com chicotes flexíveis CH-01 a CH-05 identificados.</p>
          <span class="card-spec">Painel DIN 300×400×150 mm · Fonte 12V 10A · ESP32 em protoboard MB-102 · Clamp duplo BAT54S + 1kΩ</span>
        </div>

        <!-- Component 12 -->
        <div class="component-card" id="card-12" onclick="selectComponent(12)">
          <div class="card-top">
            <span class="card-num">12</span>
            <span class="card-title">Botoeira S0 Cogumelo NR-12</span>
            <span class="card-tag">Segurança</span>
          </div>
          <p class="card-desc">Botoeira de parada de emergência tipo cogumelo Ø22 mm com trava mecânica giratória (desarme por rotação), instalada na borda frontal da bancada (X = +200 mm, Y = +40 mm, Z = +520 mm), garantindo alcance imediato ≤ 60 cm para qualquer operador conforme diretrizes da norma NR-12. Secciona a bobina do relé K1 desenergizando imediatamente motor e atuadores em &lt; 50 ms.</p>
          <span class="card-spec">Cogumelo Ø22 mm NR-12 · Alcance ≤ 60 cm · Corte K1 &lt; 50 ms · Desarme mecânico</span>
        </div>

        <!-- Component 13 -->
        <div class="component-card" id="card-13" onclick="selectComponent(13)">
          <div class="card-top">
            <span class="card-num">13</span>
            <span class="card-title">Notebook Host & Dashboard IA</span>
            <span class="card-tag">Visão IA</span>
          </div>
          <p class="card-desc">Estação de processamento com notebook sobre a bancada executando a pipeline de inferência YOLOv8 / OpenCV a 28 FPS com latência de 34 ms. Comunicação com ESP32 via cabo USB serial 115200 bps com linha VBUS 5V seccionada (VBUS ✂ / VBUS seccionada) para proteção absoluta contra retorno de corrente e ground loop entre a fonte externa de 12V e a porta do computador.</p>
          <span class="card-spec">Dashboard IA 28 FPS · Serial 115200 bps · Isolamento USB VBUS ✂ · Latência 34 ms</span>
        </div>

        <!-- Component 14 -->
        <div class="component-card" id="card-14" onclick="selectComponent(14)">
          <div class="card-top">
            <span class="card-num">14</span>
            <span class="card-title">Alimentador de Maçãs Gravitacional</span>
            <span class="card-tag">Entrada</span>
          </div>
          <p class="card-desc">Caixa reservatório em madeira naval (220 × 180 × 180 mm) com rampa de alimentação inclinada a 20° alinhada à cabeceira da esteira (X = -325 mm). Fornece fluxo contínuo de maçãs Ø80 mm para a pista de entrada com guia lateral suave, evitando quedas bruscas ou desalinhamento sobre a correia modular.</p>
          <span class="card-spec">Capacidade 8 maçãs Ø80 mm · Rampa 20° · Cabeceira tensora X = -325 mm</span>
        </div>

        <!-- Component 15 -->
        <div class="component-card" id="card-15" onclick="selectComponent(15)">
          <div class="card-top">
            <span class="card-num">15</span>
            <span class="card-title">Caixa Coletora Aprovados (Classe A)</span>
            <span class="card-tag">Descarte A</span>
          </div>
          <p class="card-desc">Caixa coletora de polipropileno verde (220 × 220 × 220 mm) apoiada no piso do estande (Y = -1400 mm, X = +560 mm) sobre rodízios industriais de 15 mm. Recebe maçãs classificadas como Aprovadas (Classe A) que transpõem o tambor tracionador motorizado ao final da esteira, amortecidas por revestimento interno de EVA.</p>
          <span class="card-spec">220×220×220 mm verde · Piso Y = -1400 mm · Rodízios Ø15 mm · Etiqueta Classe A</span>
        </div>

        <!-- Component 16 -->
        <div class="component-card" id="card-16" onclick="selectComponent(16)">
          <div class="card-top">
            <span class="card-num">16</span>
            <span class="card-title">Caixa Coletora Rejeitados (Classes B/C)</span>
            <span class="card-tag">Descarte B/C</span>
          </div>
          <p class="card-desc">Caixa coletora de polipropileno laranja (220 × 220 × 220 mm) apoiada no piso (Y = -1400 mm, X = +280 mm, Z = +380 mm) sobre rodízios industriais. Posicionada na saída inferior da rampa suave de 18°, recebe as maçãs defeituosas ou imaturas empurradas pelo mecanismo linear MG996R.</p>
          <span class="card-spec">220×220×220 mm laranja · Piso Y = -1400 mm · Rodízios Ø15 mm · Classes B/C</span>
        </div>'''

text = text[:pos_c10_end] + new_cards + text[pos_c10_end:]

# 3. In setTheme, hook updateFairTheme
old_theme_block = '''      const lineColor = (theme === 'blueprint') ? 0x7dd3fc : (theme === 'dark' ? 0x9ca3af : 0x0f172a);
      scene.traverse(obj => {
        if (obj instanceof THREE.LineSegments && obj.material && obj.material.color) {
          if (!obj.userData.isDashed) {
            obj.material.color.setHex(lineColor);
          }
        }
      });'''
new_theme_block = '''      const lineColor = (theme === 'blueprint') ? 0x7dd3fc : (theme === 'dark' ? 0x9ca3af : 0x0f172a);
      scene.traverse(obj => {
        if (obj instanceof THREE.LineSegments && obj.material && obj.material.color) {
          if (!obj.userData.isDashed) {
            obj.material.color.setHex(lineColor);
          }
        }
      });
      if (typeof updateFairTheme === 'function') {
        updateFairTheme(theme);
      }'''
assert old_theme_block in text, "old_theme_block not found!"
text = text.replace(old_theme_block, new_theme_block, 1)

# 4. Insert 3D bancaFeiraGroup right before `// BALÕES DE IDENTIFICAÇÃO ① a ⑩`
banca_insertion_point = '// BALÕES DE IDENTIFICAÇÃO ① a ⑩'
assert banca_insertion_point in text, "banca_insertion_point not found!"

with open("scratch/build_fair_code.py", "r", encoding="utf-8") as f:
    fair_code_file = f.read()

# Extract fair_js string from build_fair_code.py
start_marker = "fair_js = '''"
end_marker = "'''\n\nprint"
pos_s = fair_code_file.find(start_marker) + len(start_marker)
pos_e = fair_code_file.find(end_marker, pos_s)
fair_3d_code = fair_code_file[pos_s:pos_e]

# Append updateFairTheme function and triggerEmergencyButtonEffect to fair_3d_code
fair_3d_code += '''
      // Helper para alternância de tema no cenário da feira
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
'''

text = text.replace(banca_insertion_point, fair_3d_code + '\n      ' + banca_insertion_point, 1)

# 5. Replace pinAnchors array
old_pins = '''      pinAnchors = [
        { id: 1, title: "1: Chassi Modular 700mm (13 Mesas P2S)", pos: new THREE.Vector3(0, 85, -75) },
        { id: 2, title: "2: Correia Modular (86 Elos · Passo 17,3mm · 122mm)", pos: new THREE.Vector3(-220, 115, 0) },
        { id: 3, title: "3: Tambores Ø 60mm & Rolamentos 608ZZ", pos: new THREE.Vector3(325, 80, 0) },
        { id: 4, title: "4: Sistema Tensor M5 da Cabeceira", pos: new THREE.Vector3(-330, 80, -75) },
        { id: 5, title: "5: Cúpula de Inspeção Óptica & Câmera 1080p", pos: new THREE.Vector3(-150, 245, 0) },
        { id: 6, title: "6: Sensores Ópticos Retangulares S1 e S2 (5V TTL)", pos: new THREE.Vector3(100, 124, -75) },
        { id: 7, title: "7: Empurrador Linear MG996R (Curso 120mm)", pos: new THREE.Vector3(160, 135, -75) },
        { id: 8, title: "8: Rampa Lateral Suave 18° com Defletor EVA", pos: new THREE.Vector3(160, 85, 105) },
        { id: 9, title: "9: Caixas Coletoras 152×152×55mm (Piso Y = 0 mm)", pos: new THREE.Vector3(160, 30, 190) },
        { id: 10, title: "10: Motorredutor GA37 60 RPM & Transmissão GT2", pos: new THREE.Vector3(285, 52, -90) }
      ];'''

new_pins = '''      pinAnchors = [
        { id: 1, title: "1: Chassi Modular 700mm (13 Mesas P2S)", pos: new THREE.Vector3(0, 85, -75) },
        { id: 2, title: "2: Correia Modular (86 Elos · Passo 17,3mm · 122mm)", pos: new THREE.Vector3(-220, 115, 0) },
        { id: 3, title: "3: Tambores Ø 60mm & Rolamentos 608ZZ", pos: new THREE.Vector3(325, 80, 0) },
        { id: 4, title: "4: Sistema Tensor M5 da Cabeceira", pos: new THREE.Vector3(-330, 80, -75) },
        { id: 5, title: "5: Cúpula de Inspeção Óptica & Câmera 1080p", pos: new THREE.Vector3(-150, 245, 0) },
        { id: 6, title: "6: Sensores Ópticos Retangulares S1 e S2 (5V TTL)", pos: new THREE.Vector3(100, 124, -75) },
        { id: 7, title: "7: Empurrador Linear MG996R (Curso 120mm)", pos: new THREE.Vector3(160, 135, -75) },
        { id: 8, title: "8: Rampa Lateral Suave 18° com Defletor EVA", pos: new THREE.Vector3(160, 85, 105) },
        { id: 9, title: "9: Caixas Coletoras 152×152×55mm (Piso Y = 0 mm)", pos: new THREE.Vector3(160, 30, 190) },
        { id: 10, title: "10: Motorredutor GA37 60 RPM & Transmissão GT2", pos: new THREE.Vector3(285, 52, -90) },
        { id: 11, title: "11: Painel Elétrico DIN (Q0+PS1+K1+ESP32+Clamp BAT54S)", pos: new THREE.Vector3(850, -100, 200) },
        { id: 12, title: "12: Botoeira S0 NR-12 na Borda da Bancada", pos: new THREE.Vector3(200, 40, 520) },
        { id: 13, title: "13: Notebook Host com Dashboard IA (Serial 115200 bps)", pos: new THREE.Vector3(-500, 15, 400) },
        { id: 14, title: "14: Alimentador de Maçãs (Caixa + Rampa 20°)", pos: new THREE.Vector3(-480, 100, 0) },
        { id: 15, title: "15: Caixa Aprovados (5 maçãs · CLASSE A)", pos: new THREE.Vector3(560, -1400, 50) },
        { id: 16, title: "16: Caixa Rejeitados (2 maçãs · CLASSES B/C)", pos: new THREE.Vector3(280, -1400, 380) }
      ];'''
assert old_pins in text, "old_pins not found!"
text = text.replace(old_pins, new_pins, 1)

# 6. Update animate() loop to hide static conveyor apples during active simulation
old_anim_sim = '''        // Simulação Contínua a 60 FPS
        if (simCycle.active) {
          updateSimulationCycle(dt);
        }'''
new_anim_sim = '''        // Simulação Contínua a 60 FPS
        if (typeof conveyorApplesGroup !== 'undefined' && conveyorApplesGroup) {
          conveyorApplesGroup.visible = !simCycle.active;
        }
        if (simCycle.active) {
          updateSimulationCycle(dt);
        }'''
assert old_anim_sim in text, "old_anim_sim not found!"
text = text.replace(old_anim_sim, new_anim_sim, 1)

# 7. Update updatePinPositions() and declare currentViewMode
old_pin_func = '''    function updatePinPositions() {
      if (!camera || !overlay) return;
      const halfW = container.clientWidth / 2;
      const halfH = container.clientHeight / 2;

      pinAnchors.forEach(pin => {
        const el = document.getElementById(`pin-${pin.id}`);
        if (!el) return;

        const p = pin.pos.clone().project(camera);
        const x = p.x * halfW + halfW;
        const y = -(p.y * halfH) + halfH;

        if (p.z > 1 || x < 0 || x > container.clientWidth || y < 0 || y > container.clientHeight) {
          el.style.display = 'none';
        } else {
          el.style.display = 'flex';
          el.style.left = `${x}px`;
          el.style.top = `${y}px`;
        }
      });
    }'''

new_pin_func = '''    let currentViewMode = 'isometric';

    function updatePinPositions() {
      if (!camera || !overlay) return;
      const halfW = container.clientWidth / 2;
      const halfH = container.clientHeight / 2;

      pinAnchors.forEach(pin => {
        const el = document.getElementById(`pin-${pin.id}`);
        if (!el) return;

        // Na aba fair, exibir apenas os pinos 11 a 16 da banca; nas demais abas, exibir apenas os pinos 1 a 10
        if (currentViewMode === 'fair' && pin.id < 11) {
          el.style.display = 'none';
          return;
        }
        if (currentViewMode !== 'fair' && pin.id >= 11) {
          el.style.display = 'none';
          return;
        }

        const p = pin.pos.clone().project(camera);
        const x = p.x * halfW + halfW;
        const y = -(p.y * halfH) + halfH;

        if (p.z > 1 || x < 0 || x > container.clientWidth || y < 0 || y > container.clientHeight) {
          el.style.display = 'none';
        } else {
          el.style.display = 'flex';
          el.style.left = `${x}px`;
          el.style.top = `${y}px`;
        }
      });
    }'''
assert old_pin_func in text, "old_pin_func not found!"
text = text.replace(old_pin_func, new_pin_func, 1)

# 8. Update selectComponent to call triggerEmergencyButtonEffect if id == 12
old_select_comp = '''      const pin = document.getElementById(`pin-${id}`);
      if (pin) pin.classList.add('active');

      // Foco suave da câmera no componente selecionado'''
new_select_comp = '''      const pin = document.getElementById(`pin-${id}`);
      if (pin) pin.classList.add('active');

      if (id === 12 && typeof triggerEmergencyButtonEffect === 'function') {
        triggerEmergencyButtonEffect();
      }

      // Foco suave da câmera no componente selecionado'''
assert old_select_comp in text, "old_select_comp not found!"
text = text.replace(old_select_comp, new_select_comp, 1)

# 9. Update resetCamera()
old_reset_cam = '''    function resetCamera() {
      camera.position.set(720, 560, 720);
      controls.target.set(20, 75, 40);
      controls.update();
      applyExplosion(0);
      document.getElementById('explodeSlider').value = 0;
      toggleDomeXRay(false);
      document.getElementById('chkDomeXRay').checked = false;
      restoreFullAssemblyView();
    }'''

new_reset_cam = '''    function resetCamera() {
      if (currentViewMode === 'fair') {
        camera.position.set(1200, 420, 1300);
        controls.target.set(0, -200, 200);
        controls.update();
        applyExplosion(0);
        document.getElementById('explodeSlider').value = 0;
        return;
      }
      camera.position.set(720, 560, 720);
      controls.target.set(20, 75, 40);
      controls.update();
      applyExplosion(0);
      document.getElementById('explodeSlider').value = 0;
      toggleDomeXRay(false);
      document.getElementById('chkDomeXRay').checked = false;
      restoreFullAssemblyView();
    }'''
assert old_reset_cam in text, "old_reset_cam not found!"
text = text.replace(old_reset_cam, new_reset_cam, 1)

# 10. Update setViewMode(mode)
old_set_view = '''    function setViewMode(mode) {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      const activeTab = document.getElementById(`tab${mode.charAt(0).toUpperCase() + mode.slice(1)}`);
      if (activeTab) activeTab.classList.add('active');

      const titleEl = document.getElementById('viewTitle');
      restoreFullAssemblyView();

      if (mode === 'isometric') {'''

new_set_view = '''    function setViewMode(mode) {
      currentViewMode = mode;
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      const activeTab = document.getElementById(`tab${mode.charAt(0).toUpperCase() + mode.slice(1)}`);
      if (activeTab) activeTab.classList.add('active');

      const titleEl = document.getElementById('viewTitle');
      restoreFullAssemblyView();

      if (typeof bancaFeiraGroup !== 'undefined' && bancaFeiraGroup) {
        bancaFeiraGroup.visible = (mode === 'fair');
      }

      if (mode === 'isometric') {'''
assert old_set_view in text, "old_set_view not found!"
text = text.replace(old_set_view, new_set_view, 1)

# And add the 'fair' mode block to setViewMode
old_assembly_block = '''      } else if (mode === 'assembly') {
        titleEl.textContent = 'GUIA INTERATIVO DE MONTAGEM PASSO A PASSO (7 ETAPAS)';
        document.getElementById('secAssembly').scrollIntoView({ behavior: 'smooth' });
        setAssemblyStep(1);
      }
    }'''

new_assembly_block = '''      } else if (mode === 'assembly') {
        titleEl.textContent = 'GUIA INTERATIVO DE MONTAGEM PASSO A PASSO (7 ETAPAS)';
        document.getElementById('secAssembly').scrollIntoView({ behavior: 'smooth' });
        setAssemblyStep(1);
      } else if (mode === 'fair') {
        titleEl.textContent = 'BANCA COMPLETA MONTADA NA XXI FEIRA FUCAPI 2026';
        setOrthoView('perspective');
        applyExplosion(0);
        document.getElementById('explodeSlider').value = 0;
        camera.position.set(1200, 420, 1300);
        controls.target.set(0, -200, 200);
        controls.update();
      }
    }'''
assert old_assembly_block in text, "old_assembly_block not found!"
text = text.replace(old_assembly_block, new_assembly_block, 1)

# 11. Update setAssemblyStep & restoreFullAssemblyView to skip components >= 11
old_step_loop = '''      for (let cid in components) {
        const compGroup = components[cid];
        const isTarget = data.comps.includes(parseInt(cid));'''
new_step_loop = '''      for (let cid in components) {
        if (parseInt(cid) >= 11) continue;
        const compGroup = components[cid];
        const isTarget = data.comps.includes(parseInt(cid));'''
assert old_step_loop in text, "old_step_loop not found!"
text = text.replace(old_step_loop, new_step_loop, 1)

old_restore_loop = '''    function restoreFullAssemblyView() {
      for (let cid in components) {
        const compGroup = components[cid];
        compGroup.traverse(child => {'''
new_restore_loop = '''    function restoreFullAssemblyView() {
      for (let cid in components) {
        if (parseInt(cid) >= 11) continue;
        const compGroup = components[cid];
        compGroup.traverse(child => {'''
assert old_restore_loop in text, "old_restore_loop not found!"
text = text.replace(old_restore_loop, new_restore_loop, 1)

with open("scratch/test_manual.html", "w", encoding="utf-8") as f:
    f.write(text)

print(f"test_manual.html written successfully! New length: {len(text)} chars, {len(text.splitlines())} lines")
