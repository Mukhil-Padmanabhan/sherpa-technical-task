import { useState } from "react"
import axios from "axios"
import { Link } from "react-router-dom"

function Login() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState("")
  const API_URL = import.meta.env.VITE_API_URL;


  const handleLogin = async () => {
    setLoading(true)
    setMessage("")
    try {
      const res = await axios.post(`${API_URL}/api/auth/login`, {
        email,
        password,
      })
      localStorage.setItem("token", res?.data?.access_token)
      window.location.href = "/search";
    } catch (err) {
      setMessage(err.response?.data?.detail || "Login failed")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-r from-sky-100 to-black-100 flex items-center justify-center px-4">
      <div className="bg-white p-8 md:p-10 rounded-lg shadow-xl w-full max-w-md">
        <h2 className="text-3xl font-bold text-center text-black mb-6">
          Welcome Back
        </h2>

        <div className="space-y-5">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1 text-left">Email</label>
            <input
              type="email"
              placeholder="Enter your email"
              className="w-full px-4 py-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 text-black"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1 text-left">Password</label>
            <input
              type="password"
              placeholder="Enter your password"
              className="w-full px-4 py-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 text-black"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <button
            onClick={handleLogin}
            disabled={loading}
            className={`w-full text-white py-2 rounded transition-all duration-200 ${loading ? "bg-gray-400 cursor-not-allowed" : "bg-blue-600 hover:bg-blue-700"
              }`}
          >
            {loading ? "Logging in..." : "Login"}
          </button>

          {message && (
            <p className="mt-4 text-center text-sm font-medium text-gray-700">
              {message}
            </p>
          )}

          <p className="text-center text-sm mt-4 text-right">
            Don't have an account?{" "}
            <Link to="/register" className="text-blue-600 hover:underline">
              {'Register here >>'}
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}

export default Login
