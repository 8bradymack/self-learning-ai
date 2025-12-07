"""
Web Learning Module
Learns from websites, Wikipedia, arXiv, etc.
"""

import requests
from bs4 import BeautifulSoup
import logging
from typing import List, Dict
import time
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebLearner:
    """Learns from web content"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })

    def learn_from_wikipedia(self, topics: List[str]) -> List[Dict[str, str]]:
        """Extract knowledge from Wikipedia articles"""
        knowledge_items = []

        for topic in topics:
            try:
                # Get Wikipedia article
                url = f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}"
                response = self.session.get(url, timeout=10)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Get first paragraph (usually the summary)
                    paragraphs = soup.find_all('p')
                    content = []

                    for p in paragraphs[:5]:  # Get first 5 paragraphs
                        text = p.get_text().strip()
                        if len(text) > 100:  # Only substantial paragraphs
                            content.append(text)

                    if content:
                        knowledge_items.append({
                            'question': f"What is {topic}?",
                            'answer': ' '.join(content[:2]),  # First 2 paragraphs
                            'source': f'wikipedia_{topic}'
                        })
                        logger.info(f"✓ Learned from Wikipedia: {topic}")

                time.sleep(0.5)  # Be nice to Wikipedia

            except Exception as e:
                logger.error(f"Error learning from Wikipedia ({topic}): {e}")

        return knowledge_items

    def learn_from_simple_wikipedia(self, topics: List[str]) -> List[Dict[str, str]]:
        """Extract knowledge from Simple English Wikipedia (easier to understand)"""
        knowledge_items = []

        for topic in topics:
            try:
                url = f"https://simple.wikipedia.org/wiki/{topic.replace(' ', '_')}"
                response = self.session.get(url, timeout=10)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    paragraphs = soup.find_all('p')
                    content = []

                    for p in paragraphs[:3]:
                        text = p.get_text().strip()
                        if len(text) > 50:
                            content.append(text)

                    if content:
                        knowledge_items.append({
                            'question': f"Explain {topic} simply",
                            'answer': ' '.join(content),
                            'source': f'simple_wikipedia_{topic}'
                        })
                        logger.info(f"✓ Learned from Simple Wikipedia: {topic}")

                time.sleep(0.5)

            except Exception as e:
                logger.error(f"Error with Simple Wikipedia ({topic}): {e}")

        return knowledge_items

    def generate_topic_list(self) -> List[str]:
        """Generate comprehensive list of topics to learn"""
        topics = [
            # Computer Science
            "Algorithm", "Data_structure", "Machine_learning", "Artificial_intelligence",
            "Neural_network", "Deep_learning", "Natural_language_processing",
            "Computer_vision", "Reinforcement_learning", "Supervised_learning",

            # Mathematics
            "Calculus", "Linear_algebra", "Probability", "Statistics",
            "Differential_equation", "Matrix_(mathematics)", "Vector_space",
            "Optimization_(mathematics)", "Graph_theory", "Number_theory",

            # Physics
            "Quantum_mechanics", "Classical_mechanics", "Thermodynamics",
            "Electromagnetism", "Relativity", "Optics", "Waves",

            # Philosophy & Logic
            "Logic", "Epistemology", "Ethics", "Metaphysics", "Philosophy_of_mind",
            "Critical_thinking", "Reasoning", "Formal_logic",

            # General Knowledge
            "Scientific_method", "Research", "Analysis", "Synthesis",
            "Problem_solving", "Creative_thinking", "Systems_thinking",

            # Technology
            "Programming", "Software_engineering", "Database", "Cloud_computing",
            "Distributed_computing", "Operating_system", "Compiler",
        ]
        return topics

    def rapid_learning_session(self, n_topics: int = 20) -> List[Dict[str, str]]:
        """Rapid learning from multiple topics"""
        all_topics = self.generate_topic_list()

        # Select random topics
        import random
        selected_topics = random.sample(all_topics, min(n_topics, len(all_topics)))

        logger.info(f"\n🌐 Starting web learning session ({n_topics} topics)...")

        knowledge = []

        # Learn from regular Wikipedia
        knowledge.extend(self.learn_from_wikipedia(selected_topics[:n_topics//2]))

        # Learn from Simple Wikipedia
        knowledge.extend(self.learn_from_simple_wikipedia(selected_topics[n_topics//2:]))

        logger.info(f"✓ Web learning complete: {len(knowledge)} items learned")

        return knowledge


if __name__ == "__main__":
    learner = WebLearner()
    knowledge = learner.rapid_learning_session(n_topics=10)

    for item in knowledge[:3]:
        print(f"\nQ: {item['question']}")
        print(f"A: {item['answer'][:200]}...")
