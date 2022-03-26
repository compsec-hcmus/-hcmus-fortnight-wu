## Fortnight challenge 2022: Save me senpai

![warmup category](https://img.shields.io/badge/Category-Cryptography-brightgreen.svg)  
![score](https://img.shields.io/badge/Score_after_CTF-200-blue.svg)  
![author](https://img.shields.io/badge/Author-SpookyFish%234588-blue.svg)  
![solves](https://img.shields.io/badge/Solves-25-lightgrey.svg)

### Description
I've just got to HCM City yesterday but spookyfish is now holding me captive at this coffee place to make CTF challenges. I just left a review of this place on Google Maps. Please find where it is and come save me. Quick!

### Hints
- None

### Attached files
- 

### Summary
I used base 32 decode and base 64 decode

### Detailed solution
[Provide the detailed solution of the ctf here.]
Some rules:
Name of tool, name of file, name of functions, etc: put in 1 set of backtick:  `name of something`
Code snippet, console output, other long multilines of text: put in 3 sets of backticks on a new line: 
```code snippet```
Key ideas, name of person who invented the method, etc: put in bold **name of someone** 

From the clues in the challenge description we can deduce that the person is in a coffee place in HCM City, and the flag is in the review section of that place on Google Maps.   
Looking at the picture, we can see that the person is in The Coffee House, however, there are more than 15 TCH in HCMC. Of course one can check the reviews of each TCH to find the flag, but doing so strips the challenge of its magic.  
So I propose a way to pin point exactly where the flag is.  
Looking once again at the picture, we see that there is a Pharmacity and a Ministop in front of the TCH place. So by searching every TCH, Pharmacity, and Ministop, take a picture, then stack them onto each other, we can see where the three places intersect, and that place should contain the flag.  

The TCH places in HCMC:  

The Pharmacity places in HCMC stack on top of the TCH places:  

The Ministop places in HCMC stack on top of Pharmacity and TCH places:  

There is indeed only one place that fits the scheme:  

Looking in the reviews, we find the flag.  



### Flag
```
f0rtn1ght{y0u_f0und_m3}
```
