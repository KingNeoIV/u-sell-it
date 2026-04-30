/**
 * @fileoverview Authentication Context Provider.
 * Manages global user state, token persistence, and session lifecycle.
 */

import { createContext, useContext, useEffect, useState } from "react";
import type { ReactNode } from "react";
import type { User } from "../api/auth";

/**
 * Shape of the authentication state and available actions.
 */
interface AuthContextType {
  /** The currently authenticated user's profile data. */
  user: User | null;
  /** JWT access token for authorizing API requests. */
  access_token: string | null;
  /** Token used to obtain new access tokens when they expire. */
  refresh_token: string | null;
  /** Derived helper to quickly check if a session exists. */
  isAuthenticated: boolean;
  /** True while the provider is hydrating state from storage. */
  loading: boolean;
  /** Updates state and persistence layer with new credentials. */
  login: (access_token: string, refresh_token: string, user: User) => void;
  /** Clears session state and removes persisted credentials. */
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

/**
 * Provider component that wraps the app to provide authentication state.
 * Handles "hydration" (loading saved session from localStorage) on mount.
 */
export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [refreshToken, setRefreshToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  /**
   * Session Hydration Effect:
   * On initial mount, attempt to restore the session from localStorage.
   */
  useEffect(() => {
    const storedAccess = localStorage.getItem("access_token");
    const storedRefresh = localStorage.getItem("refresh_token");
    const storedUser = localStorage.getItem("user");

    if (storedAccess && storedRefresh && storedUser) {
      try {
        const parsedUser = JSON.parse(storedUser);
        setAccessToken(storedAccess);
        setRefreshToken(storedRefresh);
        setUser(parsedUser);
      } catch (error) {
        console.error("Failed to hydrate auth session:", error);
        // Clean up malformed data to prevent crash loops
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        localStorage.removeItem("user");
      }
    }
    setLoading(false);
  }, []);

  /**
   * Sets the application's auth state and persists credentials.
   * @param access_token - The new JWT access token.
   * @param refresh_token - The new JWT refresh token.
   * @param userData - The user profile object from the API.
   */
  const login = (access_token: string, refresh_token: string, userData: User) => {
    // 1. Update React State
    setAccessToken(access_token);
    setRefreshToken(refresh_token);
    setUser(userData);

    // 2. Update Persistence (Note: Consider HttpOnly cookies for higher security)
    localStorage.setItem("access_token", access_token);
    localStorage.setItem("refresh_token", refresh_token);
    localStorage.setItem("user", JSON.stringify(userData));
  };

  /**
   * Ends the user session and wipes all locally stored credentials.
   */
  const logout = () => {
    setAccessToken(null);
    setRefreshToken(null);
    setUser(null);
    localStorage.clear();
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        access_token: accessToken,
        refresh_token: refreshToken,
        isAuthenticated: !!accessToken,
        loading,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

/**
 * Custom hook to access authentication state.
 * @throws {Error} If used outside of an AuthProvider.
 * @returns The current AuthContextType.
 */
export const useAuthContext = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuthContext must be used inside an AuthProvider");
  }
  return ctx;
};