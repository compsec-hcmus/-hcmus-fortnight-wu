## Fortnight challenge 2022: CAPTURE THE FLAG

![warmup category](https://img.shields.io/badge/Category-Forensics-brightgreen.svg)  
![score](https://img.shields.io/badge/Score_after_CTF-200-blue.svg)  
![author](https://img.shields.io/badge/Author-SpookyFish%234588-blue.svg)  
![solves](https://img.shields.io/badge/Solves-6-lightgrey.svg)

### Description
WOW YOU HAVE GONE QUITE A LONG WAY HUH. BUT SO FAR YOU ONLY RELIED ON CAPITAL LETTERS TO GIVE YOU HINTS RIGHT? WELL, THIS TIME, TRY TO LOOK AT THE BIG PICTURE!

The format of the flag is f0rtn1ght{what_you_found} with "what_you_found" is what you found after solving the challenge.

### Hints
- None

### Attached files
- 

### Summary
Spectrogram in Audacity, binwalk, hexedit gives 8 coordinates, the first letters of each country is the flag.

### Detailed solution
For the first file, it's a .wav file with nothing interesing going on when listening to it. However, opening it in Audacity under spectrogram mode reveals 3 sets of coordinates.  

45,4215N, 75.6972W  
23.5880N, 58.3829E  
27.7172N, 85.3240E  
  
For the second file, the solution to the riddle is of course the capital letters of each line - binwalk.  

Running `binwalk FLAG_2.PNG` on it reveals that there's a .rar file hidden inside.  
```
$ binwalk FLAG_2.PNG

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             PNG image, 966 x 669, 8-bit/color RGB, non-interlaced
91            0x5B            Zlib compressed data, compressed
29086         0x719E          RAR archive data, version 5.x
5646435       0x562863        StuffIt Deluxe Segment (data): f
13090889      0xC7C049        Qualcomm device tree container, version: 1671221820, DTB entries: 1392494259
```
We can carve out the files using `binwalk -e FLAG_2.PNG`. After extracting it, we find a good_job.pdf file, and at the last page of the pdf, we find another set of coordinates.  
64.1814N, 51.6941W  
44.4268N, 26.1025E  
35.2802S, 149.1310E  

For the third file, since there's no file extension, we can try running xxd on it to check its header.  
```
$ xxd -l 64 FLAG_3
00000000: 6969 6969 0010 4a46 4946 0001 0101 0048  iiii..JFIF.....H
00000010: 0048 0000 ffe1 0022 4578 6966 0000 4d4d  .H....."Exif..MM
00000020: 002a 0000 0008 0001 0112 0003 0000 0001  .*..............
00000030: 0001 0000 0000 0000 fffe 000d 4170 706c  ............Appl
```
The file seems to be a JFIF file, but the first for bytes (69 69 69 69) are obviously edited. A quick Google search shows that it's supposed to be FF D8 FF E0. Using [hexedit](https://hexed.it/) to correct the header, it turns out the file is an image with 2 final coordinates.  
39.9334N, 32.8597E  
59.3293N, 18.0686E  
  
The 8 coordinates points to capitals of 8 different countries:  
Ottawa,     Canada
Muscat,     Oman
Kathmandu,  Nepal
Nuuk,       Greenland
Bucharest,  Romania
Canberra,   Australia
Ankara,     Turkey
Stockholm,  Sweden

Since the challenge description tells us to stop looking at the capitals and instead focus on the big picture, we can piece the first letters of each contries to form the word: CONGRATS.  

### Flag
```
f0rtn1ght{CONGRATS}
```
