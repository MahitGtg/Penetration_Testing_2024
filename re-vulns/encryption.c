#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/evp.h>
#include <openssl/aes.h>

#define AES_KEY_LENGTH 32
#define AES_BLOCK_SIZE 16

const unsigned char hardcoded_key[AES_KEY_LENGTH] = {
    0x12, 0x34, 0x56, 0x78, 0x90, 0xab, 0xcd, 0xef, 
    0xfe, 0xdc, 0xba, 0x98, 0x76, 0x54, 0x32, 0x10,
    0x0f, 0x1e, 0x2d, 0x3c, 0x4b, 0x5a, 0x6c, 0x7d,
    0x8e, 0x9f, 0xaf, 0xbf, 0xcf, 0xdf, 0xef, 0xff
};

const unsigned char hardcoded_iv[AES_BLOCK_SIZE] = {
    0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
    0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f
};

void encrypt(FILE *input_file, FILE *output_file) {
    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
    if (!ctx) {
        fprintf(stderr, "Failed to create context.\n");
        return;
    }

    if (1 != EVP_EncryptInit_ex(ctx, EVP_aes_256_cbc(), NULL, hardcoded_key, hardcoded_iv)) {
        fprintf(stderr, "Failed to initialize encryption.\n");
        return;
    }

    unsigned char buffer[AES_BLOCK_SIZE];
    unsigned char ciphertext[AES_BLOCK_SIZE + AES_BLOCK_SIZE];
    int len, ciphertext_len;

    while ((len = fread(buffer, 1, AES_BLOCK_SIZE, input_file)) > 0) {
        if (1 != EVP_EncryptUpdate(ctx, ciphertext, &ciphertext_len, buffer, len)) {
            fprintf(stderr, "Encryption failed.\n");
            return;
        }
        fwrite(ciphertext, 1, ciphertext_len, output_file);
    }

    if (1 != EVP_EncryptFinal_ex(ctx, ciphertext, &ciphertext_len)) {
        fprintf(stderr, "Failed to finalize encryption.\n");
        return;
    }
    fwrite(ciphertext, 1, ciphertext_len, output_file);

    EVP_CIPHER_CTX_free(ctx);
}

int main(int argc, char *argv[]) {
    if (argc != 4) {
        fprintf(stderr, "Usage: %s <e> <input_file> <output_file>\n", argv[0]);
        return 1;
    }

    FILE *input_file = fopen(argv[2], "rb");
    FILE *output_file = fopen(argv[3], "wb");
    if (!input_file || !output_file) {
        fprintf(stderr, "Failed to open files.\n");
        return 1;
    }

    if (argv[1][0] == 'e') {
        encrypt(input_file, output_file);
    } else {
        fprintf(stderr, "Invalid option. Use 'e' for encrypt.\n");
        return 1;
    }

    fclose(input_file);
    fclose(output_file);

    return 0;
}
