// --- 1. Interfaces (The Blueprints) ---

export interface User {
  id: string;
  email: string;
}

export interface UserRead {
  email: string;
  id: string;
  is_active: boolean;
}

export interface UserCreate {
  email: string;
  password: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: User;
}

export interface ForgotPasswordRequest {
  email: string;
}

export interface ResetPasswordRequest {
  token: string;
  new_password: string;
}

// --- 2. Configuration ---

const API_URL = "http://localhost:8000";

// --- 3. API Action Functions ---

/**
 * Register a new user account.
 */
export async function registerUser(data: UserCreate): Promise<UserRead> {
  const response = await fetch(`${API_URL}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorBody = await response.json();
    throw new Error(errorBody.detail?.[0]?.msg || "Registration failed");
  }

  return response.json();
}

/**
 * Authenticate a user and return tokens.
 */
export async function loginUser(data: LoginRequest): Promise<LoginResponse> {
  const response = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail?.[0]?.msg || "Invalid email or password");
  }

  return response.json();
}

/**
 * Request a password reset link via email.
 */
export async function forgotPassword(data: ForgotPasswordRequest): Promise<string> {
  const response = await fetch(`${API_URL}/auth/forgot-password`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorBody = await response.json();
    throw new Error(errorBody.detail?.[0]?.msg || "Could not process request");
  }

  return response.json();
}

/**
 * Reset password using a valid token.
 */
export async function resetPassword(data: ResetPasswordRequest): Promise<string> {
  const response = await fetch(`${API_URL}/auth/reset-password`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorBody = await response.json();
    throw new Error(errorBody.detail?.[0]?.msg || "Reset failed. Token may be expired.");
  }

  return response.json();
}