"use client"; // Indique que ce composant est côté client
import { useState } from "react";
import { useRouter } from "next/navigation"; // Importer le routeur de Next.js
import Image from "next/image"; // Importer le composant Image de Next.js
import Link from "next/link";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@/components/ui/tabs";

export default function AuthTabs() {
  const [formData, setFormData] = useState({ name: "", email: "", mdp: "" });
  const [response, setResponse] = useState("");
  const router = useRouter(); // Initialiser le routeur

  const handleRegisterSubmit = async (e) => {
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
        }, 2000);
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

  const [credentials, setCredentials] = useState({ username: "", password: "" });

  const handleLoginSubmit = async (e) => {
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
    <div className="min-h-screen  flex items-center justify-center bg-gradient-to-r from-custom-black to-custom-purple">
      <Tabs defaultValue="register" className="w-[400px]">
        {/* Onglets pour naviguer entre Inscription et Connexion */}
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="register">Inscription</TabsTrigger>
          <TabsTrigger value="login">Connexion</TabsTrigger>
        </TabsList>

        {/* Onglet Inscription */}
        <TabsContent value="register">
          <Card>
            <CardHeader>
              <CardTitle>Créer un compte</CardTitle>
              <CardDescription>Remplissez le formulaire ci-dessous.</CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleRegisterSubmit} className="space-y-4">
                <div className="space-y-1">
                  <Label htmlFor="name">Nom</Label>
                  <Input
                    id="name"
                    type="text"
                    placeholder="Votre nom"
                    value={formData.name}
                    onChange={(e) =>
                      setFormData({ ...formData, name: e.target.value })
                    }
                  />
                </div>
                <div className="space-y-1">
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email"
                    type="email"
                    placeholder="Votre email"
                    value={formData.email}
                    onChange={(e) =>
                      setFormData({ ...formData, email: e.target.value })
                    }
                  />
                </div>
                <div className="space-y-1">
                  <Label htmlFor="password">Mot de passe</Label>
                  <Input
                    id="password"
                    type="password"
                    placeholder="Votre mot de passe"
                    value={formData.mdp}
                    onChange={(e) =>
                      setFormData({ ...formData, mdp: e.target.value })
                    }
                  />
                </div>
                <div className="space-y-1">
                  <Label htmlFor="password">Confirmez le mot de passe</Label>
                  <Input
                    
                    type="password"
                    placeholder="Confirmez votre mot de passe"
                    value={formData.mdp}
                   
                  />
                </div>
                <Button type="submit" className="w-full">
                  S'inscrire
                </Button>
              </form>
              <p className="text-red-500 mt-4">{response}</p>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Onglet Connexion */}
        <TabsContent value="login">
          <Card>
            <CardHeader>
              <CardTitle>Connexion</CardTitle>
              <CardDescription>Connectez-vous à votre compte.</CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleLoginSubmit} className="space-y-4">
                <div>
                  <Label htmlFor="username">Email</Label>
                  <Input
                    id="username"
                    type="text"
                    placeholder="Email"
                    value={credentials.username}
                    onChange={(e) =>
                      setCredentials({
                        ...credentials,
                        username: e.target.value,
                      })
                    }
                  />
                </div>
                <div>
                  <Label htmlFor="password">Mot de passe</Label>
                  <Input
                    id="password"
                    type="password"
                    placeholder="Mot de passe"
                    value={credentials.password}
                    onChange={(e) =>
                      setCredentials({
                        ...credentials,
                        password: e.target.value,
                      })
                    }
                  />
                </div>
                <Button type="submit" className="w-full">
                  Se connecter
                </Button>
              </form>
              <Link href="/register" className="mt-4 block text-center">
                Vous n'avez pas de compte ? S'inscrire
              </Link>
              <p className="text-red-500 mt-4">{response}</p>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
