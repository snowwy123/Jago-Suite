const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),test=require('node:test');
const root=path.resolve(__dirname,'../..');
const repoNames={Wobble:'jago-wobble',Dither:'jago-dither',Repeat:'jago-repeat',Worldbuilding:'jago-world',Material:'jago-material','Music-SFX':'jago-sound','Library-Production':'jago-library'};
for(const [studio,sub] of [['Wobble','Browser'],['Dither',''],['Repeat','Web'],['Worldbuilding','Web'],['Material','Web'],['Music-SFX','Web'],['Library-Production','Web']])test(studio+' embeds current shared bridge, themes, help and examples',()=>{
const local=fs.readFileSync(path.join(root,'..',repoNames[studio],'Source',sub,'suite-bridge.js'),'utf8');
for(const name of ['suite-bridge.js','shared-themes.js','suite-help.js','suite-examples.js']){const canonical=fs.readFileSync(path.join(root,'Suite/shared',name),'utf8').replace(/^\uFEFF/,'');assert.ok(local.includes(canonical),name+' is stale');}
assert.equal((local.match(/window\.JagoSharedThemes=/g)||[]).length,1,'duplicate theme helper');
});
