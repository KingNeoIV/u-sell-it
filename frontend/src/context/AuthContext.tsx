import { createContext, useContext, useEffect, useState } from "react";
import type { ReactNode } from "react";
import type { User } from "../api/auth"; // Import the User interface we made in auth.ts

interface AuthContextType {
  user: User | null;
  access_token: string | null; // Changed to match API
  refresh_token: string | null; // Changed to match API
  isAuthenticated: boolean;
  loading: boolean;
  login: (access_token: string, refresh_token: string, user: User) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [refreshToken, setRefreshToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

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
      } catch {
        // If data is corrupt, wipe it
        localStorage.clear();
      }
    }
    setLoading(false);
  }, []);

  const login = (access_token: string, refresh_token: string, userData: User) => {
    setAccessToken(access_token);
    setRefreshToken(refresh_token);
    setUser(userData);

    localStorage.setItem("access_token", access_token);
    localStorage.setItem("refresh_token", refresh_token);
    localStorage.setItem("user", JSON.stringify(userData));
  };

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
        access_token: accessToken, // Map internal state to context name
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

export const useAuthContext = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuthContext must be used inside AuthProvider");
  return ctx;
};