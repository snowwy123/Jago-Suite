#define NOMINMAX
#include <windows.h>
#include <thumbcache.h>
#include <shlwapi.h>
#include <wrl/client.h>
#include <iostream>
using Microsoft::WRL::ComPtr;
const CLSID Jago={0x97139026,0x28d9,0x4dd5,{0x94,0x1b,0x29,0xd9,0x7c,0x0a,0xa8,0x32}};
int wmain(int argc,wchar_t**argv){if(argc<3)return 2;CoInitializeEx(nullptr,COINIT_APARTMENTTHREADED);HMODULE dll=LoadLibraryW(argv[1]);if(!dll)return 3;auto get=(HRESULT(__stdcall*)(REFCLSID,REFIID,void**))GetProcAddress(dll,"DllGetClassObject");auto unload=(HRESULT(__stdcall*)())GetProcAddress(dll,"DllCanUnloadNow");int fails=0;{ComPtr<IClassFactory>factory;if(!get||FAILED(get(Jago,IID_PPV_ARGS(&factory))))return 4;for(int i=2;i<argc;i++){ComPtr<IInitializeWithStream>init;ComPtr<IThumbnailProvider>provider;ComPtr<IStream>stream;HRESULT hr=factory->CreateInstance(nullptr,IID_PPV_ARGS(&init));if(SUCCEEDED(hr))hr=SHCreateStreamOnFileEx(argv[i],STGM_READ|STGM_SHARE_DENY_NONE,0,FALSE,nullptr,&stream);if(SUCCEEDED(hr))hr=init->Initialize(stream.Get(),STGM_READ);if(SUCCEEDED(hr))hr=init.As(&provider);HBITMAP bitmap=nullptr;WTS_ALPHATYPE alpha=WTSAT_UNKNOWN;if(SUCCEEDED(hr))hr=provider->GetThumbnail(256,&bitmap,&alpha);BITMAP info={};if(bitmap)GetObject(bitmap,sizeof(info),&info);bool ok=SUCCEEDED(hr)&&bitmap&&info.bmWidth>0&&info.bmWidth<=256&&info.bmHeight>0&&info.bmHeight<=256&&alpha==WTSAT_ARGB;bool bad=std::wstring(argv[i]).find(L"bad-")!=std::wstring::npos;std::wcout<<argv[i]<<L" "<<(bad?(FAILED(hr)?L"REJECTED":L"UNEXPECTED"):ok?L"PASS":L"FAIL")<<L" "<<std::hex<<hr<<L" "<<std::dec<<info.bmWidth<<L"x"<<info.bmHeight<<L"\n";if(bad?SUCCEEDED(hr):!ok)fails++;if(bitmap)DeleteObject(bitmap);}}if(!unload||unload()!=S_OK)fails++;FreeLibrary(dll);CoUninitialize();return fails?1:0;}
