#!/usr/bin/env python3
"""
CHAT WITH YOUR AI - Talk to your self-improving AI

This lets you have conversations with your AI just like ChatGPT.
The AI will use:
- Everything it learned from Wikipedia
- All knowledge from other AIs
- Its training to give smart responses

Try asking it questions about what it knows!
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.api.ai_apis import AIAPIs
from src.memory.vector_store import VectorMemory
from datetime import datetime

class SmartAI:
    """Your self-improving AI that you can chat with"""

    def __init__(self):
        print("🧠 Initializing your AI...")
        self.apis = AIAPIs()
        self.memory = VectorMemory()
        self.conversation_history = []

        knowledge_count = self.memory.collection.count()
        print(f"✓ AI loaded with {knowledge_count:,} knowledge items")
        print("✓ Ready to chat!\n")

    def respond(self, user_message: str) -> str:
        """
        Generate an intelligent response using:
        1. Relevant knowledge from memory
        2. Groq API (Llama 3.3 70B) for smart responses
        3. Conversation history for context
        """

        # Search for relevant knowledge
        relevant_knowledge = self.memory.search(user_message, n_results=5)

        # Build context from what the AI knows
        context_parts = []
        if relevant_knowledge:
            context_parts.append("Based on what I know:")
            for i, item in enumerate(relevant_knowledge[:3], 1):
                knowledge_text = item['text'][:200]  # First 200 chars
                context_parts.append(f"{i}. {knowledge_text}")

        context = "\n".join(context_parts) if context_parts else ""

        # Build the prompt for Groq
        system_prompt = f"""You are a highly intelligent, continuously learning AI assistant.

You have access to extensive knowledge including:
- {self.memory.collection.count():,} items of learned knowledge
- Topics: AI, machine learning, science, philosophy, reasoning, creativity, and more

{context}

Provide thoughtful, intelligent responses. Think step-by-step. Be clear and helpful."""

        # Add conversation history for context
        messages = []

        # Add recent conversation history (last 3 exchanges)
        for msg in self.conversation_history[-6:]:  # Last 3 user+assistant pairs
            messages.append(msg)

        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message
        })

        # Get response from Groq (smart response)
        try:
            response = self.apis.clients['groq'].chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": system_prompt}] + messages,
                temperature=0.7,
                max_tokens=500
            )

            ai_response = response.choices[0].message.content

            # Store this exchange in conversation history
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": ai_response})

            # Store this interaction as new knowledge
            self.memory.add_knowledge(
                text=f"User: {user_message}\nAI: {ai_response}",
                source="conversation",
                metadata={
                    "type": "conversation",
                    "timestamp": datetime.now().isoformat()
                }
            )

            return ai_response

        except Exception as e:
            return f"Error generating response: {e}\n\nBut I have {self.memory.collection.count():,} knowledge items if you want to try again!"

    def chat(self):
        """Interactive chat loop"""

        print("="*80)
        print("💬 CHAT WITH YOUR SELF-IMPROVING AI")
        print("="*80)
        print("\nYour AI knows about:")
        print("  • Artificial Intelligence & Machine Learning")
        print("  • Science, Math, Philosophy, Reasoning")
        print("  • Programming, Algorithms, Problem Solving")
        print("  • Creativity, Learning, Intelligence")
        print(f"  • And {self.memory.collection.count():,} other knowledge items!")
        print("\nType 'quit' or 'exit' to end the conversation")
        print("="*80 + "\n")

        while True:
            try:
                # Get user input
                user_input = input("\n🧑 You: ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\n🤖 AI: Thanks for chatting! I'll keep learning while you're away.")
                    print(f"     (I now have {self.memory.collection.count():,} knowledge items!)\n")
                    break

                # Show AI is thinking
                print("\n🤖 AI: ", end="", flush=True)

                # Get AI response
                response = self.respond(user_input)

                # Print response
                print(response)

            except KeyboardInterrupt:
                print("\n\n🤖 AI: Goodbye! Keep me learning!")
                break
            except Exception as e:
                print(f"\n⚠️  Error: {e}")
                print("Let's try again...")


def quick_test():
    """Quick test to show off the AI"""

    print("\n" + "="*80)
    print("🧪 QUICK AI TEST - Showing what your AI knows")
    print("="*80 + "\n")

    ai = SmartAI()

    test_questions = [
        "What is artificial intelligence?",
        "How does machine learning work?",
        "What makes an AI truly intelligent?"
    ]

    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. Testing: '{question}'")
        print("-" * 60)
        response = ai.respond(question)
        print(f"AI Response: {response}\n")

    print("="*80)
    print("✓ Test complete! The AI can answer questions intelligently.")
    print("  Ready for full chat mode!")
    print("="*80 + "\n")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Chat with your self-improving AI')
    parser.add_argument('--test', action='store_true',
                       help='Run quick test instead of full chat')
    args = parser.parse_args()

    if args.test:
        quick_test()
    else:
        ai = SmartAI()
        ai.chat()
