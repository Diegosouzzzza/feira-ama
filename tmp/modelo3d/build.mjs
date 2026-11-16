import {build} from 'esbuild';
import {readFile,writeFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
const result=await build({entryPoints:[fileURLToPath(new URL('./scene.js',import.meta.url))],bundle:true,minify:true,format:'iife',target:'es2020',write:false,legalComments:'inline'});
const template=await readFile(new URL('./template.html',import.meta.url),'utf8');
const bundle=result.outputFiles[0].text.replace(/<\/script/gi,'<\\/script');
const output=new URL('../../AmazonVision_4_0_Bancada_3D.html',import.meta.url);
await writeFile(output,template.replace('/*__APP_BUNDLE__*/',()=>bundle),'utf8');
console.log('HTML autônomo gerado:',output.pathname, (Buffer.byteLength(bundle)/1024).toFixed(0)+' KB de recursos incorporados');
