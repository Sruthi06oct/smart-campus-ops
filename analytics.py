queries = []

def log_query(q):
    queries.append(q)

def stats():
    return {"total_queries": len(queries)}
