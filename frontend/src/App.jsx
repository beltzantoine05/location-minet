import { BrowserRouter } from "react-router-dom"
import { Routes, Route } from "react-router-dom"
import Home from "./pages/Home"
import Login from "./pages/Login"
import Layout from "./components/layout/Layout"
import Mention from "./pages/Mention"
import Contact from "./pages/Contact"
import Dashboard from "./pages/Dashboard"
import { AuthProvider } from "./context/AuthContext"

const App = () => {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route element={<Layout />}>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/mentions" element={<Mention />} />
            <Route path="/contact" element={<Contact />} />
            <Route path="/dashboard" element={<Dashboard />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App


