import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Home from "./pages/Home";
import PieDetails from "./pages/PieDetails";
import AppSidebar from "./components/layout/AppSideBar";
import { ThemeProvider } from "flowbite-react";

function App() {
  return (
    <ThemeProvider>
      <Router>
        <div className="grid grid-cols-[1fr_5fr] min-h-screen bg-black text-white">
          <AppSidebar />
          <main className="p-6">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/pi/:piId" element={<PieDetails />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </main>
        </div>
      </Router>
    </ThemeProvider>
  );
}

export default App;
