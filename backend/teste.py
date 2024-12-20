# -*- coding: utf-8 -*-

from app.pineconetest import search_pinecone

if __name__ == "__main__":
    test_query = "Comment devenir vendeur sur Amazon ?"
    response = search_pinecone(test_query)
    print("Réponse : ", response)
