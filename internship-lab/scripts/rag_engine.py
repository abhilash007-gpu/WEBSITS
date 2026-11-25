"""Tiny BM25-style retrieval engine for the DocuMind learning project."""
from collections import Counter
import math,re

STOP=set("a an and are as at be been but by can could did do does for from had has have how i in into is it its may more most of on or our should that the their them then there these this to was we were what when where which who why will with would you your".split())

def tokenize(text):
    return [x for x in re.findall(r"[a-z0-9+#.-]+",text.lower()) if len(x)>1 and x not in STOP]

def chunk_text(text,size=85,overlap=18):
    if size<=overlap: raise ValueError("size must be larger than overlap")
    words=text.split()
    return [" ".join(words[i:i+size]) for i in range(0,len(words),size-overlap)]

def retrieve(query,documents,top_k=4):
    terms=set(tokenize(query)); token_lists=[tokenize(d["text"]) for d in documents]; n=len(documents)
    if not terms or not n: return []
    avg=sum(map(len,token_lists))/n; df={t:sum(t in row for row in token_lists) for t in terms}; results=[]
    for doc,tokens in zip(documents,token_lists):
        counts=Counter(tokens); score=0
        for t in terms:
            f=counts[t]
            if f:
                idf=math.log(1+(n-df[t]+.5)/(df[t]+.5))
                score+=idf*(f*2.2)/(f+1.2*(.25+.75*len(tokens)/max(1,avg)))
        if score: results.append({**doc,"score":round(score,4)})
    return sorted(results,key=lambda x:x["score"],reverse=True)[:top_k]

if __name__=="__main__":
    notes=[
      {"title":"Data Analyst Intern","text":"Data analysts clean and validate data, write SQL SELECT WHERE JOIN GROUP BY queries, use Excel and create Tableau dashboards that answer business questions."},
      {"title":"AI Engineer Intern","text":"AI projects use Python, APIs, Git, retrieval augmented generation, chunking, embeddings, vector search, tool calling and citations."},
      {"title":"Machine Learning Checklist","text":"Use a train test split, preprocessing pipeline, precision recall F1 ROC-AUC and confusion matrix. Avoid data leakage."}
    ]
    query=input("Question: ")
    for hit in retrieve(query,notes): print(hit["title"],hit["score"],hit["text"])
