Chatbot Core Engine
===================

.. mermaid::

   graph LR
      Document_Ingestion["Document Ingestion"]
      Text_Splitter["Text Splitter"]
      Vector_Store["Vector Store"]
      Embeddings_Model["Embeddings Model"]
      Language_Model_LLM_["Language Model (LLM)"]
      Retrieval_Chain["Retrieval Chain"]
      Unclassified["Unclassified"]
      Document_Ingestion -- "loads documents into" --> Text_Splitter
      Text_Splitter -- "splits text for" --> Embeddings_Model
      Embeddings_Model -- "generates embeddings for" --> Vector_Store
      Vector_Store -- "stores embeddings from" --> Embeddings_Model
      Vector_Store -- "retrieves context for" --> Retrieval_Chain
      Retrieval_Chain -- "uses" --> Language_Model_LLM_
      Language_Model_LLM_ -- "answers queries using" --> Retrieval_Chain

| |codeboarding-badge| |demo-badge| |contact-badge|

.. |codeboarding-badge| image:: https://img.shields.io/badge/Generated%20by-CodeBoarding-9cf?style=flat-square
   :target: https://github.com/CodeBoarding/CodeBoarding
.. |demo-badge| image:: https://img.shields.io/badge/Try%20our-Demo-blue?style=flat-square
   :target: https://www.codeboarding.org/demo
.. |contact-badge| image:: https://img.shields.io/badge/Contact%20us%20-%20contact@codeboarding.org-lightgrey?style=flat-square
   :target: mailto:contact@codeboarding.org

Details
-------

This graph represents the core functionality of a document processing and question-answering system. The main flow involves ingesting documents, processing them into a searchable format, and then using a language model to answer user queries based on the ingested content. Its purpose is to provide an intelligent interface for users to retrieve information from a collection of documents.

Document Ingestion
^^^^^^^^^^^^^^^^^^

Handles the loading and initial processing of various document types.

**Related Classes/Methods**:

* langchain_community.document_loaders.pdf.PyPDFLoader
* langchain_community.document_loaders.csv_loader.CSVLoader

Text Splitter
^^^^^^^^^^^^^

Breaks down large documents into smaller, manageable chunks for efficient processing and embedding.

**Related Classes/Methods**:

* langchain.text_splitter.RecursiveCharacterTextSplitter

Vector Store
^^^^^^^^^^^^

Stores and retrieves document embeddings, enabling semantic search.

**Related Classes/Methods**:

* langchain_community.vectorstores.chroma.Chroma

Embeddings Model
^^^^^^^^^^^^^^^^

Generates numerical representations (embeddings) of text chunks.

**Related Classes/Methods**:

* langchain_community.embeddings.ollama.OllamaEmbeddings

Language Model (LLM)
^^^^^^^^^^^^^^^^^^^^

Processes user queries and generates answers based on retrieved context.

**Related Classes/Methods**:

* langchain_community.llms.ollama.Ollama

Retrieval Chain
^^^^^^^^^^^^^^^

Orchestrates the retrieval of relevant document chunks and passes them to the LLM for answer generation.

**Related Classes/Methods**:

* langchain.chains.retrieval.create_retrieval_chain

Unclassified
^^^^^^^^^^^^

Component for all unclassified files and utility functions (Utility functions/External Libraries/Dependencies)

**Related Classes/Methods**: *None*
