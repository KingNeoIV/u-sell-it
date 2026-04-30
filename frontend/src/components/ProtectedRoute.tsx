/**
 * @fileoverview High-order component for route protection.
 * Prevents unauthorized users from accessing private application routes.
 */

import { Navigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

/**
 * Props for the ProtectedRoute component.
 * @property children - The component(s) to render if the user is authenticated.
 */
interface ProtectedRouteProps {
  children: React.ReactNode;
}

/**
 * A wrapper component that enforces authentication.
 * * Logic Flow:
 * 1. Checks `loading` state to prevent premature redirection during auth initialization.
 * 2. If authenticated, renders the protected `children`.
 * 3. If unauthenticated, redirects the user to the login page using a "replace" navigation
 * to prevent the login page from cluttering the browser history.
 * * @example
 * <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
 */
export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { isAuthenticated, loading } = useAuth();

  /**
   * While the authentication status is being determined (e.g., verifying JWT in storage),
   * we return a loading state. In production, consider a global Spinner component.
   */
  if (loading) {
    return (
      <div style={styles.loaderContainer}>
        <span>Loading session...</span>
      </div>
    );
  }

  /**
   * Navigate to login if user is not authenticated.
   * 'replace' is used so the user can't go back to the protected page via the browser back button.
   */
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
}

/**
 * Basic internal styles for the loading state.
 * Standard practice is to keep loaders centered and unobtrusive.
 */
const styles = {
  loaderContainer: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    height: "100vh",
    width: "100%",
    fontFamily: "sans-serif",
    color: "#666",
  },
} as const;