## Fortnight challenge 2022: Barbie Goin' Bad

![warmup category](https://img.shields.io/badge/Category-OSINT-brightgreen.svg)  
![score](https://img.shields.io/badge/Score_after_CTF-200-blue.svg)  
![author](https://img.shields.io/badge/Author-niche%233259-blue.svg)  
![solves](https://img.shields.io/badge/Solves-7-lightgrey.svg)

### Description
Welcome detectives and OSINT lovers (and also stalkers)!!! We have an emergency on finding an anonymous user involved in a mysterious case. Help us find that person, here is your clue: "Coding, Nicki Minaj, OSINT lover".

### Hints
- None

### Attached files
- None

### Summary
The flag is in an old commit of a user on Github.

### Detailed solution
From the "Coding" clue, we can relate to Github. From that, simply search using the term "nicki minaj osint lover" and we can find a suspicious account that was created only recently.  
The account has 2 repository, one of which conveniently titled "my_very_secured_flags". However, looking in the flag.txt file, we only find the string `Sorry flag not here anymore :(`  
Going throught the file's commit history, we can find the flag: `f0rtn1ght{G1thub_1s_n00b}`

### Flag
```
f0rtn1ght{G1thub_1s_n00b}
```
