"""
Vector Memory System
Long-term knowledge storage using ChromaDB
"""

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Optional
import yaml
import logging
from datetime import datetime
import uuid
from sklearn.feature_extraction.text import TfidfVectorizer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VectorMemory:
    """Manages long-term knowledge storage with vector embeddings"""

    def __init__(self, config_path: str = "configs/config.yaml"):
        self.config = self._load_config(config_path)
        self.embedding_model = None
        self.client = None
        self.collection = None
        self._initialize()

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration"""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def _initialize(self) -> None:
        """Initialize vector database and embedding model"""
        memory_config = self.config['memory']

        # Load embedding model
        logger.info(f"Loading embedding model: {memory_config['embedding_model']}")
        self.embedding_model = SentenceTransformer(memory_config['embedding_model'])

        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(
            path=memory_config['vector_db_path']
        )

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=memory_config['collection_name'],
            metadata={"description": "Learned knowledge from various sources"}
        )

        logger.info(f"Vector memory initialized. Current size: {self.collection.count()}")

    def add_knowledge(
        self,
        text: str,
        source: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Add new knowledge to memory"""

        # Generate unique ID
        doc_id = str(uuid.uuid4())

        # Prepare metadata
        doc_metadata = {
            "source": source,
            "timestamp": datetime.now().isoformat(),
            "learned": True
        }
        if metadata:
            doc_metadata.update(metadata)

        # Add to collection
        self.collection.add(
            documents=[text],
            ids=[doc_id],
            metadatas=[doc_metadata]
        )

        logger.info(f"Added knowledge from {source} (ID: {doc_id[:8]}...)")
        return doc_id

    def search(
        self,
        query: str,
        n_results: Optional[int] = None,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Search for relevant knowledge"""

        n_results = n_results or self.config['memory']['max_results']

        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=filter_metadata
        )

        # Format results
        formatted_results = []
        if results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                formatted_results.append({
                    'text': doc,
                    'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                    'distance': results['distances'][0][i] if results['distances'] else None,
                    'id': results['ids'][0][i] if results['ids'] else None
                })

        return formatted_results

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about stored knowledge"""
        count = self.collection.count()

        # Get sample of sources
        if count > 0:
            sample = self.collection.get(limit=min(100, count))
            sources = {}
            for metadata in sample['metadatas']:
                source = metadata.get('source', 'unknown')
                sources[source] = sources.get(source, 0) + 1

            return {
                "total_items": count,
                "sources": sources,
                "collection_name": self.collection.name
            }
        else:
            return {
                "total_items": 0,
                "sources": {},
                "collection_name": self.collection.name
            }

    def retrieve_context(self, query: str, max_context_length: int = 2000) -> str:
        """Retrieve relevant context for a query"""
        results = self.search(query, n_results=5)

        if not results:
            return ""

        # Build context from results
        context_parts = []
        total_length = 0

        for result in results:
            text = result['text']
            source = result['metadata'].get('source', 'unknown')

            # Format as citation
            context_part = f"[Source: {source}]\n{text}\n"

            if total_length + len(context_part) > max_context_length:
                break

            context_parts.append(context_part)
            total_length += len(context_part)

        return "\n".join(context_parts)

    def delete_knowledge(self, doc_id: str) -> None:
        """Delete knowledge by ID"""
        self.collection.delete(ids=[doc_id])
        logger.info(f"Deleted knowledge: {doc_id}")

    def clear_all(self, confirm: bool = False) -> None:
        """Clear all stored knowledge (use with caution)"""
        if not confirm:
            raise ValueError("Must set confirm=True to clear all knowledge")

        self.client.delete_collection(self.collection.name)
        self.collection = self.client.create_collection(
            name=self.config['memory']['collection_name']
        )
        logger.warning("All knowledge cleared from memory")


if __name__ == "__main__":
    # Test the vector memory system
    memory = VectorMemory()

    # Add some test knowledge
    memory.add_knowledge(
        "Python is a high-level programming language known for its simplicity.",
        source="test",
        metadata={"topic": "programming"}
    )

    memory.add_knowledge(
        "Machine learning is a subset of artificial intelligence.",
        source="test",
        metadata={"topic": "AI"}
    )

    # Search
    results = memory.search("What is Python?")
    print("\nSearch results:")
    for result in results:
        print(f"- {result['text']}")
        print(f"  Source: {result['metadata']['source']}")

    # Stats
    stats = memory.get_stats()
    print(f"\nMemory stats: {stats}")
