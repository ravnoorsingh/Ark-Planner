---
library: "pypdf"
query: "Build a production RAG service that ingests PDF manuals, chunks and embeds them into a vector database, and exposes a FastAPI endpoint that answers questions with citations back to the source page. Use pypdf for extraction and Pydantic models for request and response validation. Include streaming responses and health checks. Use pymilvus for the vector database."
url: "https://pypdf.readthedocs.io/"
resolved_url: "https://pypdf.readthedocs.io/en/stable/"
role: "primary"
rank: 0
fetched_at: "2026-08-19T12:36:05.550316+00:00"
fetched_via: "brightdata-collector:c_msx9i6aq2bz5dznadk"
sha256: "6d2fc092d79c814a03942e763c4ad836ff9d2310cc03f7ed96a2524a358cb5eb"
---

# Welcome to pypdf

pypdf is a [free](https://en.wikipedia.org/wiki/Free_software) and open source pure-python PDF library capable of splitting, merging, cropping, and transforming the pages of PDF files. It can also add custom data, viewing options, and passwords to PDF files. pypdf can retrieve text and metadata from PDFs as well.

See [pdfly](https://github.com/py-pdf/pdfly) for a CLI application that uses pypdf to interact with PDFs.

You can contribute to [pypdf on GitHub](https://github.com/py-pdf/pypdf) .

User Guide

* [Installation](user/installation.html)
* [Robustness and strict=False](user/robustness.html)
* [Security](user/security.html)
* [Exceptions, Warnings, and Log messages](user/suppress-warnings.html)
* [Metadata](user/metadata.html)
* [Extract Text from a PDF](user/extract-text.html)
* [Post-Processing of Text Extraction](user/post-processing-in-text-extraction.html)
* [Extract Images](user/extract-images.html)
* [Handle Attachments](user/handle-attachments.html)
* [Encryption and Decryption of PDFs](user/encryption-decryption.html)
* [Merging PDF files](user/merging-pdfs.html)
* [Cropping and Transforming PDFs](user/cropping-and-transforming.html)
* [Reading PDF Annotations](user/reading-pdf-annotations.html)
* [Adding PDF Annotations](user/adding-pdf-annotations.html)
* [Adding a Stamp or Watermark to a PDF](user/add-watermark.html)
* [Adding JavaScript to a PDF](user/add-javascript.html)
* [Adding Viewer Preferences](user/viewer-preferences.html)
* [Interactions with PDF Forms](user/forms.html)
* [Handling Outlines](user/handling-outlines.html)
* [Streaming Data with pypdf](user/streaming-data.html)
* [Reduce PDF File Size](user/file-size.html)
* [PDF Version Support](user/pdf-version-support.html)
* [PDF/A Compliance](user/pdfa-compliance.html)

API Reference

* [The PdfReader Class](modules/PdfReader.html)
* [The PdfWriter Class](modules/PdfWriter.html)
* [The Destination Class](modules/Destination.html)
* [The DocumentInformation Class](modules/DocumentInformation.html)
* [The Field Class](modules/Field.html)
* [The Fit Class](modules/Fit.html)
* [The PageObject Class](modules/PageObject.html)
* [The PageRange Class](modules/PageRange.html)
* [The PaperSize Class](modules/PaperSize.html)
* [The RectangleObject Class](modules/RectangleObject.html)
* [The Transformation Class](modules/Transformation.html)
* [The XmpInformation Class](modules/XmpInformation.html)
* [Actions](modules/actions.html)
* [The annotations module](modules/annotations.html)
* [Constants](modules/constants.html)
* [Errors](modules/errors.html)
* [Generic PDF objects](modules/generic.html)
* [The PdfDocCommon Class](modules/PdfDocCommon.html)

Developer Guide

* [Developer Intro](dev/intro.html)
* [The PDF Format](dev/pdf-format.html)
* [How pypdf parses PDF files](dev/pypdf-parsing.html)
* [How pypdf writes PDF files](dev/pypdf-writing.html)
* [CMaps](dev/cmaps.html)
* [The Deprecation Process](dev/deprecations.html)
* [Documentation](dev/documentation.html)
* [Testing](dev/testing.html)
* [Releasing](dev/releasing.html)

About pypdf

* [CHANGELOG](meta/CHANGELOG.html)
* [Changelog of PyPDF2 1.X](meta/changelog-v1.html)
* [Migration Guide: 1.x to 2.x](meta/migration-1-to-2.html)
* [Project Governance](meta/project-governance.html)
* [Taking Ownership of pypdf](meta/taking-ownership.html)
* [History of pypdf](meta/history.html)
* [Contributors](meta/CONTRIBUTORS.html)
* [Scope of pypdf](meta/scope-of-pypdf.html)
* [pypdf vs X](meta/comparisons.html)
* [Frequently Asked Questions](meta/faq.html)

# Indices and tables

* [Index](genindex.html)
* [Module Index](py-modindex.html)
* [Search Page](search.html)
