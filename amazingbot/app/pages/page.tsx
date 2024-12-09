import Link from "next/link";
import { FC } from "react";

import Image from 'next/image';

const Home: FC = () => {
  return (
    <div className="min-h-screen bg-gray-100">
      <div className="mx-auto md:flex justify-between md:items-center bg-white shadow-lg rounded-lg">
        {/* Texte principal */}
        <div className="md:w-1/2 p-6 pl-24  scroll-ml-6">
          <h1 className="text-4xl font-bold pb-5 text-gray-800 ">Amazing Bot</h1>
          <p className="text-gray-600 pb-6 mt-4">
            Gagnez du temps et concentrez-vous <br></br>sur la croissance de votre activité grâce à<br></br> notre chatbot intelligent.
          </p>
          <Link href="/inscrit"> {/* Modification du lien pour pointer vers /login */}
            <button className="mt-6 px-6 py-2 rounded-xl	 bg-gray-700 text-white  hover:bg-gray-900">
              START
            </button>
          </Link>
          
        </div>

        {/* Aperçu mobile */}
        <div className="w-1/2 rounded-l-3xl flex justify-center items-center min-h-screen bg-custom">
          <div className="md:w-1/2 p-6 flex justify-center">
            <div className="">
              {/* Ajoutez votre image ici */}
              <Image
                src="/phone.png" // Modifiez le chemin si nécessaire
                alt="Amazing Bot Chat Interface"
                width={375} // Largeur de l'image originale ou ajustée
                height={667} // Hauteur de l'image originale ou ajustée
                className="rounded-xl"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
