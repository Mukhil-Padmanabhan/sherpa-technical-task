import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/Login'
import Search from './pages/Search'
import Register from "./pages/Register";
import DocumentList from './pages/DocumentList';
import './App.css'

function App() {
  const isAuth = localStorage.getItem("token")
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/register" element={<Register />} />
        <Route path="/" element={<Login />} />
        <Route path="/search" element={isAuth ? <Search /> : <Navigate to="/" />} />
        <Route path="/documents" element={<DocumentList />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
