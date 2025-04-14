import React, { useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

const Register = () => {
  const [form, setForm] = useState({
    email: "",
    password: "",
    role: "user",
    tenant: "Bain",
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const API_URL = import.meta.env.VITE_API_URL;
  const handleChange = (e) => {
    const { name, value } = e.target;

    if (name === "role") {
      let autoTenant = form.tenant;

      if (value === "admin") autoTenant = "all";
      else if (value === "guest") autoTenant = "public";
      else autoTenant = "Bain";

      setForm((prev) => ({
        ...prev,
        role: value,
        tenant: autoTenant,
      }));
    } else {
      setForm({ ...form, [name]: value });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage("");

    try {
      const res = await axios.post(`${API_URL}/api/auth/register`, form);
      setMessage("✅ Registered successfully!");
    } catch (err) {
      setMessage("❌ Registration failed. Try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen w-full bg-gradient-to-r from-sky-100 to-black-100 flex items-center justify-center px-4 py-6">
      <div className="bg-white w-full max-w-xl p-8 md:p-12 rounded-lg shadow-xl">
        <h2 className="text-3xl font-bold text-center text-black mb-8">
          Create Your Account
        </h2>

        <form onSubmit={handleSubmit} className="space-y-6 text-left">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input
              type="email"
              name="email"
              className="w-full px-4 py-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 text-black"
              value={form.email}
              onChange={handleChange}
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
            <input
              type="password"
              name="password"
              className="w-full px-4 py-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 text-black"
              value={form.password}
              onChange={handleChange}
              required
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Role</label>
              <select
                name="role"
                className="w-full px-4 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-black"
                value={form.role}
                onChange={handleChange}
              >
                <option value="admin">Admin</option>
                <option value="user">User</option>
                <option value="guest">Guest</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Tenant</label>
              <select
                name="tenant"
                className="w-full px-4 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-black"
                value={form.tenant}
                onChange={handleChange}
                disabled={form.role === "admin" || form.role === "guest"}
              >
                {form.role === "admin" && (
                  <option value="all">All (Admin only)</option>
                )}
                {form.role === "guest" && (
                  <option value="public">Public</option>
                )}
                {form.role === "user" && (
                  <>
                    <option value="Bain">Bain</option>
                    <option value="BCG">BCG</option>
                    <option value="McK">McK</option>
                  </>
                )}
              </select>
            </div>
          </div>

          <button
            type="submit"
            className={`w-full py-3 text-white rounded-md text-lg font-medium transition-all ${
              loading
                ? "bg-gray-400 cursor-not-allowed"
                : "bg-blue-600 hover:bg-blue-700"
            }`}
            disabled={loading}
          >
            {loading ? "Registering..." : "Register"}
          </button>
        </form>

        <p className="text-center text-sm mt-4 text-right">
          <Link to="/" className="text-blue-600 hover:underline">
            {"Login >>"}
          </Link>
        </p>

        {message && (
          <p className="mt-6 text-center text-sm font-medium text-gray-700">{message}</p>
        )}
      </div>
    </div>
  );
};

export default Register;
