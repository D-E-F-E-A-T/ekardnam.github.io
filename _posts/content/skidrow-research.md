
I was willing to play some videogames on my computer, but at the same time I was quite annoyed of paying for them. I thought I could take this occasion to analyze some cracked videogames for malware.

I downloaded a torrent for Assassin's Creed II and got an ISO image. I decided to mount it and upload the executables contained in it on VirusTotal and watch the reports.
Here the executables and DLLs I found

    ekardnam@bakunin:~/Downloads/Assassins.Creed.II-SKIDROW/mountpoint$ find . | grep .exe
    ./SKIDROW/SKIDROW.exe
    ./Support/DirectX/DXSETUP.exe
    ./Support/GameLauncher/UbisoftGameLauncherInstaller.exe
    ./Support/VCRedist/vcredist_x86.exe
    ./UPDATE/assassins_creed_2_1.01_us.exe
    ./autorun.exe
    ./setup.exe
    ekardnam@bakunin:~/Downloads/Assassins.Creed.II-SKIDROW/mountpoint$ find . | grep .dll
    ./ISSetup.dll
    ./SKIDROW/ubiorbitapi_r2.dll
    ./Support/DirectX/DSETUP.dll
    ./Support/DirectX/dsetup32.dll
    ./Support/DirectX/dxdllreg_x86.cab
    ./\_Setup.dll

I actually focused on SKIDROW.exe and ubiorbitapi_r2.dll, both these were marked by VirusTotal.

![SKIDROW.exe report](/images/skidrow.png)

![DLL report](/images/dll.png)

Opening SKIDROW.exe in ghidra I found the following imported functions from kernel32.DLL

![SKIROW.exe imports GetProcAddress and LoadLibraryA](/images/skidrow-imports.png)

I thought it would load the ubiorbitapi_r2.dll and run some procedures from it, but the code wasn't so pretty to read and I thought I would go for dynamic analysis.

At the same time I was setting up a VM with the Flare-ON installer I saw in one of LiveOverflow's videos.

![](/images/flare-on-vm.png)

Also the DLL seemed obfuscated at first glance and anyway I'm lazy and dynamic analysis seemed the faster way.

Anyway after some DuckDuckGo-ing I found that the ubiorbitapi_r2.dll is supposed to be a Ubisoft dll for checking the game activation key. This explains why it was found in the cracked files folder. Here some functions it exports:

    0009BD7E  ?ClaimCdKey@OrbitSession@orbitdll@mg@@QAEXIPAVIClaimCdKeyListener@23@PADI@Z
    0009BDCA  ?Close@SavegameReader@orbitdll@mg@@QAEXXZ
    0009BDF4  ?Close@SavegameWriter@orbitdll@mg@@QAEX_N@Z
    0009BE20  ?CreateAccount@OrbitSession@orbitdll@mg@@QAEXIPAVICreateAccountListener@23@PAD1PAG11EEG_N3@Z
    0009BE7D  ?GetGeoIpCountry@OrbitSession@orbitdll@mg@@QAEXIPAVIGetGeoIpCountryListener@23@@Z
    0009BECF  ?GetLocText@OrbitSession@orbitdll@mg@@QAEPBGPBGPBD@Z
    0009BF04  ?GetLoginDetails@OrbitSession@orbitdll@mg@@QAEXIPAVIGetLoginDetailsListener@23@@Z
    0009BF56  ?GetName@SavegameInfo@orbitdll@mg@@QAEPBGXZ
    0009BF82  ?GetNetworkTraffic@OrbitSession@orbitdll@mg@@QAEXIPAVIGetNetworkTrafficListener@23@@Z
    0009BFD8  ?GetOrbitServer@OrbitSession@orbitdll@mg@@QAEXIPAVIGetOrbitServerListener@23@II@Z
    0009C02A  ?GetProductId@SavegameInfo@orbitdll@mg@@QAEIXZ
    0009C059  ?GetProxyIfNeeded@Proxy@orbitdll@mg@@QAE_NPBDGAAV?$StaticString@$0BAAA@@common@3@@Z
    0009C0AD  ?GetRequestUniqueId@OrbitSession@orbitdll@mg@@QAEIXZ
    0009C0E2  ?GetSavegameId@SavegameInfo@orbitdll@mg@@QAEIXZ
    0009C112  ?GetSavegameList@OrbitSession@orbitdll@mg@@QAEXIPAVIGetSavegameListListener@23@I@Z
    0009C165  ?GetSavegameReader@OrbitSession@orbitdll@mg@@QAEXIPAVIGetSavegameReaderListener@23@II@Z
    0009C1BD  ?GetSavegameWriter@OrbitSession@orbitdll@mg@@QAEXIPAVIGetSavegameWriterListener@23@II_N@Z
    0009C217  ?GetSize@SavegameInfo@orbitdll@mg@@QAEIXZ
    0009C241  ?GetTos@OrbitSession@orbitdll@mg@@QAEXIPAVIGetTosListener@23@PBD1@Z
    0009C285  ?IsSavegamesInSync@Proxy@orbitdll@mg@@QAE_NXZ
    0009C2B3  ?IsVersionBanned@OrbitSession@orbitdll@mg@@QAEXIPAVIIsVersionBannedListener@23@II@Z
    0009C307  ?LogIn@OrbitSession@orbitdll@mg@@QAEXIPAVILogInListener@23@PADPAG@Z
    0009C34B  ?LogOut@OrbitSession@orbitdll@mg@@QAEXIPAVILogOutListener@23@@Z
    0009C38B  ?OwnsProduct@OrbitSession@orbitdll@mg@@QAEXIPAVIOwnsProductListener@23@I@Z
    0009C3D6  ?Read@SavegameReader@orbitdll@mg@@QAEXIPAVISavegameReadListener@23@IPAXI@Z
    0009C421  ?RemoveSavegame@OrbitSession@orbitdll@mg@@QAEXIPAVIRemoveSavegameListener@23@II@Z
    0009C473  ?SetCookie@Proxy@orbitdll@mg@@QAEXI@Z
    0009C499  ?SetName@SavegameWriter@orbitdll@mg@@QAE_NPAG@Z
    0009C4C9  ?SetSavegameSyncCallback@Proxy@orbitdll@mg@@QAEXPAVISavegameSyncCallback@23@@Z
    0009C518  ?SetStaticProxy@Proxy@orbitdll@mg@@QAEXPBD@Z
    0009C545  ?SetUseOnlineSave@Proxy@orbitdll@mg@@QAEX_N@Z
    0009C573  ?Start@Proxy@orbitdll@mg@@QAE_NXZ
    0009C595  ?StartLauncher@OrbitSession@orbitdll@mg@@QAE_NIIPBD0@Z
    0009C5CC  ?StartProcessingSavegameSyncTasks@Proxy@orbitdll@mg@@QAEXXZ
    0009C608  ?StartSavegameSync@Proxy@orbitdll@mg@@QAEXW4TestMode@SavegameStorage@23@PAVITestStatusCallback@523@@Z
    0009C66E  ?StopSavegameSync@Proxy@orbitdll@mg@@QAEXXZ
    0009C69A  ?Update@OrbitSession@orbitdll@mg@@QAEXXZ
    0009C6C3  ?ValidateLauncherCookie@OrbitSession@orbitdll@mg@@QAEXIPAVIValidateLauncherCookieListener@23@I@Z
    0009C724  ?ValidateUsername@OrbitSession@orbitdll@mg@@QAEXIPAVIValidateUsernameListener@23@PAD@Z
    0009C77B  ?Write@SavegameWriter@orbitdll@mg@@QAEXIPAVISavegameWriteListener@23@PAXI@Z

    0009C7C7  MgOrbitdllGetFakeSession
    0009C7E0  MgOrbitdllGetLocText
    0009C7F5  MgOrbitdllGetLoginDetails
    0009C80F  MgOrbitdllGetNetworkTraffic
    0009C82B  MgOrbitdllGetOrbitServer
    0009C844  MgOrbitdllGetRequestUniqueId
    0009C861  MgOrbitdllGetSavegameList
    0009C87B  MgOrbitdllGetSavegameReader
    0009C897  MgOrbitdllGetSavegameWriter
    0009C8B3  MgOrbitdllGetSession
    0009C8C8  MgOrbitdllRemoveSavegame
    0009C8E1  MgOrbitdllSaveGameInfoGetName
    0009C8FF  MgOrbitdllSaveGameInfoGetProductId
    0009C922  MgOrbitdllSaveGameInfoGetSavegameId
    0009C946  MgOrbitdllSaveGameInfoGetSize
    0009C964  MgOrbitdllSaveGameReaderClose
    0009C982  MgOrbitdllSaveGameReaderRead
    0009C99F  MgOrbitdllSaveGameWriterClose
    0009C9BD  MgOrbitdllSaveGameWriterSetName
    0009C9DD  MgOrbitdllSaveGameWriterWrite
    0009C9FB  MgOrbitdllStartLauncher
    0009CA13  MgOrbitdllUpdate

I decided to install the game to get also the original DLL and see what's different.

![Installation process](/images/acii-install.png)

Strings of the original DLL were completely different obviously, but seems all pretty normal as the DLL is cracked.

After going with some dynamic analysis on the SKIDROW.exe binary I understood that my initial thought that it would load procedures from the ubiorbit DLL was wrong. Also, given the DLL purpose it makes sense that it is not loading procedures from there.

By setting a breakpoint at GetProcAddress and watching the stack I could see which procedures it is loading that are not marked as imported in the PE file.

![](/images/skidrowdbg-1.png)

I used procmon to monitor the calls the executable made ton the Win API and I did not get anything that to my non-expert eye looked suspicious

![](/images/skidrow-procmon.png)

Finally I looked at what was happening in the network. And here it was doing really nothing.
Also this is what it happens after you execute this binary.

![](/images/skidrow-run.png)

It just seems a "signature" by this team of crackers called Skid Row, hance as it does not seem to be downloading other payloads, I don't think it hides any particular malware.

Now there is still the DLL to analyze, but that would be for another post!
