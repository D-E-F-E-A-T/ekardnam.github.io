
This is the second part of the analisys of a SKIDROW crack for the game Assassin's Creed II I started in a previous post.

In this post we are going to analyze the DLL we have remained to analyze and see what it does.

First thing let's go for some static analysis again on both the original DLL and the cracked one.

I opened both the DLL in CFF Explorer and watched the imports

![Comaparison of the imports from the legit DLL and the cracked one](/images/dll-comparison-1.png)

The one on the left is the original DLL. You can see the original has imports for crypto libraries like Secur32.dll and CRYPT32.dll while the cracked one has an import for WINSOCK32.dll which is Windows socket library.

This WinSock import made me think. The original DLL uses WINHTTP.dll which I guess provides an HTTP(S) interface, while the cracked one uses plain sockets.

I opened the dll in ghidra and watched the imports and got this

![Cracked DLL imports](/images/dll-imports.png)

It seemed very few to do anything really. And this time GetProcAddress was not being imported like in SKIDROW.exe so it seemed to me that no procedures were getting loaded by the program itself.

I decided it was time to go for dynamic analysis. I made this simple C++ program to load the cracked DLL

    #include <windows.h>
    #include <iostream>

    int main(void)
    {
      HINSTANCE hDLL = LoadLibrary("C:\\Users\\IEUser\\Desktop\\ubiorbitapi_r2.dll");

      if (hDLL == NULL)
        std::cout << "Could not load the DLL" << std::endl;

      return 0;
    }

And compiled it using

    C:\Users\IEUser\Desktop>cl wrapper.cpp
    Microsoft (R) C/C++ Optimizing Compiler Version 19.00.24210 for x86
    Copyright (C) Microsoft Corporation.  All rights reserved.

    wrapper.cpp
    C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE\xlocale(341): warning C4530: C++ exception handler used, but unwind semantics are not enabled. Specify /EHsc
    C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE\exception(359): warning C4577: 'noexcept' used with no exception handling mode specified; termination on exception is not guaranteed. Specify /EHsc
    Microsoft (R) Incremental Linker Version 14.00.24210.0
    Copyright (C) Microsoft Corporation.  All rights reserved.

    /out:wrapper.exe
    wrapper.obj

    C:\Users\IEUser\Desktop>link wrapper.obj
    Microsoft (R) Incremental Linker Version 14.00.24210.0
    Copyright (C) Microsoft Corporation.  All rights reserved.

And after staring my wrapper program I get

![Antidebugging protection](/images/antidebug.png)

I modified my code to be more versatile into this

    #include <windows.h>
    #include <iostream>

    int main(int argc, char **argv)
    {
     if (argc < 2)
     {
       std::cout << "Usage " << argv[0] << " [DLL name]" << std::endl;
       goto quit;
     }

     std::cout << "Attach debuger now"<< std::endl;
     system("pause");

     HINSTANCE hDLL = LoadLibrary(argv[1]);

     if (hDLL == NULL)
       std::cout << "Could not load the DLL" << std::endl;

     std::cout << "DLL loaded" << std::endl;

    quit:
     system("pause");
     return 0;
    }

And I did not get a check on the debugger on the original DLL by Ubisoft, suggesting the check was added byh skidrow itself.
This is suspicious, I guess there are two reasons the skidrow guys want to protect their code from debugging:

- their code contains malware and they want to make RE more difficult
- they want to avoid their "opponents" cracking team to RE their crack and steal it

To be honest both options seem to make sense to me.

I also checked strings and got this (on the left the cracked version on the right the legit one)

![](/images/debugstrings.png)

Also the legit DLL imports IsDebuggerPresent but the error message we got from the cracked DLL is not present in the legit one. So this confirms that that message is thrown only by the cracked DLL.
