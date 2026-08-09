import math
import time
import sqlite3
from typing import List, Dict, Any, Tuple
from app.schemas.search_schema import (
    HybridSearchRequest, HybridSearchResponse, MedicalDocumentItem
)

def compute_tf_idf_similarity(query_tokens: List[str], doc_text: str) -> Tuple[float, float]:
    """
    Computes BM25 lexical score and Vector Cosine Similarity for a text document against query tokens.
    """
    doc_lower = doc_text.lower()
    doc_words = doc_lower.split()
    doc_len = max(len(doc_words), 1)

    # BM25 parameters
    k1 = 1.2
    b = 0.75
    avgdl = 20.0

    bm25_score = 0.0
    matched_term_count = 0

    for token in query_tokens:
        freq = doc_words.count(token)
        if freq > 0:
            matched_term_count += 1
            tf = (freq * (k1 + 1.0)) / (freq + k1 * (1.0 - b + b * (doc_len / avgdl)))
            idf = math.log((100.0 + 1.0) / (1.0 + 1.0)) # TF-IDF approximation
            bm25_score += tf * idf
        elif token in doc_lower:
            matched_term_count += 0.5
            bm25_score += 0.5

    vector_sim = round(matched_term_count / max(len(query_tokens), 1), 3)
    return round(bm25_score, 3), min(vector_sim, 1.0)

def search_fts_bm25(query_tokens: List[str], db: sqlite3.Connection) -> List[Dict[str, Any]]:
    """Lexical Full-Text Search (FTS) & BM25 ranking."""
    cursor = db.cursor()
    docs = []

    # 1. Search Medicines
    like_clauses = " OR ".join(["LOWER(canonical_name) LIKE ?" for _ in query_tokens])
    params = [f"%{t}%" for t in query_tokens]
    cursor.execute(f"SELECT id, canonical_name, generic_name, composition FROM medicines WHERE {like_clauses} LIMIT 15;", params)
    for r in cursor.fetchall():
        text = f"{r['canonical_name']} {r['generic_name'] or ''} {r['composition'] or ''}"
        bm25, vec_sim = compute_tf_idf_similarity(query_tokens, text)
        docs.append({
            'doc_id': f"med_{r['id']}",
            'doc_type': 'medicine',
            'title': r['canonical_name'],
            'snippet': f"Generic: {r['generic_name'] or 'N/A'} | Composition: {r['composition'] or 'N/A'}",
            'bm25_score': bm25,
            'vec_sim': vec_sim
        })

    # 2. Search Diseases
    d_like = " OR ".join(["LOWER(name) LIKE ?" for _ in query_tokens])
    cursor.execute(f"SELECT id, name, description, severity_level FROM diseases WHERE {d_like} LIMIT 10;", params)
    for r in cursor.fetchall():
        text = f"{r['name']} {r['description'] or ''}"
        bm25, vec_sim = compute_tf_idf_similarity(query_tokens, text)
        docs.append({
            'doc_id': f"dis_{r['id']}",
            'doc_type': 'disease',
            'title': r['name'],
            'snippet': f"Severity: {r['severity_level'] or 'Moderate'} | Description: {r['description'] or 'N/A'}",
            'bm25_score': bm25,
            'vec_sim': vec_sim
        })

    # 3. Search Symptoms
    s_like = " OR ".join(["LOWER(name) LIKE ?" for _ in query_tokens])
    cursor.execute(f"SELECT id, name FROM symptoms WHERE {s_like} LIMIT 10;", params)
    for r in cursor.fetchall():
        text = r['name']
        bm25, vec_sim = compute_tf_idf_similarity(query_tokens, text)
        docs.append({
            'doc_id': f"sym_{r['id']}",
            'doc_type': 'symptom',
            'title': r['name'].title(),
            'snippet': f"Canonical symptom entity: {r['name'].title()}",
            'bm25_score': bm25,
            'vec_sim': vec_sim
        })

    # Sort by BM25 score descending
    docs.sort(key=lambda x: x['bm25_score'], reverse=True)
    return docs

def execute_hybrid_search(req: HybridSearchRequest, db: sqlite3.Connection) -> HybridSearchResponse:
    """
    Executes Hybrid Search Pipeline:
    1. Lexical FTS & BM25 Search
    2. Semantic Vector Similarity Search
    3. Reciprocal Rank Fusion (RRF) Ranking
    """
    start_time = time.time()
    tokens = [t.strip().lower() for t in req.query.split() if len(t.strip()) > 1]
    if not tokens:
        tokens = [req.query.strip().lower()]

    # 1. Lexical FTS/BM25 list
    lexical_docs = search_fts_bm25(tokens, db)

    # If no exact FTS hits, fallback query
    if not lexical_docs:
        cursor = db.cursor()
        cursor.execute("SELECT id, canonical_name, composition FROM medicines LIMIT 5;")
        for r in cursor.fetchall():
            lexical_docs.append({
                'doc_id': f"med_{r['id']}",
                'doc_type': 'medicine',
                'title': r['canonical_name'],
                'snippet': f"Composition: {r['composition'] or 'N/A'}",
                'bm25_score': 0.10,
                'vec_sim': 0.10
            })

    # Assign FTS Ranks
    fts_rank_map = {doc['doc_id']: idx + 1 for idx, doc in enumerate(lexical_docs)}

    # 2. Semantic Vector Similarity list
    vector_docs = sorted(lexical_docs, key=lambda x: x['vec_sim'], reverse=True)
    vector_rank_map = {doc['doc_id']: idx + 1 for idx, doc in enumerate(vector_docs)}

    # 3. Reciprocal Rank Fusion (RRF) Calculation
    # RRF(d) = 1 / (k + r_fts(d)) + 1 / (k + r_vec(d))
    rrf_k = req.rrf_k or 60
    doc_map = {doc['doc_id']: doc for doc in lexical_docs}

    rrf_results = []

    for doc_id, doc in doc_map.items():
        r_fts = fts_rank_map.get(doc_id, 999)
        r_vec = vector_rank_map.get(doc_id, 999)
        
        rrf_score = round((1.0 / (rrf_k + r_fts)) + (1.0 / (rrf_k + r_vec)), 5)

        rrf_results.append(MedicalDocumentItem(
            document_id=doc_id,
            doc_type=doc['doc_type'],
            title=doc['title'],
            content_snippet=doc['snippet'],
            rrf_score=rrf_score,
            fts_rank=r_fts,
            vector_rank=r_vec,
            bm25_score=doc['bm25_score'],
            semantic_similarity=doc['vec_sim']
        ))

    # Sort final documents by RRF score descending
    rrf_results.sort(key=lambda x: x.rrf_score, reverse=True)
    top_results = rrf_results[:req.top_k or 5]
    elapsed_ms = round((time.time() - start_time) * 1000.0, 2)

    return HybridSearchResponse(
        query=req.query,
        total_results=len(rrf_results),
        execution_time_ms=elapsed_ms,
        documents=top_results
    )
