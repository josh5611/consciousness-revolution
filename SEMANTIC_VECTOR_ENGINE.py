#!/usr/bin/env python3
"""
SEMANTIC VECTOR ENGINE - Meaning-Based Search for Cyclotron

Transforms Cyclotron from text matching to semantic understanding.
Uses sentence-transformers for embeddings and ChromaDB for vector storage.

Features:
- Generate embeddings for all indexed files
- Semantic similarity search ("files about Pattern Theory")
- Concept clustering and discovery
- Integration with existing Cyclotron FTS

Usage:
    python SEMANTIC_VECTOR_ENGINE.py index     # Index all files
    python SEMANTIC_VECTOR_ENGINE.py search "query"  # Semantic search
    python SEMANTIC_VECTOR_ENGINE.py similar /path   # Find similar files
    python SEMANTIC_VECTOR_ENGINE.py status   # Show index stats
"""

import os
import sys
import json
import sqlite3
from pathlib import Path
from datetime import datetime

# Check for required packages
try:
    from sentence_transformers import SentenceTransformer
    import chromadb
    from chromadb.config import Settings
except ImportError:
    print("Installing required packages...")
    os.system("pip install sentence-transformers chromadb")
    from sentence_transformers import SentenceTransformer
    import chromadb
    from chromadb.config import Settings

# Configuration
CYCLOTRON_DB = Path("C:/Users/dwrek/100X_DEPLOYMENT/.cyclotron_atoms/cyclotron.db")
CHROMA_DIR = Path("C:/Users/dwrek/100X_DEPLOYMENT/.cyclotron_atoms/chroma")
MODEL_NAME = "all-MiniLM-L6-v2"  # Fast, 384-dim embeddings
BATCH_SIZE = 100
MAX_CHUNK_SIZE = 1000  # Characters per chunk for embedding


class SemanticVectorEngine:
    """Semantic search layer for Cyclotron"""

    def __init__(self):
        print("Initializing Semantic Vector Engine...")

        # Load embedding model
        print(f"Loading model: {MODEL_NAME}")
        self.model = SentenceTransformer(MODEL_NAME)

        # Initialize ChromaDB
        CHROMA_DIR.mkdir(parents=True, exist_ok=True)
        self.chroma_client = chromadb.PersistentClient(
            path=str(CHROMA_DIR),
            settings=Settings(anonymized_telemetry=False)
        )

        # Get or create collection
        self.collection = self.chroma_client.get_or_create_collection(
            name="cyclotron_knowledge",
            metadata={"hnsw:space": "cosine"}
        )

        # Connect to Cyclotron FTS database
        self.fts_conn = sqlite3.connect(str(CYCLOTRON_DB))

        print(f"Engine ready. Collection has {self.collection.count()} embeddings.")

    def chunk_text(self, text, chunk_size=MAX_CHUNK_SIZE):
        """Split text into chunks for embedding"""
        words = text.split()
        chunks = []
        current_chunk = []
        current_size = 0

        for word in words:
            if current_size + len(word) + 1 > chunk_size:
                if current_chunk:
                    chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                current_size = len(word)
            else:
                current_chunk.append(word)
                current_size += len(word) + 1

        if current_chunk:
            chunks.append(' '.join(current_chunk))

        return chunks if chunks else [text[:chunk_size]]

    def index_all(self):
        """Index all files from Cyclotron FTS into vector store"""
        print("Starting semantic indexing...")

        # Get all files from FTS
        cursor = self.fts_conn.cursor()
        cursor.execute("SELECT path, name, content FROM knowledge")
        rows = cursor.fetchall()

        total = len(rows)
        print(f"Found {total} files to index")

        # Process in batches
        indexed = 0
        skipped = 0

        for i in range(0, total, BATCH_SIZE):
            batch = rows[i:i+BATCH_SIZE]

            ids = []
            documents = []
            metadatas = []

            for path, name, content in batch:
                if not content or len(content.strip()) < 50:
                    skipped += 1
                    continue

                # Create chunks
                chunks = self.chunk_text(content)

                for j, chunk in enumerate(chunks):
                    chunk_id = f"{path}_{j}"

                    # Skip if already indexed
                    try:
                        existing = self.collection.get(ids=[chunk_id])
                        if existing['ids']:
                            continue
                    except:
                        pass

                    ids.append(chunk_id)
                    documents.append(chunk)
                    metadatas.append({
                        "path": path,
                        "name": name,
                        "chunk": j,
                        "total_chunks": len(chunks)
                    })

            if ids:
                # Generate embeddings and add to collection
                self.collection.add(
                    ids=ids,
                    documents=documents,
                    metadatas=metadatas
                )
                indexed += len(ids)

            print(f"Progress: {min(i+BATCH_SIZE, total)}/{total} files processed, {indexed} chunks indexed")

        print(f"\nIndexing complete: {indexed} chunks indexed, {skipped} skipped")
        return indexed

    def search(self, query, n_results=10):
        """Semantic search - find files by meaning"""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )

        # Deduplicate by file path
        seen_paths = set()
        unique_results = []

        for i, doc in enumerate(results['documents'][0]):
            meta = results['metadatas'][0][i]
            path = meta['path']

            if path not in seen_paths:
                seen_paths.add(path)
                unique_results.append({
                    'path': path,
                    'name': meta['name'],
                    'preview': doc[:300] + '...' if len(doc) > 300 else doc,
                    'similarity': 1 - results['distances'][0][i],  # Convert distance to similarity
                    'chunk': meta['chunk']
                })

        return unique_results

    def find_similar(self, file_path, n_results=10):
        """Find files similar to a given file"""
        # Get content from FTS
        cursor = self.fts_conn.cursor()
        cursor.execute("SELECT content FROM knowledge WHERE path = ?", (file_path,))
        row = cursor.fetchone()

        if not row:
            return []

        # Use first chunk as query
        content = row[0]
        chunks = self.chunk_text(content)

        # Search for similar
        results = self.search(chunks[0], n_results + 1)

        # Remove the query file itself
        results = [r for r in results if r['path'] != file_path]

        return results[:n_results]

    def get_stats(self):
        """Get engine statistics"""
        # Chroma stats
        chroma_count = self.collection.count()

        # FTS stats
        cursor = self.fts_conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM knowledge")
        fts_count = cursor.fetchone()[0]

        return {
            'vector_chunks': chroma_count,
            'fts_files': fts_count,
            'model': MODEL_NAME,
            'chroma_dir': str(CHROMA_DIR),
            'coverage': f"{(chroma_count / max(fts_count, 1) * 100):.1f}%" if fts_count else "0%"
        }

    def cluster_concepts(self, n_clusters=7):
        """Discover concept clusters (maps to Seven Domains)"""
        # Get all embeddings
        all_data = self.collection.get(
            include=["embeddings", "metadatas"]
        )

        if not all_data['embeddings']:
            return []

        # Simple clustering using k-means
        try:
            from sklearn.cluster import KMeans
            import numpy as np

            embeddings = np.array(all_data['embeddings'])

            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            clusters = kmeans.fit_predict(embeddings)

            # Group files by cluster
            cluster_files = {}
            for i, cluster_id in enumerate(clusters):
                if cluster_id not in cluster_files:
                    cluster_files[cluster_id] = []
                cluster_files[cluster_id].append(all_data['metadatas'][i]['path'])

            return cluster_files

        except ImportError:
            print("sklearn not installed - clustering unavailable")
            return {}


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1].lower()
    engine = SemanticVectorEngine()

    if cmd == 'index':
        engine.index_all()

    elif cmd == 'search':
        if len(sys.argv) < 3:
            print("Usage: python SEMANTIC_VECTOR_ENGINE.py search 'your query'")
            return

        query = ' '.join(sys.argv[2:])
        results = engine.search(query)

        print(f"\n=== SEMANTIC SEARCH: '{query}' ===\n")
        for i, r in enumerate(results, 1):
            print(f"{i}. {r['name']} ({r['similarity']:.2%} match)")
            print(f"   {r['path']}")
            print(f"   {r['preview'][:150]}...")
            print()

    elif cmd == 'similar':
        if len(sys.argv) < 3:
            print("Usage: python SEMANTIC_VECTOR_ENGINE.py similar /path/to/file")
            return

        file_path = sys.argv[2]
        results = engine.find_similar(file_path)

        print(f"\n=== FILES SIMILAR TO: {file_path} ===\n")
        for i, r in enumerate(results, 1):
            print(f"{i}. {r['name']} ({r['similarity']:.2%} similar)")
            print(f"   {r['path']}")
            print()

    elif cmd == 'status':
        stats = engine.get_stats()
        print("\n=== SEMANTIC VECTOR ENGINE STATUS ===")
        print(f"Vector chunks: {stats['vector_chunks']:,}")
        print(f"FTS files: {stats['fts_files']:,}")
        print(f"Coverage: {stats['coverage']}")
        print(f"Model: {stats['model']}")
        print(f"Storage: {stats['chroma_dir']}")
        print()

    elif cmd == 'cluster':
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        clusters = engine.cluster_concepts(n)

        print(f"\n=== {n} CONCEPT CLUSTERS ===\n")
        for cluster_id, files in clusters.items():
            print(f"Cluster {cluster_id}: {len(files)} files")
            for f in files[:5]:
                print(f"  - {Path(f).name}")
            if len(files) > 5:
                print(f"  ... and {len(files)-5} more")
            print()

    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)


if __name__ == '__main__':
    main()
