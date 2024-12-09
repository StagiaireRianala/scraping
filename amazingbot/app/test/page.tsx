"use client"; // Ajoutez cette ligne au début du fichier

import { useState } from "react";

export default function Home() {
  const [message, setMessage] = useState("");

  const testBackend = async () => {
    try {
      const response = await fetch("http://localhost:8000", {
        method: "GET",
      });
      const data = await response.json();
      setMessage(data.message);
    } catch (error) {
      console.error("Erreur:", error);
      setMessage("Erreur de connexion au backend");
    }
  };

  return (
    <div>
      <button onClick={testBackend}>Tester le Backend</button>
      <p>{message}</p>
    </div>
  );
}
