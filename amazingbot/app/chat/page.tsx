"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import * as React from "react";
import { Send, Plus } from "lucide-react";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export default function ChatPage() {
  const [user, setUser] = useState(null);
  const [messages, setMessages] = React.useState([
    { id: 1, text: "Hi, how can I help you today?", isUser: false },
    { id: 2, text: "Hey, I'm having trouble with my account.", isUser: true },
    { id: 3, text: "What seems to be the problem?", isUser: false },
    { id: 4, text: "I can't log in.", isUser: true },
  ]);
  const [newMessage, setNewMessage] = React.useState("");
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      // Rediriger vers la page de login si le token est absent
      router.push("/login");
    } else {
      // Vérifier le token avec le backend
      const checkToken = async () => {
        const res = await fetch("http://localhost:8000/protected", {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        if (res.ok) {
          const data = await res.json();
          setUser(data); // Définir l'utilisateur si le token est valide
        } else {
          router.push("/login"); // Rediriger en cas d'échec
        }
      };
      checkToken();
    }
  }, [router]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (newMessage.trim()) {
      setMessages([...messages, { id: messages.length + 1, text: newMessage, isUser: true }]);
      setNewMessage("");
    }
  };

  if (!user) {
    return <p>Chargement...</p>; // Afficher un message de chargement
  }

  return (
    <div className="flex h-screen bg-black text-white">
      {/* Sidebar */}
      <div className="w-1/4  bg-gray-800 p-4">
        <h2 className="text-lg font-semibold text-gray-200">Historique des discussions</h2>
        <div className="mt-4 space-y-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`p-2 rounded-md cursor-pointer ${
                message.isUser ? "bg-blue-600" : "bg-gray-700"
              }`}
            >
              <p className="text-sm text-gray-200">{message.text}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="flex  items-center justify-between p-4 border-b border-gray-800">
          <div className="flex items-center gap-3">
            <Avatar className="h-10 w-10">
              <AvatarImage src="/placeholder.svg" />
              <AvatarFallback>{user.name?.[0]?.toUpperCase()}</AvatarFallback>
            </Avatar>
            <div>
              <h2 className="text-sm font-semibold">{user.name}</h2>
              <p className="text-sm text-gray-400">{user.email}</p>
            </div>
          </div>
          <Button size="icon" variant="ghost" className="rounded-full">
            <Plus className="h-6 w-6" />
          </Button>
        </div>

        {/* Chat Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.isUser ? "justify-end" : "justify-start"}`}
            >
              <div
                className={`max-w-[80%] rounded-lg px-4 py-2 ${
                  message.isUser ? "bg-white text-black" : "bg-gray-800 text-white"
                }`}
              >
                <p className="text-sm">{message.text}</p>
              </div>
            </div>
          ))}
        </div>

        {/* Message Input */}
        <form onSubmit={handleSubmit} className="p-4 border-t border-gray-800">
          <div className="flex gap-2">
            <Input
              type="text"
              placeholder="Type your message..."
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              className="flex-1 bg-gray-800 border-0 focus-visible:ring-0 text-white placeholder:text-gray-400"
            />
            <Button type="submit" size="icon" className="rounded-lg bg-gray-700 hover:bg-gray-600">
              <Send className="h-4 w-4" />
              <span className="sr-only">Send message</span>
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
