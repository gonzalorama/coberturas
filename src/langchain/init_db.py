from _document_processor import CompanyDocumentIndexer

db_loader = CompanyDocumentIndexer()

db_loader.index_all_company_documents('/home/gonzalo/coberturas/data/documents')
