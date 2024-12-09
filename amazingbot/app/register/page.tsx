"use client"; // Indique que ce composant est côté client
import { useState } from "react";
import { useRouter } from "next/navigation"; // Importer le routeur de Next.js
import Image from "next/image"; // Importer le composant Image de Next.js

export default function Register() {
  const [formData, setFormData] = useState({ name: "", email: "", mdp: "" });
  const [response, setResponse] = useState("");
  const router = useRouter(); // Initialiser le routeur

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch("http://localhost:8000/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const data = await res.json();
      if (res.ok) {
        setResponse("Inscription réussie !");
        setTimeout(() => {
          router.push("/login"); // Rediriger vers la page de login après succès
        }, 2000); // Attendre 2 secondes pour afficher le message
      } else {
        if (data.detail && Array.isArray(data.detail)) {
          const errorMessages = data.detail.map((err) => err.msg).join(", ");
          setResponse(errorMessages);
        } else {
          setResponse(data.detail || "Erreur lors de l'inscription");
        }
      }
    } catch (error) {
      console.error(error);
      setResponse("Erreur de connexion au backend");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="flex flex-col md:flex-row items-center bg-white shadow-lg rounded-lg overflow-hidden">
        {/* Section de gauche : formulaire */}
        <div className="md:w-1/2 p-8">
          <h1 className="text-3xl font-bold text-center  text-gray-800 mb-6">Inscription</h1>
          <form onSubmit={handleSubmit} className="space-y-4">
            <input 
              type="text"
              placeholder="Nom"
              value={formData.name}
              onChange={(e) =>
                setFormData({ ...formData, name: e.target.value })
              }
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-black"
            />
            <input
              type="email"
              placeholder="Email"
              value={formData.email}
              onChange={(e) =>
                setFormData({ ...formData, email: e.target.value })
              }
              className="w-full text-black px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <input
              type="password"
              placeholder="Mot de passe"
              value={formData.mdp}
              onChange={(e) =>
                setFormData({ ...formData, mdp: e.target.value })
              }
              className="w-full text-black px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              type="submit"
              className="w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-700 transition duration-300"
            >
              S'inscrire
            </button>
          </form>
          <p className="text-red-500 mt-4">{response}</p>
        </div>

        {/* Section de droite : image */}
        <div className="md:w-1/2 bg-custom flex items-center justify-center">
          <Image
            src="/phone.png" // Remplacez par le chemin de votre image
            alt="Illustration de l'inscription"
            width={300}
            height={300}
            className="rounded-lg"
          />
        </div>
      </div>
    </div>
  );
}
