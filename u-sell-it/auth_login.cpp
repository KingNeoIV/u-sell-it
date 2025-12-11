// auth_logic.cpp
#include <cctype>
#include <cstring>
#include <iostream>
#include <pqxx/pqxx>
#include <string>

extern "C" __declspec(dllexport) int validate_login(const char *username,
                                                    const char *password) {
  try {
    pqxx::connection conn("host= "    // Enter the database ip address HERE
                          "dbname= "  // Enter the name of the database HERE
                          "user= "    // Enter the admin/user
                          "password=" // Enter password for admin/user
    );

    pqxx::work txn(conn);
    pqxx::result result = txn.exec(
        "SELECT user_id FROM users WHERE username = " + txn.quote(username) +
        " AND password = " + txn.quote(password));

    txn.commit();
    return !result.empty() ? 1 : 0;
  } catch (const std::exception &e) {
    std::cerr << "Database error: " << e.what() << std::endl;
    return 0; // Connection or query failed
  }
}

extern "C" __declspec(dllexport) int register_user(
    const char *first_name, const char *last_name, const char *street_address,
    const char *city, const char *state, const char *zip_code,
    const char *phone, const char *email, const char *username,
    const char *password) {
  std::string user(username);
  std::string pass(password);

  // Username must be at least 4 characters
  if (user.length() < 4 || !std::isalpha(user[0]) || pass.length() <= 6)
    return 0;

  bool has_letter = false, has_digit = false, has_special = false;
  for (char ch : pass) {
    if (std::isalpha(ch))
      has_letter = true;
    else if (std::isdigit(ch))
      has_digit = true;
    else if (std::ispunct(ch))
      has_special = true;
  }
  if (!has_letter || !has_digit || !has_special)
    return 0;

  // ============ Field Validation ============
  auto is_alpha_str = [](const std::string &s) {
    return !s.empty() && std::all_of(s.begin(), s.end(), [](unsigned char c) {
      return std::isalpha(c);
    });
  };

  auto is_digit_str = [](const std::string &s) {
    return !s.empty() && std::all_of(s.begin(), s.end(), [](unsigned char c) {
      return std::isdigit(c);
    });
  };

  // First/Last name
  if (!is_alpha_str(first_name) || !is_alpha_str(last_name))
    return 0;

  // Street address (basic non-empty check)
  if (std::string(street_address).empty())
    return 0;

  // City/State
  if (!is_alpha_str(city) || !is_alpha_str(state))
    return 0;

  // Zip code (5 digits)
  if (!is_digit_str(zip_code) || std::string(zip_code).length() != 5)
    return 0;

  // Phone (10 digits)
  if (!is_digit_str(phone) || std::string(phone).length() != 10)
    return 0;

  // Email (basic check)
  std::string mail(email);
  if (mail.find('@') == std::string::npos ||
      mail.find('.') == std::string::npos)
    return 0;

  // Username must be at least 4 chars and contain letter, digit, special char
  if (user.length() < 4 || !std::isalpha(user[0]))
    return 0;

  // Password must be > 6 chars and contain letter, digit, special
  if (pass.length() <= 6)
    return 0;
  bool has_letter = false, has_digit = false, has_special = false;
  for (char ch : pass) {
    if (std::isalpha(ch))
      has_letter = true;
    else if (std::isdigit(ch))
      has_digit = true;
    else if (std::ispunct(ch))
      has_special = true;
  }
  if (!has_letter || !has_digit || !has_special)
    return 0;

  try {
    pqxx::connection conn("host= "    // Enter the database ip address HERE
                          "dbname= "  // Enter the name of the database HERE
                          "user= "    // Enter the admin/user
                          "password=" // Enter password for admin/user
    );

    pqxx::work txn(conn);

    // Check if username or email already exits
    pqxx::result check = txn.exec(
        "SELECT user_id FROM users WHERE username = " + txn.quote(username) +
        " OR email = " + txn.quote(email));
    if (!check.empty())
      return 0;

    // Insert new user
    txn.exec("INSERT INTO users (username, email, password, first_name, "
             "last_name, phone, street_address, city, zip_code, state) "
             "VALUES (" +
             txn.quote(username) + ", " + txn.quote(email) + ", " +
             txn.quote(password) + ", " + txn.quote(first_name) + ", " +
             txn.quote(last_name) + ", " + txn.quote(phone) + ", " +
             txn.quote(street_address) + ", " + txn.quote(city) + ", " +
             txn.quote(zip_code) + ", " + txn.quote(state) + ")");

    txn.commit();
    return 1; // Success
  } catch (const std::exception &e) {
    return 0; // Registration failed
  }
}