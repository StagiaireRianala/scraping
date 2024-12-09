"use client"; // Assurez-vous d'ajouter cette ligne en haut de votre fichier.
import Link from "next/link";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Image from "next/image";

export default function Login() {
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
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="w-full max-w-4xl flex bg-white shadow-lg rounded-lg overflow-hidden">
        {/* Section de gauche : formulaire */}
        <div className="w-full md:w-1/2 p-8">
          <h1 className="text-2xl text-center font-bold text-gray-800 mt-10 text-lg, md:text-2xl">Connexion</h1>
          <p className="text-gray-600 text-center mt-2  mb-6">Veuillez entrer vos informations pour continuer.</p>
          <form onSubmit={handleSubmit} className="space-y-4 mb-2 mt-10">
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
              className="w-full  bg-gray-700 text-white py-2 rounded-md hover:bg-gray-900 transition"
            >
              Se connecter
            </button>
          </form>
              
          <Link href="/register"> {/* Modification du lien pour pointer vers /login */}
            <button className="w-full  bg-gray-700 text-white py-2 rounded-md hover:bg-gray-900 transition">
              S'inscrire 
            </button>
          </Link>
          
            <p className="mt-4 text-sm text-gray-600">{response}</p>
        </div>

        {/* Section de droite : image */}
        <div className="hidden md:flex md:w-1/2 w-11 bg-custom items-center justify-center">
          <Image
            src="/phone.png" // Modifiez le chemin si nécessaire
            alt="Connexion à Amazing Bot"
            width={300}
            height={300}
            className="rounded-xl"
          />
        </div>
      </div>
    </div>
  );
}
