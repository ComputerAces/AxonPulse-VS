# 🧩 AI Nodes

This document covers nodes within the **AI** core category.

## 📂 Providers

### Gemini Provider

**Version**: `2.3.0`

Service provider for Google's Gemini AI models.
Registers an AI capability scope for 'Ask AI' and other consumer nodes.

Inputs:
- Flow: Start the provider service and enter the AI scope.
- Provider End: Close the provider service and exit the scope.
- API Key: Your Google Gemini API Key.
- Model: The Gemini model ID to use (default: gemini-1.5-pro).

Outputs:
- Provider Flow: Active while the provider service is running.
- Provider ID: Unique ID for this specific provider instance.
- Flow: Triggered when the service is stopped.

---

### Ollama Provider

**Version**: `2.3.0`

Service provider for locally hosted Ollama AI models.
Registers an AI capability scope for 'Ask AI' and other consumer nodes.

Inputs:
- Flow: Start the local service connection and enter the AI scope.
- Provider End: Close the connection and exit the scope.
- Host: URL of the Ollama API (default: http://localhost:11434).
- Model: The Ollama model name to use (default: llama3).
- Temperature: Creativity setting for the model (0.0 to 1.0).

Outputs:
- Provider Flow: Active while the provider service is running.
- Provider ID: Unique ID for this specific provider instance.
- Flow: Triggered when the service is stopped.

---

### OpenAI Provider

**Version**: `2.3.0`

Service provider for OpenAI's GPT models (or OpenAI-compatible APIs).
Registers an AI capability scope for 'Ask AI' and other consumer nodes.

Inputs:
- Flow: Start the provider service and enter the AI scope.
- Provider End: Close the provider service and exit the scope.
- API Key: Your OpenAI API Key.
- Model: The GPT model ID to use (default: gpt-4o).
- Base URL: The API endpoint URL (allows usage with local models like LM Studio).

Outputs:
- Provider Flow: Active while the provider service is running.
- Provider ID: Unique ID for this specific provider instance.
- Flow: Triggered when the service is stopped.

---

## 📂 Vector

### BM25 Provider

**Version**: `2.3.0`

Service provider for BM25 (Best Matching 25) rank-based keyword search.
Operates as a local Vector Provider using lexical relevance.

Inputs:
- Flow: Start the BM25 service scope.
- Provider End: Close the service scope.
- Corpus: A list of text documents to index for searching.

Outputs:
- Provider Flow: Active while the provider service is running.
- Provider ID: Unique ID for this specific provider instance.
- Flow: Triggered when the service is stopped.

---

### FastEmbed Provider

**Version**: `2.3.0`

Service provider for local document embedding using the 'fastembed' library.
Highly optimized for CPU-based vector generation.

Inputs:
- Flow: Start resizing/embedding service scope.
- Provider End: Close the service scope.
- Model Name: The specific embedding model to load (e.g., 'BAAI/bge-small-en-v1.5').

Outputs:
- Provider Flow: Active while the embedding service is running.
- Provider ID: Unique ID for this specific provider instance.
- Flow: Triggered when the service is stopped.

---

### Gemini Embeddings

**Version**: `2.3.0`

Service provider for Google's Gemini embedding models.
Generates high-quality vector representations of text for semantic search.

Inputs:
- Flow: Start the embedding service and enter the EMBED scope.
- Provider End: Close the service and exit the scope.
- API Key: Your Google Gemini API Key.

Outputs:
- Provider Flow: Active while the embedding service is running.
- Provider ID: Unique ID for this specific provider instance.
- Flow: Triggered when the service is stopped.

---

### LanceDB

**Version**: `2.3.0`

Service provider for LanceDB, a serverless, persistent vector database.
Stores and retrieves embedded vectors directly from local disk.

Inputs:
- Flow: Start the LanceDB service and enter the vector scope.
- Provider End: Close the database connection and exit the scope.
- Storage Path: Directory path where the database files are stored.
- Table Name: The specific collection/table to interact with.

Outputs:
- Provider Flow: Active while the database connection is open.
- Provider ID: Unique ID for this specific provider instance.
- Flow: Triggered when the service is stopped.

---

### Milvus

**Version**: `2.3.0`

Service provider for Milvus, a high-performance, cloud-native vector database.
Manages connections to standalone Milvus instances or Milvus Lite.

Inputs:
- Flow: Start the Milvus service and enter the vector scope.
- Provider End: Close the database connection and exit the scope.
- URI: The Milvus server address (e.g., 'http://localhost:19530').
- Token: Authentication token/password (if required).
- Collection Name: The target collection for search/add operations.

Outputs:
- Provider Flow: Active while the database connection is open.
- Provider ID: Unique ID for this specific provider instance.
- Flow: Triggered when the service is stopped.

---

### OpenAI Embeddings

**Version**: `2.3.0`

Service provider for OpenAI's text embedding models.
Converts text into dense vectors for high-accuracy similarity search.

Inputs:
- Flow: Start the embedding service and enter the EMBED scope.
- Provider End: Close the service and exit the scope.
- API Key: Your OpenAI API Key.

Outputs:
- Provider Flow: Active while the embedding service is running.
- Provider ID: Unique ID for this specific provider instance.
- Flow: Triggered when the service is stopped.

---

### Pinecone

**Version**: `2.3.0`

Service provider for Pinecone, a managed cloud-native vector database.
Enables high-scale similarity search and persistent storage for AI applications.

Inputs:
- Flow: Start the Pinecone service and enter the vector scope.
- Provider End: Close the database connection and exit the scope.
- API Key: Your Pinecone API Key.

Outputs:
- Provider Flow: Active while the database connection is open.
- Provider ID: Unique ID for this specific provider instance.
- Flow: Triggered when the service is stopped.

---

### TF-IDF Provider

**Version**: `2.3.0`

Service provider for TF-IDF (Term Frequency-Inverse Document Frequency) search.
Operates as a local Vector Provider using statistical relevance rankings.

Inputs:
- Flow: Start the TF-IDF service scope.
- Provider End: Close the service scope.
- Corpus: A list of text documents to index for searching.

Outputs:
- Provider Flow: Active while the provider service is running.
- Provider ID: Unique ID for this specific provider instance.
- Flow: Triggered when the service is stopped.

---

[Back to Node Index](Index.md)
