#include <stdio.h>
#include <string.h>
#include <openssl/evp.h>

#define SHA256_DIGEST_LENGTH 32

const char name[] = "abdul";
unsigned char stored_password_hash[] = {
    0xE6, 0x56, 0xEB, 0xB3, 0x74, 0xBB, 0x90, 0xE9, 
    0xA8, 0xF8, 0x6F, 0xBB, 0xE0, 0x4A, 0x6F, 0x9D,
    0xC8, 0x81, 0x7E, 0xDF, 0x33, 0x98, 0x4F, 0xF4,
    0xD5, 0xD2, 0x4D, 0x48, 0xE6, 0x1B, 0xAE, 0x00
};

void calculate_sha256(const char *input, unsigned char output[SHA256_DIGEST_LENGTH]) {
    EVP_MD_CTX *mdctx;
    const EVP_MD *md;
    unsigned int output_len;

    mdctx = EVP_MD_CTX_new();
    md = EVP_sha256();

    EVP_DigestInit_ex(mdctx, md, NULL);
    EVP_DigestUpdate(mdctx, input, strlen(input));
    EVP_DigestFinal_ex(mdctx, output, &output_len);

    EVP_MD_CTX_free(mdctx);
}

int compare_hashes(const unsigned char *hash1, const unsigned char *hash2, size_t length) {
    return memcmp(hash1, hash2, length) == 0;
}

int check_credentials(const char *entered_username, const char *entered_password) {
    unsigned char input_password_hash[SHA256_DIGEST_LENGTH];

    if (strcmp(entered_username, name) != 0) {
        printf("User not yet registered.\n");
        return 0;
    }

    calculate_sha256(entered_password, input_password_hash);

    if (compare_hashes(input_password_hash, stored_password_hash, SHA256_DIGEST_LENGTH)) {
        printf("Access granted! Welcome, %s.\n", entered_username);
        return 1;
    } else {
        printf("Access denied! Incorrect password.\n");
        return 0;
    }
}

int main() {
    char username[50];
    char password[50];

    printf("Enter your username: ");
    scanf("%49s", username);

    printf("Enter your password: ");
    scanf("%49s", password);

    check_credentials(username, password);

    return 0;
}
