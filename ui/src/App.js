import React, { useState } from "react";
import Navbar from "./components/utilities/navbar/Navbar";
import Login from "./components/utilities/login/Login";

import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";

function App() {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const openModal = () => setIsModalOpen(true);
  const closeModal = () => setIsModalOpen(false);

  return (
    <div className="App">
      <Navbar onLoginClick={openModal} />
      <Login isOpen={isModalOpen} closeDialog={closeModal} />
    </div>
  );
}

export default App;
