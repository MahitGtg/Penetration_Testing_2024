# Instructions to exploit RE vulnerabilities

# Installations:
- apt install execstack

## encryption - 
openssl enc -aes-256-cbc -d -in encrypted.txt -out decrypted.txt -K 1234567890abcdeffedcba98765432100f1e2d3c4b5a6c7d8e9fafbfcfdfefff -iv 000102030405060708090a0b0c0d0e0f

## password_manager - exploit
### Steps:
1. strings password_manager
- see the username connor
2. objdump -d password_manager
- main
- check_credentials
- compare_hashes
- calculate_sha256
3. gdb password_manager
4. disas check_credentials
5. x/32bx 0x4020
- Outputs: 
0xd7 0x4f 0x2f 0xa4 0x3d 0xef 0x46 0x98 
0xbf 0xe0 0xb8 0xab 0x7f 0xc0 0xf8 0x3c
0xd3 0x67 0xbc 0x08 0x0a 0xbf 0x5c 0x24
0x74 0x40 0xf8 0x99 0x5f 0x8b 0x7f 0x80
6. Put two and two together... password hash + sha256
7. Crack the hash to get the password rubberducky
8. Try rubberducky with username connor
9. Success!