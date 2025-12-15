#include <algorithm>
#include <cctype>
#include <cstdlib>
#include <cstring>
#include <ctime>
#include <fstream>
#include <iostream>
#include <nlohmann/json.hpp>
#include <pqxx/pqxx>
#include <string>

// Global storage for demo code and timestamp
static std::string last_demo_code;
static std::time_t last_demo_timestamp;

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

  static bool isPhone(const std::string &s);
};

// ================= Phone Validation =================
#include <regex>
bool InputValidator::isPhone(const std::string &s) {
  // Accepts numbers like "1234567890" or "+123456789012"
  static const std::regex phoneRegex(R"(^\+?[0-9]{10,15}$)");
  return std::regex_match(s, phoneRegex);
}

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

// ================= Email/Phone Validation Function =================
extern "C" __declspec(dllexport) int validate_contact(const char *contact) {
  try {
    // Basic format validation first: must be either email OR phone
    bool isEmail = InputValidator::isEmail(contact);
    bool isPhone =
        InputValidator::isPhone(contact); // <-- you need to implement this

    if (!isEmail && !isPhone) {
      return 0; // invalid format
    }

    pqxx::connection conn = DatabaseConnector::getConnection();
    pqxx::work txn(conn);

    // Query depending on type
    pqxx::result result;
    if (isEmail) {
      result = txn.exec("SELECT user_id FROM users WHERE email = " +
                        txn.quote(contact) + " LIMIT 1");
    } else if (isPhone) {
      result = txn.exec("SELECT user_id FROM users WHERE phone = " +
                        txn.quote(contact) + " LIMIT 1");
    }

    txn.commit();
    return !result.empty() ? 1 : 0;

  } catch (const std::exception &e) {
    std::cerr << "Database error: " << e.what() << std::endl;
    return 0;
  }
}

// ================= Demo Code Generator =================
extern "C" __declspec(dllexport) const char *generate_demo_code() {
  try {
    // Seed RNG once per process
    std::srand(static_cast<unsigned int>(std::time(nullptr)));

    // Generate random 6-digit code
    int code = 100000 + (std::rand() % 900000); // ensures 6 digits
    last_demo_code = std::to_string(code);

    // Save timestamp
    last_demo_timestamp = std::time(nullptr);

    // Log for debugging (optional)
    std::cout << "Generated demo code: " << last_demo_code << " at "
              << std::ctime(&last_demo_timestamp) << std::endl;

    // Return C-string pointer (safe because last_demo_code is static)
    return last_demo_code.c_str();
  } catch (const std::exception &e) {
    std::cerr << "Error generating demo code: " << e.what() << std::endl;
    return nullptr;
  }
}

// ================= Demo Code Validation =================
extern "C" __declspec(dllexport) int validate_demo_code(const char *input) {
  try {
    std::time_t now = std::time(nullptr);

    // Expire after 90 seconds
    if (difftime(now, last_demo_timestamp) > 90) {
      return 0; // expired
    }

    // Compare with stored code
    return (last_demo_code == input) ? 1 : 0;
  } catch (const std::exception &e) {
    std::cerr << "Error validating demo code: " << e.what() << std::endl;
    return 0;
  }
}

// ================= Demo Code Remaining Time =================
extern "C" __declspec(dllexport) int get_demo_code_remaining_time() {
  try {
    std::time_t now = std::time(nullptr);
    int elapsed = static_cast<int>(difftime(now, last_demo_timestamp));
    int remaining = 90 - elapsed;
    return (remaining > 0) ? remaining : 0;
  } catch (const std::exception &e) {
    std::cerr << "Error getting remaining time: " << e.what() << std::endl;
    return 0;
  }
}

// ================= Password Update by Contact =================
extern "C" __declspec(dllexport) int update_password_by_contact(
    const char *contact, const char *new_password,
    const char *confirm_password) {
  try {
    std::string newPass(new_password);
    std::string confirmPass(confirm_password);

    // Validation checks
    if (newPass.empty() || confirmPass.empty())
      return -1;
    if (newPass != confirmPass)
      return -2;
    if (newPass.length() < 8)
      return -3;
    if (!InputValidator::isStrongPassword(newPass))
      return -4;

    pqxx::connection conn = DatabaseConnector::getConnection();
    pqxx::work txn(conn);

    bool isEmail = InputValidator::isEmail(contact);
    bool isPhone = InputValidator::isPhone(contact);
    if (!isEmail && !isPhone)
      return -5;

    std::string query;
    if (isEmail) {
      query = "UPDATE users SET password = " + txn.quote(newPass) +
              " WHERE email = " + txn.quote(contact);
    } else {
      query = "UPDATE users SET password = " + txn.quote(newPass) +
              " WHERE phone = " + txn.quote(contact);
    }

    txn.exec(query);
    txn.commit();
    return 1; // Success
  } catch (const std::exception &e) {
    std::cerr << "Database error: " << e.what() << std::endl;
    return 0; // General failure
  }
}