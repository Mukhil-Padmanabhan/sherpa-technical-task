from app.services.chroma_indexer import ChromaIndexer
from app.services import summarizer, pdf_loader

TENANTS = {
    "Bain": "MBB_AI_reports/Bain",
    "BCG": "MBB_AI_reports/BCG",
    "McK": "MBB_AI_reports/McK"
}

def initialize_all_tenants():
    all_docs = []
    tenant_docs = {}
    all_indexers = {}
    summarizer_service = summarizer.Summarizer()

    for tenant, folder in TENANTS.items():
        print(f"Loading {tenant} PDFs from {folder}")
        docs = pdf_loader.load_pdfs(folder)
        if not docs:
            print(f"No docs found for {tenant}")
            continue

        for i, doc in enumerate(docs):
            doc.id =  f"{tenant}_{i}"
            doc.summary = summarizer_service.generate_summary(doc.content)

        tenant_indexer = ChromaIndexer()
        tenant_indexer.index_documents(tenant, docs)

        tenant_docs[tenant] = docs
        all_indexers[tenant] = tenant_indexer
        all_docs.extend(docs)

    if all_docs:
        indexer_all = ChromaIndexer()
        indexer_all.index_documents("all", all_docs)
        tenant_docs["all"] = all_docs
        all_indexers["all"] = indexer_all

    print("All tenants indexed")
    return tenant_docs, all_indexers
