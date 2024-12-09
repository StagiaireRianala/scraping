"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { GoogleLogin, CredentialResponse } from "@react-oauth/google";
import AppleSignin from "react-apple-signin-auth";
import Image from "next/image";

export default function Login() {
  const [formData, setFormData] = useState({ email: "", password: "" });
  const [responseMessage, setResponseMessage] = useState("");
  const router = useRouter();

  // Gestion de la connexion Google
  const handleGoogleSuccess = (credentialResponse: CredentialResponse) => {
    console.log("Google Credential:", credentialResponse);

    fetch("http://localhost:8000/auth/google", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ token: credentialResponse.credential }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          setResponseMessage("Connexion réussie avec Google !");
          router.push("/dashboard"); // Redirection après succès
        } else {
          setResponseMessage("Erreur lors de la connexion Google.");
        }
      })
      .catch(() => setResponseMessage("Erreur de connexion au backend."));
  };

  const handleGoogleError = () => {
    console.error("Erreur lors de la connexion Google");
    setResponseMessage("Erreur lors de la connexion avec Google.");
  };

  // Gestion de la connexion Apple
  const handleAppleSuccess = (response: any) => {
    console.log("Apple Response:", response);

    fetch("http://localhost:8000/auth/apple", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(response),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          setResponseMessage("Connexion réussie avec Apple !");
          router.push("/dashboard");
        } else {
          setResponseMessage("Erreur lors de la connexion Apple.");
        }
      })
      .catch(() => setResponseMessage("Erreur de connexion au backend."));
  };

  const handleAppleError = (error: any) => {
    console.error("Erreur lors de la connexion Apple:", error);
    setResponseMessage("Erreur lors de la connexion avec Apple.");
  };

  // Gestion du formulaire classique
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch("http://localhost:8000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const data = await res.json();
      if (res.ok) {
        setResponseMessage("Connexion réussie !");
        router.push("/dashboard");
      } else {
        setResponseMessage(data.message || "Erreur lors de la connexion.");
      }
    } catch (error) {
      console.error(error);
      setResponseMessage("Erreur de connexion au backend.");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="w-full max-w-md bg-white p-8 rounded shadow">
        <h1 className="text-2xl font-bold mb-4">Login</h1>

        {/* Formulaire classique */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="email"
            placeholder="Email"
            className="w-full px-4 py-2 border rounded"
            value={formData.email}
            onChange={(e) =>
              setFormData({ ...formData, email: e.target.value })
            }
          />
          <input
            type="password"
            placeholder="Mot de passe"
            className="w-full px-4 py-2 border rounded"
            value={formData.password}
            onChange={(e) =>
              setFormData({ ...formData, password: e.target.value })
            }
          />
          <button
            type="submit"
            className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600"
          >
            Connexion
          </button>
        </form>

        {/* Ouverture OAuth */}
        <div className="mt-6">
          <div className="flex items-center justify-between">
            <span className="border-b w-1/5 lg:w-1/4"></span>
            <span className="text-xs text-gray-500 uppercase">ou</span>
            <span className="border-b w-1/5 lg:w-1/4"></span>
          </div>

          <div className="mt-4 flex flex-col space-y-4">
            {/* Bouton Google */}
            <GoogleLogin
              onSuccess={handleGoogleSuccess}
              onError={handleGoogleError}
              render={(renderProps) => (
                <button
                  onClick={renderProps.onClick}
                  disabled={renderProps.disabled}
                  className="w-full flex items-center justify-center px-4 py-2 border rounded bg-white shadow-sm hover:bg-gray-100"
                >
                  <Image
                    src="/google-icon.svg"
                    alt="Google"
                    width={20}
                    height={20}
                    className="mr-2"
                  />
                  Connexion avec Google
                </button>
              )}
            />
            {/* Bouton Apple */}
            <AppleSignin
              clientId="com.example.app"
              redirectURI="http://localhost:8000/auth/apple/callback"
              scope="email name"
              onSuccess={handleAppleSuccess}
              onError={handleAppleError}
              render={(renderProps) => (
                <button
                  onClick={renderProps.onClick}
                  className="w-full flex items-center justify-center px-4 py-2 border rounded bg-black text-white shadow-sm hover:bg-gray-800"
                >
                  <Image
                    src="/apple-icon.svg"
                    alt="Apple"
                    width={20}
                    height={20}
                    className="mr-2"
                  />
                  Connexion avec Apple
                </button>
              )}
            />
          </div>
        </div>
        {/* Message de retour */}
        <p className="text-red-500 mt-4">{responseMessage}</p>
      </div>
    </div>
  );
}
