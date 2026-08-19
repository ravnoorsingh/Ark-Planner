---
library: "sentence-transformers"
query: "Build a production RAG service that ingests PDF manuals, chunks and embeds them into a vector database, and exposes a FastAPI endpoint that answers questions with citations back to the source page. Use pypdf for extraction, python-multipart for uploads, and Pydantic models for validation. Use weaviate-client for the vector database. Use sentence-transformers for the embedding library."
url: "https://sbert.net/"
role: "primary"
rank: 0
fetched_at: "2026-08-19T19:23:44.509121+00:00"
fetched_via: "brightdata-collector:c_msx9i6aq2bz5dznadk"
sha256: "1470da3122ea9bc3af71da6826f4671bcd0f923f5740a8907f3d099ed9800c75"
---

Tip

Sentence Transformers v6.0 recently released, introducing the  [`MultiVectorEncoder`](docs/package_reference/multi_vector_encoder/model.html#sentence_transformers.multi_vector_encoder.model.MultiVectorEncoder "sentence_transformers.multi_vector_encoder.model.MultiVectorEncoder")  , a fourth model family for ColBERT-style late-interaction retrieval using token-level (multi-vector) embeddings, covering both text retrieval and ColPali-style visual document retrieval. Existing ColBERT, PyLate, and ColPali models load out of the box, with full training and evaluation support. Read the [Multi-Vector Encoder quickstart](docs/quickstart.html#multi-vector-encoder) , the [v6.0 Release Notes](https://github.com/huggingface/sentence-transformers/releases/tag/v6.0.0) , or the [migration guide](docs/migration_guide.html) for more details.

# SentenceTransformers Documentation

Sentence Transformers (a.k.a. SBERT) is the go-to Python module for using and training state-of-the-art embedding and reranker models. It can be used to compute embeddings from text, images, audio, or video using Sentence Transformer models ( [quickstart](docs/quickstart.html#sentence-transformer) ), to calculate similarity scores using Cross-Encoder (a.k.a. reranker) models ( [quickstart](docs/quickstart.html#cross-encoder) ), to generate sparse embeddings using Sparse Encoder models ( [quickstart](docs/quickstart.html#sparse-encoder) ), or to compute token-level embeddings for ColBERT-style late-interaction retrieval using Multi-Vector Encoder models ( [quickstart](docs/quickstart.html#multi-vector-encoder) ). This unlocks a wide range of applications, including [semantic search](examples/sentence_transformer/applications/semantic-search/README.html) , [semantic textual similarity](docs/sentence_transformer/usage/semantic_textual_similarity.html) , and [paraphrase mining](examples/sentence_transformer/applications/paraphrase-mining/README.html) .

A wide selection of over [25,000 pre-trained Sentence Transformers models](https://huggingface.co/models?library=sentence-transformers) are available for immediate use on 🤗 Hugging Face, including many of the state-of-the-art models from the [Massive Text Embeddings Benchmark (MTEB) leaderboard](https://huggingface.co/spaces/mteb/leaderboard) . Additionally, it is easy to train or finetune your own [embedding models](docs/sentence_transformer/training_overview.html) , [reranker models](docs/cross_encoder/training_overview.html) , [sparse encoder models](docs/sparse_encoder/training_overview.html) , or [multi-vector encoder models](docs/multi_vector_encoder/training_overview.html) using Sentence Transformers, enabling you to create custom models for your specific use cases.

Sentence Transformers was created by [UKP Lab](http://www.ukp.tu-darmstadt.de/) and is being maintained by [🤗 Hugging Face](https://huggingface.co) . Don’t hesitate to open an issue on the [Sentence Transformers repository](https://github.com/huggingface/sentence-transformers) if something is broken or if you have further questions.

# Usage

See also

See the [Quickstart](docs/quickstart.html) for more quick information on how to use Sentence Transformers.

Working with Sentence Transformer models is straightforward:

Embedding Models

Text

```
from sentence_transformers import SentenceTransformer

# 1. Load a pretrained Sentence Transformer modelmodel = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# The sentences to encodesentences = [
    "The weather is lovely today.",
    "It's so sunny outside!",
    "He drove to the stadium.",]

# 2. Calculate embeddings by calling model.encode()embeddings = model.encode(sentences)print(embeddings.shape)# [3, 384]

# 3. Calculate the embedding similaritiessimilarities = model.similarity(embeddings, embeddings)print(similarities)# tensor([[1.0000, 0.6660, 0.1046],#         [0.6660, 1.0000, 0.1411],#         [0.1046, 0.1411, 1.0000]])
```

 Multimodal

```
from sentence_transformers import SentenceTransformer

# 1. Load a model that supports both text and imagesmodel = SentenceTransformer("Qwen/Qwen3-VL-Embedding-2B")

# 2. Encode images from URLsimg_embeddings = model.encode([
    "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/tasks/car.jpg",
    "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/bee.jpg",])

# 3. Encode text queries (one matching + one hard negative per image)text_embeddings = model.encode([
    "A green car parked in front of a yellow building",
    "A red car driving on a highway",
    "A bee on a pink flower",
    "A wasp on a wooden table",])

# 4. Compute cross-modal similaritiessimilarities = model.similarity(text_embeddings, img_embeddings)print(similarities)# tensor([[0.5115, 0.1078],#         [0.1999, 0.1108],#         [0.1255, 0.6749],#         [0.1283, 0.2704]])
```

 Reranker Models

Text

```
from sentence_transformers import CrossEncoder

# 1. Load a pretrained CrossEncoder modelmodel = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")

# The texts for which to predict similarity scoresquery = "How many people live in Berlin?"passages = [
    "Berlin had a population of 3,520,031 registered inhabitants in an area of 891.82 square kilometers.",
    "Berlin has a yearly total of about 135 million day visitors, making it one of the most-visited cities in the European Union.",
    "In 2013 around 600,000 Berliners were registered in one of the more than 2,300 sport and fitness clubs.",]

# 2a. Either predict scores pairs of textsscores = model.predict([(query, passage) for passage in passages])print(scores)# => [8.607139 5.506266 6.352977]

# 2b. Or rank a list of passages for a queryranks = model.rank(query, passages, return_documents=True)

print("Query:", query)for rank in ranks:
    print(f"- #{rank['corpus_id']} ({rank['score']:.2f}): {rank['text']}")"""Query: How many people live in Berlin?- #0 (8.61): Berlin had a population of 3,520,031 registered inhabitants in an area of 891.82 square kilometers.- #2 (6.35): In 2013 around 600,000 Berliners were registered in one of the more than 2,300 sport and fitness clubs.- #1 (5.51): Berlin has a yearly total of about 135 million day visitors, making it one of the most-visited cities in the European Union."""
```

 Multimodal

```
from sentence_transformers import CrossEncoder

# 1. Load a multimodal CrossEncoder modelmodel = CrossEncoder("Qwen/Qwen3-VL-Reranker-2B")

# 2. Rank images by relevance to a text queryquery = "A green car parked in front of a yellow building"documents = [
    # Image documents (URL or local file path)
    "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/tasks/car.jpg",
    "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/bee.jpg",
    # Text document
    "A vintage Volkswagen Beetle painted in bright green sits in a driveway.",
    # Combined text + image document
    {
        "text": "A car in a European city",
        "image": "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/tasks/car.jpg",
    },]

rankings = model.rank(query, documents)for rank in rankings:
    print(f"{rank['score']:.4f}\t(document {rank['corpus_id']})")"""0.9375  (document 0)0.5000  (document 3)-1.2500 (document 2)-2.4375 (document 1)"""
```

 Sparse Encoder Models

```
from sentence_transformers import SparseEncoder

# 1. Load a pretrained SparseEncoder modelmodel = SparseEncoder("naver/splade-cocondenser-ensembledistil")

# The sentences to encodesentences = [
    "The weather is lovely today.",
    "It's so sunny outside!",
    "He drove to the stadium.",]

# 2. Calculate sparse embeddings by calling model.encode()embeddings = model.encode(sentences)print(embeddings.shape)# [3, 30522] - sparse representation with vocabulary size dimensions

# 3. Calculate the embedding similaritiessimilarities = model.similarity(embeddings, embeddings)print(similarities)# tensor([[   35.629,     9.154,     0.098],#         [    9.154,    27.478,     0.019],#         [    0.098,     0.019,    29.553]])

# 4. Check sparsity statsstats = SparseEncoder.sparsity(embeddings)print(f"Sparsity: {stats['sparsity_ratio']:.2%}")# Sparsity: 99.84%
```

 Multi-Vector Encoder Models

Text

```
from sentence_transformers import MultiVectorEncoder

# 1. Load a pretrained MultiVectorEncoder modelmodel = MultiVectorEncoder("lightonai/LateOn")

queries = ["What is the capital of France?"]documents = [
    "Paris is the capital of France.",
    "Berlin is the capital of Germany.",]

# 2. Encode queries and documents (note the asymmetric encode_query / encode_document split)query_embeddings = model.encode_query(queries)document_embeddings = model.encode_document(documents)

# Each entry is a 2D tensor of shape (num_tokens_i, embedding_dim), variable-length per input.print(query_embeddings[0].shape)# torch.Size([10, 128])

# 3. Score with MaxSimscores = model.similarity(query_embeddings, document_embeddings)print(scores)# tensor([[9.1129, 8.8769]], device='cuda:0')
```

 Multimodal

```
from sentence_transformers import MultiVectorEncoder

# 1. Load a model that matches text queries against page images, no OCR stepmodel = MultiVectorEncoder("vidore/colqwen2.5-v0.2")

queries = [
    "What is the variable represented on the y-axis of the graph?",
    "Total outlay is maximum in which year?",]# Image documents are passed as URLs, local paths, or PIL imagesimages = [
    "https://huggingface.co/datasets/sentence-transformers/example-documents/resolve/main/doc1.jpg",
    "https://huggingface.co/datasets/sentence-transformers/example-documents/resolve/main/doc2.jpg",
    "https://huggingface.co/datasets/sentence-transformers/example-documents/resolve/main/doc3.jpg",
    "https://huggingface.co/datasets/sentence-transformers/example-documents/resolve/main/doc4.jpg",]

# 2. Encode with the same two calls as for textquery_embeddings = model.encode_query(queries)document_embeddings = model.encode_document(images)

# A page yields far more vectors than a query: one per image patchprint(query_embeddings[0].shape, document_embeddings[0].shape)# torch.Size([25, 128]) torch.Size([755, 128])

# 3. Score query text tokens against document image patches with MaxSimscores = model.similarity(query_embeddings, document_embeddings)print(scores)# tensor([[13.8672, 12.3115, 12.1670, 11.0293],#         [ 7.2012, 14.7207,  6.9414,  6.9746]])
```

# What Next?

Consider reading one of the following sections to answer the related questions:

* Embedding Models:
  :   + How to **use** Sentence Transformer models? [Sentence Transformers > Usage](docs/sentence_transformer/usage/usage.html)
      + What Sentence Transformer **models** can I use? [Sentence Transformers > Pretrained Models](docs/sentence_transformer/pretrained_models.html)
      + How do I make Sentence Transformer models **faster** ? [Sentence Transformers > Usage > Speeding up Inference](docs/sentence_transformer/usage/efficiency.html)
      + How do I **train/finetune** a Sentence Transformer model? [Sentence Transformers > Training Overview](docs/sentence_transformer/training_overview.html)
* Reranker Models:
  :   + How to **use** Cross Encoder models? [Cross Encoder > Usage](docs/cross_encoder/usage/usage.html)
      + What Cross Encoder **models** can I use? [Cross Encoder > Pretrained Models](docs/cross_encoder/pretrained_models.html)
      + How do I make Cross Encoder models **faster** ? [Cross Encoder > Usage > Speeding up Inference](docs/cross_encoder/usage/efficiency.html)
      + How do I **train/finetune** a Cross Encoder model? [Cross Encoder > Training Overview](docs/cross_encoder/training_overview.html)
* Sparse Encoder Models:
  :   + How to **use** Sparse Encoder models? [Sparse Encoder > Usage](docs/sparse_encoder/usage/usage.html)
      + What Sparse Encoder **models** can I use? [Sparse Encoder > Pretrained Models](docs/sparse_encoder/pretrained_models.html)
      + How do I make Sparse Encoder models **faster** ? [Sparse Encoder > Usage > Speeding up Inference](docs/sparse_encoder/usage/efficiency.html)
      + How do I **train/finetune** a Sparse Encoder model? [Sparse Encoder > Training Overview](docs/sparse_encoder/training_overview.html)
      + How do I **integrate** Sparse Encoder models with search engines? [Sparse Encoder > Vector Database Integration](examples/sparse_encoder/applications/semantic_search/README.html#vector-database-search)
* Multi-Vector Encoder Models:
  :   + How to **use** Multi-Vector Encoder models? [Multi-Vector Encoder > Usage](docs/multi_vector_encoder/usage/usage.html)
      + What Multi-Vector Encoder **models** can I use? [Multi-Vector Encoder > Pretrained Models](docs/multi_vector_encoder/pretrained_models.html)
      + How do I make Multi-Vector Encoder models **faster** ? [Multi-Vector Encoder > Usage > Speeding up Inference](docs/multi_vector_encoder/usage/efficiency.html)
      + How do I **train/finetune** a Multi-Vector Encoder model? [Multi-Vector Encoder > Training Overview](docs/multi_vector_encoder/training_overview.html)

# Companion Blog Posts

The following Hugging Face blog posts complement this documentation with narrative walkthroughs and full training examples:

* Training guides:

  > + [Training and Finetuning Embedding Models](https://huggingface.co/blog/train-sentence-transformers) : end-to-end training of bi-encoder embedding models.
  > + [Training and Finetuning Reranker Models](https://huggingface.co/blog/train-reranker) : training Cross Encoder (reranker) models.
  > + [Training and Finetuning Sparse Embedding Models](https://huggingface.co/blog/train-sparse-encoder) : training SPLADE and other sparse encoders.
* Multimodal:

  > + [Multimodal Embedding & Reranker Models](https://huggingface.co/blog/multimodal-sentence-transformers) : text, image, audio, and video models through a single API.
  > + [Training and Finetuning Multimodal Embedding & Reranker Models](https://huggingface.co/blog/train-multimodal-sentence-transformers) : finetuning a multimodal embedding model for Visual Document Retrieval.
* Efficiency techniques:

  > + [Introduction to Matryoshka Embedding Models](https://huggingface.co/blog/matryoshka) : variable-size embeddings that truncate gracefully.
  > + [Train 400x faster Static Embedding Models](https://huggingface.co/blog/static-embeddings) : attention-free CPU-friendly embedding models.
  > + [Binary and Scalar Embedding Quantization for Significantly Faster & Cheaper Retrieval](https://huggingface.co/blog/embedding-quantization) : post-training compression of embedding vectors.

# Citing

If you find this repository helpful, feel free to cite our publication [Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks](https://huggingface.co/papers/1908.10084) :

> ```
> @inproceedings{reimers-2019-sentence-bert,  title = "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks",  author = "Reimers, Nils and Gurevych, Iryna",  booktitle = "Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing",  month = "11",  year = "2019",  publisher = "Association for Computational Linguistics",  url = "https://arxiv.org/abs/1908.10084",}
> ```

If you use one of the multilingual models, feel free to cite our publication [Making Monolingual Sentence Embeddings Multilingual using Knowledge Distillation](https://huggingface.co/papers/2004.09813) :

> ```
> @inproceedings{reimers-2020-multilingual-sentence-bert,  title = "Making Monolingual Sentence Embeddings Multilingual using Knowledge Distillation",  author = "Reimers, Nils and Gurevych, Iryna",  booktitle = "Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing",  month = "11",  year = "2020",  publisher = "Association for Computational Linguistics",  url = "https://arxiv.org/abs/2004.09813",}
> ```

If you use the code for [data augmentation](https://github.com/huggingface/sentence-transformers/tree/main/examples/sentence_transformer/training/data_augmentation) , feel free to cite our publication [Augmented SBERT: Data Augmentation Method for Improving Bi-Encoders for Pairwise Sentence Scoring Tasks](https://huggingface.co/papers/2010.08240) :

> ```
> @inproceedings{thakur-2020-AugSBERT,  title = "Augmented {SBERT}: Data Augmentation Method for Improving Bi-Encoders for Pairwise Sentence Scoring Tasks",  author = "Thakur, Nandan and Reimers, Nils and Daxenberger, Johannes  and Gurevych, Iryna",  booktitle = "Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies",  month = jun,  year = "2021",  address = "Online",  publisher = "Association for Computational Linguistics",  url = "https://www.aclweb.org/anthology/2021.naacl-main.28",  pages = "296--310",}
> ```
