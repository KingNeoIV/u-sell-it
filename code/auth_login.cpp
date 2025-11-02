// login_logic.cpp
#include <cstring>
#include <cctype>
#include <string>

extern "C" __declspec(dllexport) int validate_login(const char* username, const char* password) {
    // Replace with Oracle DB logic later
    if (strcmp(username, "admin") == 0 && strcmp(password, "1234") == 0) {
        return 1;   // success
    }
    return 0; // failure
}

extern "C" __declspec(dllexport) int register_user(const char* username, const char* email, const char* password) {
    std::string user(username);
    std::string pass(password);

    // Username must be at least 4 characters
    if (user.length() < 4) return 0;

    // First character must be a letter
    if (!std::isalpha(user[0])) return 0;

    // Password must be longer than 6 characters
    if (pass.length() <= 6) return 0;

    bool has_letter = false;
    bool has_digit = false;
    bool has_special = false;

    for (char ch : pass) {
        if (std::isalpha(ch)) has_letter = true;
        else if (std::isdigit(ch)) has_digit = true;
        else if (std::ispunct(ch)) has_special = true;
    }

    if (!has_letter || !has_digit || !has_special) return 0;

    // If all checks pass, return success
    return 1;
}