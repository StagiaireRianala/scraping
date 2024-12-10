"use client"; // Indique que ce composant est côté client
import { useState } from "react";
import { useRouter } from "next/navigation"; // Importer le routeur de Next.js
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
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
import login from "./LoginPopup"; // Importez le composant LoginPopup

export default function AuthTabs() {
  const [formData, setFormData] = useState({ name: "", email: "", mdp: "" });
  const [response, setResponse] = useState("");
  const [showLoginPopup, setShowLoginPopup] = useState(false); // État pour gérer la popup
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
          setShowLoginPopup(true); // Afficher la popup après succès
        }, 1000);
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
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-r from-custom-black to-custom-purple">
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
              {/* Vous pouvez laisser le formulaire de connexion ici si nécessaire */}
              <p>Connectez-vous ici !</p>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Afficher la popup de connexion */}
      {showLoginPopup && <LoginPopup onClose={() => setShowLoginPopup(false)} />}
    </div>
  );
}
