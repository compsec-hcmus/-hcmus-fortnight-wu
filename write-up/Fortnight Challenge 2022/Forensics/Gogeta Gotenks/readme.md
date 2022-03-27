## Fortnight challenge 2022: Gogeta Gotenks

![warmup category](https://img.shields.io/badge/Category-Forensics-brightgreen.svg)  
![score](https://img.shields.io/badge/Score_after_CTF-200-blue.svg)  
![author](https://img.shields.io/badge/Author-SpookyFish%234588-blue.svg)  
![solves](https://img.shields.io/badge/Solves-9-lightgrey.svg)

### Description
I just fished 2 pictures out from the trashbin. I don't need both of them at once tho, just one at a time is enough. How can I retrieve anything from these images?

### Hints
- None

### Attached files
- [img_1.png](https://github.com/compsec-hcmus/hcmus-wu/blob/main/write-up/Fortnight%20Challenge%202022/Forensics/Gogeta%20Gotenks/img_1.png?raw=true)
- [img_2.png](https://github.com/compsec-hcmus/hcmus-wu/blob/main/write-up/Fortnight%20Challenge%202022/Forensics/Gogeta%20Gotenks/img_2.png?raw=true)

### Summary
Xor the two images together.

### Detailed solution
The challenge description seems to indicate that we should xor the two images together. A quick [search from Google](https://stackoverflow.com/questions/8504882/searching-for-a-way-to-do-bitwise-xor-on-images) returns a convenient console command:  
```
convert img1 img2 -fx "(((255*u)&(255*(1-v)))|((255*(1-u))&(255*v)))/255" img_out
``` 

Substitute in the correct filenames:
```
convert img_1.png img_2.png -fx "(((255*u)&(255*(1-v)))|((255*(1-u))&(255*v)))/255" flag.png
```

And we get the flag image:  
![flag](https://user-images.githubusercontent.com/100995040/160264962-6cf88adb-edbb-40ca-ac52-36f452c42a52.png)  

### Flag
```
f0rtn1ght{1_l1ke_x0ring_stuff}
```
