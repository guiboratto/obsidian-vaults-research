#!/usr/bin/env python3
"""
Setup ChromaDB for Obsidian Knowledge Base

This script:
1. Loads all markdown files from the unified vault
2. Creates embeddings using Ollama
3. Stores documents in ChromaDB with metadata
4. Creates multiple collections for different domains
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

try:
    from chromadb import PersistentClient
    from chromadb.config import Settings
    from langchain_community.document_loaders import ObsidianLoader
    from langchain_community.embeddings import OllamaEmbeddings
    from langchain_community.vectorstores import Chroma
    from langchain.schema import Document
except ImportError as e:
    print(f"Error importing required packages: {e}")
    print("Please install: pip install chromadb langchain-community langchain-ollama")
    sys.exit(1)


class ObsidianChromaDB:
    """Manages ChromaDB for Obsidian knowledge base."""
    
    def __init__(self, vault_path: str, chroma_path: str = "./chromadb"):
        self.vault_path = Path(vault_path)
        self.chroma_path = Path(chroma_path)
        self.client = None
        self.embeddings = None
        self.collections = {}
        
    def initialize(self):
        """Initialize ChromaDB client and embeddings."""
        print("Initializing ChromaDB...")
        
        # Create client with persistence
        self.client = PersistentClient(
            path=str(self.chroma_path),
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Initialize Ollama embeddings
        print("Loading Ollama embeddings model...")
        self.embeddings = OllamaEmbeddings(model="llama3.2")
        print("✓ Embeddings loaded")
    
    def load_documents(self) -> List[Document]:
        """Load all markdown files from the vault."""
        print(f"\nLoading documents from {self.vault_path}...")
        
        if not self.vault_path.exists():
            print(f"✗ Vault path not found: {self.vault_path}")
            sys.exit(1)
        
        # Use LangChain's ObsidianLoader
        loader = ObsidianLoader(
            str(self.vault_path),
            glob="**/*.md",
            silent_errors=True
        )
        
        documents = loader.load()
        print(f"✓ Loaded {len(documents)} documents")
        
        return documents
    
    def create_collection(self, name: str, filter_fn=None) -> Chroma:
        """Create or get a collection."""
        if filter_fn is None:
            filter_fn = lambda x: True
        
        print(f"Creating collection: {name}")
        
        collection = Chroma(
            client=self.client,
            collection_name=name,
            embedding_function=self.embeddings,
            metadata={"description": name}
        )
        
        self.collections[name] = collection
        return collection
    
    def index_collection(
        self,
        collection_name: str,
        documents: List[Document],
        metadata_filter: Dict[str, Any] = None
    ) -> int:
        """Index documents in a collection."""
        print(f"\nIndexing {len(documents)} documents into '{collection_name}'...")
        
        # Filter documents by metadata
        if metadata_filter:
            filtered_docs = [
                doc for doc in documents
                if all(
                    doc.metadata.get(k) == v
                    for k, v in metadata_filter.items()
                )
            ]
            print(f"  Filtered to {len(filtered_docs)} documents")
            documents = filtered_docs
        
        if not documents:
            print(f"  No documents to index")
            return 0
        
        # Add to collection
        collection = self.create_collection(collection_name)
        collection.add(
            documents=[doc.page_content for doc in documents],
            metadatas=[self._enhance_metadata(doc) for doc in documents],
            ids=[f"{collection_name}_{i}" for i in range(len(documents))]
        )
        
        print(f"✓ Indexed {len(documents)} documents into '{collection_name}'")
        return len(documents)
    
    def _enhance_metadata(self, doc: Document) -> Dict[str, Any]:
        """Enhance document metadata with additional information."""
        metadata = doc.metadata.copy()
        
        # Extract path components
        path_parts = Path(metadata.get("path", "")).parts
        
        metadata["folder"] = path_parts[0] if path_parts else "unknown"
        metadata["filename"] = Path(metadata.get("path", "")).stem
        metadata["extension"] = Path(metadata.get("path", "")).suffix
        
        # Try to extract type from frontmatter
        if "frontmatter" in metadata and isinstance(metadata["frontmatter"], dict):
            metadata["type"] = metadata["frontmatter"].get("type", "unknown")
            metadata["status"] = metadata["frontmatter"].get("status", "active")
            metadata["tags"] = metadata["frontmatter"].get("tags", [])
        else:
            metadata["type"] = "unknown"
            metadata["status"] = "active"
            metadata["tags"] = []
        
        metadata["indexed_at"] = datetime.now().isoformat()
        
        return metadata
    
    def create_domain_collections(self, documents: List[Document]):
        """Create collections for different domains."""
        print("\nCreating domain collections...")
        
        # Define domain filters
        domains = {
            "all": None,
            "meetings": {"folder": "03-Work-System/01-Meetings"},
            "decisions": {"folder": "03-Work-System/02-Decisions"},
            "projects": {"folder": "01-Active/01-Projects"},
            "areas": {"folder": "01-Active/02-Areas"},
            "resources": {"folder": "01-Active/03-Resources"},
            "shared-knowledge": {"folder": "02-Shared-Knowledge"},
            "personal": {"folder": "04-Personal"},
            "ideas": {"folder": "02-Shared-Knowledge/01-Ideas"},
            "books": {"folder": "02-Shared-Knowledge/02-Books"},
            "research": {"folder": "02-Shared-Knowledge/03-Research"}
        }
        
        for collection_name, filter_config in domains.items():
            self.index_collection(collection_name, documents, filter_config)
    
    def get_collection_stats(self) -> Dict[str, int]:
        """Get statistics for all collections."""
        stats = {}
        
        for name, collection in self.collections.items():
            try:
                count = collection.count()
                stats[name] = count
            except Exception as e:
                stats[name] = f"Error: {e}"
        
        return stats
    
    def save_index(self):
        """Save index information to a file."""
        stats = self.get_collection_stats()
        
        index_data = {
            "vault_path": str(self.vault_path),
            "chroma_path": str(self.chroma_path),
            "indexed_at": datetime.now().isoformat(),
            "statistics": stats
        }
        
        output_path = self.chroma_path / "index.json"
        with open(output_path, 'w') as f:
            json.dump(index_data, f, indent=2)
        
        print(f"\n✓ Index saved to {output_path}")
    
    def run(self):
        """Run the complete setup process."""
        print("=" * 60)
        print("Obsidian ChromaDB Setup")
        print("=" * 60)
        
        # Initialize
        self.initialize()
        
        # Load documents
        documents = self.load_documents()
        
        if not documents:
            print("\n✗ No documents found. Exiting.")
            return
        
        # Create domain collections
        self.create_domain_collections(documents)
        
        # Save index
        self.save_index()
        
        # Print statistics
        print("\n" + "=" * 60)
        print("Setup Complete!")
        print("=" * 60)
        print("\nCollection Statistics:")
        for name, count in self.get_collection_stats().items():
            print(f"  {name}: {count} documents")
        
        print(f"\nChromaDB location: {self.chroma_path}")
        print("=" * 60)


def main():
    vault_path = os.getenv("UNIFIED_VAULT_PATH", "./unified-brain")
    chroma_path = os.getenv("CHROMA_PATH", "./chromadb")
    
    # Allow command line arguments
    if len(sys.argv) > 1:
        vault_path = sys.argv[1]
    if len(sys.argv) > 2:
        chroma_path = sys.argv[2]
    
    setup = ObsidianChromaDB(vault_path, chroma_path)
    setup.run()


if __name__ == "__main__":
    main()
