/**
 * @fileoverview Authentication API client for FastAPI backend integration.
 * Handles user registration, session management, and password recovery.
 */

// --- 1. Interfaces (Data Models) ---

/** Core user profile information. */
export interface User {
  id: string;
  email: string;
}

/** User data returned from read operations, including status flags. */
export interface UserRead {
  email: string;
  id: string;
  is_active: boolean;
}

/** Schema for creating a new user account. */
export interface UserCreate {
  email: string;
  password: string;
}

/** Credentials required for authentication. */
export interface LoginRequest {
  email: string;
  password: string;
}

/** Server response containing JWT credentials and user profile. */
export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: User;
}

/** Request payload for password recovery. */
export interface ForgotPasswordRequest {
  email: string;
}

/** Response containing the generated reset token and expiration metadata. */
export interface ForgotPasswordResponse {
  message: string;
  token: string;
  expires_at: string;
}

/** Payload for setting a new password via recovery token. */
export interface ResetPasswordRequest {
  token: string;
  new_password: string;
}

/** Confirmation message after a successful password reset. */
export interface ResetPasswordResponse {
  message: string;
}

// --- 2. Configuration ---

/** Base URL for API requests, defaulting to local development if env is not set. */
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

// --- 3. API Action Functions ---

/**
 * Registers a new user with the backend.
 * @param data - The user's registration details (email and password).
 * @returns A promise resolving to the created user's public profile.
 * @throws {Error} If registration fails or validation errors occur.
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
 * Authenticates a user and retrieves access tokens.
 * @param data - Login credentials.
 * @returns A promise resolving to the access token and user object.
 * @throws {Error} On invalid credentials or server errors.
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
 * Initiates the password recovery process.
 * @param data - The email address associated with the account.
 * @returns A promise resolving to the server's confirmation and token details.
 */
export async function forgotPassword(data: ForgotPasswordRequest): Promise<ForgotPasswordResponse> {
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
 * Resets a user's password using a verification token.
 * @param data - The new password and the token received via email.
 * @returns A promise resolving to a success message.
 * @throws {Error} If the token is invalid or expired.
 */
export async function resetPassword(data: ResetPasswordRequest): Promise<ResetPasswordResponse> {
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