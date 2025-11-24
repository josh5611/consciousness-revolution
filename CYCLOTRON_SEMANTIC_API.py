#!/usr/bin/env python3
"""
CYCLOTRON SEMANTIC API - HTTP interface for semantic search

Exposes semantic vector search via REST API on port 6670.
Requires SEMANTIC_VECTOR_ENGINE.py to have indexed the content first.

Endpoints:
- GET /api/semantic?q=query - Semantic similarity search
- GET /api/similar?path=/path/to/file - Find similar files
- GET /api/clusters?n=7 - Get concept clusters
- GET /api/stats - Engine statistics
- GET /health - Health check

Usage:
    python CYCLOTRON_SEMANTIC_API.py
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add parent to path
sys.path.insert(0, os.path.dirname(__file__))

from SEMANTIC_VECTOR_ENGINE import SemanticVectorEngine

app = Flask(__name__)
CORS(app)

# Initialize engine on startup
print("Initializing Semantic API...")
engine = None

def get_engine():
    global engine
    if engine is None:
        engine = SemanticVectorEngine()
    return engine


@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    try:
        eng = get_engine()
        stats = eng.get_stats()
        return jsonify({
            'status': 'healthy',
            'vector_chunks': stats['vector_chunks'],
            'model': stats['model']
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/semantic', methods=['GET'])
def semantic_search():
    """Semantic similarity search - find files by meaning"""
    query = request.args.get('q', '')
    limit = int(request.args.get('limit', 10))

    if not query:
        return jsonify({'error': 'Query parameter q is required'}), 400

    try:
        eng = get_engine()
        results = eng.search(query, n_results=limit)

        return jsonify({
            'query': query,
            'results': results,
            'count': len(results)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/similar', methods=['GET'])
def find_similar():
    """Find files similar to a given file"""
    path = request.args.get('path', '')
    limit = int(request.args.get('limit', 10))

    if not path:
        return jsonify({'error': 'Parameter path is required'}), 400

    try:
        eng = get_engine()
        results = eng.find_similar(path, n_results=limit)

        return jsonify({
            'source_file': path,
            'similar_files': results,
            'count': len(results)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/clusters', methods=['GET'])
def get_clusters():
    """Get concept clusters (maps to Seven Domains)"""
    n = int(request.args.get('n', 7))

    try:
        eng = get_engine()
        clusters = eng.cluster_concepts(n_clusters=n)

        # Format for API response
        formatted = {}
        for cluster_id, files in clusters.items():
            formatted[f'cluster_{cluster_id}'] = {
                'count': len(files),
                'files': files[:10],  # Limit to 10 per cluster
                'has_more': len(files) > 10
            }

        return jsonify({
            'n_clusters': n,
            'clusters': formatted
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get engine statistics"""
    try:
        eng = get_engine()
        stats = eng.get_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/ask', methods=['GET'])
def ask_semantic():
    """Natural language question - semantic version"""
    question = request.args.get('q', '')
    limit = int(request.args.get('limit', 5))

    if not question:
        return jsonify({'error': 'Query parameter q is required'}), 400

    try:
        eng = get_engine()
        results = eng.search(question, n_results=limit)

        # Format as answers
        answers = []
        for r in results:
            answers.append({
                'source': r['name'],
                'path': r['path'],
                'answer': r['preview'],
                'relevance': f"{r['similarity']:.1%}"
            })

        return jsonify({
            'question': question,
            'answers': answers
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("Starting Cyclotron Semantic API on port 6670...")
    print("Endpoints:")
    print("  GET /api/semantic?q=query  - Semantic search")
    print("  GET /api/similar?path=...  - Find similar files")
    print("  GET /api/clusters?n=7      - Concept clusters")
    print("  GET /api/stats             - Engine stats")
    print("  GET /api/ask?q=question    - Natural language")
    print()

    app.run(host='0.0.0.0', port=6670, debug=False)
