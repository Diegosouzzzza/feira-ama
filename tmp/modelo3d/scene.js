import * as T from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {RoomEnvironment} from 'three/addons/environments/RoomEnvironment.js';
import {RoundedBoxGeometry} from 'three/addons/geometries/RoundedBoxGeometry.js';
import {mergeGeometries} from 'three/addons/utils/BufferGeometryUtils.js';
import {refineAssembly} from './refinements.js';

const $=s=>document.querySelector(s), canvas=$('#scene'), viewport=$('#viewport');
let renderer;
try{renderer=new T.WebGLRenderer({canvas,antialias:true,alpha:false,preserveDrawingBuffer:true,powerPreference:'high-performance'});}catch(e){$('#loading').innerHTML='<div class="loading-box"><strong>O navegador não iniciou o 3D.</strong>Abra este HTML no Chrome ou Edge com a aceleração gráfica ativada.</div>';throw e;}
renderer.setPixelRatio(Math.min(devicePixelRatio,2));
renderer.outputColorSpace=T.SRGBColorSpace;renderer.toneMapping=T.ACESFilmicToneMapping;renderer.toneMappingExposure=.96;
renderer.shadowMap.enabled=true;renderer.shadowMap.type=T.VSMShadowMap;
const scene=new T.Scene();scene.background=new T.Color('#e8e9e2');scene.fog=new T.Fog('#e8e9e2',420,1000);
const camera=new T.PerspectiveCamera(36,1,.3,1500);
const controls=new OrbitControls(camera,canvas);controls.enableDamping=false;controls.minDistance=18;controls.maxDistance=950;controls.maxPolarAngle=Math.PI*.49;controls.target.set(0,13,0);
const pmrem=new T.PMREMGenerator(renderer),room=new RoomEnvironment();scene.environment=pmrem.fromScene(room,.06).texture;scene.environmentIntensity=.5;room.dispose();pmrem.dispose();
scene.add(new T.HemisphereLight(0xf8ffec,0x7d8171,.65));
const key=new T.DirectionalLight(0xfff4df,2.15);key.position.set(-65,160,80);key.castShadow=true;key.shadow.mapSize.set(2048,2048);Object.assign(key.shadow.camera,{left:-145,right:145,top:115,bottom:-125,near:1,far:450});key.shadow.normalBias=.12;key.shadow.bias=-.0001;key.shadow.radius=4;key.shadow.blurSamples=8;scene.add(key);
const fill=new T.DirectionalLight(0xdce9ff,.85);fill.position.set(80,80,-110);scene.add(fill);

const mat=(color,roughness=.5,metalness=0)=>new T.MeshStandardMaterial({color,roughness,metalness});
const M={black:mat('#202923',.42,.3),dark:mat('#111813',.53,.05),rubber:mat('#282b26',.91),steel:mat('#b5c1bd',.27,.85),aluminum:mat('#c4ceca',.36,.75),gold:mat('#ba984c',.35,.72),white:mat('#e8e9da',.58),green:mat('#164d33',.48,.18),blue:mat('#235c91',.46,.15),terminal:mat('#227da6',.5),red:mat('#b9432d',.55),yellow:mat('#e8b73d',.46,.1),chip:mat('#171c19',.72),copper:mat('#be8647',.34,.7)};
const glass=new T.MeshPhysicalMaterial({color:'#edf9f7',transparent:true,opacity:.16,roughness:.09,metalness:.12,clearcoat:1,clearcoatRoughness:.07,side:T.DoubleSide,depthWrite:false});
const glow=new T.MeshStandardMaterial({color:0xf5fff2,emissive:0xe6ffdb,emissiveIntensity:2,roughness:.25});
const ledGreen=new T.MeshStandardMaterial({color:0x55c98c,emissive:0x33d96a,emissiveIntensity:1.3});
const ledRed=new T.MeshStandardMaterial({color:0xe35230,emissive:0xe13c17,emissiveIntensity:.8});
const wireMats={};const parts=[],allGroups=[];
function group(name,x=0,y=0,z=0){const g=new T.Group();g.name=name;g.position.set(x,y,z);scene.add(g);allGroups.push(g);return g;}
function mesh(geo,material,parent,x=0,y=0,z=0){const m=new T.Mesh(geo,material);m.position.set(x,y,z);m.castShadow=material!==glass;m.receiveShadow=true;parent.add(m);return m;}
function box(p,w,h,d,x,y,z,m=M.black,r=0){return mesh(r?new RoundedBoxGeometry(w,h,d,3,Math.min(r,w*.49,h*.49,d*.49)):new T.BoxGeometry(w,h,d),m,p,x,y,z);}
function cyl(p,r,h,x,y,z,m=M.steel,segments=24){return mesh(new T.CylinderGeometry(r,r,h,segments),m,p,x,y,z);}
function sph(p,r,x,y,z,m=M.black,sx=1,sy=1,sz=1){const a=mesh(new T.SphereGeometry(r,24,16),m,p,x,y,z);a.scale.set(sx,sy,sz);return a;}
function rod(p,a,b,r,m=M.steel){const start=new T.Vector3(...a),end=new T.Vector3(...b);const o=cyl(p,r,start.distanceTo(end),...(start.clone().add(end).multiplyScalar(.5).toArray()),m);o.quaternion.setFromUnitVectors(new T.Vector3(0,1,0),end.sub(start).normalize());return o;}
function screw(p,x,y,z,axis='y',size=.3){const g=new T.Group();g.position.set(x,y,z);if(axis==='z')g.rotation.x=Math.PI/2;if(axis==='x')g.rotation.z=Math.PI/2;p.add(g);cyl(g,size*1.27,.065,0,-.08,0,M.steel,24);cyl(g,size,.16,0,0,0,M.steel,24);cyl(g,size*.48,.012,0,.085,0,M.dark,6);return g;}
function wire(p,pts,color='#20241f',radius=.13){const m=wireMats[color]??(wireMats[color]=mat(color,.65));return mesh(new T.TubeGeometry(new T.CatmullRomCurve3(pts.map(a=>new T.Vector3(...a))),Math.max(20,pts.length*8),radius,7,false),m,p);}
let seed=8734;function rand(){seed=(seed*1664525+1013904223)>>>0;return seed/4294967296;}
function texture(w,h,paint){const c=document.createElement('canvas');c.width=w;c.height=h;paint(c.getContext('2d'),w,h);const t=new T.CanvasTexture(c);t.colorSpace=T.SRGBColorSpace;t.anisotropy=8;return t;}
function label(p,text,w,h,x,y,z,{bg='#e7e9db',fg='#243b30',font=40,rotX=0,rotY=0}={}){const t=texture(512,Math.max(64,Math.round(512*h/w)),(c,cw,ch)=>{c.fillStyle=bg;c.fillRect(0,0,cw,ch);c.fillStyle=fg;c.font=`600 ${font}px Arial`;c.textAlign='center';c.textBaseline='middle';c.fillText(text,cw/2,ch/2,cw-22);});const o=mesh(new T.PlaneGeometry(w,h),new T.MeshStandardMaterial({map:t,roughness:.73,metalness:0}),p,x,y,z);o.rotation.set(rotX,rotY,0);o.castShadow=false;return o;}
function part(id,title,sub,desc,spec,point,pos,target,radius=38){const g=group(title,...pos);g.userData.part=id;parts.push({id,title,sub,desc,spec,point:new T.Vector3(...point),target:new T.Vector3(...target),radius,g});return g;}

// Bancada: tampo laminado, bordas arredondadas, perfis, pés e niveladores.
const table=group('Bancada');
const topTexture=texture(512,512,(c,w,h)=>{c.fillStyle='#e0ddce';c.fillRect(0,0,w,h);for(let i=0;i<38000;i++){const v=rand()>.5?255:90;c.fillStyle=`rgba(${v},${v},${v},${rand()*.035})`;c.fillRect(rand()*w,rand()*h,1+rand()*2,1);}});
topTexture.wrapS=topTexture.wrapT=T.RepeatWrapping;topTexture.repeat.set(4,3);
const topMat=new T.MeshStandardMaterial({map:topTexture,roughness:.59,bumpMap:topTexture,bumpScale:.08});
box(table,184,3.4,110,0,-1.7,0,topMat,.8);box(table,183,1.4,109,0,-3.3,0,M.white,.5);
for(const x of [-80,80]){for(const z of [-45,45]){box(table,4,68,4,x,-39,z,M.aluminum,.35);cyl(table,2.9,2,x,-74.5,z,M.rubber);cyl(table,1.1,4,x,-72,z,M.steel);}box(table,4,4,92,x,-61,0,M.aluminum,.2);}
for(const z of [-45,45]){box(table,164,5,3,0,-8,z,M.aluminum,.25);box(table,158,3,3,0,-61,z,M.aluminum,.2);}
label(table,'AMAZONVISION 4.0  /  FUCAPI 2026',36,2.2,-52,-1.5,55.06,{bg:'#e0ddce',fg:'#455444',font:23});
const floor=mesh(new T.PlaneGeometry(2000,2000),mat('#dcdfd4',.87),scene,0,-76,0);floor.rotation.x=-Math.PI/2;floor.castShadow=false;

// Esteira transportadora: correia contínua envolvendo dois roletes e laterais fixadas.
const belt=part('01','Miniesteira transportadora','Estrutura, correia e roletes','Miniesteira de bancada com laterais metálicas, roletes, correia clara e pés reguláveis. O produto permanece parado nesta representação.','Conjunto mecânico · 1 unidade',[-7,25,6],[-12,0,-5],[-12,15,-5],100);
for(const x of [-40,40])for(const z of [-13,13]){box(belt,2.4,16,2.4,x,10,z,M.black,.25);box(belt,7,1,6,x,1.4,z,M.black,.4);screw(belt,x-2,2,z);screw(belt,x+2,2,z);cyl(belt,1.7,1.3,x,.6,z,M.rubber);}
for(const z of [-13.3,13.3]){box(belt,101,8,1.6,0,17,z,M.black,.6);box(belt,99,.7,1.9,0,21,z,M.aluminum,.2);for(let x=-46;x<=46;x+=11.5)screw(belt,x,17.5,z+(z>0?.86:-.86),'z',.34);for(const x of [-44,44]){const b=cyl(belt,2.7,1.9,x,18,z,M.dark);b.rotation.x=Math.PI/2;const cap=cyl(belt,1.25,2,x,18,z,M.steel);cap.rotation.x=Math.PI/2;}}
for(const x of [-46,46]){const o=cyl(belt,3.8,24,x,18,0,M.aluminum,48);o.rotation.x=Math.PI/2;}
const beltTex=texture(256,256,(c,w,h)=>{c.fillStyle='#dfdeca';c.fillRect(0,0,w,h);for(let y=0;y<h;y+=3){c.strokeStyle='rgba(110,110,88,.12)';c.beginPath();c.moveTo(0,y);c.lineTo(w,y);c.stroke();}for(let x=0;x<w;x+=4){c.strokeStyle='rgba(255,255,245,.23)';c.beginPath();c.moveTo(x,0);c.lineTo(x,h);c.stroke();}});beltTex.wrapS=beltTex.wrapT=T.RepeatWrapping;beltTex.repeat.set(5,2);
const beltMat=new T.MeshStandardMaterial({map:beltTex,bumpMap:beltTex,bumpScale:.10,roughness:.91});
box(belt,92,.3,23.7,0,22,0,beltMat,.1);box(belt,92,.28,23.7,0,14,0,beltMat,.1);
for(const side of [-1,1]){const cap=mesh(new T.CylinderGeometry(4,4,23.7,40,1,true,side===1?0:Math.PI,Math.PI),beltMat,belt,46*side,18,0);cap.rotation.x=Math.PI/2;}
label(belt,'AMAZONVISION 4.0',26,3,0,17,14.17,{bg:'#1d3025',fg:'#d7ebc5',font:35});label(belt,'→  FLUXO',10,2,-34,17,14.18,{bg:'#202923',fg:'#c2ceba',font:38});
// Guias e seus espaçadores, ajustáveis para os três produtos do projeto.
const guides=part('02','Guias laterais','Posicionamento do produto','Duas guias laterais mantêm o produto sobre a correia. Suportes e folgas são ilustrativos e devem acompanhar o tamanho real dos produtos.','Guias metálicas · 2 unidades',[0,26,-14],[0,0,0],[-12,23,-5],65);
for(const z of [-15,5]){rod(guides,[-55,25,z],[26,25,z],.42);for(const x of [-52,-8,24]){rod(guides,[x,21,z+(z<0?-3:3)],[x,25,z],.38);screw(guides,x,21.5,z+(z<0?-3:3));}}

// Sensores fotoelétricos: cilindro roscado, porcas, lente, suporte em L, cabo.
function sensor(id,title,x){const s=part(id,title,'Fotoelétrico PNP · presença',id==='03'?'S1 marca o ponto de inspeção, abaixo da câmera. Seu sinal é levado à interface de optoacopladores antes do ESP32.':'S2 marca a chegada ao ponto de separação. O corpo e o suporte mostram uma montagem possível sobre a lateral da esteira.','Sensor 12 V · PNP · interface PC817',[x,30,10],[x,0,0],[x,24,3],34);
box(s,4,.7,9,0,21.5,8,M.black,.2);box(s,4,9,.6,0,26,11.5,M.black,.15);for(const xx of [-1.3,1.3])screw(s,xx,22,8);
const body=cyl(s,.96,6.8,0,27,9.4,M.steel,32);body.rotation.x=Math.PI/2;
for(let z=6.8;z<=12.4;z+=.3){const ring=mesh(new T.TorusGeometry(.97,.06,6,24),M.aluminum,s,0,27,z);}
for(const z of [10.7,12.1]){const nut=cyl(s,1.48,.48,0,27,z,M.gold,6);nut.rotation.x=Math.PI/2;}
const lens=cyl(s,.82,.25,0,27,5.89,M.dark);lens.rotation.x=Math.PI/2;const redLens=cyl(s,.64,.28,0,27,5.73,new T.MeshPhysicalMaterial({color:'#68140e',roughness:.16,metalness:.3,clearcoat:1}));redLens.rotation.x=Math.PI/2;
sph(s,.16,.48,27.6,12.8,ledRed);wire(s,[[0,27,13],[0,27,16],[2,24,18],[3,12,18],[4,3,21]],'#252823',.19);
label(s,id==='03'?'S1':'S2',2,1.2,0,29.1,11.9,{bg:'#e1b640',fg:'#242c20',font:80});return s;}
sensor('03','Sensor S1 · inspeção',-33);sensor('04','Sensor S2 · separação',24);

// Suporte fixo, celular com lentes voltadas para baixo e iluminação circular LED.
const vision=part('05','Celular e suporte de câmera','Captura superior da imagem','Celular instalado na horizontal, com as câmeras voltadas para a correia. O suporte mantém a distância e o enquadramento da área de inspeção.','Celular fixo · suporte articulado',[-33,61,-5],[-33,0,-5],[-33,43,-6],60);
box(vision,18,1.3,12,0,1.4,-22,M.black,.5);for(const x of [-6,6])for(const z of [-25,-19])screw(vision,x,2.1,z);
cyl(vision,1.05,57,0,29,-22,M.aluminum);cyl(vision,1.7,5,0,52,-22,M.black);rod(vision,[0,54,-22],[0,54,0],.9,M.black);
for(const z of [-21,-3]){const k=cyl(vision,1.5,2,0,53,z,M.dark);k.rotation.z=Math.PI/2;}
box(vision,8.6,.9,17,0,55.2,-1,M.dark,.5);box(vision,7.9,.13,16.2,0,55.72,-1,M.black,.4);
const phoneTex=texture(400,800,(c,w,h)=>{c.fillStyle='#12271d';c.fillRect(0,0,w,h);const grad=c.createRadialGradient(180,380,10,200,500,500);grad.addColorStop(0,'#355943');grad.addColorStop(1,'#081e18');c.fillStyle=grad;c.fillRect(0,0,w,h);c.fillStyle='#e0efd5';c.font='35px Arial';c.textAlign='center';c.fillText('AmazonVision',200,230);c.font='17px Arial';c.fillStyle='#8cab84';c.fillText('CÂMERA DE INSPEÇÃO',200,270);c.strokeStyle='#b4c3a6';c.lineWidth=3;c.strokeRect(55,350,290,220);c.fillStyle='#9db284';c.font='16px Arial';c.fillText('CÂMERA FIXA · VISTA SUPERIOR',200,660);});
const phoneScreen=mesh(new T.PlaneGeometry(7.9,15.6),new T.MeshBasicMaterial({map:phoneTex}),vision,0,55.81,-1);phoneScreen.rotation.x=-Math.PI/2;
for(const x of [-2.2,.2]){const l=cyl(vision,.65,.5,x,54.55,-7,M.dark);cyl(vision,.43,.52,x,54.5,-7,mat('#284d52',.1,.65));}
box(vision,11,1.2,1.1,0,56,0,M.black,.3);box(vision,1.1,2.4,3,-4.9,55.5,0,M.black,.25);box(vision,1.1,2.4,3,4.9,55.5,0,M.black,.25);
wire(vision,[[4,55,5],[7,56,8],[9,51,-6],[2,49,-22],[2,6,-22],[7,1,-24],[18,1,-25]],'#242824',.21);
const lighting=part('06','Iluminação LED','Luz uniforme no ponto de inspeção','Anel de iluminação abaixo do celular, montado no mesmo suporte. A luz padroniza a aparência do produto diante da câmera.','Iluminação fixa · 1 conjunto',[-33,50,-5],[-33,49,-5],[-33,47,-5],34);
const ring=mesh(new T.TorusGeometry(5.6,.75,12,64),M.dark,lighting);ring.rotation.x=Math.PI/2;const diffuser=mesh(new T.TorusGeometry(5.6,.43,12,64),glow,lighting,0,-.48,0);diffuser.rotation.x=Math.PI/2;rod(lighting,[0,0,-6],[0,0,-16],.3,M.black);
const lamp=new T.SpotLight(0xf3ffe5,360,48,Math.PI*.27,.65,1.5);lamp.position.set(-33,47,-5);lamp.target.position.set(-33,21,-5);scene.add(lamp,lamp.target);

// Conjunto motorredutor e acoplamento externo.
const motor=part('07','Motor DC e transmissão','Acionamento da correia','Motor DC com caixa de redução fixado à lateral. O eixo aciona o rolete; o driver DRV8833 fica na base eletrônica.','Motor DC · tensão depende do motor',[31,21,14],[30,0,11],[30,16,11],35);
box(motor,8,7,3.7,0,16,1,M.yellow,.65);const can=cyl(motor,2.3,6.5,0,16,6,M.steel,32);can.rotation.x=Math.PI/2;const end=cyl(motor,2.3,1.2,0,16,9.6,M.dark);end.rotation.x=Math.PI/2;rod(motor,[0,16,-4],[0,16,0],.6,M.steel);box(motor,11,.8,8,0,11.8,2.5,M.black,.2);for(const x of [-4.2,4.2])screw(motor,x,12.3,3);screw(motor,-2.7,16,3,'z');screw(motor,2.7,16,3,'z');wire(motor,[[1.4,16,10],[2,12,12],[-2,6,12],[-9,2,12],[-15,2,16]],'#a44831',.19);wire(motor,[[-1.4,16,10],[-1.2,12,12],[-4,5,13],[-9,2.3,13],[-15,2.3,17]],'#202720',.19);

// Separador e calhas: duas saídas físicas para aprovado / rejeitado.
const servo=part('08','Servo MG996R e pá','Separação física dos itens','Servo de 180° sobre um suporte lateral, com braço e pá desviadora. A pá está em posição recolhida, sem animação.','MG996R 180° · 1 unidade',[29,30,4],[28,0,2],[28,24,4],40);
box(servo,7,1,7,0,21,6,M.aluminum,.3);box(servo,4.2,6,2.4,0,24,6,M.dark,.4);box(servo,6.4,.6,2.8,0,26,6,M.dark,.2);for(const x of [-2.6,2.6])screw(servo,x,26.5,6);cyl(servo,.55,1.4,0,27.2,6,M.gold);box(servo,4,.4,.9,-.4,27.8,6,M.white,.3);screw(servo,0,28.1,6);
box(servo,.55,4,13,-1.5,25.8,-.2,M.aluminum,.16);label(servo,'MG996R',3.5,1.7,0,24,7.23,{bg:'#ae7324',fg:'#f8e9bd',font:60});
wire(servo,[[1,22,6],[3,20,7],[2,10,12],[-4,3,14],[-15,2,16]],'#94662b',.13);wire(servo,[[1.3,22,6],[3.3,20,7],[2.3,10,12],[-3.7,3,14],[-14.7,2,16.3]],'#ab422a',.13);wire(servo,[[1.6,22,6],[3.6,20,7],[2.6,10,12],[-3.4,3,14],[-14.4,2,16.6]],'#bfaa62',.13);
const chute=group('Calhas de saída');const out=box(chute,18,.35,23,44,16,-5,M.aluminum,.14);out.rotation.z=-.35;for(const z of [-16.3,6.3]){const edge=box(chute,18,2,.35,44,17,z,M.aluminum,.12);edge.rotation.z=-.35;}const rej=box(chute,17,.35,18,23,15,15,M.aluminum,.15);rej.rotation.x=.53;for(const x of [14.7,31.3]){const edge=box(chute,.35,2,18,x,16,15,M.aluminum,.1);edge.rotation.x=.53;}

function bin(id,title,pos,bg){const b=part(id,title,'Recipiente em acrílico',id==='09'?'Recipiente no fim da esteira para os itens aprovados visualmente. As castanhas no interior são amostras estáticas.':'Recipiente na saída lateral para itens rejeitados. O projeto possui duas saídas físicas, ainda que a IA utilize três classes.','Acrílico transparente · 1 unidade',[pos[0],15,pos[2]],pos,[pos[0],8,pos[2]],40);
box(b,25,.65,25,0,.9,0,glass,.15);for(const x of [-12.4,12.4])box(b,.5,15,25,x,8.7,0,glass,.14);for(const z of [-12.4,12.4])box(b,25,15,.5,0,8.7,z,glass,.14);
const edgeMat=mat('#aec4b9',.3,.25);for(const x of [-12.4,12.4])for(const z of [-12.4,12.4])rod(b,[x,1,z],[x,16.2,z],.065,edgeMat);for(const z of [-12.4,12.4])rod(b,[-12.4,16.2,z],[12.4,16.2,z],.065,edgeMat);for(const x of [-12.4,12.4])rod(b,[x,16.2,-12.4],[x,16.2,12.4],.065,edgeMat);
label(b,id==='09'?'APROVADOS':'REJEITADOS',16,3.3,0,10,12.72,{bg,fg:'#f2f5df',font:48});return b;}
const approved=bin('09','Recipiente de aprovados',[62,0,-5],'#3c654a'),rejected=bin('10','Recipiente de rejeitados',[28,0,35],'#975b41');

// Placa de montagem com espaçadores; fiação realista de baixa tensão.
const tray=part('11','Base de montagem e protoboard','Organização da eletrônica','Base transparente sobre espaçadores, com protoboard dedicada aos sinais e à lógica. Os cabos de motor e servo seguem fora da protoboard.','Base em acrílico · protoboard de sinais',[-37,7,35],[-31,0,32],[-31,5,32],62);
box(tray,65,.8,28,0,2,0,glass,.4);for(const x of [-29,29])for(const z of [-11,11]){cyl(tray,.75,1.4,x,1,z,M.aluminum);screw(tray,x,2.6,z);}
const bread=box(tray,17,1.3,5.8,-14,3.05,7,M.white,.32);
for(let x=-21.4;x<=-6.5;x+=.49)for(const z of [5,5.5,6,7.9,8.4,8.9])box(tray,.15,.035,.15,x,3.72,z,M.dark);
box(tray,15,.04,.07,-14,3.73,4.5,M.red);box(tray,15,.04,.07,-14,3.73,9.5,M.blue);box(tray,15,.04,.15,-14,3.73,7,M.rubber);
label(tray,'CONTROLE / SINAIS',15,1.4,-15,2.5,12,{bg:'#e8eadc',font:36,rotX:-Math.PI/2});

function pcb(p,w,d,x,y,z,color=M.green){box(p,w,.17,d,x,y,z,color,.13);for(const xx of [-w/2+.55,w/2-.55])for(const zz of [-d/2+.5,d/2-.5]){cyl(p,.32,.13,x+xx,y+.1,z+zz,M.gold,16);cyl(p,.16,.14,x+xx,y+.12,z+zz,M.dark,12);const height=Math.max(.35,p.position.y-2.5);cyl(p,.26,height,x+xx,y-height/2-.08,z+zz,M.gold,6);}
for(let i=0;i<7;i++){const zz=z-d*.34+i*d*.11;box(p,w*.63,.018,.032,x,y+.098,zz,M.gold);box(p,.035,.018,d*.3,x-w*.31+i*.17,y+.10,z-d*.18);}return y+.2;}
function chip(p,w,d,x,y,z){box(p,w,.35,d,x,y,z,M.chip,.06);for(const side of [-1,1])for(let k=-d*.38;k<=d*.38;k+=.35)box(p,.35,.1,.12,x+side*(w/2+.09),y-.03,z+k,M.steel);}
function cap(p,x,y,z,r=.48,h=1.4){cyl(p,r,h,x,y+h/2,z,M.dark);cyl(p,r*.93,.07,x,y+h+.025,z,M.aluminum);box(p,r*1.3,.015,.045,x,y+h+.065,z,M.dark);}
function terminal(p,x,y,z,n=2){box(p,n*.8,.85,1.25,x,y+.4,z,M.terminal,.1);for(let i=0;i<n;i++){const xx=x+(i-(n-1)/2)*.8;screw(p,xx,y+.9,z,'y',.21);box(p,.39,.38,.05,xx,y+.32,z+.64,M.dark);}}
const esp=part('12','ESP32 DevKit','Controle da sequência física','Placa de controle ligada ao notebook por USB. Recebe os sinais de S1 e S2 e comanda o driver do motor e o servo. A IA é executada no notebook.','Microcontrolador · USB / serial',[-45,8,27],[-45,4,27],[-45,5,27],23);
pcb(esp,5.7,10,0,0,0,M.dark);box(esp,3.5,.65,5.1,0,.55,-.7,M.steel,.14);label(esp,'ESP32',2.8,1.2,0,.89,-.2,{bg:'#b5c1bd',fg:'#364237',font:66,rotX:-Math.PI/2});
box(esp,4.5,.17,2,0,.24,-3.8,M.dark);for(let i=0;i<5;i++)box(esp,.14,.035,1.4,-1.65+i*.7,.35,-3.8,M.gold);box(esp,3,.035,.14,0,.35,-4.4,M.gold);
for(const x of [-2.35,2.35])for(let z=-4.2;z<=4.2;z+=.57){box(esp,.43,.4,.42,x,.25,z,M.black);box(esp,.1,.68,.1,x,-.23,z,M.gold);}box(esp,1.55,.7,1.3,0,.4,4.9,M.steel,.15);box(esp,1.15,.35,.1,0,.39,5.56,M.dark);for(const x of [-1.7,1.7]){box(esp,.68,.26,.78,x,.32,3.8,M.black,.1);box(esp,.4,.2,.4,x,.5,3.8,M.white,.1);}sph(esp,.13,1.45,.38,2.8,ledGreen);chip(esp,1.4,1.2,0,.35,2.6);

const opto=part('13','Interface PC817','Isolamento dos sinais dos sensores','Dois canais com optoacopladores representam a interface entre os sensores PNP de 12 V e os sinais do ESP32. Resistores e conexões são ilustrativos.','PC817 · 2 canais',[-58,6,36],[-58,3.2,34],[-58,4,34],21);
pcb(opto,6,5,0,0,0);for(const x of [-1.3,1.3]){chip(opto,.8,1.1,x,.4,0);box(opto,.5,.28,.2,x,.33,1.2,M.white,.07);cyl(opto,.15,.16,x,.27,-1.4,M.red,12);}terminal(opto,0,.3,2,3);terminal(opto,0,.3,-2,3);label(opto,'PC817',3,1,0,.23,-.85,{bg:'#164d33',fg:'#dae6bb',font:64,rotX:-Math.PI/2});

const driver=part('14','Driver DRV8833','Potência do motor DC','Módulo intermediário entre o ESP32 e o motor da esteira. A alimentação é recebida de um dos conversores XL4015.','Driver de motor · 1 módulo',[-12,6,36],[-12,3.1,36],[-12,4,36],22);
pcb(driver,6,5,0,0,0,M.green);chip(driver,1.3,1.8,0,.42,0);cap(driver,-1.8,.2,-.8,.46,1);terminal(driver,0,.3,1.85,3);terminal(driver,0,.3,-1.85,3);label(driver,'DRV8833',4,1,0,.23,.4,{bg:'#164d33',fg:'#e1e9c2',font:60,rotX:-Math.PI/2});

function buck(id,x,name){const b=part(id,name,'Conversor de tensão XL4015','Módulo ajustável com indutor, dissipador e terminais de entrada e saída. A tensão de saída deve ser definida conforme o componente alimentado.','XL4015 · conversor DC–DC',[x,7,23],[x,3.15,23],[x,5,23],25);
pcb(b,10,6,0,0,0,M.blue);const tor=mesh(new T.TorusGeometry(1.15,.5,10,24),M.copper,b,-1.5,1.2,0);tor.rotation.x=Math.PI/2;for(let a=0;a<Math.PI*2;a+=.4){const coil=mesh(new T.TorusGeometry(.48,.105,6,10),M.gold,b,-1.5+Math.cos(a)*1.15,1.2,Math.sin(a)*1.15);coil.rotation.y=-a;}
box(b,2.6,.6,3,2,1,0,M.aluminum,.08);for(let x=1;x<3.1;x+=.4)box(b,.17,1.6,3,x,1.85,0,M.aluminum,.04);cap(b,-3.4,.2,-1.3,.65,1.8);cap(b,-3.4,.2,1.2,.55,1.5);terminal(b,4.15,.2,0,2);terminal(b,-4.1,.2,0,2);box(b,1.4,.7,.8,.2,.65,2,M.terminal,.1);screw(b,.2,1.06,2,'y',.25);label(b,'XL4015',4.7,1.05,-.5,.22,-2.32,{bg:'#235c91',fg:'#e8eaca',font:58,rotX:-Math.PI/2});return b;}
buck('15',-28,'XL4015 · alimentação do servo');buck('16',-13,'XL4015 · alimentação do motor');

const supply=part('17','Fonte 12 V / 5 A','Alimentação externa','Fonte externa fechada, representada com cabo de entrada, cabo de saída DC e identificação. Alimenta sensores e os dois conversores.','12 V · 5 A · 1 fonte',[-73,7,28],[-73,0,28],[-73,4,28],32);
box(supply,13,5.6,22,0,3.1,0,M.dark,1.05);for(let z=-7;z<=7;z+=1.4){box(supply,.06,2.7,.37,-6.52,3.2,z,M.rubber);box(supply,.06,2.7,.37,6.52,3.2,z,M.rubber);}label(supply,'AC / DC  •  12 V  5 A',10,5,0,5.94,0,{bg:'#303930',fg:'#bdc6ad',font:36,rotX:-Math.PI/2});
wire(supply,[[0,3,-11],[-8,2,-16],[-12,1,-43],[-5,1,-75],[38,1,-78],[57,2,-74],[59,3.5,-74]],'#242721',.35);wire(supply,[[0,3,11],[1,2,15],[10,1,16],[17,2,12],[21,3,7]],'#252a22',.23);
// Chicotes externos, trajetos visuais por canal e pequenos fixadores.
const cables=group('Chicotes e conectores');
for(let i=0;i<4;i++){const color=['#a64d34','#282f26','#b59b4e','#698362'][i];wire(cables,[[-58.8+i*.55,4,36.6],[-54+i*.55,5,33],[-50+i*.55,5.2,29],[-47.35,4.6,26+i*.58]],color,.10);}
// Distribuição DC em bornes sobre a base e conectores de extremidade.
terminal(cables,-57,2.6,23,4);label(cables,'12 V DC',6,1.2,-57,2.48,25.4,{bg:'#e4e8d8',fg:'#3d5340',font:59,rotX:-Math.PI/2});
wire(cables,[[-52,3,35],[-50.5,3,31],[-54,3,26],[-57,3.1,23.6]],'#252a22',.23);
wire(cables,[[-57.7,3.5,23.6],[-53,3.5,18],[-35,2.6,17],[-32.1,3.7,23.5]],'#a34831',.17);wire(cables,[[-56.9,3.5,23.6],[-52.4,3.5,17.4],[-34.4,2.6,16.4],[-31.3,3.7,23.5]],'#252a23',.17);
wire(cables,[[-56.1,3.5,23.6],[-52,3.5,15],[-19,2.6,13],[-17.1,3.7,23.5]],'#a34831',.17);wire(cables,[[-55.3,3.5,23.6],[-51.4,3.5,14.4],[-18.4,2.6,12.4],[-16.3,3.7,23.5]],'#252a23',.17);
wire(cables,[[-8,4,23],[-5,4,25],[-5,4,32],[-11,4,34]],'#a84c31',.15);wire(cables,[[-8,4,24],[-4.5,4,26],[-4.5,4,32.5],[-11,4,35]],'#262b23',.15);
wire(cables,[[-23,4,23],[-20,4,20],[-2,2,19],[9,2,20],[13,3,18]],'#aa4b30',.17);wire(cables,[[-23,4,24],[-20,4,20.6],[-2,2,19.6],[9,2,20.6],[13,3,18.6]],'#2a3027',.17);
for(let i=0;i<3;i++)wire(cables,[[-42.65,4.6,28+i*.57],[-38,6,32+i],[-31,5,36+i],[-17,4,37+i*.4],[-12.8+i*.8,3.7,38.5]],['#a59443','#517e75','#658dc1'][i],.105);
wire(cables,[[-29,3,21],[-34,3,17],[-39,2,15],[-54,3,19],[-58,3.7,31.5]],'#292e24',.22);wire(cables,[[28,3,21],[20,2.5,22],[12,2,17],[-5,2,15],[-35,2,16],[-57.2,3.7,31.5]],'#292e24',.22);
wire(cables,[[15,2,27],[9,2.5,29],[0,3,31],[-8,4,33],[-12.4,3.7,33.5]],'#a44831',.19);
wire(cables,[[15,2.3,28],[9,2.7,30],[0,3.2,32],[-7.4,4,33.5],[-11.6,3.7,33.5]],'#202720',.19);
wire(cables,[[13.6,2,18.6],[4,2.5,22],[-3,3,31],[-24,5,42],[-41,5,36],[-42.65,4.6,26.3]],'#bfaa62',.13);
for(let i=0;i<2;i++)wire(cables,[[-58+i*.8,3.8,36.5],[-54,5,41+i],[-48,4.5,40+i],[-45+i*.5,3.73,37.5]],['#507061','#987247'][i],.1);
for(const x of [-35,-18,0,15]){box(cables,.6,.5,2.4,x,2,18,M.white,.1);screw(cables,x,2.27,18,'y',.16);}

// Notebook: carcaça, teclado completo, trackpad, dobradiças e tela fixa.
const laptop=part('18','Notebook com GPU RTX','Visão computacional e dashboard','Notebook responsável pelos modelos de IA, painel e registros. A tela mostra uma composição estática do dashboard, sem análise ou contadores em execução.','Processamento local · USB / serial',[46,32,-32],[49,1,-33],[49,17,-33],68);
laptop.rotation.y=-.12;box(laptop,37,1.3,25,0,.5,0,M.black,.6);box(laptop,36.4,.2,24.4,0,1.21,0,M.aluminum,.42);
box(laptop,32,.25,11.2,0,1.41,-3.9,M.dark,.45);for(let row=0;row<5;row++){for(let col=0;col<14;col++){box(laptop,1.86,.25,1.6,-14.6+col*2.23,1.65,-8.5+row*2.05,M.black,.19);box(laptop,.54,.035,.07,-14.6+col*2.23,1.79,-8.8+row*2.05,M.aluminum,.015);}}
box(laptop,11.5,.03,6.3,0,1.34,7.6,M.steel,.3);box(laptop,11,.025,5.8,0,1.37,7.6,M.aluminum,.24);label(laptop,'RTX',3.4,1.8,14,1.34,8,{bg:'#223d23',fg:'#d3ecab',font:85,rotX:-Math.PI/2});
for(const x of [-11,11]){const h=cyl(laptop,.9,6,x,1.4,-11.3,M.black);h.rotation.z=Math.PI/2;}
const lid=new T.Group();lid.position.set(0,1.7,-11.4);lid.rotation.x=-.14;laptop.add(lid);box(lid,37,24,.85,0,12,0,M.black,.65);box(lid,35,21.4,.1,0,12,.48,M.dark,.3);
const screenTexture=texture(1400,850,(c,w,h)=>{
c.fillStyle='#eff3e9';c.fillRect(0,0,w,h);c.fillStyle='#173d2a';c.fillRect(0,0,w,90);c.fillStyle='#e5f4d9';c.font='bold 39px Arial';c.fillText('AmazonVision 4.0',46,59);c.fillStyle='#a9c69c';c.font='20px Arial';c.fillText('PAINEL DE INSPEÇÃO',960,55);c.fillStyle='#d4decd';c.fillRect(40,126,715,460);c.fillStyle='#e4e0c7';c.fillRect(67,159,659,395);
c.save();c.translate(395,352);c.rotate(-.4);c.fillStyle='#96613b';c.beginPath();c.ellipse(0,0,156,81,0,0,Math.PI*2);c.fill();c.fillStyle='#e9cea0';c.beginPath();c.ellipse(-10,-5,115,61,0,0,Math.PI*2);c.fill();c.restore();c.strokeStyle='#39734c';c.lineWidth=3;c.strokeRect(192,228,415,233);c.fillStyle='#39734c';c.fillRect(192,200,260,28);c.fillStyle='#fff';c.font='19px Arial';c.fillText('CASTANHA · VISTA FIXA',203,221);
c.fillStyle='#2e4c34';c.font='24px Arial';c.fillText('PRODUTO SELECIONADO',810,173);c.font='bold 44px Arial';c.fillText('Castanha-do-pará',810,235);c.font='23px Arial';c.fillStyle='#78896c';c.fillText('INSPEÇÃO VISUAL EXTERNA',810,282);c.fillStyle='#dce7d1';c.fillRect(809,318,540,97);c.fillStyle='#355f35';c.font='bold 29px Arial';c.fillText('Modelo de apresentação',835,375);
c.fillStyle='#687760';c.font='22px Arial';c.fillText('Câmera fixa • Iluminação LED',810,464);c.fillText('ESP32 • USB / serial',810,507);c.fillText('Processamento local • GPU RTX',810,550);
for(let i=0;i<3;i++){const x=40+i*452;c.fillStyle='#fff';c.fillRect(x,628,418,133);c.fillStyle='#65765b';c.font='21px Arial';c.fillText(['CLASSES DO MODELO','SAÍDAS FÍSICAS','MODO DA CENA'][i],x+22,668);c.fillStyle='#284b31';c.font='bold 32px Arial';c.fillText(['A / B / C','Aprovado / rejeitado','Estático'][i],x+22,721);}c.fillStyle='#8b9682';c.font='17px Arial';c.fillText('Ilustração do painel • Sem dados de produção ou análise em execução',43,810);
});
mesh(new T.PlaneGeometry(34.8,20.8),new T.MeshBasicMaterial({map:screenTexture}),lid,0,12,.551);sph(lid,.16,0,23.25,.52,M.dark);label(lid,'AMAZONVISION',9,.6,0,.9,.52,{bg:'#202923',fg:'#aebca1',font:34});
wire(cables,[[-45,4.4,32.7],[-45,5.8,35],[-39,4,42],[-34,1.3,45],[-5,1.3,46],[6,1.3,32],[7,1.3,-21],[25,1.3,-27],[31,2,-27]],'#242a22',.21);
box(laptop,.85,.55,1.55,-18.55,.7,3.8,M.dark,.12);
wire(cables,[[-15,1,-30],[-4,1,-34],[12,1,-40],[25,1,-39],[31.4,1.9,-38]],'#242824',.21);
box(laptop,.85,.5,1.3,-18.55,.7,-7.4,M.dark,.1);
// Dois pequenos apoios fixam a base do anel à coluna.
rod(vision,[0,49,-22],[0,49,-16],.4,M.black);cyl(vision,1.45,2,0,49,-22,M.black);

// Produtos estáticos: superfícies procedurais sem imagens ou recursos externos.
function productMaterial(type){const t=texture(1024,512,(c,w,h)=>{const img=c.createImageData(w,h);for(let y=0;y<h;y++)for(let x=0;x<w;x++){const u=x/w,v=y/h,n=Math.sin(u*19+Math.sin(v*8))* .4+Math.cos(v*21+u*11)*.22,noise=(rand()-.5)*11;let col;if(type==='nut'){const shell=v>.70+n*.075||v<.13+n*.04||Math.sin(u*16+v*7)>.94&&v>.5;const fiber=Math.sin(u*640+Math.sin(v*12)*4)*2;col=shell?[93+noise+n*17,52+noise+n*10,28+noise]:[223+noise+fiber,198+noise+fiber,154+noise+fiber];}else if(type==='tucuma'){const spot=rand()>.986?45:0;col=[195+noise+n*24-spot,92+noise+n*30-spot,19+noise*.6];}else{const lines=Math.sin(u*410+Math.sin(v*32)*9)*14;col=[145+noise+lines,110+noise+lines,64+noise+lines];}const i=(y*w+x)*4;img.data[i]=col[0];img.data[i+1]=col[1];img.data[i+2]=col[2];img.data[i+3]=255;}c.putImageData(img,0,0);});return new T.MeshStandardMaterial({map:t,bumpMap:t,bumpScale:type==='acai'?.065:.018,roughness:type==='tucuma'?.48:.74});}
const productMats={nut:productMaterial('nut'),tucuma:productMaterial('tucuma'),acai:productMaterial('acai')};
function product(p,type,x,y,z,size=1,angle=0){const geo=new T.SphereGeometry(1,40,24),attr=geo.attributes.position;for(let i=0;i<attr.count;i++){const vx=attr.getX(i),vy=attr.getY(i),vz=attr.getZ(i);const r=1+.012*Math.sin(vx*12+vz*5)*Math.sin(vy*9)+.009*Math.cos(vz*16);const taper=type==='nut'?1-.28*vx:.99;attr.setXYZ(i,vx*r,vy*r*taper+ (type==='nut'?.12*vx*vx:0),vz*r*taper);}geo.computeVertexNormals();const m=mesh(geo,productMats[type],p,x,y,z);if(type==='nut')m.scale.set(3.4*size,1.25*size,1.65*size);else if(type==='tucuma')m.scale.set(2.7*size,2.65*size,2.45*size);else m.scale.set(1.35*size,1.25*size,1.35*size);m.rotation.y=angle;return m;}
product(belt,'nut',-21,23.5,0,1,-.4); // Um único produto no ponto S1.
for(let i=0;i<10;i++)product(approved,'nut',-8+rand()*16,2.2+(i>6?2:0),-8+rand()*16,.74+rand()*.25,rand()*Math.PI);
for(let i=0;i<5;i++)product(rejected,'nut',-7+rand()*14,2.1,-7+rand()*14,.45+rand()*.3,rand()*Math.PI);
const samples=part('19','Amostras da bioeconomia','Tucumã, castanha e caroço de açaí','Três bandejas identificam os produtos previstos no PDF. A esteira foi representada com uma única castanha na área de inspeção.','3 produtos · amostras estáticas',[-61,7,-35],[-60,0,-34],[-60,6,-34],47);
['tucuma','nut','acai'].forEach((type,i)=>{const x=-15+i*15;box(samples,13,.6,18,x,.6,0,M.white,.55);for(const z of [-8.5,8.5])box(samples,13,1,.4,x,1.3,z,M.white,.15);for(const side of [-1,1])box(samples,.4,1,17,x+side*6.3,1.3,0,M.white,.12);label(samples,['TUCUMÃ','CASTANHA','CAROÇO DE AÇAÍ'][i],12,2.3,x,1.1,6.5,{bg:'#e8e9da',fg:'#416037',font:42,rotX:-Math.PI/2});for(let j=0;j<4;j++)product(samples,type,x+(j%2?2.5:-2.5),type==='tucuma'?3.5:2,(j<2?-4:1),type==='tucuma'?.85:type==='nut'?.72:.95,j*.75);});

refineAssembly({T,scene,M,mat,texture,rand,mesh,box,cyl,sph,rod,screw,wire,label,group,part,parts,glass,glow,table,topMat,belt,beltMat,guides,vision,lighting,motor,servo,chute,tray,esp,opto,driver,supply,cables,laptop,lid,approved,rejected});

// Compactar geometrias estáticas por componente/material, mantendo seleção individual.
function optimize(g){g.updateWorldMatrix(true,true);const bins=new Map();g.traverse(o=>{if(!o.isMesh||Array.isArray(o.material))return;const k=o.material.uuid;let bin=bins.get(k);if(!bin){bin={material:o.material,objects:[],geos:[],shadow:o.castShadow};bins.set(k,bin);}const geo=o.geometry.clone().applyMatrix4(o.matrixWorld);bin.objects.push(o);bin.geos.push(geo.index?geo.toNonIndexed():geo);});
for(const b of bins.values()){if(b.geos.length<2){b.geos.forEach(x=>x.dispose());continue;}const merged=mergeGeometries(b.geos,false);if(!merged)continue;const inv=new T.Matrix4().copy(g.matrixWorld).invert();merged.applyMatrix4(inv);for(const o of b.objects){o.removeFromParent();o.geometry.dispose();}const m=new T.Mesh(merged,b.material);m.castShadow=b.shadow;m.receiveShadow=true;g.add(m);b.geos.forEach(x=>x.dispose());}}
allGroups.forEach(optimize);

// Interface d'inspection : seuls la caméra et les identifiants changent, jamais la machine.
const inventory=$('#inventory'),labels=$('#labels');let selected=null,labelsVisible=true;
for(const p of parts){const b=document.createElement('button');b.dataset.part=p.id;b.innerHTML=`<span class="part-no">${p.id}</span><span><span class="part-title">${p.title}</span><span class="part-sub">${p.sub}</span></span><span class="part-arrow">↗</span>`;b.addEventListener('click',()=>select(p));inventory.appendChild(b);const h=document.createElement('button');h.className='hotspot';h.textContent=p.id;h.title=p.title;h.setAttribute('aria-label',p.title);h.addEventListener('click',()=>select(p));labels.appendChild(h);p.label=h;p.button=b;}
function select(p){selected=p;viewport.classList.add('closeup');parts.forEach(o=>{o.button.classList.toggle('active',o===p);o.label.classList.toggle('selected',o===p);});$('#detailTitle').textContent=p.title;$('#detailText').textContent=p.desc;$('#detailSpec').textContent=p.spec;$('#detail').classList.add('open');p.button.scrollIntoView({block:'nearest'});const direction=new T.Vector3(.63,.7,.86).normalize();camera.position.copy(p.target).addScaledVector(direction,p.radius*(viewport.clientWidth/viewport.clientHeight<.8?1.7:1));controls.target.copy(p.target);controls.update();document.querySelectorAll('[data-view]').forEach(b=>b.classList.remove('active'));if(innerWidth<701){$('aside').classList.remove('show');$('#menu').setAttribute('aria-expanded','false');toast(p.title+' · Veja a descrição no menu ☰');}render();}
const views={overview:{pos:[157,134,195],target:[-4,9,0]},front:{pos:[-3,88,220],target:[-4,15,0]},top:{pos:[-4,237,1],target:[-4,0,0]},electronics:{pos:[-5,68,112],target:[-31,4,28]},inspection:{pos:[-95,86,70],target:[-27,32,-7]},separation:{pos:[107,76,102],target:[35,19,12]}};
function view(name){const v=views[name];viewport.classList.toggle('closeup',name!=='overview');camera.position.set(...v.pos);controls.target.set(...v.target);const aspect=viewport.clientWidth/viewport.clientHeight;if(aspect<1.1){camera.position.sub(controls.target).multiplyScalar(Math.max(1.05,1.12/aspect));camera.position.add(controls.target);}controls.update();document.querySelectorAll('[data-view]').forEach(b=>b.classList.toggle('active',b.dataset.view===name));render();}
function updateLabels(){const width=viewport.clientWidth,height=viewport.clientHeight;for(const p of parts){const v=p.point.clone().project(camera),d=camera.position.distanceTo(p.point);const show=labelsVisible&&v.z<1&&v.z>-1&&Math.abs(v.x)<.96&&Math.abs(v.y)<.92&&(d<110||['01','03','04','05','09','10','11','18','19','21'].includes(p.id));p.label.style.display=show?'grid':'none';p.label.style.left=(v.x*.5+.5)*width+'px';p.label.style.top=(-v.y*.5+.5)*height+'px';}}
function render(){const w=viewport.clientWidth,h=viewport.clientHeight;if(canvas.width!==Math.floor(w*renderer.getPixelRatio())||canvas.height!==Math.floor(h*renderer.getPixelRatio())){renderer.setSize(w,h,false);camera.aspect=w/h;camera.updateProjectionMatrix();}renderer.render(scene,camera);updateLabels();}
const sepButton=document.createElement('button');sepButton.dataset.view='separation';sepButton.textContent='Separação';$('.toolbar').appendChild(sepButton);$('.toolbar').style.overflowX='auto';$('.toolbar').style.maxWidth='calc(100% - 45px)';
controls.addEventListener('change',render);new ResizeObserver(render).observe(viewport);document.querySelectorAll('[data-view]').forEach(b=>b.addEventListener('click',()=>view(b.dataset.view)));
$('#labelsToggle').addEventListener('click',()=>{labelsVisible=!labelsVisible;$('#labelsToggle').classList.toggle('active',labelsVisible);$('#labelsToggle').setAttribute('aria-pressed',String(labelsVisible));render();});
$('#closeDetail').addEventListener('click',()=>{$('#detail').classList.remove('open');selected=null;parts.forEach(p=>{p.button.classList.remove('active');p.label.classList.remove('selected');});});
$('#menu').addEventListener('click',()=>{const expanded=$('aside').classList.toggle('show');$('#menu').setAttribute('aria-expanded',String(expanded));});
function toast(text){$('#toast').textContent=text;$('#toast').style.display='block';setTimeout(()=>$('#toast').style.display='none',3000);}
$('#fullscreen').addEventListener('click',async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await document.documentElement.requestFullscreen();}catch{toast('Use F11 para abrir em tela cheia.');}});
$('#save').addEventListener('click',()=>{render();const a=document.createElement('a');a.download='AmazonVision-bancada-3D.png';a.href=canvas.toDataURL('image/png');a.click();toast('Imagem da vista salva.');});
const ray=new T.Raycaster(),pointer=new T.Vector2();let down=[0,0];canvas.addEventListener('pointerdown',e=>down=[e.clientX,e.clientY]);canvas.addEventListener('pointerup',e=>{if(e.button!==0||Math.hypot(e.clientX-down[0],e.clientY-down[1])>5)return;const r=canvas.getBoundingClientRect();pointer.set((e.clientX-r.left)/r.width*2-1,-(e.clientY-r.top)/r.height*2+1);ray.setFromCamera(pointer,camera);const hit=ray.intersectObjects(parts.map(p=>p.g),true)[0];if(hit){let o=hit.object;while(o&&!o.userData.part)o=o.parent;if(o)select(parts.find(p=>p.id===o.userData.part));}});
canvas.addEventListener('keydown',e=>{if(e.key==='Home'){e.preventDefault();view('overview');}if(e.key==='Escape'){$('#detail').classList.remove('open');}if(['+','=','-','ArrowLeft','ArrowRight','ArrowUp','ArrowDown'].includes(e.key)){e.preventDefault();const offset=camera.position.clone().sub(controls.target);if(e.key==='+'||e.key==='=')offset.multiplyScalar(.9);else if(e.key==='-')offset.multiplyScalar(1.1);else{const s=new T.Spherical().setFromVector3(offset);if(e.key==='ArrowLeft')s.theta-=.1;if(e.key==='ArrowRight')s.theta+=.1;if(e.key==='ArrowUp')s.phi=Math.max(.1,s.phi-.1);if(e.key==='ArrowDown')s.phi=Math.min(Math.PI*.49,s.phi+.1);offset.setFromSpherical(s);}camera.position.copy(controls.target).add(offset);controls.update();render();}});
canvas.addEventListener('webglcontextlost',e=>{e.preventDefault();toast('Contexto gráfico interrompido. Recarregue a página.');});
view('overview');$('#loading').style.display='none';
window.__amazonvision={ready:true,components:parts.length,static:true,renderer:'Three.js r180',info:()=>({drawCalls:renderer.info.render.calls,triangles:renderer.info.render.triangles,views:Object.keys(views),externalResources:performance.getEntriesByType('resource').length})};
