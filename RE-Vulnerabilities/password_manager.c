#include <stdio.h>
#include <string.h>
#include <openssl/evp.h>

#define SHA256_DIGEST_LENGTH 32

const char name[] = "Abdul";
unsigned char stored_password_hash[] = {
    0x8d, 0x03, 0x09, 0x03, 0xb2, 0x5e, 0xc4, 0x41,
    0x0b, 0x46, 0xac, 0x38, 0x39, 0x91, 0x0f, 0x71,
    0x70, 0x82, 0xca, 0x1c, 0x6d, 0x95, 0x7f, 0xf5,
    0xe9, 0x60, 0x6b, 0x55, 0xa6, 0x0d, 0x85, 0xbc
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
