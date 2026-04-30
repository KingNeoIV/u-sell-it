/**
 * @fileoverview Custom hook for accessing authentication state and actions.
 * Acts as a proxy to the AuthContext, providing a clean API for components.
 */

import { useAuthContext } from "../context/AuthContext";

/**
 * Hook to interact with the global Authentication state.
 * * This hook provides access to:
 * - Current user profile
 * - Auth tokens (access and refresh)
 * - Authentication status (isAuthenticated)
 * - Session actions (login, logout)
 * * @returns {AuthContextType} The complete authentication context.
 * * @example
 * const { user, isAuthenticated, logout } = useAuth();
 * * if (!isAuthenticated) return <LoginButton />;
 * return <button onClick={logout}>Log out {user.email}</button>;
 */
export const useAuth = () => {
  const context = useAuthContext();

  // In industry-level apps, you might add computed properties here,
  // such as role-checking logic:
  // const isAdmin = context.user?.role === 'admin';

  return {
    ...context,
    // isAdmin,
  };
};