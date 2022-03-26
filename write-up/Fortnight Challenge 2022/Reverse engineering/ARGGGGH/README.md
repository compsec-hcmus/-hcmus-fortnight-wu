## ARGGGGH
 
![Category](https://img.shields.io/badge/Category-Reverse_Engineering-brightgreen.svg)  
![Author](https://img.shields.io/badge/Author-xikhud-blue.svg)    

### Description
Can you crack the password for this challenge? If you think you can, prove it. Good luck!

### Summary
Bài này sử dụng hai thuật toán nổi tiếng là RC4 và Base64. Ngoài ra nó còn sử dụng thủ thuật [compile-time string literal obfuscation](https://github.com/adamyaxley/Obfuscate).

### Detailed solution
Hàm `main`:
```c
__int64 __fastcall main(int a1, char **a2, char **a3)
{
  // [COLLAPSED LOCAL DECLARATIONS. PRESS KEYPAD CTRL-"+" TO EXPAND]

  v19 = __readfsqword(0x28u);
  v3 = sub_1588();
  v4 = (const char *)sub_1E84((__int64)v3);
  printf(v4);
  fgets(s, 256, stdin);
  s[strlen(s) - 1] = 0;
  v16 = sub_24D9(s);
  v5 = strlen(v16);
  s1 = (char *)calloc(v5 + 1, 1uLL);
  v6 = sub_16CC();
  v7 = sub_1F32((__int64)v6);
  sub_1500(v7, (__int64)v16, (__int64)s1);
  v8 = sub_1844();
  v9 = (const char *)sub_1FE0((__int64)v8);
  if ( !strcmp(s1, v9) )
  {
    v10 = sub_19CC();
    v11 = (const char *)sub_208E((__int64)v10);
    printf(v11, s);
  }
  else
  {
    v12 = sub_1AE8(&v15);
    v13 = (const char *)sub_213C(v12);
    printf(v13);
  }
  free(s1);
  free(v16);
  return 0LL;
}
```
Để ý rằng trong đoạn code trên có một số pattern như sau:
```c
v3 = sub_XXXX();
v4 = (const char *)sub_YYYY((__int64)v3);
printf(v4); // use v4, don't have to be printf
```
Trong đó hàm `sub_XXXX` và `sub_YYYY` trông giống giống như sau:
```c
void *sub_XXXX()
{
  char v1[40]; // [rsp+20h] [rbp-40h] BYREF
  unsigned __int64 v2; // [rsp+48h] [rbp-18h]

  v2 = __readfsqword(0x28u);
  v1[0] = 71;
  v1[1] = -12;
  v1[2] = -101;
  v1[3] = 43;
  v1[4] = -119;
  v1[5] = 71;
  v1[6] = -113;
  v1[7] = 119;
  v1[8] = 121;
  v1[9] = -20;
  v1[10] = -101;
  v1[11] = 56;
  v1[12] = -38;
  v1[13] = 86;
  v1[14] = -57;
  v1[15] = 119;
  v1[16] = 55;
  v1[17] = -24;
  v1[18] = -97;
  v1[19] = 57;
  v1[20] = -119;
  v1[21] = 85;
  v1[22] = -64;
  v1[23] = 96;
  v1[24] = 115;
  v1[25] = -94;
  v1[26] = -34;
  v1[27] = 74;
  if ( (_BYTE)byte_5060 || !__cxa_guard_acquire(&byte_5060) )
    return &unk_5040;
  sub_1DF8(&unk_5040, v1);
  __cxa_guard_release(&byte_5060);
  __cxa_atexit(func, &unk_5040, &dso_handle);
  return &unk_5040;
}

__int64 __fastcall sub_YYYY(__int64 a1)
{
  __int64 result; // rax

  result = *(unsigned __int8 *)(a1 + 28);
  if ( !(_BYTE)result )
    return result;
  sub_1D91(a1, 28LL, 0x12AF22FA4AFE9817LL); // xor with [0x17, 0x98, 0xFE, 0x4A, 0xFA, 0x22, 0xAF, 0x12]
  result = a1;
  *(_BYTE *)(a1 + 28) = 0;
  return result;
}
```

Khi đó đoạn code trên sẽ xor `[71, -12, -101, 43, ...]` với `[0x17, 0x98, 0xFE, 0x4A, 0xFA, 0x22, 0xAF, 0x12]` cho ra chuỗi `"Please enter the password: "` 

Các pattern khác làm tương tự. Đây chính là [compile-time string literal obfuscation](https://github.com/adamyaxley/Obfuscate).

Đầu tiên input của chúng ta được đưa vào hàm `sub_24D9`. Hàm này thực chất là hàm base64 encode, nhưng làm sao để nhận diện hàm này? Có 1 số cách:
- Dùng debugger để quan sát return value sau khi chạy hàm này, sẽ thấy tất cả các character của nó đều thuộc khoảng A-Z, a-z, 0-9 và +, /.
- Đọc code của hàm `sub_24D9` thấy có chỗ `malloc(4 * v1 / 3 + 4)` với `v1` là độ dài chuỗi input. Thuật toán encode mà làm cho độ dài của chuỗi dài thêm 4/3 lần chính là base64.

Tuy nhiên khi các bạn quan sát giá trị sau khi base64 encode thì sẽ thấy nó không chính xác so với việc các bạn tự encode. Đó là vì hàm base64 encode của mình sử dụng custom alphabet (xem hàm `sub_2302`).

`abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ+/`

Sau khi được base64 encode, nó lại được RC4 encrypt tại hàm `sub_1500`. Có 1 số cách để biết được hàm này là RC4, đã được viết trên fanpage, [tại đây](https://www.facebook.com/hcmus.compsec.club/posts/482321203493081).

Cuối cùng, sau khi được RC4 encrypt (với key là `"YEKDx2ZoxDcCFZzjnhx8Vx8y9mp7DySPhKipmz0s"`), nó sẽ được so sánh với một chuỗi hardcode bằng hàm `strcmp`. Từ đó ta dễ dàng tìm được flag là
```
flag = CustomBase64(RC4Decrypt(hardcode_string,  "YEKDx2ZoxDcCFZzjnhx8Vx8y9mp7DySPhKipmz0s"))
```
![]([img.png](https://github.com/compsec-hcmus/hcmus-wu/raw/main/write-up/Fortnight%20Challenge%202022/Reverse%20engineering/ARGGGGH/img.png))
[----------------------- Link để test -----------------------](https://gchq.github.io/CyberChef/#recipe=From_Hex('%5C%5Cx')RC4(%7B'option':'UTF8','string':'YEKDx2ZoxDcCFZzjnhx8Vx8y9mp7DySPhKipmz0s'%7D,'Latin1','Latin1')From_Base64('abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ%2B/',true)&input=XHhjNVx4ZjRceGNlXHgwM1x4MmFceGQyXHhmZlx4MzhceDFlXHhiZFx4NjdceDQ5XHhlNFx4MTBceGU2XHg4Nlx4MTFceGU4XHgzYlx4MTBceDE4XHg4Nlx4ZGZceGVmXHhhOFx4YTdceDk4XHgzOFx4NjlceGFiXHhjNFx4ZWVceGUxXHg1YVx4NGFceDU0XHg4Ylx4ZTFceDAzXHgyMVx4NWNceGFmXHgxM1x4NmU).

### Flag
```
f0rtn1ght{arc4_And_base64_boizzz}
```