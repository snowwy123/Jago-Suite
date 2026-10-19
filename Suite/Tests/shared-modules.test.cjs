const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),test=require('node:test');
const root=path.resolve(__dirname,'../..');
const repoNames={Wobble:'jago-wobble',Dither:'jago-dither',Repeat:'jago-repeat',Worldbuilding:'jago-world',Material:'jago-material','Music-SFX':'jago-sound','Library-Production':'jago-library'};
const githubNames={Wobble:'Jago-Wobble-Studio',Dither:'Jago-Dither-Studio',Repeat:'Jago-Repeat-Studio',Worldbuilding:'Jago-World-Studio',Material:'Jago-Material-Studio','Music-SFX':'Jago-Sound-Studio','Library-Production':'Jago-Library-Studio'};
function studioRoot(studio){const legacy=path.join(root,'..',repoNames[studio]);return fs.existsSync(legacy)?legacy:path.join(root,'..',githubNames[studio]);}

for(const [studio,sub] of [['Wobble','Browser'],['Dither',''],['Repeat','Web'],['Worldbuilding','Web'],['Material','Web'],['Music-SFX','Web'],['Library-Production','Web']])test(studio+' embeds current shared bridge, themes, help and examples',()=>{
const local=fs.readFileSync(path.join(studioRoot(studio),'Source',sub,'suite-bridge.js'),'utf8');
for(const name of ['suite-bridge.js','shared-themes.js','suite-help.js','suite-examples.js']){const canonical=fs.readFileSync(path.join(root,'Suite/shared',name),'utf8').replace(/^\uFEFF/,'');assert.ok(local.includes(canonical),name+' is stale');}
assert.equal((local.match(/window\.JagoSharedThemes=/g)||[]).length,1,'duplicate theme helper');
});

test('All seven Windows hosts share validated Workscape discovery',()=>{const canonical=fs.readFileSync(path.join(root,'Suite/shared/workscape-host-routing.cs'),'utf8').replace(/\r\n/g,'\n').trim();for(const studio of Object.keys(repoNames)){const host=fs.readFileSync(path.join(studioRoot(studio),'Source/Windows/JagoSuiteHost.cs'),'utf8').replace(/\r\n/g,'\n');assert.ok(host.includes(canonical),studio+' has stale Workscape routing');}});


test('Native studios and Workscape carry the current exact-document and recovery boundary helper',()=>{let read=p=>fs.readFileSync(p,'utf8').replace(/\r\n/g,'\n'),extract=s=>s.slice(s.indexOf('// BEGIN JAGO HOST SECURITY'),s.indexOf('// END JAGO HOST SECURITY'));const expected=extract(read(path.join(root,'Suite/shared/JagoSuiteHost.cs')));assert(expected.includes('JSON.parse(')&&expected.includes('Mutex'));for(const studio of Object.keys(repoNames))assert.equal(extract(read(path.join(studioRoot(studio),'Source/Windows/JagoSuiteHost.cs'))),expected,studio);for(const [repo,file]of [['Jago-Pulse-Studio','Source/Windows/App.cs'],['Jago-Workscape','Source/Workspace.cs']])assert.equal(extract(read(path.join(root,'..',repo,file))),expected,repo);});
