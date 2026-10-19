from pathlib import Path
import subprocess,json,sys
repo=Path(__file__).resolve().parents[2];out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
s=(repo/'Suite/shared/JagoSuiteHost.cs').read_text(encoding='utf-8-sig');helper=s[s.index('// BEGIN JAGO HOST SECURITY'):s.index('// END JAGO HOST SECURITY')]
(out/'HostSecurity.cs').write_text(helper,encoding='utf-8');compiler=Path(r'C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe');subprocess.run([str(compiler),'/nologo','/reference:System.Web.Extensions.dll','/out:'+str(out/'HostSecurityTests.exe'),str(out/'HostSecurity.cs'),str(Path(__file__).with_name('HostSecurityTests.cs'))],check=True);subprocess.run([str(out/'HostSecurityTests.exe'),str(out/'Fixtures')],check=True)
# A real JS evaluation verifies strings/prototype-like keys remain inert data.
subprocess.run(['node','-e',"const fs=require('fs'),vm=require('vm'),assert=require('assert/strict'),scope={};let v=vm.runInNewContext(fs.readFileSync(process.argv[1],'utf8'),scope);assert.equal(scope.compromised,undefined);assert.equal(v.name,');globalThis.compromised=true;//');assert.equal(v.__proto__.polluted,true);assert.equal(vm.runInNewContext('({}).polluted',scope),undefined);console.log('Quoted data execution check passed');",str(out/'Fixtures/argument.js')],check=True)
