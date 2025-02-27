import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import Register from "./components/Register"
import Login from "./components/Login"
import Home  from "./components/Home"
import CreateApplication from "./components/CreateApplication"

function App() {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/home" element={<Home />} />
          <Route path="/create_application" element={<CreateApplication />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App

