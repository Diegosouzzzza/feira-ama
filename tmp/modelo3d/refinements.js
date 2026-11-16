// Detalhamento estático da montagem: materiais, ferragens e acabamentos.
export function refineAssembly(a){
const {T,scene,M,mat,texture,rand,mesh,box,cyl,sph,rod,screw,wire,label,group,part,parts,glass,glow,table,topMat,belt,beltMat,guides,vision,lighting,motor,servo,tray,esp,opto,driver,supply,cables,laptop,lid,approved,rejected}=a;
const repeat=(t,x,y)=>{t.wrapS=t.wrapT=T.RepeatWrapping;t.repeat.set(x,y);return t;};
const brushed=texture(1024,512,(c,w,h)=>{c.fillStyle='#919191';c.fillRect(0,0,w,h);for(let i=0;i<12500;i++){const v=110+rand()*90;c.strokeStyle=`rgba(${v},${v},${v},.23)`;const x=rand()*w,y=rand()*h;c.beginPath();c.moveTo(x,y);c.lineTo(x+35+rand()*280,y+.15);c.stroke();}});
brushed.colorSpace=T.NoColorSpace;repeat(brushed,2,2);
for(const m of [M.aluminum,M.steel]){m.bumpMap=brushed;m.bumpScale=.035;m.roughnessMap=brushed;m.roughness=.53;m.envMapIntensity=1.3;}
const powder=texture(256,256,(c,w,h)=>{const im=c.createImageData(w,h);for(let i=0;i<im.data.length;i+=4){const v=118+rand()*40;im.data[i]=im.data[i+1]=im.data[i+2]=v;im.data[i+3]=255;}c.putImageData(im,0,0);});powder.colorSpace=T.NoColorSpace;repeat(powder,7,3);M.black.bumpMap=powder;M.black.bumpScale=.027;M.black.roughness=.43;M.black.color.set('#242927');
M.dark.roughness=.42;M.rubber.color.set('#202420');M.green.color.set('#164830');M.blue.color.set('#185a77');
// Tampo laminado com veios, emendas discretas e aresta de madeira.
const wood=texture(2048,1024,(c,w,h)=>{c.fillStyle='#c9ae87';c.fillRect(0,0,w,h);for(let y=0;y<h;y++){const v=Math.sin(y*.032)*5+Math.sin(y*.71)*2;c.strokeStyle=`rgba(${102+v},${69+v},${38+v},${.04+rand()*.09})`;c.beginPath();for(let x=0;x<=w;x+=24){const yy=y+Math.sin(x*.006+y*.04)*2.4+Math.sin(x*.013)*.7;x===0?c.moveTo(x,yy):c.lineTo(x,yy);}c.stroke();}for(let i=0;i<40000;i++){c.fillStyle=rand()>.5?'#ffffff08':'#29180509';c.fillRect(rand()*w,rand()*h,rand()*15+2,.7);}});
topMat.map=wood;topMat.bumpMap=wood;topMat.bumpScale=.055;topMat.roughness=.66;topMat.needsUpdate=true;
const edge=mat('#ac865b',.67);for(const z of [-55.03,55.03]){box(table,180,.08,.03,0,-2.9,z,edge);box(table,180,.08,.03,0,-.45,z,edge);}
// Nervures de profilé et assemblages de la table.
for(const x of [-80,80])for(const z of [-45,45]){for(const dx of [-1.1,1.1])box(table,.26,65,.08,x+dx,-39,z+2.05,M.dark);box(table,6,8,.45,x,-8,z+2.3,M.black,.2);for(const yy of [-5.5,-10.5])screw(table,x,yy,z+2.65,'z',.4);box(table,4.1,.5,4.1,x,-72,z,M.dark,.18);}
// Ombres de contact douces sous les ensembles : présence et poids sur le plateau.
const shade=texture(128,128,(c,w,h)=>{const g=c.createRadialGradient(w/2,h/2,5,w/2,h/2,w/2);g.addColorStop(0,'rgba(20,24,20,.38)');g.addColorStop(.45,'rgba(20,24,20,.19)');g.addColorStop(1,'rgba(20,24,20,0)');c.fillStyle=g;c.fillRect(0,0,w,h);});
const contacts=group('Ombres de contact');function contact(x,z,w,d,opacity=.65,y=.055){const m=new T.MeshBasicMaterial({map:shade,transparent:true,opacity,depthWrite:false});const o=mesh(new T.PlaneGeometry(w,d),m,contacts,x,y,z);o.rotation.x=-Math.PI/2;o.castShadow=false;o.receiveShadow=false;}
contact(-12,-5,119,43,.65);contact(-31,32,73,33,.6);contact(-73,28,19,28,.9);contact(49,-33,45,32,.8);contact(62,-5,30,30,.65);contact(28,35,30,30,.65);contact(-33,-27,23,17,.6);
// Cadre de la miniesteira : tirants, manchons et tendeurs réellement fixés.
for(const z of [-13.3,13.3]){
box(belt,91,.55,.16,0,14.8,z+(z>0?.85:-.85),M.dark);
for(const x of [-46,46]){const side=z>0?1:-1;box(belt,7,6,.5,x,18,z+side*1.1,M.black,.35);const hub=cyl(belt,1.8,1.3,x,18,z+side*1.35,M.steel,32);hub.rotation.x=Math.PI/2;const ring=mesh(new T.TorusGeometry(1.27,.17,10,40),M.dark,belt,x,18,z+side*2.05);for(const dx of [-2.4,2.4])for(const dy of [-1.7,1.7])screw(belt,x+dx,18+dy,z+side*1.44,'z',.23);}
box(belt,5.4,2.7,2.1,-49,17.8,z,M.black,.2);rod(belt,[-53,18,z],[-47,18,z],.25,M.steel);const nut=cyl(belt,.58,.55,-51.5,18,z,M.gold,6);nut.rotation.z=Math.PI/2;
}
for(const x of [-35,0,35]){box(belt,2,2,25,x,13,0,M.aluminum,.15);for(const z of [-11,11])screw(belt,x,14.05,z);}
for(const x of [-40,40])for(const z of [-13,13]){box(belt,.5,5,5,x-1.7,18,z,M.black,.2);for(const yy of [16.5,19.5])screw(belt,x-2,yy,z+2.55,'z',.22);}
// Vis de réglage des guides et molettes.
for(const z of [-15,5])for(const x of [-52,-8,24]){cyl(guides,.78,.45,x,23.7,z,M.black,16);cyl(guides,.22,1.4,x,24.1,z,M.steel,20);for(let i=0;i<8;i++){const ang=i*Math.PI/4;sph(guides,.12,x+Math.cos(ang)*.69,23.7,z+Math.sin(ang)*.69,M.rubber);}}
// Accouplement entre la boîte du moteur et le rouleau : axes coaxiaux.
motor.position.set(34,2,11);const motorPart=parts.find(p=>p.id==='07');motorPart.point.set(34,23,14);motorPart.target.set(34,18,11);
rod(motor,[0,16,-8],[0,16,-2],.6,M.steel);const coupler=cyl(motor,1.2,3,0,16,-4.6,M.aluminum,32);coupler.rotation.x=Math.PI/2;
for(const z of [-5.5,-4.9,-4.3,-3.7]){const r=mesh(new T.TorusGeometry(1.21,.045,6,32),M.dark,motor,0,16,z);}box(motor,2,5,6,-4.1,14,2,M.black,.15);
label(motor,'DC  /  GEAR MOTOR',5,1.6,0,19.53,1,{bg:'#d6b843',fg:'#333323',font:40,rotX:-Math.PI/2});
for(let ang=0;ang<Math.PI*2;ang+=Math.PI/4){const x=Math.sin(ang)*2.31,y=16+Math.cos(ang)*2.31;box(motor,.36,1.5,2,x,y,6,M.dark,.06).rotation.z=-ang;}
wire(cables,[[19,4,27],[17,3.5,27],[15,2,27]],'#a44831',.19);wire(cables,[[19,4.3,28],[17,3.5,28],[15,2.3,28]],'#202720',.19);
// Servo : assemblage du boîtier, oreilles, rotule et attache de la palette.
box(servo,4.26,.12,2.48,0,22.3,6,M.rubber,.08);box(servo,4.26,.12,2.48,0,25.25,6,M.rubber,.08);
for(const x of [-1.65,1.65])for(const z of [5.15,6.85])screw(servo,x,27,z,'y',.18);
box(servo,2.5,.32,3,-1.3,28.12,4.3,M.aluminum,.15);rod(servo,[-1.5,28.05,2.5],[-1.5,26,2.5],.26,M.steel);for(const z of [2.8,5.2])screw(servo,-1.4,28.33,z,'y',.22);
// Monture caméra : manettes, bagues, mors caoutchoutés, câbles retenus.
for(const yy of [11,29,47]){const tie=mesh(new T.TorusGeometry(1.21,.15,6,28),M.dark,vision,0,yy,-22);tie.rotation.x=Math.PI/2;box(vision,.7,.45,.7,1.2,yy,-22,M.dark,.1);}
for(const yy of [49,53]){rod(vision,[1.1,yy,-22],[3.5,yy,-22],.3,M.steel);cyl(vision,.75,.8,3.5,yy,-22,M.dark,12).rotation.z=Math.PI/2;}
for(const x of [-4.15,4.15])box(vision,.45,1.7,2.9,x,55.2,0,M.rubber,.1);
box(vision,.15,.23,2.3,4.33,55.22,-3.8,M.aluminum,.05);box(vision,.15,.23,1,4.33,55.22,-.8,M.aluminum,.05);box(vision,1.2,.25,.3,0,55.2,7.65,M.dark,.08);
// Anel LED com tampa translúcida e LEDs individuais pela face inferior.
for(let i=0;i<40;i++){const ang=i/40*Math.PI*2;const x=Math.cos(ang)*5.6,z=Math.sin(ang)*5.6;box(lighting,.25,.08,.36,x,-.87,z,glow,.03).rotation.y=-ang;}
wire(lighting,[[0,0,-6],[1,0,-12],[1,-5,-22],[2,-39,-22],[8,-48,-26]],'#242824',.13);
// Serigrafia de placas, soldas e componentes discretos.
for(const board of [esp,opto,driver,...parts.filter(p=>['15','16'].includes(p.id)).map(p=>p.g)]){
const isESP=board===esp,w=isESP?5.7:board===opto||board===driver?6:10,d=isESP?10:board===opto||board===driver?5:6;
for(let i=0;i<18;i++){const x=-w*.34+rand()*w*.68,z=-d*.35+rand()*d*.7;if(isESP&&Math.abs(x)<1.9&&z<1.9)continue;box(board,.38,.12,.17,x,.23,z,M.chip,.02);box(board,.065,.14,.18,x-.17,.23,z,M.steel);box(board,.065,.14,.18,x+.17,.23,z,M.steel);}
for(let i=0;i<12;i++){const x=-w*.43+(i%2)*w*.86,z=-d*.32+Math.floor(i/2)*d*.13;cyl(board,.12,.035,x,.12,z,M.steel,12);}
}
// Brochage sérigraphié de chaque côté du DevKit (repères visuels).
for(let i=0;i<12;i++){const z=-3.8+i*.58;label(esp,['3V3','EN','VP','VN','34','35','32','33','25','26','27','GND'][i],.72,.3,-1.86,.235,z,{bg:'#151d18',fg:'#b7c2b4',font:100,rotX:-Math.PI/2});}
label(esp,'ESP32-WROOM',2.7,.55,0,.901,-1.3,{bg:'#b5c1bd',fg:'#3e4a43',font:68,rotX:-Math.PI/2});
label(opto,'IN1  IN2  GND',4,.55,0,.22,-1.65,{bg:'#164830',fg:'#bdc7af',font:55,rotX:-Math.PI/2});
for(const id of ['15','16']){const b=parts.find(p=>p.id===id).g;label(b,'IN+  IN−',2,.45,-3.5,.23,-2.25,{bg:'#185a77',fg:'#e0e7d2',font:66,rotX:-Math.PI/2});label(b,'OUT+ OUT−',2.7,.45,3.35,.23,2.36,{bg:'#185a77',fg:'#e0e7d2',font:57,rotX:-Math.PI/2});}
// Connecteurs Dupont, gaines et colliers autour des points de terminaison.
for(let i=0;i<3;i++)box(cables,.42,.8,.42,-42.65,4.5,28+i*.57,M.dark,.06);
for(const [x,z] of [[-34,17],[-18,13],[9,20],[-31,38],[-7,33]]){const tie=mesh(new T.TorusGeometry(.65,.065,6,20),M.dark,cables,x,2.8,z);tie.rotation.y=Math.PI/2;box(cables,.28,.3,.4,x,3.4,z,M.dark,.04);}
for(const [x,z,text] of [[-35,17,'12 V'],[-19,20,'SERVO'],[-20,38,'SINAL'],[9,29,'MOTOR']])label(cables,text,3.5,1.1,x,3.4,z,{bg:'#e6e0bf',fg:'#353c32',font:68,rotX:-Math.PI/2});
for(const x of [-29,29])for(const z of [-11,11]){cyl(tray,.93,.12,x,2.56,z,M.white,24);screw(tray,x,2.66,z);}
// Acrílico com juntas e apoios de borracha; sem aparência de caixa vazada.
for(const b of [approved,rejected]){for(const x of [-11,11])for(const z of [-11,11])cyl(b,.7,.45,x,.4,z,M.rubber);for(const z of [-12.3,12.3])rod(b,[-12,1.3,z],[12,1.3,z],.12,M.aluminum);}
// Notebook : touches imprimées, port USB, aérations et cordon secteur.
const keyboard=texture(1536,600,(c,w,h)=>{c.clearRect(0,0,w,h);const rows=['ESC 1 2 3 4 5 6 7 8 9 0 − ⌫','TAB Q W E R T Y U I O P [ ] \\','CAP A S D F G H J K L ; ENTER ↑','SHIFT Z X C V B N M , . / SHIFT ↑','CTRL FN WIN ALT SPACE SPACE SPACE SPACE ALT CTRL ← ↓ →'];c.fillStyle='#b2bdb9';c.font='21px Arial';c.textAlign='center';c.textBaseline='middle';rows.forEach((row,y)=>row.split(' ').forEach((t,x)=>c.fillText(t,55+x*108,53+y*116)));});
const keymat=new T.MeshBasicMaterial({map:keyboard,transparent:true,depthWrite:false});const keylabels=mesh(new T.PlaneGeometry(31.8,10.4),keymat,laptop,0,1.81,-4.4);keylabels.rotation.x=-Math.PI/2;keylabels.castShadow=false;
for(const x of [-16.8,16.8])for(let z=-7;z<1;z+=.6)box(laptop,.3,.035,.25,x,1.35,z,M.dark);
for(let x=-13;x<14;x+=.6)box(laptop,.24,.5,.14,x,.6,12.54,M.dark,.03);
label(lid,'AMAZONVISION  /  LOCAL INFERENCE',13,.6,0,.8,-.46,{bg:'#242927',fg:'#c1cbbf',font:40,rotY:Math.PI});
// Filtro de linha completo e caixa de operação, montados e identificados.
const strip=part('20','Filtro de linha e tomadas','Distribuição de energia da bancada','Filtro de linha fechado com tomadas, interruptor e cabos das fontes. Representação visual de uma bancada organizada.','Conjunto de alimentação',[-5,7,-46],[-5,0,-46],[-5,4,-46],44);
box(strip,36,3.5,6,0,2,0,M.white,.7);for(const x of [-11,-3,5]){box(strip,5.5,.17,4.9,x,3.84,0,M.white,.7);for(const [dx,dz] of [[-.85,.65],[.85,.65],[0,-.8]])cyl(strip,.27,.04,x+dx,3.95,dz,M.dark,16);}
box(strip,3.5,.3,3.2,13,3.92,0,M.dark,.4);box(strip,2.5,.4,2.2,13,4.1,0,M.red,.3);label(strip,'I',.5,.8,13,4.33,0,{bg:'#b9432d',fg:'#eedccd',font:120,rotX:-Math.PI/2});
for(const x of [-9,-1]){box(strip,2.5,2.1,3,x,4.7,0,M.dark,.5);rod(strip,[x,4.8,0],[x,4.8,2.2],.25,M.rubber);}
wire(strip,[[18,2,0],[23,1.5,-1],[44,1,-6],[71,1,-7],[90,-4,-7],[91,-36,-7]],'#242824',.32);
const panel=part('21','Comando e parada de emergência','Botões físicos na bancada','Caixa fechada com chave liga/desliga e botão de emergência. Complementa visualmente os itens de montagem da lista de materiais.','Caixa ABS · botões e prensa-cabos',[67,10,33],[67,0,33],[67,7,33],33);
box(panel,18,5.8,14,0,3.1,0,M.white,.7);box(panel,18.15,.55,14.15,0,6.2,0,M.white,.5);for(const x of [-7.2,7.2])for(const z of [-5.2,5.2])screw(panel,x,6.6,z);
cyl(panel,3,.4,-3,6.65,-1,M.yellow,48);cyl(panel,1.1,1.6,-3,7.5,-1,M.dark,32);cyl(panel,2.2,1.3,-3,8.7,-1,M.red,48);sph(panel,2.2,-3,9.2,-1,M.red,1,.18,1);
cyl(panel,1.8,.5,4,6.65,-1,M.steel);cyl(panel,1.5,.55,4,7,-1,M.dark);box(panel,.6,.8,2.6,4,7.6,-1,M.dark,.16);label(panel,'EMERGÊNCIA',7,1.4,-3,6.5,4,{bg:'#e8e9da',fg:'#6e3429',font:45,rotX:-Math.PI/2});label(panel,'I / O',3,1.4,4.3,6.5,4,{bg:'#e8e9da',fg:'#324631',font:60,rotX:-Math.PI/2});
const gland=cyl(panel,.75,1.7,-9.5,2.7,0,M.dark,12);gland.rotation.z=Math.PI/2;wire(cables,[[57,2.7,33],[50,2,28],[44,1,21],[8,1,16],[-5,2,23]],'#272d28',.25);
// Acessórios discretos: plaqueta técnica fixada e régua de referência na base.
label(belt,'AV-01   /   INSPEÇÃO VISUAL',20,1.4,16,14.8,14.2,{bg:'#b5c1bd',fg:'#273931',font:36});
for(let i=0;i<31;i++){box(tray,.04,.02,i%5===0?1.1:.6,-15+i,2.43,-12.6,M.dark);if(i%10===0)label(tray,String(i),1,.5,-15+i,2.44,-11.65,{bg:'#dfe6d6',font:100,rotX:-Math.PI/2});}
}
