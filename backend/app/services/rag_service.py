import chromadb
import os
import requests
import json

class CareerRAGService:
    def __init__(self):
        # Initialize the local vector database
        self.chroma_client = chromadb.Client()
        self.collection = self.chroma_client.get_or_create_collection(name="career_roadmaps")
        self.ollama_url = "http://localhost:11434/api/generate"

    def get_context_for_goal(self, career_goal: str):
        # Query ChromaDB for roadmaps matching the student's goal
        results = self.collection.query(
            query_texts=[career_goal],
            n_results=2
        )
        return results['documents'][0] if results['documents'] else ["No specific context found."]

    def generate_student_quest(self, student_profile: dict, career_goal: str):
        # 1. Retrieve verified industry data
        context = self.get_context_for_goal(career_goal)
        
        # 2. Build the prompt
        prompt = f"""
        You are a career tutor. The student's current profile is: {student_profile}. 
        Their goal is: {career_goal}.
        Using this verified industry framework: {context}, 
        generate ONE highly actionable, gamified task (a 'Quest') for them to complete today.
        Include a title, description, and XP reward (10-50).
        """

        # 3. Stream to local Ollama LLM (e.g., Llama 3 or Mistral)
        payload = {
            "model": "llama3", # Ensure you have pulled this model in Ollama
            "prompt": prompt,
            "stream": False
        }
        
        response = requests.post(self.ollama_url, json=payload)
        return response.json().get("response")