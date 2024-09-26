# Instructions to exploit RE vulnerabilities

# Installations:
- apt install execstack

## encryption - 
openssl enc -aes-256-cbc -d -in encrypted.txt -out decrypted.txt -K 1234567890abcdeffedcba98765432100f1e2d3c4b5a6c7d8e9fafbfcfdfefff -iv 000102030405060708090a0b0c0d0e0f

## password_manager - exploit
### Steps:
1. strings password_checker
- see the username abdul
2. objdump -d password_checker
- main
- check_credentials
- compare_hashes
- calculate_sha256
3. gdb password_checker
4. disas check_credentials # 4020 <stored_password_hash>
5. x/32bx 0x4020
- Outputs: 
<stored_password_hash> 0xd7 0x4f 0x2f 0xa4 0x3d 0xef 0x46 0x98 
<stored_password_hash> 0xbf 0xe0 0xb8 0xab 0x7f 0xc0 0xf8 0x3c
<stored_password_hash> 0xd3 0x67 0xbc 0x08 0x0a 0xbf 0x5c 0x24
<stored_password_hash> 0x74 0x40 0xf8 0x99 0x5f 0x8b 0x7f 0x80

e656ebb374bb90e9a8f86fbbe04a6f9dc8817edf33984ff4d5d24d48e61bae00

6. Put two and two together... password hash + sha256
7. Crack the hash to get the password nInJaP3NgUiN
8. Try nInJaP3NgUiN with username abdul
9. Success!