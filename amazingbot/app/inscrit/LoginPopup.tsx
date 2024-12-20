"use client"; // Assurez-vous d'ajouter cette ligne en haut de votre fichier.
import Link from "next/link";
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function LoginPopup({ onClose }) {
  const [credentials, setCredentials] = useState({ username: "", password: "" });
  const [response, setResponse] = useState("");
  const router = useRouter(); // Utiliser le routeur de Next.js

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch("http://localhost:8000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams(credentials),
      });
      const data = await res.json();
      if (res.ok) {
        localStorage.setItem("token", data.access_token); // Stocker le token
        setResponse("Connexion réussie !");
        router.push("/chat"); // Rediriger vers la page chat
      } else {
        setResponse(data.detail || "Erreur de connexion");
      }
    } catch (error) {
      console.error(error);
      setResponse("Erreur de connexion au backend");
    }
  };

  return (
    <div className="fixed inset-0 flex items-center  justify-center bg-black bg-opacity-50 z-50">
      {/* Popup container */}
      <div className="bg-white w-full max-w-md p-6 rounded-s-3xl	 shadow-lg">
        <button
          onClick={onClose}
          className="text-gray-400 hover:text-gray-600 float-right text-xl"
        >
          &times; {/* Bouton de fermeture */}
        </button>
        <h1 className="text-2xl font-bold text-gray-800 text-center mt-2">
          Connexion
        </h1>
        <p className="text-gray-600 text-center mt-2 mb-6">
          Veuillez entrer vos informations pour continuer.
        </p>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <input
              type="text"
              placeholder="Email"
              value={credentials.username}
              onChange={(e) =>
                setCredentials({ ...credentials, username: e.target.value })
              }
              className="w-full text-black px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-gray-700"
            />
          </div>
          <div>
            <input
              type="password"
              placeholder="Mot de passe"
              value={credentials.password}
              onChange={(e) =>
                setCredentials({ ...credentials, password: e.target.value })
              }
              className="w-full text-black px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-gray-700"
            />
          </div>
          <button
            type="submit"
            className="w-full bg-gray-700 text-white py-2 rounded-md hover:bg-gray-900 transition"
          >
            Se connecter
          </button>
        </form>
        <Link href="/inscrit">
          <button className="w-full mt-4 bg-gray-700 text-white py-2 rounded-md hover:bg-gray-900 transition">
            S'inscrire
          </button>
        </Link>
        <p className="mt-4 text-sm text-gray-600">{response}</p>
      </div>
    </div>
  );
}
