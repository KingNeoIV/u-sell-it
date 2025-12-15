#include <algorithm>
#include <cctype>
#include <cstdlib>
#include <cstring>
#include <fstream>
#include <iostream>
#include <nlohmann/json.hpp>
#include <pqxx/pqxx>
#include <string>

// ================= Input Validation =================
class InputValidator {
public:
  static bool isAlphaStr(const std::string &s) {
    return s.length() >= 2 &&
           std::all_of(s.begin(), s.end(),
                       [](unsigned char c) { return std::isalpha(c); });
  }

  static bool isAddressStr(const std::string &s) {
    return !s.empty() && std::all_of(s.begin(), s.end(), [](unsigned char c) {
      return std::isalnum(c) || std::isspace(c) || c == '#' || c == '-';
    });
  }

  static bool isDigitStr(const std::string &s, size_t length) {
    return s.length() == length && std::all_of(s.begin(), s.end(), ::isdigit);
  }

  static bool isEmail(const std::string &s) {
    auto at = s.find('@');
    auto dot = s.find('.', at);
    return at != std::string::npos && dot != std::string::npos &&
           s.find(' ') == std::string::npos;
  }

  static bool isUsername(const std::string &s) {
    if (s.length() < 4 || !std::isalpha(s[0]))
      return false;
    return std::all_of(s.begin(), s.end(), [](unsigned char c) {
      return std::isalnum(c) || c == '_';
    });
  }

  static bool isStrongPassword(const std::string &s) {
    if (s.length() < 8)
      return false;
    bool has_upper = false, has_lower = false, has_digit = false,
         has_special = false;
    for (char ch : s) {
      if (std::isupper(ch))
        has_upper = true;
      else if (std::islower(ch))
        has_lower = true;
      else if (std::isdigit(ch))
        has_digit = true;
      else if (std::ispunct(ch))
        has_special = true;
    }
    return has_upper && has_lower && has_digit && has_special;
  }
};

// ================= Database Connector =================
class DatabaseConnector {
public:
  static pqxx::connection getConnection() {
    std::ifstream file("db_config.json");
    nlohmann::json config;
    file >> config;

    std::string conn_str = "host=" + config["DB_HOST"].get<std::string>() +
                           " port=" + config["DB_PORT"].get<std::string>() +
                           " dbname=" + config["DB_NAME"].get<std::string>() +
                           " user=" + config["DB_USER"].get<std::string>() +
                           " password=" + config["DB_PASS"].get<std::string>();

    return pqxx::connection(conn_str);
  }
};

// ================= Exported Functions =================
extern "C" __declspec(dllexport) int validate_login(const char *username,
                                                    const char *password) {
  try {
    pqxx::connection conn = DatabaseConnector::getConnection();
    pqxx::work txn(conn);

    pqxx::result result = txn.exec(
        "SELECT user_id FROM users WHERE username = " + txn.quote(username) +
        " AND password = " + txn.quote(password));

    txn.commit();
    return !result.empty() ? 1 : 0;
  } catch (const std::exception &e) {
    std::cerr << "Database error: " << e.what() << std::endl;
    return 0;
  }
}

extern "C" __declspec(dllexport) int register_user(
    const char *first_name, const char *last_name, const char *street_address,
    const char *city, const char *state, const char *zip_code,
    const char *phone, const char *email, const char *username,
    const char *password) {
  std::string user(username);
  std::string pass(password);

  // Run validations
  if (!InputValidator::isAlphaStr(first_name) ||
      !InputValidator::isAlphaStr(last_name))
    return 0;
  if (!InputValidator::isAddressStr(street_address))
    return 0;
  if (!InputValidator::isAlphaStr(city) || !InputValidator::isAlphaStr(state))
    return 0;
  if (!InputValidator::isDigitStr(zip_code, 5))
    return 0;
  if (!InputValidator::isDigitStr(phone, 10))
    return 0;
  if (!InputValidator::isEmail(email))
    return 0;
  if (!InputValidator::isUsername(user))
    return 0;
  if (!InputValidator::isStrongPassword(pass))
    return 0;

  try {
    pqxx::connection conn = DatabaseConnector::getConnection();
    pqxx::work txn(conn);

    // Check if username or email already exists
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
    std::cerr << "Database error: " << e.what() << std::endl;
    return 0;
  }
}