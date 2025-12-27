from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from PyPDF2 import PdfReader

model = SentenceTransformer("all-MiniLM-L6-v2")

texts = []
index = None

def load_pdf(path):
    global texts, index
    reader = PdfReader(path)
    texts = []
    for page in reader.pages:
        t = page.extract_text()
        if t:
            texts.extend(t.split("\n"))
    embeddings = model.encode(texts)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))

def retrieve(query, k=3):
    if index is None:
        return ["Upload a document first."]
    q = model.encode([query])
    D, I = index.search(np.array(q), k)
    return [texts[i] for i in I[0]]
