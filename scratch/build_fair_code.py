import sys
sys.stdout.reconfigure(encoding='utf-8')

# Let's draft the bancaFeiraGroup JS code and inspect it
fair_js = '''
      // =============================================================
      // BANCA COMPLETA DA FEIRA FUCAPI 2026 (bancaFeiraGroup)
      // =============================================================
      const bancaFeiraGroup = new THREE.Group();
      bancaFeiraGroup.name = 'bancaFeiraGroup';
      bancaFeiraGroup.visible = false;
      scene.add(bancaFeiraGroup);

      // Helper: Criação de Sprites de Alta Resolução com Canvas 2D
      function createFairSprite(text, bgCol, textCol, borderCol, w = 256, h = 64, scX = 80, scY = 20, font = 'bold 22px "Space Grotesk", sans-serif') {
        const c = document.createElement('canvas');
        c.width = w * 2;
        c.height = h * 2;
        const ctx = c.getContext('2d');
        ctx.scale(2, 2);
        if (bgCol) {
          ctx.fillStyle = bgCol;
          ctx.fillRect(0, 0, w, h);
        }
        if (borderCol) {
          ctx.strokeStyle = borderCol;
          ctx.lineWidth = 3;
          ctx.strokeRect(2, 2, w - 4, h - 4);
        }
        ctx.fillStyle = textCol;
        ctx.font = font;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(text, w / 2, h / 2);

        const tex = new THREE.CanvasTexture(c);
        const mat = new THREE.SpriteMaterial({ map: tex, transparent: true });
        const sp = new THREE.Sprite(mat);
        sp.scale.set(scX, scY, 1);
        return sp;
      }

      // -------------------------------------------------------------
      // L. PISO DO ESTANDE (Carpete claro Y = -1620)
      // -------------------------------------------------------------
      const fairFloorGeo = new THREE.PlaneGeometry(3000, 2500);
      const fairFloorMesh = makeSketchMesh(fairFloorGeo, 0xcbd5e1);
      fairFloorMesh.rotation.x = -Math.PI / 2;
      fairFloorMesh.position.set(0, -1620, 150);
      fairFloorMesh.userData.isFairFloor = true;
      bancaFeiraGroup.add(fairFloorMesh);

      // -------------------------------------------------------------
      // A. MESA DE APRESENTAÇÃO (benchTableGroup)
      // -------------------------------------------------------------
      const benchTableGroup = new THREE.Group();
      bancaFeiraGroup.add(benchTableGroup);

      // Tampo MDF 1800 x 15 x 700 mm (X x Y x Z) em Y = -15 a 0, centro X=0, Z=150
      const tableTopMesh = makeSketchMesh(new THREE.BoxGeometry(1800, 15, 700), 0xa16207);
      tableTopMesh.position.set(0, -7.5, 150);
      benchTableGroup.add(tableTopMesh);

      // Toalha Azul-Marinho #1e293b cobrindo o tampo
      const clothTop = makeSketchMesh(new THREE.BoxGeometry(1700, 1, 650), 0x1e293b);
      clothTop.position.set(0, 0.5, 150);
      benchTableGroup.add(clothTop);

      // Saia frontal da toalha com inscrição técnica
      const clothSkirt = makeSketchMesh(new THREE.BoxGeometry(1700, 120, 2), 0x1e293b);
      clothSkirt.position.set(0, -60, 475);
      benchTableGroup.add(clothSkirt);

      const tableBannerSprite = createFairSprite(
        "AmazonVision 4.0 · Esteira Seletora Inteligente · FUCAPI 2026",
        "#1e293b", "#f8fafc", "#d97706",
        640, 64, 480, 48, 'bold 22px "Space Grotesk", sans-serif'
      );
      tableBannerSprite.position.set(0, -60, 478);
      benchTableGroup.add(tableBannerSprite);

      // 4 Cavaletes Metálicos nas pontas (2 conjuntos em X = -720 e X = +720)
      [-720, 720].forEach(tX => {
        // Pernas em V invertido: BoxGeometry(6, 760, 40)
        // Perna traseira inclinada
        const legBack = makeSketchMesh(new THREE.BoxGeometry(6, 760, 40), 0x334155);
        legBack.position.set(tX, -387.5, 150 - 130);
        legBack.rotation.x = -0.18;
        benchTableGroup.add(legBack);

        // Perna frontal inclinada
        const legFront = makeSketchMesh(new THREE.BoxGeometry(6, 760, 40), 0x334155);
        legFront.position.set(tX, -387.5, 150 + 130);
        legFront.rotation.x = 0.18;
        benchTableGroup.add(legFront);

        // Travessa horizontal do cavalete
        const crossTrestle = makeSketchMesh(new THREE.BoxGeometry(8, 20, 460), 0x334155);
        crossTrestle.position.set(tX, -450, 150);
        benchTableGroup.add(crossTrestle);

        // Sapatas antiderrapantes CylinderGeometry(25, 25, 12, 16) em #0f172a no pé de cada perna
        const padBack = makeSketchMesh(new THREE.CylinderGeometry(25, 25, 12, 16), 0x0f172a);
        padBack.position.set(tX, -754, 150 - 260);
        benchTableGroup.add(padBack);

        const padFront = makeSketchMesh(new THREE.CylinderGeometry(25, 25, 12, 16), 0x0f172a);
        padFront.position.set(tX, -754, 150 + 260);
        benchTableGroup.add(padFront);
      });

      // -------------------------------------------------------------
      // B. ALIMENTADOR DE MAÇÃS (appleFeederGroup) - Entrada da esteira
      // -------------------------------------------------------------
      const appleFeederGroup = new THREE.Group();
      bancaFeiraGroup.add(appleFeederGroup);
      components[14] = appleFeederGroup;

      // Caixa aberta em madeira #a16207 BoxGeometry(220, 180, 180) em X=-480, Y=0..180, Z=0
      const boxBase = makeSketchMesh(new THREE.BoxGeometry(220, 10, 180), 0xa16207);
      boxBase.position.set(-480, 5, 0);
      appleFeederGroup.add(boxBase);

      const boxWallBack = makeSketchMesh(new THREE.BoxGeometry(220, 170, 10), 0xa16207);
      boxWallBack.position.set(-480, 95, -85);
      appleFeederGroup.add(boxWallBack);

      const boxWallFront = makeSketchMesh(new THREE.BoxGeometry(220, 170, 10), 0xa16207);
      boxWallFront.position.set(-480, 95, 85);
      appleFeederGroup.add(boxWallFront);

      const boxWallLeft = makeSketchMesh(new THREE.BoxGeometry(10, 170, 180), 0xa16207);
      boxWallLeft.position.set(-585, 95, 0);
      appleFeederGroup.add(boxWallLeft);

      // Anteparo inferior da saída para a rampa
      const boxWallRightLip = makeSketchMesh(new THREE.BoxGeometry(10, 40, 180), 0xa16207);
      boxWallRightLip.position.set(-375, 25, 0);
      appleFeederGroup.add(boxWallRightLip);

      // Rampa inclinada 20° (BoxGeometry(110, 4, 160)) saindo da caixa até X = -325 (entrada esteira)
      const feederRamp = makeSketchMesh(new THREE.BoxGeometry(110, 4, 160), 0xa16207);
      feederRamp.position.set(-345, 142, 0);
      feederRamp.rotation.z = -0.349; // 20° para baixo em direção a +X
      appleFeederGroup.add(feederRamp);

      // Guias laterais da rampa
      [-78, 78].forEach(gZ => {
        const rampGuide = makeSketchMesh(new THREE.BoxGeometry(110, 24, 4), 0xa16207);
        rampGuide.position.set(-345, 150, gZ);
        rampGuide.rotation.z = -0.349;
        appleFeederGroup.add(rampGuide);
      });

      // 8 Maçãs esféricas SphereGeometry(40, 20, 20) em #c62828 com cabinho CylinderGeometry(2, 2, 8) em #78350f
      const applePositionsFeeder = [
        [-520, 45, -45], [-520, 45, +45], [-450, 45, -45], [-450, 45, +45],
        [-485, 95, 0],   [-525, 115, -15], [-455, 115, -20], [-445, 105, +35]
      ];
      applePositionsFeeder.forEach(pos => {
        const appleSub = new THREE.Group();
        appleSub.position.set(pos[0], pos[1], pos[2]);
        const aSphere = makeSketchMesh(new THREE.SphereGeometry(40, 20, 20), 0xc62828);
        appleSub.add(aSphere);
        const aStem = makeSketchMesh(new THREE.CylinderGeometry(2, 2, 8, 8), 0x78350f);
        aStem.position.set(0, 42, 0);
        appleSub.add(aStem);
        appleFeederGroup.add(appleSub);
      });

      // -------------------------------------------------------------
      // C. MAÇÃS EM CENA SOBRE A CORREIA (conveyorApplesGroup)
      // -------------------------------------------------------------
      const conveyorApplesGroup = new THREE.Group();
      bancaFeiraGroup.add(conveyorApplesGroup);

      const conveyorApplesConfig = [
        { tag: 'apple-entry',       pos: [-300, 167.5, 0] },
        { tag: 'apple-inspection',  pos: [-150, 167.5, 0] },
        { tag: 'apple-prepush',     pos: [ 130, 167.5, 0] }
      ];
      conveyorApplesConfig.forEach(cfg => {
        const aSub = new THREE.Group();
        aSub.userData.tag = cfg.tag;
        aSub.position.set(cfg.pos[0], cfg.pos[1], cfg.pos[2]);
        const aSphere = makeSketchMesh(new THREE.SphereGeometry(40, 22, 22), 0xdc2626);
        aSub.add(aSphere);
        const aStem = makeSketchMesh(new THREE.CylinderGeometry(2, 2, 8, 8), 0x78350f);
        aStem.position.set(0, 42, 0);
        aSub.add(aStem);
        conveyorApplesGroup.add(aSub);
      });

      // -------------------------------------------------------------
      // D. CAIXAS COLETORAS NO PISO (collectorBinsGroup) - Y = -1620
      // -------------------------------------------------------------
      const collectorBinsGroup = new THREE.Group();
      bancaFeiraGroup.add(collectorBinsGroup);

      // Caixa APROVADOS (verde #059669) em X=+560, Y=-1400 (base -1510, topo -1290), Z=+50
      const approvedBoxGroup = new THREE.Group();
      collectorBinsGroup.add(approvedBoxGroup);
      components[15] = approvedBoxGroup;

      const appBase = makeSketchMesh(new THREE.BoxGeometry(220, 10, 220), 0x059669);
      appBase.position.set(560, -1505, 50);
      approvedBoxGroup.add(appBase);

      const appWallF = makeSketchMesh(new THREE.BoxGeometry(220, 210, 10), 0x059669);
      appWallF.position.set(560, -1400, 155);
      approvedBoxGroup.add(appWallF);

      const appWallB = makeSketchMesh(new THREE.BoxGeometry(220, 210, 10), 0x059669);
      appWallB.position.set(560, -1400, -55);
      approvedBoxGroup.add(appWallB);

      const appWallL = makeSketchMesh(new THREE.BoxGeometry(10, 210, 220), 0x059669);
      appWallL.position.set(455, -1400, 50);
      approvedBoxGroup.add(appWallL);

      const appWallR = makeSketchMesh(new THREE.BoxGeometry(10, 210, 220), 0x059669);
      appWallR.position.set(665, -1400, 50);
      approvedBoxGroup.add(appWallR);

      // Rodízios e pés de apoio da caixa Aprovados até o piso Y = -1620
      [[-95, -95], [95, -95], [-95, 95], [95, 95]].forEach(cOff => {
        const cLeg = makeSketchMesh(new THREE.BoxGeometry(14, 100, 14), 0x334155);
        cLeg.position.set(560 + cOff[0], -1560, 50 + cOff[1]);
        approvedBoxGroup.add(cLeg);
        const cWheel = makeSketchMesh(new THREE.CylinderGeometry(15, 15, 20, 14), 0x0f172a);
        cWheel.rotation.z = Math.PI / 2;
        cWheel.position.set(560 + cOff[0], -1610, 50 + cOff[1]);
        approvedBoxGroup.add(cWheel);
      });

      // 5 Maçãs Ø80 empilhadas dentro da caixa Aprovados (Y = -1460 a -1380)
      const appApples = [
        [530, -1465, 25], [590, -1465, 25], [530, -1465, 75], [590, -1465, 75], [560, -1400, 50]
      ];
      appApples.forEach(pos => {
        const aSub = new THREE.Group();
        aSub.position.set(pos[0], pos[1], pos[2]);
        aSub.add(makeSketchMesh(new THREE.SphereGeometry(40, 20, 20), 0xdc2626));
        const st = makeSketchMesh(new THREE.CylinderGeometry(2, 2, 8, 8), 0x78350f);
        st.position.set(0, 42, 0);
        aSub.add(st);
        approvedBoxGroup.add(aSub);
      });

      // Etiqueta Aprovados
      const appSprite = createFairSprite(
        "APROVADOS · CLASSE A", "#059669", "#ffffff", "#34d399",
        320, 64, 150, 30, 'bold 22px "Space Grotesk", sans-serif'
      );
      appSprite.position.set(560, -1400, 163);
      approvedBoxGroup.add(appSprite);

      // Caixa REJEITADOS (laranja #d97706) em X=+280, Y=-1400, Z=+380
      const rejectedBoxGroup = new THREE.Group();
      collectorBinsGroup.add(rejectedBoxGroup);
      components[16] = rejectedBoxGroup;

      const rejBase = makeSketchMesh(new THREE.BoxGeometry(220, 10, 220), 0xd97706);
      rejBase.position.set(280, -1505, 380);
      rejectedBoxGroup.add(rejBase);

      const rejWallF = makeSketchMesh(new THREE.BoxGeometry(220, 210, 10), 0xd97706);
      rejWallF.position.set(280, -1400, 485);
      rejectedBoxGroup.add(rejWallF);

      const rejWallB = makeSketchMesh(new THREE.BoxGeometry(220, 210, 10), 0xd97706);
      rejWallB.position.set(280, -1400, 275);
      rejectedBoxGroup.add(rejWallB);

      const rejWallL = makeSketchMesh(new THREE.BoxGeometry(10, 210, 220), 0xd97706);
      rejWallL.position.set(175, -1400, 380);
      rejectedBoxGroup.add(rejWallL);

      const rejWallR = makeSketchMesh(new THREE.BoxGeometry(10, 210, 220), 0xd97706);
      rejWallR.position.set(385, -1400, 380);
      rejectedBoxGroup.add(rejWallR);

      // Rodízios da caixa Rejeitados até o piso
      [[-95, -95], [95, -95], [-95, 95], [95, 95]].forEach(cOff => {
        const cLeg = makeSketchMesh(new THREE.BoxGeometry(14, 100, 14), 0x334155);
        cLeg.position.set(280 + cOff[0], -1560, 380 + cOff[1]);
        rejectedBoxGroup.add(cLeg);
        const cWheel = makeSketchMesh(new THREE.CylinderGeometry(15, 15, 20, 14), 0x0f172a);
        cWheel.rotation.z = Math.PI / 2;
        cWheel.position.set(280 + cOff[0], -1610, 380 + cOff[1]);
        rejectedBoxGroup.add(cWheel);
      });

      // 2 Maçãs Ø80 na caixa Rejeitados em Y = -1480
      const rejApples = [[260, -1470, 365], [300, -1450, 395]];
      rejApples.forEach(pos => {
        const aSub = new THREE.Group();
        aSub.position.set(pos[0], pos[1], pos[2]);
        aSub.add(makeSketchMesh(new THREE.SphereGeometry(40, 20, 20), 0xdc2626));
        const st = makeSketchMesh(new THREE.CylinderGeometry(2, 2, 8, 8), 0x78350f);
        st.position.set(0, 42, 0);
        aSub.add(st);
        rejectedBoxGroup.add(aSub);
      });

      // Etiqueta Rejeitados
      const rejSprite = createFairSprite(
        "REJEITADOS · CLASSES B/C", "#d97706", "#ffffff", "#fbbf24",
        340, 64, 160, 30, 'bold 20px "Space Grotesk", sans-serif'
      );
      rejSprite.position.set(280, -1400, 493);
      rejectedBoxGroup.add(rejSprite);

      // -------------------------------------------------------------
      // E. PAINEL ELÉTRICO INDUSTRIAL EM TRIPÉ (fieldPanelGroup)
      // -------------------------------------------------------------
      const fieldPanelGroup = new THREE.Group();
      bancaFeiraGroup.add(fieldPanelGroup);
      components[11] = fieldPanelGroup;

      // Armário DIN 300 x 400 x 150 mm (X x Y x Z) em #1e293b, X=+850, Y=-100 (-300 a +100), Z=+200
      const cabinetBox = makeSketchMesh(new THREE.BoxGeometry(300, 400, 150), 0x1e293b);
      cabinetBox.position.set(850, -100, 200);
      fieldPanelGroup.add(cabinetBox);

      // Placa de montagem interna laranja/metálica
      const dinBackplate = makeSketchMesh(new THREE.BoxGeometry(280, 380, 4), 0xea580c);
      dinBackplate.position.set(850, -100, 132);
      fieldPanelGroup.add(dinBackplate);

      // Trilhos DIN 35mm
      [-40, -160].forEach(dY => {
        const dRail = makeSketchMesh(new THREE.BoxGeometry(260, 35, 8), 0x94a3b8);
        dRail.position.set(850, dY, 140);
        fieldPanelGroup.add(dRail);
      });

      // Tampa frontal transparente em policarbonato #bfdbfe com opacidade 0.25
      const cabDoor = makeSketchMesh(new THREE.BoxGeometry(290, 390, 4), 0xbfdbfe, 0.25, true);
      cabDoor.position.set(850, -100, 276);
      fieldPanelGroup.add(cabDoor);

      // Componentes Internos do Painel Elétrico:
      // Q0: Disjuntor 10A bipolar DIN
      const q0Mesh = makeSketchMesh(new THREE.BoxGeometry(36, 85, 55), 0xcbd5e1);
      q0Mesh.position.set(750, -40, 170);
      fieldPanelGroup.add(q0Mesh);
      const q0Lever = makeSketchMesh(new THREE.BoxGeometry(10, 18, 14), 0xdc2626);
      q0Lever.position.set(750, -35, 200);
      fieldPanelGroup.add(q0Lever);
      const spQ0 = createFairSprite("Q0 10A", "#0f172a", "#f8fafc", "#94a3b8", 128, 48, 45, 16);
      spQ0.position.set(750, -88, 185);
      fieldPanelGroup.add(spQ0);

      // PS1: Fonte 12V 10A colmeia (mono-fonte do sistema)
      const ps1Mesh = makeSketchMesh(new THREE.BoxGeometry(95, 140, 50), 0x64748b);
      ps1Mesh.position.set(830, 0, 170);
      fieldPanelGroup.add(ps1Mesh);
      const spPS1 = createFairSprite("PS1 12V 10A", "#0f172a", "#facc15", "#eab308", 180, 48, 65, 16);
      spPS1.position.set(830, -75, 185);
      fieldPanelGroup.add(spPS1);

      // K1: Relé de segurança 40A NR-12
      const k1Mesh = makeSketchMesh(new THREE.BoxGeometry(45, 60, 45), 0xb91c1c);
      k1Mesh.position.set(930, 10, 170);
      fieldPanelGroup.add(k1Mesh);
      const spK1 = createFairSprite("K1 NR-12", "#b91c1c", "#ffffff", "#fef08a", 140, 48, 50, 16);
      spK1.position.set(930, -30, 185);
      fieldPanelGroup.add(spK1);

      // U1: ESP32 montado em protoboard MB-102 (azul-neve com furos)
      const protoMesh = makeSketchMesh(new THREE.BoxGeometry(85, 165, 10), 0xe0f2fe);
      protoMesh.position.set(845, -155, 155);
      fieldPanelGroup.add(protoMesh);

      // Linhas de furos da protoboard MB-102
      [-50, -25, 0, 25, 50].forEach(pY => {
        const furos = makeSketchMesh(new THREE.BoxGeometry(70, 4, 2), 0x334155);
        furos.position.set(845, -155 + pY, 161);
        fieldPanelGroup.add(furos);
      });

      // Módulo ESP32 DevKit sobre a protoboard MB-102
      const espMesh = makeSketchMesh(new THREE.BoxGeometry(28, 54, 6), 0x1e293b);
      espMesh.position.set(845, -140, 164);
      fieldPanelGroup.add(espMesh);
      const espShield = makeSketchMesh(new THREE.BoxGeometry(18, 22, 3), 0xcfd8dc);
      espShield.position.set(845, -135, 168);
      fieldPanelGroup.add(espShield);
      const spESP = createFairSprite("ESP32 (protoboard)", "#0284c7", "#ffffff", "#38bdf8", 220, 48, 75, 16);
      spESP.position.set(845, -105, 185);
      fieldPanelGroup.add(spESP);

      // Clamp BAT54S + R=1kΩ (2 canais para S1 e S2)
      const clampS1 = makeSketchMesh(new THREE.BoxGeometry(8, 6, 4), 0x0f172a);
      clampS1.position.set(825, -200, 163);
      fieldPanelGroup.add(clampS1);
      const spClampS1 = createFairSprite("S1 CLAMP (BAT54S + 1kΩ)", "#15803d", "#f0fdf4", "#22c55e", 260, 48, 85, 15);
      spClampS1.position.set(825, -212, 185);
      fieldPanelGroup.add(spClampS1);

      const clampS2 = makeSketchMesh(new THREE.BoxGeometry(8, 6, 4), 0x0f172a);
      clampS2.position.set(865, -200, 163);
      fieldPanelGroup.add(clampS2);
      const spClampS2 = createFairSprite("S2 CLAMP (BAT54S + 1kΩ)", "#15803d", "#f0fdf4", "#22c55e", 260, 48, 85, 15);
      spClampS2.position.set(865, -212, 185);
      fieldPanelGroup.add(spClampS2);

      // U2: Buck XL4015 (5V 5A para Servo MG996R)
      const u2Mesh = makeSketchMesh(new THREE.BoxGeometry(45, 24, 18), 0x0284c7);
      u2Mesh.position.set(750, -150, 165);
      fieldPanelGroup.add(u2Mesh);
      const spU2 = createFairSprite("U2 XL4015 (5V)", "#0369a1", "#ffffff", "#38bdf8", 160, 48, 55, 15);
      spU2.position.set(750, -170, 185);
      fieldPanelGroup.add(spU2);

      // U4: Buck MP1584 (3.3V Sensores)
      const u4Mesh = makeSketchMesh(new THREE.BoxGeometry(22, 17, 8), 0x0369a1);
      u4Mesh.position.set(750, -215, 160);
      fieldPanelGroup.add(u4Mesh);
      const spU4 = createFairSprite("U4 MP1584", "#0369a1", "#ffffff", "#7dd3fc", 140, 48, 48, 15);
      spU4.position.set(750, -230, 185);
      fieldPanelGroup.add(spU4);

      // D4184: MOSFET PWM Motorredutor GA37
      const d4184Mesh = makeSketchMesh(new THREE.BoxGeometry(34, 17, 12), 0xdc2626);
      d4184Mesh.position.set(845, -235, 162);
      fieldPanelGroup.add(d4184Mesh);
      const spD4184 = createFairSprite("D4184 MOSFET", "#991b1b", "#ffffff", "#f87171", 160, 48, 55, 15);
      spD4184.position.set(845, -250, 185);
      fieldPanelGroup.add(spD4184);

      // X1 / X2 / X3: 3 Réguas de Bornes DIN
      const bornesMesh = makeSketchMesh(new THREE.BoxGeometry(65, 22, 28), 0x475569);
      bornesMesh.position.set(935, -150, 165);
      fieldPanelGroup.add(bornesMesh);
      const spBornes = createFairSprite("X1 / X2 / X3", "#334155", "#ffffff", "#cbd5e1", 140, 48, 50, 15);
      spBornes.position.set(935, -172, 185);
      fieldPanelGroup.add(spBornes);

      // Tripé Metálico do Painel Elétrico até Y = -1600 (piso)
      const tripodFeet = [
        [720, -1600, 80],
        [980, -1600, 80],
        [850, -1600, 360]
      ];
      tripodFeet.forEach(fPos => {
        const legCurve = new THREE.LineCurve3(
          new THREE.Vector3(850, -300, 200),
          new THREE.Vector3(fPos[0], fPos[1], fPos[2])
        );
        const legGeo = new THREE.TubeGeometry(legCurve, 16, 10, 12, false);
        const legM = makeSketchMesh(legGeo, 0x475569);
        fieldPanelGroup.add(legM);

        const pad = makeSketchMesh(new THREE.CylinderGeometry(25, 25, 15, 16), 0x0f172a);
        pad.position.set(fPos[0], fPos[1] + 7.5, fPos[2]);
        fieldPanelGroup.add(pad);
      });

      // Chicotes Flexíveis da Eletrocalha (CH-01 a CH-05)
      const harnesses = [
        { id: 'CH-01', name: 'CH-01 12V',   col: 0xffd600, pEnd: [320, 40, -60] },
        { id: 'CH-02', name: 'CH-02 ESTOP', col: 0xef4444, pEnd: [200, 40, 500] },
        { id: 'CH-03', name: 'CH-03 MOTOR', col: 0xd97706, pEnd: [285, 45, -75] },
        { id: 'CH-04', name: 'CH-04 S1/S2', col: 0xa855f7, pEnd: [100, 90, -60] },
        { id: 'CH-05', name: 'CH-05 SERVO', col: 0x06b6d4, pEnd: [160, 95, -70] }
      ];
      harnesses.forEach((hn, idx) => {
        const startX = 810 + idx * 20;
        const curve = new THREE.CatmullRomCurve3([
          new THREE.Vector3(startX, -300, 180),
          new THREE.Vector3(startX - 60, -420, 210),
          new THREE.Vector3(550 + idx * 25, -280, 200),
          new THREE.Vector3(380 + idx * 20, -90, 160),
          new THREE.Vector3(hn.pEnd[0], hn.pEnd[1], hn.pEnd[2])
        ]);
        const tubeGeo = new THREE.TubeGeometry(curve, 32, 4, 8, false);
        const tubeM = makeSketchMesh(tubeGeo, hn.col);
        fieldPanelGroup.add(tubeM);

        const spLabel = createFairSprite(hn.name, "#0f172a", "#f8fafc", "#475569", 140, 48, 45, 14);
        const midPoint = curve.getPoint(0.45);
        spLabel.position.copy(midPoint).add(new THREE.Vector3(0, 14, 0));
        fieldPanelGroup.add(spLabel);
      });

      // -------------------------------------------------------------
      // F. BOTOEIRA S0 COGUMELO NR-12 NA BORDA DA BANCADA
      // -------------------------------------------------------------
      const emergencyButtonGroup = new THREE.Group();
      bancaFeiraGroup.add(emergencyButtonGroup);
      components[12] = emergencyButtonGroup;

      // Base cilíndrica amarela/metálica na borda frontal da mesa (X=+200, Y=+20, Z=+520)
      const s0Base = makeSketchMesh(new THREE.CylinderGeometry(15, 15, 40, 20), 0xfacc15);
      s0Base.position.set(200, 20, 520);
      emergencyButtonGroup.add(s0Base);

      // Cogumelo vermelho Ø22 mm
      const s0Cap = makeSketchMesh(new THREE.CylinderGeometry(22, 18, 18, 20), 0xdc2626);
      s0Cap.position.set(200, 45, 520);
      emergencyButtonGroup.add(s0Cap);

      // Sprite PARE em caixa alta acima do botão
      const s0Sprite = createFairSprite("PARE", "#dc2626", "#ffffff", "#fef08a", 160, 64, 45, 18, 'bold 28px "Space Grotesk", sans-serif');
      s0Sprite.position.set(200, 72, 520);
      emergencyButtonGroup.add(s0Sprite);

      // -------------------------------------------------------------
      // G. NOTEBOOK HOST COM DASHBOARD IA (notebookHostGroup)
      // -------------------------------------------------------------
      const notebookHostGroup = new THREE.Group();
      bancaFeiraGroup.add(notebookHostGroup);
      components[13] = notebookHostGroup;

      // Base do notebook BoxGeometry(340, 10, 230) em #1e293b em X=-500, Y=+5..+15, Z=+400
      const lapBase = makeSketchMesh(new THREE.BoxGeometry(340, 10, 230), 0x1e293b);
      lapBase.position.set(-500, 10, 400);
      notebookHostGroup.add(lapBase);

      // Teclado e trackpad contrastantes
      const lapKeyboard = makeSketchMesh(new THREE.BoxGeometry(300, 2, 110), 0x334155);
      lapKeyboard.position.set(-500, 15.5, 360);
      notebookHostGroup.add(lapKeyboard);

      const lapTrackpad = makeSketchMesh(new THREE.BoxGeometry(90, 2, 60), 0x334155);
      lapTrackpad.position.set(-500, 15.5, 460);
      notebookHostGroup.add(lapTrackpad);

      // Tela aberta BoxGeometry(340, 220, 10) inclinada 110° (20° com vertical)
      const lapScreenGroup = new THREE.Group();
      lapScreenGroup.position.set(-500, 15, 285);
      lapScreenGroup.rotation.x = -0.349; // 20° inclinação para trás
      notebookHostGroup.add(lapScreenGroup);

      const lapScreenBezel = makeSketchMesh(new THREE.BoxGeometry(340, 220, 10), 0x0f172a);
      lapScreenBezel.position.set(0, 110, 0);
      lapScreenGroup.add(lapScreenBezel);

      // CanvasTexture de Alta Resolução do Dashboard IA
      const dashCanvas = document.createElement('canvas');
      dashCanvas.width = 680;
      dashCanvas.height = 440;
      const dctx = dashCanvas.getContext('2d');

      // Fundo Dashboard Dark
      dctx.fillStyle = '#0f172a';
      dctx.fillRect(0, 0, 680, 440);

      // Barra de Topo
      dctx.fillStyle = '#1e293b';
      dctx.fillRect(0, 0, 680, 55);
      dctx.font = 'bold 22px "Space Grotesk", sans-serif';
      dctx.fillStyle = '#ffffff';
      dctx.fillText('AmazonVision 4.0 · Monitor de Produção', 25, 36);

      // Indicador Online
      dctx.fillStyle = '#10b981';
      dctx.beginPath();
      dctx.arc(640, 28, 8, 0, Math.PI * 2);
      dctx.fill();

      // Grade 2x3 de Miniaturas de Maçãs (4 Verdes = Aprovadas, 2 Laranjas = Rejeitadas)
      const thumbs = [
        { x: 30,  y: 75,  w: 180, h: 100, col: '#059669', label: 'CAM 1 · 98% OK', tag: 'A' },
        { x: 250, y: 75,  w: 180, h: 100, col: '#059669', label: 'CAM 1 · 96% OK', tag: 'A' },
        { x: 470, y: 75,  w: 180, h: 100, col: '#d97706', label: 'CAM 1 · DEF 88%', tag: 'B' },
        { x: 30,  y: 195, w: 180, h: 100, col: '#059669', label: 'CAM 1 · 99% OK', tag: 'A' },
        { x: 250, y: 195, w: 180, h: 100, col: '#059669', label: 'CAM 1 · 97% OK', tag: 'A' },
        { x: 470, y: 195, w: 180, h: 100, col: '#dc2626', label: 'CAM 1 · MANCHA', tag: 'C' }
      ];
      thumbs.forEach(tb => {
        dctx.fillStyle = '#1e293b';
        dctx.fillRect(tb.x, tb.y, tb.w, tb.h);
        dctx.strokeStyle = tb.col;
        dctx.lineWidth = 3;
        dctx.strokeRect(tb.x, tb.y, tb.w, tb.h);

        // Ícone Maçã
        dctx.fillStyle = tb.col;
        dctx.beginPath();
        dctx.arc(tb.x + 90, tb.y + 45, 26, 0, Math.PI * 2);
        dctx.fill();

        dctx.font = 'bold 13px "Fira Code", monospace';
        dctx.fillStyle = '#f8fafc';
        dctx.fillText(tb.label, tb.x + 15, tb.y + 88);
      });

      // Card de Contadores Grandes
      dctx.fillStyle = '#1e293b';
      dctx.fillRect(30, 315, 620, 60);
      dctx.font = 'bold 24px "Space Grotesk", sans-serif';
      dctx.fillStyle = '#10b981';
      dctx.fillText('Aprovadas: 47', 55, 353);
      dctx.fillStyle = '#64748b';
      dctx.fillText('|', 280, 353);
      dctx.fillStyle = '#f59e0b';
      dctx.fillText('Rejeitadas: 12', 320, 353);

      // Barra de IA & FPS
      dctx.font = 'bold 14px "Fira Code", monospace';
      dctx.fillStyle = '#38bdf8';
      dctx.fillText('IA: 28 FPS · Latência 34 ms · YOLOv8n-seg', 55, 395);

      // Barra de Rodapé Serial
      dctx.fillStyle = '#090d16';
      dctx.fillRect(0, 405, 680, 35);
      dctx.font = '12px "Fira Code", monospace';
      dctx.fillStyle = '#94a3b8';
      dctx.fillText('ESP32 Serial 115200 bps · ESTOP: OK · Belt: 94 mm/s · Servo: PRONTO', 25, 427);

      const dashTexture = new THREE.CanvasTexture(dashCanvas);
      const dashMaterial = new THREE.MeshStandardMaterial({
        map: dashTexture,
        roughness: 0.3,
        emissive: 0x3730a3,
        emissiveIntensity: 0.55
      });
      const dashScreen = new THREE.Mesh(new THREE.PlaneGeometry(320, 200), dashMaterial);
      dashScreen.position.set(0, 110, 5.5);
      lapScreenGroup.add(dashScreen);

      // Cabo USB saindo do notebook até o painel elétrico com VBUS seccionada
      const usbCurve = new THREE.CatmullRomCurve3([
        new THREE.Vector3(-330, 10, 400),
        new THREE.Vector3(-150, 4, 430),
        new THREE.Vector3(100, 4, 440),
        new THREE.Vector3(450, 4, 400),
        new THREE.Vector3(750, -140, 200)
      ]);
      const usbGeo = new THREE.TubeGeometry(usbCurve, 40, 3, 8, false);
      const usbMesh = makeSketchMesh(usbGeo, 0x0f172a);
      notebookHostGroup.add(usbMesh);

      // Disco vermelho de corte da VBUS e sprite de aviso
      const vbusCutDisk = makeSketchMesh(new THREE.CylinderGeometry(6, 6, 4, 16), 0xdc2626);
      vbusCutDisk.position.set(0, 6, 435);
      notebookHostGroup.add(vbusCutDisk);

      const vbusSprite = createFairSprite(
        "VBUS ✂", "#dc2626", "#ffffff", "#f87171",
        160, 64, 45, 18, 'bold 22px monospace'
      );
      vbusSprite.position.set(0, 26, 435);
      notebookHostGroup.add(vbusSprite);

      // -------------------------------------------------------------
      // H. LONA DE FUNDO (fairBackdropGroup) - Z = -400
      // -------------------------------------------------------------
      const fairBackdropGroup = new THREE.Group();
      bancaFeiraGroup.add(fairBackdropGroup);

      // CanvasTexture para a Lona de Fundo Oficial
      const bannerCanvas = document.createElement('canvas');
      bannerCanvas.width = 1024;
      bannerCanvas.height = 1024;
      const bctx = bannerCanvas.getContext('2d');

      // Gradiente de fundo azul escuro -> marinho profundo
      const grad = bctx.createLinearGradient(0, 0, 0, 1024);
      grad.addColorStop(0, '#0f172a');
      grad.addColorStop(0.5, '#1e3a8a');
      grad.addColorStop(1, '#09192f');
      bctx.fillStyle = grad;
      bctx.fillRect(0, 0, 1024, 1024);

      // Grade técnica decorativa sutil
      bctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
      bctx.lineWidth = 1;
      for (let gy = 0; gy < 1024; gy += 64) {
        bctx.beginPath();
        bctx.moveTo(0, gy);
        bctx.lineTo(1024, gy);
        bctx.stroke();
      }
      for (let gx = 0; gx < 1024; gx += 64) {
        bctx.beginPath();
        bctx.moveTo(gx, 0);
        bctx.lineTo(gx, 1024);
        bctx.stroke();
      }

      // Moldura e Brasão FUCAPI 2026
      bctx.strokeStyle = '#d97706';
      bctx.lineWidth = 6;
      bctx.strokeRect(30, 30, 964, 964);

      bctx.font = 'bold 26px "Space Grotesk", sans-serif';
      bctx.fillStyle = '#f59e0b';
      bctx.textAlign = 'center';
      bctx.fillText('XXI FEIRA TECNOLÓGICA FUCAPI · 2026', 512, 110);

      // Título Principal
      bctx.font = '900 68px "Space Grotesk", sans-serif';
      bctx.fillStyle = '#ffffff';
      bctx.fillText('AmazonVision 4.0', 512, 210);

      // Subtítulo
      bctx.font = 'bold 24px "Space Grotesk", sans-serif';
      bctx.fillStyle = '#93c5fd';
      bctx.fillText('Esteira Seletora Inteligente · Classificação de Maçãs por Visão Computacional', 512, 270);

      // 3 Selos de Classificação Oficiais (Classe A, B, C)
      const seals = [
        { x: 200, y: 520, r: 85, col: '#059669', name: 'CLASSE A', sub: 'Aprovadas' },
        { x: 512, y: 520, r: 85, col: '#d97706', name: 'CLASSE B', sub: 'Mercado Int.' },
        { x: 824, y: 520, r: 85, col: '#dc2626', name: 'CLASSE C', sub: 'Defeituosas' }
      ];
      seals.forEach(sl => {
        bctx.fillStyle = sl.col;
        bctx.beginPath();
        bctx.arc(sl.x, sl.y, sl.r, 0, Math.PI * 2);
        bctx.fill();
        bctx.strokeStyle = '#ffffff';
        bctx.lineWidth = 4;
        bctx.stroke();

        // Mini maçã central
        bctx.fillStyle = '#ffffff';
        bctx.beginPath();
        bctx.arc(sl.x, sl.y - 12, 28, 0, Math.PI * 2);
        bctx.fill();

        bctx.font = '900 20px "Space Grotesk", sans-serif';
        bctx.fillStyle = '#0f172a';
        bctx.fillText(sl.name, sl.x, sl.y - 8);

        bctx.font = 'bold 15px "Space Grotesk", sans-serif';
        bctx.fillStyle = '#ffffff';
        bctx.fillText(sl.sub, sl.x, sl.y + 40);
      });

      // Rodapé da Lona
      bctx.font = 'bold 18px "Fira Code", monospace';
      bctx.fillStyle = '#94a3b8';
      bctx.fillText('Engenharia Mecatrônica · Hardware Aberto · Arquitetura 12V Mono-Fonte', 512, 880);

      const bannerTex = new THREE.CanvasTexture(bannerCanvas);
      const bannerMat = new THREE.MeshStandardMaterial({
        map: bannerTex,
        roughness: 0.6,
        metalness: 0.1
      });
      const bannerPlane = new THREE.Mesh(new THREE.PlaneGeometry(2400, 2400), bannerMat);
      bannerPlane.position.set(0, -420, -400);
      fairBackdropGroup.add(bannerPlane);

      // 2 Barras LED Cenográficas no topo da lona BoxGeometry(900, 20, 30) em #e0f2fe
      [-500, 500].forEach(lx => {
        const ledMesh = makeSketchMesh(new THREE.BoxGeometry(900, 20, 30), 0xe0f2fe);
        ledMesh.position.set(lx, 780, -380);
        fairBackdropGroup.add(ledMesh);
      });

      // -------------------------------------------------------------
      // I. SILHUETAS HUMANAS: OPERADOR + VISITANTES (peopleGroup)
      // -------------------------------------------------------------
      const peopleGroup = new THREE.Group();
      bancaFeiraGroup.add(peopleGroup);

      // Helper para montar silhueta humana em estilo CAD nanquim
      function createPersonFigure(colorHex, armAngle = 0) {
        const pGroup = new THREE.Group();
        // Pernas (Y=-1620 a -870)
        [-35, 35].forEach(legX => {
          const leg = makeSketchMesh(new THREE.BoxGeometry(70, 750, 70), colorHex);
          leg.position.set(legX, -1245, 0);
          pGroup.add(leg);
        });
        // Tronco (Y=-870 a -270)
        const torso = makeSketchMesh(new THREE.BoxGeometry(260, 600, 120), colorHex);
        torso.position.set(0, -570, 0);
        pGroup.add(torso);
        // Cabeça
        const head = makeSketchMesh(new THREE.SphereGeometry(90, 16, 16), colorHex);
        head.position.set(0, -140, 0);
        pGroup.add(head);
        // Braço esquerdo
        const armL = makeSketchMesh(new THREE.BoxGeometry(60, 550, 60), colorHex);
        armL.position.set(-165, -570, 0);
        pGroup.add(armL);
        // Braço direito
        const armR = makeSketchMesh(new THREE.BoxGeometry(60, 550, 60), colorHex);
        armR.position.set(165, -570, 0);
        if (armAngle !== 0) {
          armR.position.set(165, -450, 120);
          armR.rotation.x = -armAngle; // apontando para a esteira
        }
        pGroup.add(armR);
        return pGroup;
      }

      // Operador à esquerda da bancada (X=-700, Z=+300) olhando para o notebook
      const operatorFigure = createPersonFigure(0x475569);
      operatorFigure.position.set(-700, 0, 300);
      operatorFigure.rotation.y = 0.55; // virado para a tela do notebook
      peopleGroup.add(operatorFigure);

      // Visitante 1 à frente (X=-150, Z=+650)
      const visitor1 = createPersonFigure(0x334155);
      visitor1.position.set(-150, 0, 650);
      visitor1.rotation.y = -0.15;
      peopleGroup.add(visitor1);

      // Visitante 2 à frente (X=+150, Z=+680) apontando para a esteira
      const visitor2 = createPersonFigure(0x64748b, 0.78);
      visitor2.position.set(150, 0, 680);
      visitor2.rotation.y = -0.35;
      peopleGroup.add(visitor2);

      // -------------------------------------------------------------
      // J. PLACA DE IDENTIFICAÇÃO DO PROJETO (signageGroup)
      // -------------------------------------------------------------
      const signageGroup = new THREE.Group();
      bancaFeiraGroup.add(signageGroup);

      // Placa A4 vertical (210 x 297 mm) em acrílico #f8fafc em X=-300, Y=-250, Z=+600
      const signCanvas = document.createElement('canvas');
      signCanvas.width = 420;
      signCanvas.height = 594;
      const sctx = signCanvas.getContext('2d');

      sctx.fillStyle = '#f8fafc';
      sctx.fillRect(0, 0, 420, 594);

      // Borda verde #059669 de 6px (3mm em escala)
      sctx.strokeStyle = '#059669';
      sctx.lineWidth = 10;
      sctx.strokeRect(8, 8, 404, 578);

      sctx.textAlign = 'center';
      sctx.font = '900 36px "Space Grotesk", sans-serif';
      sctx.fillStyle = '#0f172a';
      sctx.fillText('AmazonVision 4.0', 210, 110);

      sctx.font = 'bold 20px "Space Grotesk", sans-serif';
      sctx.fillStyle = '#059669';
      sctx.fillText('Esteira Seletora Inteligente', 210, 165);
      sctx.fillText('de Maçãs', 210, 195);

      sctx.font = '16px "Space Grotesk", sans-serif';
      sctx.fillStyle = '#475569';
      sctx.fillText('Visão Computacional · Classificação A/B/C', 210, 260);
      sctx.fillText('Arquitetura 12V Mono-Fonte & NR-12', 210, 295);

      sctx.font = 'bold 18px "Space Grotesk", sans-serif';
      sctx.fillStyle = '#1e293b';
      sctx.fillText('Equipe FUCAPI 2026', 210, 420);

      sctx.font = '13px "Fira Code", monospace';
      sctx.fillStyle = '#94a3b8';
      sctx.fillText('XXI Feira Tecnológica · Manaus/AM', 210, 460);

      const signTex = new THREE.CanvasTexture(signCanvas);
      const signMesh = makeSketchMesh(new THREE.BoxGeometry(210, 297, 6), 0xf8fafc);
      signMesh.position.set(-300, -250, 600);
      signMesh.rotation.x = -0.15;
      signageGroup.add(signMesh);

      const signFace = new THREE.Mesh(
        new THREE.PlaneGeometry(204, 291),
        new THREE.MeshBasicMaterial({ map: signTex })
      );
      signFace.position.set(-300, -250, 604);
      signFace.rotation.x = -0.15;
      signageGroup.add(signFace);

      // Pedestal/haste da placa até o piso
      const signPole = makeSketchMesh(new THREE.CylinderGeometry(8, 8, 1200, 12), 0x334155);
      signPole.position.set(-300, -1000, 580);
      signageGroup.add(signPole);
      const signBaseFoot = makeSketchMesh(new THREE.CylinderGeometry(80, 80, 15, 20), 0x0f172a);
      signBaseFoot.position.set(-300, -1612.5, 580);
      signageGroup.add(signBaseFoot);

      // -------------------------------------------------------------
      // K. SETAS DE FLUXO (flowArrowsGroup)
      // -------------------------------------------------------------
      const flowArrowsGroup = new THREE.Group();
      bancaFeiraGroup.add(flowArrowsGroup);

      // Trajetória Aprovada: Verde #059669
      const approvedPath = [
        new THREE.Vector3(-450, 180, 0),
        new THREE.Vector3(-300, 140, 0),
        new THREE.Vector3(-150, 140, 0),
        new THREE.Vector3( 100, 140, 0),
        new THREE.Vector3( 325, 140, 0),
        new THREE.Vector3( 450, -400, 30),
        new THREE.Vector3( 560, -1400, 50)
      ];
      const appCurve = new THREE.CatmullRomCurve3(approvedPath);
      const appFlowGeo = new THREE.BufferGeometry().setFromPoints(appCurve.getPoints(50));
      const appFlowMat = new THREE.LineDashedMaterial({ color: 0x059669, dashSize: 18, gapSize: 10, linewidth: 2 });
      const appFlowLine = new THREE.Line(appFlowGeo, appFlowMat);
      appFlowLine.computeLineDistances();
      flowArrowsGroup.add(appFlowLine);

      const spFlowApp = createFairSprite("FLUXO APROVADO · CLASSE A", "#059669", "#ffffff", "#34d399", 320, 64, 150, 30);
      spFlowApp.position.set(430, 200, 0);
      flowArrowsGroup.add(spFlowApp);

      // Trajetória Rejeitada: Laranja #d97706
      const rejectedPath = [
        new THREE.Vector3( 160, 140, 0),
        new THREE.Vector3( 160, 80, 105),
        new THREE.Vector3( 200, -400, 240),
        new THREE.Vector3( 280, -1400, 380)
      ];
      const rejCurve = new THREE.CatmullRomCurve3(rejectedPath);
      const rejFlowGeo = new THREE.BufferGeometry().setFromPoints(rejCurve.getPoints(40));
      const rejFlowMat = new THREE.LineDashedMaterial({ color: 0xd97706, dashSize: 18, gapSize: 10, linewidth: 2 });
      const rejFlowLine = new THREE.Line(rejFlowGeo, rejFlowMat);
      rejFlowLine.computeLineDistances();
      flowArrowsGroup.add(rejFlowLine);

      const spFlowRej = createFairSprite("FLUXO REJEITADO · CLASSES B/C", "#d97706", "#ffffff", "#fbbf24", 340, 64, 160, 30);
      spFlowRej.position.set(220, 140, 180);
      flowArrowsGroup.add(spFlowRej);
'''

print(f"Fair JS lines: {len(fair_js.strip().splitlines())}")
