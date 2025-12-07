#!/usr/bin/env python3
"""
MEGA LEARNING SCRIPT
Uses all available sources to learn as fast as possible:
- Groq API (with retry on rate limit)
- HuggingFace API
- Wikipedia scraping
- Simple Wikipedia scraping
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.memory.vector_store import VectorMemory
from src.api.ai_apis import AIAPIs
from src.learning.web_learner import WebLearner
import random
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_diverse_questions(n: int = 50) -> list:
    """Generate diverse questions across many domains"""
    topics = [
        "machine learning", "neural networks", "algorithms", "data structures",
        "quantum physics", "relativity", "thermodynamics", "electromagnetism",
        "calculus", "linear algebra", "probability", "statistics",
        "philosophy", "logic", "ethics", "epistemology",
        "biology", "chemistry", "astronomy", "geology",
        "psychology", "economics", "sociology", "history",
        "computer science", "software engineering", "databases", "operating systems",
        "cryptography", "cybersecurity", "networking", "distributed systems",
        "optimization", "game theory", "graph theory", "number theory",
        "linguistics", "semantics", "syntax", "pragmatics"
    ]

    question_templates = [
        "What are the fundamental principles of {}?",
        "Explain the key concepts in {}",
        "What are the most important ideas in {}?",
        "Describe the core theory of {}",
        "What are advanced concepts in {}?",
        "How does {} work?",
        "What are the applications of {}?",
        "What are the main challenges in {}?",
    ]

    questions = []
    selected_topics = random.sample(topics, min(n // 2, len(topics)))

    for topic in selected_topics:
        template = random.choice(question_templates)
        questions.append(template.format(topic))

    return questions


def learn_from_apis_with_retry(apis: AIAPIs, questions: list, memory: VectorMemory) -> int:
    """Learn from APIs with automatic retry and fallback"""
    learned = 0

    for question in questions:
        max_retries = 3
        retry_count = 0

        while retry_count < max_retries:
            try:
                result = apis.query_any(question)

                if result['response']:
                    memory.add_knowledge(
                        text=f"Q: {question}\nA: {result['response']}",
                        source=f"api_{result['source']}",
                        metadata={
                            "type": "qa_pair",
                            "question": question,
                            "api_source": result['source']
                        }
                    )
                    learned += 1
                    logger.info(f"✓ API learning ({result['source']}): {question[:50]}...")
                    break

            except Exception as e:
                retry_count += 1
                if "rate limit" in str(e).lower() or "429" in str(e):
                    wait_time = 10 * retry_count
                    logger.warning(f"Rate limit hit, waiting {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Error: {e}")
                    break

    return learned


def learn_from_web(web_learner: WebLearner, memory: VectorMemory, n_topics: int = 30) -> int:
    """Learn from web scraping"""
    knowledge_items = web_learner.rapid_learning_session(n_topics=n_topics)

    learned = 0
    for item in knowledge_items:
        try:
            memory.add_knowledge(
                text=f"Q: {item['question']}\nA: {item['answer']}",
                source=item['source'],
                metadata={
                    "type": "qa_pair",
                    "question": item['question'],
                    "web_source": item['source']
                }
            )
            learned += 1
        except Exception as e:
            logger.error(f"Error storing web knowledge: {e}")

    return learned


def mega_learning_session(n_iterations: int = 5):
    """
    Mega learning session using ALL available sources
    """
    print("\n" + "="*70)
    print("🚀 MEGA LEARNING SESSION")
    print("="*70)
    print("\nUsing ALL available sources:")
    print("  - Groq API (with retry)")
    print("  - HuggingFace API")
    print("  - Wikipedia scraping")
    print("  - Simple Wikipedia scraping")
    print("\n" + "="*70 + "\n")

    memory = VectorMemory()
    apis = AIAPIs()
    web_learner = WebLearner()

    total_learned = 0
    start_knowledge = memory.get_stats()['total_items']

    for i in range(n_iterations):
        print(f"\n{'='*70}")
        print(f"ITERATION {i+1}/{n_iterations}")
        print(f"{'='*70}\n")

        iteration_learned = 0

        # 1. Learn from APIs (10 questions)
        print("📡 Learning from AI APIs...")
        api_questions = generate_diverse_questions(n=10)
        api_learned = learn_from_apis_with_retry(apis, api_questions, memory)
        iteration_learned += api_learned
        print(f"  ✓ Learned {api_learned} items from APIs\n")

        # 2. Learn from web (20 topics)
        print("🌐 Learning from Wikipedia...")
        web_learned = learn_from_web(web_learner, memory, n_topics=20)
        iteration_learned += web_learned
        print(f"  ✓ Learned {web_learned} items from web\n")

        total_learned += iteration_learned

        # Show progress
        current_stats = memory.get_stats()
        print(f"📊 Session Progress:")
        print(f"  - This iteration: {iteration_learned} items")
        print(f"  - Total this session: {total_learned} items")
        print(f"  - Knowledge base: {current_stats['total_items']} items")
        print(f"  - Growth: +{current_stats['total_items'] - start_knowledge} items")

        # Small delay between iterations
        if i < n_iterations - 1:
            time.sleep(2)

    print("\n" + "="*70)
    print("✅ MEGA LEARNING SESSION COMPLETE!")
    print("="*70)
    print(f"\nTotal learned: {total_learned} items")
    print(f"Final knowledge base: {memory.get_stats()['total_items']} items")
    print("\nYour AI is now significantly smarter!")
    print("="*70 + "\n")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Mega learning session')
    parser.add_argument('--iterations', type=int, default=5, help='Number of learning iterations')
    args = parser.parse_args()

    mega_learning_session(n_iterations=args.iterations)
