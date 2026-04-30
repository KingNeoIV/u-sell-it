/**
 * @fileoverview Main Application Router.
 * Configures the client-side routing tree, separating public authentication
 * views from protected application management views using nested layouts.
 */

import { BrowserRouter, Routes, Route, Navigate, Outlet } from "react-router-dom";
import ProtectedRoute from "../components/ProtectedRoute";
import Layout from "../components/Layout";

// Page Imports
import Login from "../pages/Login";
import Register from "../pages/Register";
import ForgotPassword from "../pages/ForgotPassWord";
import ResetPassword from "../pages/ResetPassword";
import Dashboard from "../pages/Dashboard";
import Profile from "../pages/Profile";
import MyListings from "../pages/MyListings";
import CreateListing from "../pages/CreateListing";

/**
 * AppRouter Component.
 * * Architecture:
 * 1. Public Routes: Accessible to everyone (Auth flow).
 * 2. Protected Wrapper: A nested route structure that enforces authentication 
 * and applies a consistent UI Layout to all internal pages.
 * 3. Catch-all: Redirects unknown paths to the login page.
 */
export default function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        {/* --- PUBLIC ROUTES --- */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/reset-password" element={<ResetPassword />} />

        {/* --- PROTECTED ROUTES (NESTED) --- */}
        {/* Standard Pattern: Use a single Route to wrap all protected children.
          This ensures you only define the logic for ProtectedRoute and Layout once.
        */}
        <Route
          element={
            <ProtectedRoute>
              <Layout>
                <Outlet />
              </Layout>
            </ProtectedRoute>
          }
        >
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/listings" element={<MyListings />} />
          <Route path="/listings/create" element={<CreateListing />} />
        </Route>

        {/* --- FALLBACK --- */}
        {/* Industry standard: Use Navigate for redirects rather than just rendering the component */}
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </BrowserRouter>
  );
}