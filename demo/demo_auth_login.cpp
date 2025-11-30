// login_logic.cpp (Demo Mode)
#include <cstring>
#include <cctype>
#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

// Simple in-memory "user table"
struct User {
    std::string username;
    std::string password;
    std::string email;
};

static std::vector<User> users = {
    {"testuser", "Test@123", "test@example.com"} // preloaded demo account
};

extern "C" __declspec(dllexport) int validate_login(const char* username, const char* password)
{
    std::string u(username);
    std::string p(password);

    for (const auto& user : users) {
        if (user.username == u && user.password == p) {
            return 1; // success
        }
    }
    return 0; // fail
}

extern "C" __declspec(dllexport) int register_user(
    const char* first_name,
    const char* last_name,
    const char* street_address,
    const char* city,
    const char* state,
    const char* zip_code,
    const char* phone,
    const char* email,
    const char* username,
    const char* password
)
{
    std::string u(username);
    std::string p(password);
    std::string e(email);

    // Basic validation (shortened for demo mode)
    if (u.length() < 4 || p.length() <= 6) return 0;
    if (e.find('@') == std::string::npos) return 0;

    // Check if username/email already exists
    for (const auto& user : users) {
        if (user.username == u || user.email == e) {
            return 0; // already exists
        }
    }

    // Add new user to simulated "table"
    users.push_back({u, p, e});
    std::cout << "Registered user: " << u << std::endl;
    return 1; // success
}