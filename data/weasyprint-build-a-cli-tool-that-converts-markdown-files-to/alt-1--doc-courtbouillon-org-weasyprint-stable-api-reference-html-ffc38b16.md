---
library: "weasyprint"
query: "Build a CLI tool that converts markdown files to styled PDFs with a table of contents. Use markdown for the markdown parser. Use weasyprint for the pdf generator. Use click for the cli framework."
url: "https://doc.courtbouillon.org/weasyprint/stable/api_reference.html"
role: "alternate"
rank: 1
fetched_at: "2026-08-21T07:20:24.888655+00:00"
fetched_via: "brightdata-collector:c_msx9i6aq2bz5dznadk"
sha256: "2e736acd2416cd65b247a2e316da5f8e3d1f2dd331bbd7c69833b6143424ac14"
---

# API Reference

This page is for WeasyPrint ‘stable’. See  [changelog](changelog.html)  for older versions.

## API Stability

Everything described here is considered “public”: this is what you can rely on. We will try to maintain backward-compatibility, and we really often do, but there is no hard promise.

Anything else should not be used outside of WeasyPrint itself. We reserve the right to change it or remove it at any point. Use it at your own risk, or have dependency to a specific WeasyPrint version.

## Versioning

WeasyPrint provides frequent major releases, and minor releases with only bug fixes. Versioning is close to what many browsers do, including Firefox and Chrome: big major numbers, small minor numbers.

Even if each version does not break the API, each version does break the way documents are rendered, which is what really matters at the end. Providing minor versions would give the illusion that developers can just update WeasyPrint without checking that everything works.

Unfortunately, we have the same problem as the other browsers: when a new version is released, most of the user’s websites are rendered exactly the same, but a small part is not. And the only ways to know that, for web developers, are to read the changelog and to check that their pages are correctly rendered.

More about this choice can be found in issue [#900](https://github.com/Kozea/WeasyPrint/issues/900) .

## Command-line API

weasyprint.\_\_main\_\_. main ( *argv = sys.argv* )
:   The `weasyprint` program takes at least two arguments:

    > ```
    > weasyprint [options]
    > ```

    input
    :   URL or filename of the HTML input, or - for stdin.

    output
    :   Filename where output is written, or - for stdout.

    -i , --info
    :   Print system information and exit.

    --version
    :   Print WeasyPrint’s version number and exit.

    ### Rendering options

    -s <stylesheet> , --stylesheet <stylesheet>
    :   URL or filename for a user CSS stylesheet.

        This option can be passed multiple times.

    -a <attachment> , --attachment <attachment>
    :   URL or filename of a file to attach to the PDF document.

        This option can be passed multiple times.

    --attachment-relationship <attachment-relationship>
    :   Relationship of the attachment file to attach to the PDF.

        This option can be passed multiple times.

    --pdf-identifier <pdf-identifier>
    :   PDF file identifier.

    --pdf-variant <pdf-variant>
    :   PDF variant to generate.

        Possible choices: pdf/a-1b, pdf/a-2b, pdf/a-3b, pdf/a-2u, pdf/a-3u, pdf/a-4u, pdf/a-1a, pdf/a-2a, pdf/a-3a, pdf/a-4e, pdf/a-4f, pdf/ua-1, pdf/ua-2, pdf/x-1a, pdf/x-3, pdf/x-4, pdf/x-5g, debug.

    --pdf-version <pdf-version>
    :   PDF version number.

    --pdf-forms
    :   Include PDF forms.

    --pdf-tags
    :   Tag PDF for accessibility.

    --uncompressed-pdf
    :   Do not compress PDF content, mainly for debugging purpose.

    --xmp-metadata <xmp-metadata>
    :   URL or filename of a file to include into the XMP metadata.

        This option can be passed multiple times.

    --custom-metadata
    :   Include custom HTML meta tags in PDF metadata.

    --output-intent <output-intent>
    :   Srgb, device-cmyk, or CSS identifier of the output intent color space.

    -p , --presentational-hints
    :   Follow HTML presentational hints.

    --optimize-images
    :   Optimize size of embedded images with no quality loss.

    -j <jpeg-quality> , --jpeg-quality <jpeg-quality>
    :   JPEG quality between 0 (worst) to 95 (best).

    -D <dpi> , --dpi <dpi>
    :   Set maximum resolution of images embedded in the PDF.

    --full-fonts
    :   Embed unmodified font files when possible.

    --hinting
    :   Keep hinting information in embedded fonts.

    -c <cache-folder> , --cache-folder <cache-folder>
    :   Store cache on disk instead of memory, folder is created if needed and cleaned after the PDF is generated.

    ### HTML options

    -e <encoding> , --encoding <encoding>
    :   Force the input character encoding.

    -m <media-type> , --media-type <media-type>
    :   Media type to use for @media, defaults to print.

    -u <base-url> , --base-url <base-url>
    :   Base for relative URLs in the HTML input, defaults to the input’s own filename or URL or the current directory for stdin.

    ### URL fetcher options

    -t <timeout> , --timeout <timeout>
    :   Set timeout in seconds for HTTP requests.

    --allowed-protocols <allowed-protocols>
    :   Only authorize comma-separated list of protocols for fetching URLs.

    --no-http-redirects
    :   Do not follow HTTP redirects.

    --fail-on-http-errors
    :   Abort document rendering on any HTTP error.

## Python API

*class* weasyprint. HTML ( *input* , *\*\* kwargs* )
:   HTML document parsed by tinyhtml5.

    You can just create an instance with a positional argument: `doc = HTML(something)` The class will try to guess if the input is a filename, an absolute URL, or a  [file object](https://docs.python.org/3/glossary.html#term-file-object "(in Python v3.14)")  .

    Alternatively, use **one** named argument so that no guessing is involved:

    Parameters :
    :   * **filename** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")   *or*   [*pathlib.Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path "(in Python v3.14)")  ) – A filename, relative to the current directory, or absolute.
        * **url** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – An absolute, fully qualified URL.
        * **file\_obj** (  [file object](https://docs.python.org/3/glossary.html#term-file-object "(in Python v3.14)")  ) – Any object with a `read` method.
        * **string** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – A string of HTML source.

    Specifying multiple inputs is an error: `HTML(filename="foo.html", url="localhost://bar.html")` will raise a  [`TypeError`](https://docs.python.org/3/library/exceptions.html#TypeError "(in Python v3.14)")  .

    You can also pass optional named arguments:

    Parameters :
    :   * **encoding** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – Force the source character encoding.
        * **base\_url** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")   *or*   [*pathlib.Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path "(in Python v3.14)")  ) – The base used to resolve relative URLs (e.g. in `<img src="../foo.png">` ). If not provided, try to use the input filename, URL, or `name` attribute of  [file objects](https://docs.python.org/3/glossary.html#term-file-object "(in Python v3.14)")  .
        * **url\_fetcher** (  [callable](https://docs.python.org/3/glossary.html#term-callable "(in Python v3.14)")  ) – An instance of  [`urls.URLFetcher`](#weasyprint.urls.URLFetcher "weasyprint.urls.URLFetcher")  . (See  [URL Fetchers](first_steps.html#url-fetchers)  .)
        * **media\_type** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – The media type to use for `@media` . Defaults to `'print'` . **Note:** In some cases like `HTML(string=foo)` relative URLs will be invalid if `base_url` is not provided.

    render ( *font\_config = None* , *counter\_style = None* , *color\_profiles = None* , *\*\* options* )
    :   Lay out and paginate the document, but do not (yet) export it.

        This returns a  [`document.Document`](#weasyprint.document.Document "weasyprint.document.Document")  object which provides access to individual pages and various meta-data. See  [`write_pdf()`](#weasyprint.HTML.write_pdf "weasyprint.HTML.write_pdf")  to get a PDF directly.

        Parameters :
        :   * **font\_config** (  [`text.fonts.FontConfiguration`](#weasyprint.text.fonts.FontConfiguration "weasyprint.text.fonts.FontConfiguration")  ) – A font configuration handling `@font-face` rules.
            * **counter\_style** (  [`css.counters.CounterStyle`](#weasyprint.css.counters.CounterStyle "weasyprint.css.counters.CounterStyle")  ) – A dictionary storing `@counter-style` rules.
            * **options** – The `options` parameter includes by default the  [`DEFAULT_OPTIONS`](#weasyprint.DEFAULT_OPTIONS "weasyprint.DEFAULT_OPTIONS")  values.

        Returns :
        :   A  [`document.Document`](#weasyprint.document.Document "weasyprint.document.Document")  object.

    write\_pdf ( *target = None* , *zoom = 1* , *finisher = None* , *font\_config = None* , *counter\_style = None* , *color\_profiles = None* , *\*\* options* )
    :   Render the document to a PDF file.

        This is a shortcut for calling  [`render()`](#weasyprint.HTML.render "weasyprint.HTML.render")  , then  [`Document.write_pdf()`](#weasyprint.document.Document.write_pdf "weasyprint.document.Document.write_pdf")  .

        Parameters :
        :   * **target** (  [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ,  [`pathlib.Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path "(in Python v3.14)")  or  [file object](https://docs.python.org/3/glossary.html#term-file-object "(in Python v3.14)")  ) – A filename where the PDF file is generated, a file object, or  [`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")  .
            * **zoom** (  [*float*](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")  ) – The zoom factor in PDF units per CSS units. **Warning** : All CSS units are affected, including physical units like `cm` and named sizes like `A4` . For values other than 1, the physical CSS units will thus be “wrong”.
            * **finisher** (  [callable](https://docs.python.org/3/glossary.html#term-callable "(in Python v3.14)")  ) – A finisher function or callable that accepts the document and a  [`pydyf.PDF`](https://doc.courtbouillon.org/pydyf/stable/api_reference.html#pydyf.PDF "(in pydyf v'stable')")  object as parameters. Can be passed to perform post-processing on the PDF right before the trailer is written.
            * **font\_config** (  [`text.fonts.FontConfiguration`](#weasyprint.text.fonts.FontConfiguration "weasyprint.text.fonts.FontConfiguration")  ) – A font configuration handling `@font-face` rules.
            * **counter\_style** (  [`css.counters.CounterStyle`](#weasyprint.css.counters.CounterStyle "weasyprint.css.counters.CounterStyle")  ) – A dictionary storing `@counter-style` rules.
            * **options** – The `options` parameter includes by default the  [`DEFAULT_OPTIONS`](#weasyprint.DEFAULT_OPTIONS "weasyprint.DEFAULT_OPTIONS")  values.

        Returns :
        :   The PDF as  [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)")  if `target` is not provided or  [`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")  , otherwise  [`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")  (the PDF is written to `target` ).

*class* weasyprint. CSS ( *input* , *\*\* kwargs* )
:   CSS stylesheet parsed by tinycss2.

    An instance is created in the same way as  [`HTML`](#weasyprint.HTML "weasyprint.HTML")  , with the same arguments.

    An additional argument called `font_config` must be provided to handle `@font-face` rules. The same `text.fonts.FontConfiguration` object must be used for different `CSS` objects applied to the same document.

    `CSS` objects have no public attributes or methods. They are only meant to be used in the  [`HTML.write_pdf()`](#weasyprint.HTML.write_pdf "weasyprint.HTML.write_pdf")  and  [`HTML.render()`](#weasyprint.HTML.render "weasyprint.HTML.render")  methods of  [`HTML`](#weasyprint.HTML "weasyprint.HTML")  objects.

*class* weasyprint. Attachment ( *input* , *\*\* kwargs* )
:   File attachment for a PDF document.

    An instance is created in the same way as  [`HTML`](#weasyprint.HTML "weasyprint.HTML")  , except that the HTML specific arguments ( `encoding` and `media_type` ) are not supported.

    Parameters :
    :   * **name** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – The name of the attachment to be included in the PDF document. May be  [`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")  .
        * **description** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – A description of the attachment to be included in the PDF document. May be  [`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")  .
        * **created** (  [`datetime.datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)")  ) – Creation date and time. Default is current date and time.
        * **modified** (  [`datetime.datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)")  ) – Modification date and time. Default is current date and time.
        * **relationship** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – A string that represents the relationship between the attachment and the PDF it is embedded in. Default is ‘Unspecified’, other common values are defined in ISO-32000-2:2020, 7.11.3.

weasyprint. DEFAULT\_OPTIONS *= {'attachment\_relationships': None, 'attachments': None, 'cache': None, 'custom\_metadata': False, 'dpi': None, 'full\_fonts': False, 'hinting': False, 'jpeg\_quality': None, 'optimize\_images': False, 'output\_intent': None, 'pdf\_forms': None, 'pdf\_identifier': None, 'pdf\_tags': False, 'pdf\_variant': None, 'pdf\_version': None, 'presentational\_hints': False, 'stylesheets': None, 'uncompressed\_pdf': False, 'xmp\_metadata': None}*
:   Default values for command-line and Python API rendering options. See  [`__main__.main()`](#weasyprint.__main__.main "weasyprint.__main__.main")  to learn more about specific options for command-line.

    Parameters :
    :   * **stylesheets** (  [*list*](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")  ) – An optional list of user stylesheets. The list can include are  [`CSS`](#weasyprint.CSS "weasyprint.CSS")  objects, filenames, URLs, or file-like objects. (See  [Stylesheet Origins](#stylesheet-origins)  .)
        * **media\_type** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – Media type to use for @media.
        * **attachments** (  [*list*](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")  ) – A list of additional file attachments for the generated PDF document or  [`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")  . The list’s elements are  [`Attachment`](#weasyprint.Attachment "weasyprint.Attachment")  objects, filenames, URLs or file-like objects.
        * **pdf\_identifier** (  [*bytes*](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)")  ) – A bytestring used as PDF file identifier.
        * **pdf\_variant** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – A PDF variant name.
        * **pdf\_version** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – A PDF version number.
        * **pdf\_forms** (  [*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")  ) – Whether PDF forms have to be included.
        * **pdf\_tags** (  [*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")  ) – Whether PDF should be tagged for accessibility.
        * **uncompressed\_pdf** (  [*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")  ) – Whether PDF content should be compressed.
        * **custom\_metadata** (  [*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")  ) – Whether custom HTML metadata should be stored in the generated PDF.
        * **presentational\_hints** (  [*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")  ) – Whether HTML presentational hints are followed.
        * **output\_intent** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – srgb, device-cmyk, or CSS identifier of the output intent color space.
        * **optimize\_images** (  [*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")  ) – Whether size of embedded images should be optimized, with no quality loss.
        * **jpeg\_quality** (  [*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")  ) – JPEG quality between 0 (worst) to 95 (best).
        * **dpi** (  [*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")  ) – Maximum resolution of images embedded in the PDF.
        * **full\_fonts** (  [*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")  ) – Whether unmodified font files should be embedded when possible.
        * **hinting** (  [*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")  ) – Whether hinting information should be kept in embedded fonts.
        * **cache** (  [`dict`](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)")  ,  [`pathlib.Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path "(in Python v3.14)")  or  [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – A dictionary used to cache images in memory, or a folder path where images are temporarily stored.

*class* weasyprint.document. Document ( *pages* , *metadata* , *url\_fetcher* , *font\_config* , *color\_profiles* , *output\_intent* )
:   A rendered document ready to be painted in a pydyf stream.

    Typically obtained from  [`HTML.render()`](#weasyprint.HTML.render "weasyprint.HTML.render")  , but can also be instantiated directly with a list of  [`pages`](#weasyprint.document.Page "weasyprint.document.Page")  , a set of  [`metadata`](#weasyprint.document.DocumentMetadata "weasyprint.document.DocumentMetadata")  , a  [`url_fetcher`](#weasyprint.urls.URLFetcher "weasyprint.urls.URLFetcher")  , and a  [`font_config`](#weasyprint.text.fonts.FontConfiguration "weasyprint.text.fonts.FontConfiguration")  .

    copy ( *pages = 'all'* )
    :   Take a subset of the pages.

        Parameters :
        :   **pages** (  [iterable](https://docs.python.org/3/glossary.html#term-iterable "(in Python v3.14)")  ) – An iterable of  [`Page`](#weasyprint.document.Page "weasyprint.document.Page")  objects from  [`pages`](#weasyprint.document.Document.pages "weasyprint.document.Document.pages")  .

        Returns :
        :   A new  [`Document`](#weasyprint.document.Document "weasyprint.document.Document")  object.

        Examples:

        Write two PDF files for odd-numbered and even-numbered pages:

        ```
        # Python lists count from 0 but pages are numbered from 1.# [::2] is a slice of even list indexes but odd-numbered pages.document.copy(document.pages[::2]).write_pdf('odd_pages.pdf')document.copy(document.pages[1::2]).write_pdf('even_pages.pdf')
        ```

        Combine multiple documents into one PDF file, using metadata from the first:

        ```
        all_pages = [p for doc in documents for p in doc.pages]documents[0].copy(all_pages).write_pdf('combined.pdf')
        ```

    fonts
    :   A  [`dict`](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)")  of fonts used by the document. Keys are hashes used to identify fonts, values are `Font` objects.

    make\_bookmark\_tree ( *scale = 1* , *transform\_pages = False* )
    :   Make a tree of all bookmarks in the document.

        Parameters :
        :   * **scale** (  [*float*](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")  ) – Zoom scale.
            * **transform\_pages** (  [*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")  ) – A boolean defining whether the default PDF page transformation matrix has to be applied to bookmark coordinates, setting the bottom-left corner as the origin.

        Returns :
        :   A list of bookmark subtrees. A subtree is `(label, target, children, state)` . `label` is a string, `target` is `(page_number, x, y)` and `children` is a list of child subtrees.

    metadata
    :   A  [`DocumentMetadata`](#weasyprint.document.DocumentMetadata "weasyprint.document.DocumentMetadata")  object. Contains information that does not belong to a specific page but to the whole document.

    pages
    :   A list of  [`Page`](#weasyprint.document.Page "weasyprint.document.Page")  objects.

    url\_fetcher
    :   A  [`weasyprint.urls.URLFetcher`](#weasyprint.urls.URLFetcher "weasyprint.urls.URLFetcher")  object (see  [URL Fetchers](first_steps.html#url-fetchers)  .)

    write\_pdf ( *target = None* , *zoom = 1* , *finisher = None* , *\*\* options* )
    :   Paint the pages in a PDF file, with metadata.

        Parameters :
        :   * **target** (  [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ,  [`pathlib.Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path "(in Python v3.14)")  or  [file object](https://docs.python.org/3/glossary.html#term-file-object "(in Python v3.14)")  ) – A filename where the PDF file is generated, a file object, or  [`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")  .
            * **zoom** (  [*float*](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")  ) – The zoom factor in PDF units per CSS units. **Warning** : All CSS units are affected, including physical units like `cm` and named sizes like `A4` . For values other than 1, the physical CSS units will thus be “wrong”.
            * **finisher** (  [callable](https://docs.python.org/3/glossary.html#term-callable "(in Python v3.14)")  ) – A finisher function or callable that accepts the document and a  [`pydyf.PDF`](https://doc.courtbouillon.org/pydyf/stable/api_reference.html#pydyf.PDF "(in pydyf v'stable')")  object as parameters. Can be passed to perform post-processing on the PDF right before the trailer is written.
            * **options** – The `options` parameter includes by default the  [`weasyprint.DEFAULT_OPTIONS`](#weasyprint.DEFAULT_OPTIONS "weasyprint.DEFAULT_OPTIONS")  values.

        Returns :
        :   The PDF as  [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)")  if `target` is not provided or  [`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")  , otherwise  [`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")  (the PDF is written to `target` ).

*class* weasyprint.document. DocumentMetadata
:   Meta-information belonging to a whole  [`Document`](#weasyprint.document.Document "weasyprint.document.Document")  .

    New attributes may be added in future versions of WeasyPrint.

    attachments
    :   A list of  [`attachments`](#weasyprint.Attachment "weasyprint.Attachment")  , empty by default. Extracted from the `<link rel=attachment>` elements in HTML and written to the `/EmbeddedFiles` dictionary in PDF.

    authors
    :   The authors of the document, as a list of strings. (Defaults to the empty list.) Extracted from the `<meta name=author>` elements in HTML and written to the `/Author` info field in PDF.

    created
    :   The creation date of the document, as a string or  [`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")  . Dates are in one of the six formats specified in [W3C’s profile of ISO 8601](https://www.w3.org/TR/NOTE-datetime) . Extracted from the `<meta name=dcterms.created>` element in HTML and written to the `/CreationDate` info field in PDF.

    custom
    :   Custom metadata, as a dict whose keys are the metadata names and values are the metadata values.

    description
    :   The description of the document, as a string or  [`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")  . Extracted from the `<meta name=description>` element in HTML and written to the `/Subject` info field in PDF.

    generate\_rdf\_metadata ( *variant* , *version* , *conformance* )
    :   Generate RDF metadata as a bytestring.

    generator
    :   The name of one of the software packages used to generate the document, as a string or  [`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")  . Extracted from the `<meta name=generator>` element in HTML and written to the `/Creator` info field in PDF.

    include\_in\_pdf ( *pdf* , *variant* , *version* , *conformance* , *compress* )
    :   Add PDF stream of metadata.

        Described in ISO-32000-1:2008, 14.3.2.

    keywords
    :   Keywords associated with the document, as a list of strings. (Defaults to the empty list.) Extracted from `<meta name=keywords>` elements in HTML and written to the `/Keywords` info field in PDF.

    lang
    :   Document language as BCP 47 language tags. Extracted from `<html lang=lang>` in HTML.

    modified
    :   The modification date of the document, as a string or  [`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")  . Dates are in one of the six formats specified in [W3C’s profile of ISO 8601](https://www.w3.org/TR/NOTE-datetime) . Extracted from the `<meta name=dcterms.modified>` element in HTML and written to the `/ModDate` info field in PDF.

    title
    :   The title of the document, as a string or  [`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")  . Extracted from the `<title>` element in HTML and written to the `/Title` info field in PDF.

    xmp\_metadata
    :   A list of XML bytestrings to add into the XMP metadata.

*class* weasyprint.document. Page
:   Represents a single rendered page.

    Should be obtained from  [`Document.pages`](#weasyprint.document.Document.pages "weasyprint.document.Document.pages")  but not instantiated directly.

    anchors
    :   The  [`dict`](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)")  mapping each anchor name to its target, an `(x, y)` point in CSS pixels from the top-left of the page.

    bleed
    :   The page bleed widths as a  [`dict`](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)")  with `'top'` , `'right'` , `'bottom'` and `'left'` as keys, and values in CSS pixels.

    bookmarks
    :   The  [`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")  of `(level, label, target, state)`  [`tuples`](https://docs.python.org/3/library/stdtypes.html#tuple "(in Python v3.14)")  . `level` and `label` are respectively an  [`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")  and a  [`string`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  , based on the CSS properties of the same names. `target` is an `(x, y)` point in CSS pixels from the top-left of the page.

    forms
    :   The  [`dict`](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)")  mapping form elements to a list of `(element, attributes, rectangle)`  [`tuples`](https://docs.python.org/3/library/stdtypes.html#tuple "(in Python v3.14)")  . A `rectangle` is `(x, y, width, height)` , in CSS pixels from the top-left of the page. `atributes` is a  [`dict`](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)")  of HTML tag attributes and values. The key `None` will contain inputs that are not part of a form.

    height
    :   The page height, including margins, in CSS pixels.

    links
    :   The  [`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")  of `(link_type, target, rectangle, box)`  [`tuples`](https://docs.python.org/3/library/stdtypes.html#tuple "(in Python v3.14)")  . A `rectangle` is `(x, y, width, height)` , in CSS pixels from the top-left of the page. `link_type` is one of three strings:

        * `'external'` : `target` is an absolute URL
        * `'internal'` : `target` is an anchor name (see  [`Page.anchors`](#weasyprint.document.Page.anchors "weasyprint.document.Page.anchors")  ). The anchor might be defined in another page, in multiple pages (in which case the first occurence is used), or not at all.
        * `'attachment'` : `target` is an absolute URL and points to a resource to attach to the document.

    width
    :   The page width, including margins, in CSS pixels.

*class* weasyprint.urls. URLFetcher ( *timeout = 10* , *ssl\_context = None* , *http\_headers = None* , *allowed\_protocols = None* , *allow\_redirects = True* , *fail\_on\_errors = False* , *\*\* kwargs* )
:   Fetcher of external resources such as images or stylesheets.

    Parameters :
    :   * **timeout** (  [*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")  ) – The number of seconds before HTTP requests are dropped.
        * **ssl\_context** (  [*ssl.SSLContext*](https://docs.python.org/3/library/ssl.html#ssl.SSLContext "(in Python v3.14)")  ) – An SSL context used for HTTPS requests.
        * **http\_headers** (  [*dict*](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)")  ) – Additional HTTP headers used for HTTP requests.
        * **allowed\_protocols** (  [sequence](https://docs.python.org/3/glossary.html#term-sequence "(in Python v3.14)")  ) – A set of authorized protocols,  [`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")  means all.
        * **allow\_redirects** (  [*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")  ) – Whether HTTP redirects must be followed.
        * **fail\_on\_errors** (  [*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")  ) – Whether HTTP errors should stop the rendering.

    Another class inheriting from this class, with a `fetch` method that has a compatible signature, can be given as the `url_fetcher` argument to  [`weasyprint.HTML`](#weasyprint.HTML "weasyprint.HTML")  or  [`weasyprint.CSS`](#weasyprint.CSS "weasyprint.CSS")  .

    See  [URL Fetchers](first_steps.html#url-fetchers)  for more information and examples.

    fetch ( *url* , *headers = None* )
    :   Fetch a given URL.

        Returns :
        :   A  [`URLFetcherResponse`](#weasyprint.urls.URLFetcherResponse "weasyprint.urls.URLFetcherResponse")  instance.

        Raises :
        :   An exception indicating failure, e.g.  [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError "(in Python v3.14)")  on syntactically invalid URL. All exceptions are catched internally by WeasyPrint, except when they inherit from  [`FatalURLFetchingError`](#weasyprint.urls.FatalURLFetchingError "weasyprint.urls.FatalURLFetchingError")  .

*class* weasyprint.urls. URLFetcherResponse ( *url* , *body = None* , *headers = None* , *status = 200* , *\*\* kwargs* )
:   The HTTP response of an URL fetcher.

    Parameters :
    :   * **url** (  [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ) – The URL of the HTTP response.
        * **body** (  [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")  ,  [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)")  or  [file object](https://docs.python.org/3/glossary.html#term-file-object "(in Python v3.14)")  ) – The body of the HTTP response.
        * **headers** (  [*dict*](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)")   *or*   [*email.message.EmailMessage*](https://docs.python.org/3/library/email.message.html#email.message.EmailMessage "(in Python v3.14)")  ) – The headers of the HTTP response.
        * **status** (  [*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")  ) – The status of the HTTP response.

    Has the same interface as  [`urllib.response.addinfourl`](https://docs.python.org/3/library/urllib.request.html#urllib.response.addinfourl "(in Python v3.14)")  .

    If a  [file object](https://docs.python.org/3/glossary.html#term-file-object "(in Python v3.14)")  is given for the body, it is the caller’s responsibility to call `close()` on it. The default function used internally to fetch data in WeasyPrint tries to close the file object after retreiving; but if this URL fetcher is used elsewhere, the file object has to be closed manually.

*class* weasyprint.urls. FatalURLFetchingError
:   Some error happened when fetching an URL and must stop the rendering.

*class* weasyprint.text.fonts. FontConfiguration
:   A Fontconfig font configuration.

    Keep a list of fonts, including fonts installed on the system, fonts installed for the current user, and fonts referenced by cascading stylesheets.

    When created, an instance of this class gathers available fonts. It can then be given to  [`weasyprint.HTML`](#weasyprint.HTML "weasyprint.HTML")  methods or to  [`weasyprint.CSS`](#weasyprint.CSS "weasyprint.CSS")  to find fonts in `@font-face` rules.

*class* weasyprint.css.counters. CounterStyle
:   Counter styles dictionary.

    Keep a list of counter styles defined by `@counter-style` rules, indexed by their names.

    See <https://www.w3.org/TR/css-counter-styles-3/> .

## Supported Features

### URLs

WeasyPrint can read normal files, HTTP, FTP and [data URIs](https://en.wikipedia.org/wiki/Data_URI_scheme) . It will follow HTTP redirects but more advanced features like cookies and authentication are currently not supported, although a custom  [URL fetcher](first_steps.html#url-fetchers)  can help.

### HTML

#### Supported HTML Tags

Many HTML elements are implemented in CSS through the HTML5 [User-Agent stylesheet](https://github.com/Kozea/WeasyPrint/blob/main/weasyprint/css/html5_ua.css) .

Some elements need special treatment:

* The `<base>` element, if present, determines the base for relative URLs.
* CSS stylesheets can be embedded in `<style>` elements or linked by `<link rel=stylesheet>` elements.
* `<img>` , `<embed>` or `<object>` elements accept images either in raster formats supported by [Pillow](https://python-pillow.org/) (including PNG, JPEG, GIF, …) or in SVG. SVG images are not rasterized but rendered as vectors in the PDF output.

HTML [presentational hints](https://www.w3.org/TR/html5/rendering.html#presentational-hints) are not supported by default, but most of them can be supported:

* by using the `--presentational-hints` CLI parameter, or
* by setting the `presentational_hints` parameter of the `HTML.render` or `HTML.write_*` methods to `True` .

Presentational hints include a wide array of attributes that direct styling in HTML, including font `color` and `size` , list attributes like `type` and `start` , various table alignment attributes, and others. If the document generated by WeasyPrint is missing some of the features you expect from the HTML, try to enable this option.

#### Stylesheet Origins

HTML documents are rendered with stylesheets from three *origins* :

* The HTML5 [user agent stylesheet](https://github.com/Kozea/WeasyPrint/blob/main/weasyprint/css/html5_ua.css) (defines the default appearance of HTML elements);
* Author stylesheets embedded in the document in `<style>` elements or linked by `<link rel=stylesheet>` elements;
* User stylesheets provided in the API.

Keep in mind that *user* stylesheets have a lower priority than *author* stylesheets in the [cascade](https://www.w3.org/TR/CSS21/cascade.html#cascading-order) , unless you use [!important](https://www.w3.org/TR/CSS21/cascade.html#important-rules) in declarations to raise their priority.

### PDF

In addition to text, raster and vector graphics, WeasyPrint’s PDF files can contain hyperlinks, bookmarks, attachments and forms.

Hyperlinks will be clickable in PDF viewers that support them. They can be either internal, to another part of the same document (eg. `<a href="#pdf">` ) or external, to an URL. External links are resolved to absolute URLs: `<a href="/blog-articles/">` on the CourtBouillon website would always point to <https://www.courtbouillon.org/blog-articles/> in PDF files.

PDF bookmarks are also called outlines and are generally shown in a sidebar. Clicking on an entry scrolls the matching part of the document into view. By default all `<h1>` to `<h6>` titles generate bookmarks, but this can be controlled with [PDF bookmarks](https://www.w3.org/TR/css-content-3/#bookmark-generation) .)

Attachments are related files, embedded in the PDF itself. They can be specified through `<link rel=attachment>` elements to add resources globally or through regular links with `<a rel=attachment>` to attach a resource that can be saved by clicking on said link. The `title` attribute can be used as description of the attachment.

Generated documents can also include PDF forms, using the `appearance: auto` CSS property or the `--pdf-forms` CLI option.

The generation of PDF/A and PDF/UA documents is supported. However, the generated documents are not guaranteed to be valid, and users have the responsibility to check that they follow the rules listed by the related specifications.

### Fonts

WeasyPrint can use any font that [Pango](https://www.pango.org/) can find installed on the system. Fonts are automatically embedded in PDF files and are subset by default to only include the glyphs used in the PDF. Subsetting is done with [hb-subset](https://harfbuzz.github.io/harfbuzz-hb-subset.html) when available on the system, or by the slower [fontTools](https://fonttools.readthedocs.io/en/latest/) library as a fallback.

[Pango](https://www.pango.org/) always uses [Fontconfig](https://www.freedesktop.org/wiki/Software/fontconfig/) to access fonts, even on Windows and macOS. You can list the available fonts thanks to the `fc-list` command, and know which font is matched by a given pattern thanks to `fc-match` . Copying a font file into the `~/.local/share/fonts` directory is generally enough to install a new font. WeasyPrint should support the major font formats handled by [HarfBuzz](https://harfbuzz.github.io/) .

WeasyPrint follows the [Fontconfig](https://www.freedesktop.org/wiki/Software/fontconfig/) configuration of the system. This default configuration is often useful for many cases: font fallbacks for missing glyphs, aliases for standard font families like “serif” or “monospace”, colored variants for emojis, etc. But some of these default rules can sometimes interfere with CSS rules, and it may be interesting to disable them if you need to tweak details about font management.

When a Unicode code point is not supported by a font and its fallbacks, the font’s [.notdef glyph](https://en.wikipedia.org/wiki/Notdef_glyph) is displayed instead, and a warning is displayed in logs. Because of the way Pango handles this case, the .notdef glyph may be rendered with an incorrect width (advance), but the layout of the other glyphs is correct. Text search and selection work as if the glyph was available.

### CSS

WeasyPrint supports many of the [CSS specifications](https://www.w3.org/Style/CSS/current-work) written by the W3C. You will find in this chapter a comprehensive list of the specifications or drafts with at least one feature implemented in WeasyPrint.

#### CSS Level 2 Revision 1

The [CSS Level 2 Revision 1](https://www.w3.org/TR/CSS21/) specification, best known as CSS 2.1, is pretty well supported by WeasyPrint. Since version 0.11, it passes the famous [Acid2 Test](https://www.webstandards.org/files/acid2/test.html) .

The CSS 2.1 features listed here are **not** supported:

* On tables: [visibility: collapse](https://www.w3.org/TR/CSS21/tables.html#dynamic-effects) .
* Minimum and maximum [height](https://www.w3.org/TR/CSS21/visudet.html#min-max-heights) on table-related boxes.
* Minimum and maximum [width](https://www.w3.org/TR/CSS21/visudet.html#min-max-widths) and [height](https://www.w3.org/TR/CSS21/visudet.html#min-max-heights) on page-margin boxes.
* Conforming [font matching algorithm](https://www.w3.org/TR/CSS21/fonts.html#algorithm) . Currently `font-family` is passed as-is to Pango.
* Right-to-left or [bi-directional text](https://www.w3.org/TR/CSS21/visuren.html#direction) .
* [System colors](https://www.w3.org/TR/CSS21/ui.html#system-colors) and [system fonts](https://www.w3.org/TR/CSS21/fonts.html#propdef-font) . The former are deprecated in [CSS Color Module Level 3](https://www.w3.org/TR/css-color-3/) .

To the best of our knowledge, everything else that applies to the print media **is** supported. Please report a bug if you find this list incomplete.

#### Selectors Level 3 / 4

With the exceptions noted here, all [Selectors Level 3](https://www.w3.org/TR/selectors-3/) are supported.

PDF is generally not interactive. The `:hover` , `:active` , `:focus` , `:target` and `:visited` pseudo-classes are accepted as valid but never match anything.

Everything in [Selectors Level 4](https://www.w3.org/TR/selectors-4/) is supported, except:

* `:dir` ,
* input pseudo-classes ( `:valid` , `:invalid` …),
* column selector ( `||` , `:nth-col()` , `:nth-last-col()` ).

#### CSS Text Module Level 3 / 4

The [CSS Text Module Level 3](https://www.w3.org/TR/css-text-3/) and [CSS Text Module Level 4](https://www.w3.org/TR/css-text-4/) are working drafts defining “properties for text manipulation” and covering “line breaking, justification and alignment, white space handling, and text transformation”.

Among their features, some are already included in CSS 2.1, sometimes with missing or different values ( `text-indent` , `text-align` , `letter-spacing` , `word-spacing` , `text-transform` , `white-space` ).

New properties defined in Level 3 are supported:

* the `overflow-wrap` property replacing `word-wrap` ;
* the `break-all` value of the `word-break` property (see [#1153](https://github.com/Kozea/WeasyPrint/issues/1153) );
* the `full-width` value of the `text-transform` property; and
* the `start` , `end` and `justify-all` values of the `text-align` property;
* the `text-align-last` and `text-justify` properties; and
* the `tab-size` property.

Properties controlling [hyphenation](https://www.w3.org/TR/css-text-3/#hyphenation) are supported by WeasyPrint:

* `hyphens` ,
* `hyphenate-character` ,
* `hyphenate-limit-chars` , and
* `hyphenate-limit-zone` .

To get automatic hyphenation, you to set it to `auto` *and* have the `lang` HTML attribute set to one of the languages [supported by Pyphen](https://github.com/Kozea/Pyphen/tree/main/pyphen/dictionaries) .

```
<!doctype html><html lang=en><style>  html { hyphens: auto }</style>

…
```

Automatic hyphenation can be disabled again with the `manual` value:

```
html { hyphens: auto }a[href]::after { content: ' [' attr(href) ']'; hyphens: manual }
```

The other features provided by [CSS Text Module Level 3](https://www.w3.org/TR/css-text-3/) are **not** supported:

* the `line-break` property;
* the `match-parent` value of the `text-align` property;
* the `text-indent` and `hanging-punctuation` properties.

The other features provided by [CSS Text Module Level 4](https://www.w3.org/TR/css-text-4/) are **not** supported:

* the `text-space-collapse` and `text-space-trim` properties;
* the `text-wrap` , `wrap-before` , `wrap-after` and `wrap-inside` properties;
* the `text-align` property with an alignment character;
* the `pre-wrap-auto` value of the `white-space` property; and
* the `text-spacing` property.

#### CSS Fonts Module Level 3 / 4

The [CSS Fonts Module Level 3](https://www.w3.org/TR/css-fonts-3/) is a candidate recommendation describing “how font properties are specified and how font resources are loaded dynamically”.

WeasyPrint supports the `font-size` , `font-stretch` , `font-style` and `font-weight` properties, coming from CSS 2.1.

WeasyPrint also supports the following font features added in Level 3: - `font-kerning` , - `font-variant-ligatures` , - `font-variant-position` , - `font-variant-caps` , - `font-variant-numeric` , - `font-variant-east-asian` , - `font-feature-settings` , and - `font-language-override` .

`font-family` is supported. The string is given to Pango that tries to find a matching font in a way different from what is defined in the recommendation, but that should not be a problem for common use.

The shorthand `font` and `font-variant` properties are supported.

WeasyPrint supports the `@font-face` rule.

WeasyPrint does **not** support the `@font-feature-values` rule and the values of `font-variant-alternates` other than `normal` and `historical-forms` .

From [CSS Fonts Module Level 4](https://www.w3.org/TR/css-fonts-4/) we only support the `font-variation-settings` property enabling specific font variations.

#### CSS Paged Media Module Level 3

The [CSS Paged Media Module Level 3](https://drafts.csswg.org/css-page-3/) is a working draft including features for paged media “describing how:

* page breaks are created and avoided;
* the page properties such as size, orientation, margins, border, and padding are specified;
* headers and footers are established within the page margins;
* content such as page counters are placed in the headers and footers; and
* orphans and widows can be controlled.”

All the features of this draft are available, including:

* the `@page` rule and the `:left` , `:right` , `:first` and `:blank` selectors;
* the page margin boxes;
* the page-based counters (with known limitations [#93](https://github.com/Kozea/WeasyPrint/issues/93) );
* the page `size` , `bleed` and `marks` properties;
* the named pages.

#### CSS Generated Content for Paged Media Module

The [CSS Generated Content for Paged Media Module](https://www.w3.org/TR/css-gcpm-3/) (GCPM) is a working draft defining “new properties and values, so that authors may bring new techniques (running headers and footers, footnotes, page selection) to paged media”.

[Page selectors](https://www.w3.org/TR/css-gcpm-3/#document-page-selectors) are supported by WeasyPrint. You can select pages according to their position in the document:

```
@page :nth(3) { background: red } /* Third page */@page :nth(2n+1) { background: green } /* Odd pages */@page :nth(1 of chapter) { background: blue } /* First pages of chapters */
```

You can also use [running elements](https://www.w3.org/TR/css-gcpm-3/#running-elements) to put HTML boxes into the page margins (but the `start` parameter of `element()` is not supported).

[Footnotes](https://www.w3.org/TR/css-gcpm-3/#footnotes) are supported. You can put a box in the footnote area using the `float: footnote` property. Footnote markers and footnote calls can be defined using the `::footnote-marker` and `::footnote-call` pseudo-elements. You can also change the way footnotes are displayed using the `footnote-display` property ( `compact` is not supported), and influence over the rendering of difficult pages with `footnote-policy` .

#### CSS Generated Content Module Level 3

The [CSS Generated Content Module Level 3](https://www.w3.org/TR/css-content-3/) is a working draft helping “authors [who] sometimes want user agents to render content that does not come from the document tree. One familiar example of this is numbered headings […]. Similarly, authors may want the user agent to insert the word “Figure” before the caption of a figure […], or replacing elements with images or other multimedia content.”

[Named strings](https://www.w3.org/TR/css-content-3/#named-strings) are supported by WeasyPrint. You can define strings related to the first or last element of a type present on a page, and display these strings in page borders. This feature is really useful to add the title of the current chapter at the top of the pages of a book for example.

The named strings can embed static strings, counters, cross-references, tag contents and tag attributes.

```
@top-center { content: string(chapter) }h2 { string-set: chapter "Current chapter: " content() }
```

[Cross-references](https://www.w3.org/TR/css-content-3/#cross-references) retrieve counter or content values from targets (anchors or identifiers) in the current document:

```
a::after { content: ", on page " target-counter(attr(href), page) }a::after { content: ", see " target-text(attr(href)) }
```

In particular, `target-counter()` and `target-text()` are useful when it comes to tables of contents (see [an example](https://github.com/Kozea/WeasyPrint/pull/652#issuecomment-403276559) ).

You can also control [PDF bookmarks](https://www.w3.org/TR/css-content-3/#bookmark-generation) with WeasyPrint. Using the `bookmark-level` , `bookmark-label` and `bookmark-state` properties, you can add bookmarks that will be available in your PDF reader.

Bookmarks have already been added in the WeasyPrint’s [user agent stylesheet](https://github.com/Kozea/WeasyPrint/blob/main/weasyprint/css/html5_ua.css) , so your generated documents will automatically have bookmarks on headers (from `<h1>` to `<h6>` ). But for example, if you have only one top-level `<h1>` and do not wish to include it in the bookmarks, add this in your stylesheet:

```
h1 { bookmark-level: none }
```

[Leaders](https://www.w3.org/TR/css-content-3/#leaders) are also supported:

```
li a::after {    content: ' ' leader(dotted) ' ' target-counter(attr(href), page);}
```

The other features of this module are **not** implemented:

* quotes ( `content: *-quote` );

#### CSS Color Module Level 4 / 5

The [CSS Color Module Level 4](https://www.w3.org/TR/css-color-4/) is a recommendation defining “CSS properties which allow authors to specify the foreground color and opacity of the text content of an element”. Its main goal is to specify how colors are defined, including color keywords and many color notations including `#rgba` , `rgb()` , `hsl()` , `hwb()` , `lab()` , etc. The standard `color()` function gives a common way to define colors giving their color space. Opacity and alpha compositing are also defined in this document.

This recommendation is fully implemented in WeasyPrint, except the deprecated System Colors.

The [CSS Color Module Level 5](https://www.w3.org/TR/css-color-5/) is a working draft adding “color modification functions, custom color spaces (ICC profiles), `contrast-color()` , `light-dark()` and `device-cmyk()` ” to level 4.

WeasyPrint supports the `light-dark()` and `device-cmyk()` properties, and the `@color-profile` at-rule.

WeasyPrint does **not** support the `color-mix()` and `contrast-color()` properties.

#### CSS Transforms Module Level 1

The [CSS Transforms Module Level 1](https://drafts.csswg.org/css-transforms-1/) working draft “describes a coordinate system within each element is positioned. This coordinate space can be modified with the transform property. Using transform, elements can be translated, rotated and scaled in two or three dimensional space.”

WeasyPrint supports the `transform` and `transform-origin` properties, and all the 2D transformations ( `matrix` , `rotate` , `translate` , `translateX` , `translateY` , `scale` , `scaleX` , `scaleY` , `skew` , `skewX` , `skewY` ).

WeasyPrint does **not** support the `transform-style` , `perspective` , `perspective-origin` and `backface-visibility` properties, and all the 3D transformations ( `matrix3d` , `rotate3d` , `rotateX` , `rotateY` , `rotateZ` , `translate3d` , `translateZ` , `scale3d` , `scaleZ` ).

#### CSS Backgrounds and Borders Module Level 3

The [CSS Backgrounds and Borders Module Level 3](#css-backgrounds-and-borders-module-level-3) is a candidate recommendation defining properties dealing “with the decoration of the border area and with the background of the content, padding and border areas”.

The [border part](https://www.w3.org/TR/css-backgrounds-3/#borders) of this module is supported, as it is already included in the the CSS 2.1 specification.

WeasyPrint supports the [background part](https://www.w3.org/TR/css-backgrounds-3/#backgrounds) of this module (allowing multiple background layers per box), including the `background` , `background-color` , `background-image` , `background-repeat` , `background-attachment` , `background-position` , `background-clip` , `background-origin` and `background-size` properties.

WeasyPrint also supports the [rounded corners part](https://www.w3.org/TR/css-backgrounds-3/#corners) of this module, including the `border-radius` property.

WeasyPrint also supports the [border images part](https://www.w3.org/TR/css-backgrounds-3/#border-images) of this module, including the `border-image` , `border-image-source` , `border-image-slice` , `border-image-width` , `border-image-outset` and `border-image-repeat` properties.

WeasyPrint does **not** support the [box shadow part](https://www.w3.org/TR/css-backgrounds-3/#misc) of this module, including the `box-shadow` property. This feature has been implemented in a [git branch](https://github.com/Kozea/WeasyPrint/pull/149) that is not released, as it relies on raster implementation of shadows.

#### CSS Image Values and Replaced Content Module Level 3 / 4

The [Image Values and Replaced Content Module Level 3](https://www.w3.org/TR/css-images-3/) is a candidate recommendation introducing “additional ways of representing 2D images, for example as a list of URIs denoting fallbacks, or as a gradient”, defining “several properties for manipulating raster images and for sizing or positioning replaced elements” and “generic sizing algorithm for replaced elements”.

The [Image Values and Replaced Content Module Level 4](https://www.w3.org/TR/css-images-4/) is a working draft on the same subject.

The `linear-gradient()` , `radial-gradient()` and `repeating-radial-gradient()` properties are supported as background images.

The the `url()` notation is supported, but the `image()` notation is **not** supported for background images.

The `object-fit` and `object-position` properties are supported.

The `from-image` and `snap` values of the `image-resolution` property are **not** supported, but the `resolution` value is supported.

The `image-rendering` and `image-orientation` properties are supported.

#### CSS Box Sizing Module Level 3

The [CSS Box Sizing Module Level 3](https://www.w3.org/TR/css-sizing-3/) is a candidate recommendation extending “the CSS sizing properties with keywords that represent content-based ‘intrinsic’ sizes and context-based ‘extrinsic’ sizes.”

The new property defined in this document is implemented in WeasyPrint: `box-sizing` .

The `min-content` , `max-content` and `fit-content()` sizing values are **not** supported.

#### CSS Overflow Module Level 3

The [CSS Overflow Module Level 3](https://www.w3.org/TR/2020/WD-css-overflow-3-20200603/) is a working draft containing “the features of CSS relating to scrollable overflow handling in visual media.”

The `overflow` property is supported, as defined in CSS2. `overflow-x` , `overflow-y` , `overflow-clip-margin` , `overflow-inline` and `overflow-block` are **not** supported.

The `text-overflow` , `block-ellipsis` , `line-clamp` , `max-lines` and `continue` properties are supported.

#### CSS Values and Units Module Level 3 / 4

The [CSS Values and Units Module Level 3](https://www.w3.org/TR/css3-values/) defines various units and keywords used in “value definition field of each CSS property”.

The [CSS Values and Units Module Level 4](https://www.w3.org/TR/css-values-4/) adds many new units, unit types and math functions.

The `initial` and `inherit` CSS-wide keywords are supported, but the `unset` keyword is **not** supported.

Quoted strings, URLs and numeric data types are supported.

Font-relative lengths ( `*em` , `*ex` , `*ch` , `*cap` , `*ic` , `*lh` ), viewport-relative lengths ( `*vw` , `*vh` , `*vi` , `*vb` , `*vmin` , `*vmax` ), absolute lengths ( `cm` , `mm` , `q` , `in` , `pt` , `pc` , `px` ), angles ( `rad` , `grad` , `turn` , `deg` ), resolutions ( `dpi` , `dpcm` , `dppx` , `x` ) are supported.

Unspecified page-relative units ( `pvw` , `pvh` …) are also supported. They are relative to the whole page size (including page margins), while all the other units are relative to the page area size (without page margins).

The `attr()` functional notation is allowed in the `content` and `string-set` properties.

All the mathematical functions ( `calc()` …) are supported.

#### CSS Multi-column Layout Module

The [CSS Multi-column Layout Module](https://www.w3.org/TR/css-multicol-1/) “describes multi-column layouts in CSS, a style sheet language for the web. Using functionality described in the specification, content can be flowed into multiple columns with a gap and a rule between them.”

Simple multi-column layouts are supported in WeasyPrint. Features such as constrained height, spanning columns or column breaks are **not** supported. Pagination and overflow are not seriously tested.

The `column-width` and `column-count` properties, and the `columns` shorthand property are supported.

The `column-gap` , `column-rule-color` , `column-rule-style` and `column-rule-width` properties, and the `column-rule` shorthand property are supported.

The `break-before` , `break-after` and `break-inside` properties are supported.

The `column-span` property is supported for direct children of columns.

The `column-fill` property is supported, with a column balancing algorithm that should be efficient with simple cases.

#### CSS Fragmentation Module Level 3 / 4

The [CSS Fragmentation Module Level 3](https://www.w3.org/TR/css-break-3/) “describes the fragmentation model that partitions a flow into pages, columns, or regions. It builds on the Page model module and introduces and defines the fragmentation model. It adds functionality for pagination, breaking variable fragment size and orientation, widows and orphans.”

The [CSS Fragmentation Module Level 4](https://www.w3.org/TR/css-break-4/) is a working draft on the same subject.

The `break-before` , `break-after` and `break-inside` properties are supported for pages, but **not** for columns and regions. `page-break-*` aliases as defined in CSS2 are supported too.

The `orphans` and `widows` properties are supported.

The `box-decoration-break` property is supported, but backgrounds are always repeated and not extended through the whole box as it should be with ‘slice’ value.

The `margin-break` property is supported.

#### CSS Custom Properties for Cascading Variables Module Level 1

The [CSS Custom Properties for Cascading Variables Module Level 1](https://www.w3.org/TR/css-variables/) “introduces cascading variables as a new primitive value type that is accepted by all CSS properties, and custom properties for defining them.”

The custom properties and the `var()` notation are supported.

#### CSS Text Decoration Module Level 3 / 4

The [CSS Text Decoration Module Level 3](https://www.w3.org/TR/css-text-decor-3/) “contains the features of CSS relating to text decoration, such as underlines, text shadows, and emphasis marks.”

The [CSS Text Decoration Module Level 4](https://www.w3.org/TR/css-text-decor-4/) is a working draft on the same subject.

The `text-decoration-line` , `text-decoration-style` , `text-decoration-color` , `text-decoration-thickness` and `text-underline-offset` properties are supported. The `text-decoration` shorthand is also supported.

The other properties ( `text-underline-position` , `text-emphasis-*` , `text-shadow` ) are not supported.

#### CSS Flexible Box Layout Module Level 1

The [CSS Flexible Box Layout Module Level 1](https://www.w3.org/TR/css-flexbox-1/) “describes a CSS box model optimized for user interface design”, also known as “flexbox”.

This module works for simple use cases but is not deeply tested.

All the `flex-*` , `align-*` , `justify-*` and `order` properties are supported. The `flex` and `flex-flow` shorthands are supported too.

#### CSS Grid Layout Module Level 2

The [CSS Grid Layout Module Level 2](https://www.w3.org/TR/css-grid-2/) “defines a two-dimensional grid-based layout system, optimized for user interface design”.

This module works for simple cases, but has some limitations. Here are non-exhaustive lists of supported/unsupported features.

Supported:

* `display: grid` ,
* `grid-auto-*` , `grid-template-*` and other `grid-*` properties,
* `grid` and other `grid-*` shorthands,
* flexible lengths ( `fr` unit),
* line names,
* grid areas,
* auto rows and auto columns,
* `z-index` ,
* `repeat(X, *)` ,
* `minmax()` ,
* `align-*` and `justify-*` alignment properties,
* `gap` and `*-gap` properties for gutters,
* dense auto flow,
* `order` ,
* margins, borders, padding on grid containers and grid items,
* fragmentation between rows.

Unsupported or untested:

* `display: inline-grid` ,
* auto content size for grid containers,
* `grid-auto-flow: column` ,
* subgrids,
* `repeat(auto-fill, *)` and `repeat(auto-fit, *)` ,
* auto margins for grid items,
* `span` with line names,
* `span` for flexible tracks,
* `safe` and `unsafe` alignments,
* baseline alignment,
* grid items with intrinsic size (images),
* distribute space beyond limits,
* grid items larger than grid containers,
* `min-width` , `max-width` , `min-height` , `max-height` on grid items,
* complex `min-content` and `max-content` cases,
* absolutely positioned and floating grid items,
* fragmentation in rows.

#### CSS Logical Properties and Values Module Level 1

The [CSS Logical Properties and Values Module Level 1](#css-logical-properties-and-values-module-level-1) “defines how to map between flow-relative and physical terms.”

All the logical properties and shorthands based on `start` , `end` , `block` and `inline` are supported. But, as `writing-mode` is not supported, the `block` and `inline` axes always correspond to the vertical and horizontal axes.

#### CSS Basic User Interface Module Level 4

The [CSS Basic User Interface Module Level 4](https://www.w3.org/TR/css-ui-4/) “enables authors to style user interface related properties and values.”

The `outline-width` , `outline-style` , `outline-color` properties and the `outline` shorthand are supported. The `outline-offset` property is also supported.

The `resize` , `cursor` , `caret-*` and `nav-*` properties are **not** supported.

The `appearance` property is supported. When set to `auto` , it displays form fields as PDF form fields (supported for text inputs, check boxes, text areas, and select only).

The `accent-color` property is **not** supported.
