---
library: "pypdf"
query: "Build a production RAG service that ingests PDF manuals, chunks and embeds them into a vector database, and exposes a FastAPI endpoint that answers questions with citations back to the source page. Use pypdf for extraction and Pydantic models for request and response validation. Include streaming responses and health checks. Use pymilvus for the vector database."
url: "https://pypdf.readthedocs.io/en/stable/modules/PdfReader.html"
role: "alternate"
rank: 2
fetched_at: "2026-08-19T12:36:06.290378+00:00"
fetched_via: "brightdata-collector:c_msx9i6aq2bz5dznadk"
sha256: "5dde1f955d23a85075b817acaa780e3daec6121bb09a568a333f7ac425e56115"
---

# The PdfReader Class

*class* pypdf. PdfReader ( *stream : [str](https://docs.python.org/3.14/library/stdtypes.html#str "(in Python v3.14)") | [IO](https://docs.python.org/3.14/library/typing.html#typing.IO "(in Python v3.14)") [ [Any](https://docs.python.org/3.14/library/typing.html#typing.Any "(in Python v3.14)") ] | [Path](https://docs.python.org/3.14/library/pathlib.html#pathlib.Path "(in Python v3.14)")* , *strict : [bool](https://docs.python.org/3.14/library/functions.html#bool "(in Python v3.14)") = False* , *password : [str](https://docs.python.org/3.14/library/stdtypes.html#str "(in Python v3.14)") | [bytes](https://docs.python.org/3.14/library/stdtypes.html#bytes "(in Python v3.14)") | [None](https://docs.python.org/3.14/library/constants.html#None "(in Python v3.14)") = None* , *\** , *root\_object\_recovery\_limit : [int](https://docs.python.org/3.14/library/functions.html#int "(in Python v3.14)") | [None](https://docs.python.org/3.14/library/constants.html#None "(in Python v3.14)") = 10000* ) [[source]](../_modules/pypdf/_reader.html#PdfReader)
:   Bases:  [`PdfDocCommon`](PdfDocCommon.html#pypdf._doc_common.PdfDocCommon "pypdf._doc_common.PdfDocCommon")

    Initialize a PdfReader object.

    This operation can take some time, as the PDF stream’s cross-reference tables are read into memory.

    Parameters :
    :   * **stream** – A File object or an object that supports the standard read and seek methods similar to a File object. Could also be a string representing a path to a PDF file.
        * **strict** – Determines whether user should be warned of all problems and also causes some correctable problems to be fatal. Defaults to `False` .
        * **password** – Decrypt PDF file at initialization. If the password is None, the file will not be decrypted. Defaults to `None` .
        * **root\_object\_recovery\_limit** – The maximum number of objects to query for recovering the Root object in non-strict mode. To disable this security measure, pass `None` .

    strict *: [bool](https://docs.python.org/3.14/library/functions.html#bool "(in Python v3.14)")* *= False*

    flattened\_pages *: [list](https://docs.python.org/3.14/library/stdtypes.html#list "(in Python v3.14)") [ [PageObject](PageObject.html#pypdf._page.PageObject "pypdf._page.PageObject") ] | [None](https://docs.python.org/3.14/library/constants.html#None "(in Python v3.14)")* *= None*

    resolved\_objects *: [dict](https://docs.python.org/3.14/library/stdtypes.html#dict "(in Python v3.14)") [ [tuple](https://docs.python.org/3.14/library/stdtypes.html#tuple "(in Python v3.14)") [ Any , Any ] , [PdfObject](generic.html#pypdf.generic.PdfObject "pypdf.generic.PdfObject") | [None](https://docs.python.org/3.14/library/constants.html#None "(in Python v3.14)") ]*
    :   Storage of parsed PDF objects.

    close ( ) → [None](https://docs.python.org/3.14/library/constants.html#None "(in Python v3.14)") [[source]](../_modules/pypdf/_reader.html#PdfReader.close)
    :   Close the stream if opened in \_\_init\_\_ and clear memory.

    *property* root\_object *: [DictionaryObject](generic.html#pypdf.generic.DictionaryObject "pypdf.generic._data_structures.DictionaryObject")*
    :   Provide access to “/Root”. Standardized with PdfWriter.

    *property* pdf\_header *: [str](https://docs.python.org/3.14/library/stdtypes.html#str "(in Python v3.14)")*
    :   The first 8 bytes of the file.

        This is typically something like `'%PDF-1.6'` and can be used to detect if the file is actually a PDF file and which version it is.

    *property* xmp\_metadata *: [XmpInformation](XmpInformation.html#pypdf.xmp.XmpInformation "pypdf.xmp.XmpInformation") | [None](https://docs.python.org/3.14/library/constants.html#None "(in Python v3.14)")*
    :   XMP (Extensible Metadata Platform) data.

    get\_object ( *indirect\_reference : [int](https://docs.python.org/3.14/library/functions.html#int "(in Python v3.14)") | [IndirectObject](generic.html#pypdf.generic.IndirectObject "pypdf.generic._base.IndirectObject")* ) → [PdfObject](generic.html#pypdf.generic.PdfObject "pypdf.generic._base.PdfObject") | [None](https://docs.python.org/3.14/library/constants.html#None "(in Python v3.14)") [[source]](../_modules/pypdf/_reader.html#PdfReader.get_object)

    read\_object\_header ( *stream : [IO](https://docs.python.org/3.14/library/typing.html#typing.IO "(in Python v3.14)") [ [Any](https://docs.python.org/3.14/library/typing.html#typing.Any "(in Python v3.14)") ]* ) → [tuple](https://docs.python.org/3.14/library/stdtypes.html#tuple "(in Python v3.14)") [ [int](https://docs.python.org/3.14/library/functions.html#int "(in Python v3.14)") , [int](https://docs.python.org/3.14/library/functions.html#int "(in Python v3.14)") ] [[source]](../_modules/pypdf/_reader.html#PdfReader.read_object_header)

    cache\_get\_indirect\_object ( *generation : [int](https://docs.python.org/3.14/library/functions.html#int "(in Python v3.14)")* , *idnum : [int](https://docs.python.org/3.14/library/functions.html#int "(in Python v3.14)")* ) → [PdfObject](generic.html#pypdf.generic.PdfObject "pypdf.generic._base.PdfObject") | [None](https://docs.python.org/3.14/library/constants.html#None "(in Python v3.14)") [[source]](../_modules/pypdf/_reader.html#PdfReader.cache_get_indirect_object)

    cache\_indirect\_object ( *generation : [int](https://docs.python.org/3.14/library/functions.html#int "(in Python v3.14)")* , *idnum : [int](https://docs.python.org/3.14/library/functions.html#int "(in Python v3.14)")* , *obj : [PdfObject](generic.html#pypdf.generic.PdfObject "pypdf.generic._base.PdfObject") | [None](https://docs.python.org/3.14/library/constants.html#None "(in Python v3.14)")* ) → [PdfObject](generic.html#pypdf.generic.PdfObject "pypdf.generic._base.PdfObject") | [None](https://docs.python.org/3.14/library/constants.html#None "(in Python v3.14)") [[source]](../_modules/pypdf/_reader.html#PdfReader.cache_indirect_object)

    read ( *stream : [IO](https://docs.python.org/3.14/library/typing.html#typing.IO "(in Python v3.14)") [ [Any](https://docs.python.org/3.14/library/typing.html#typing.Any "(in Python v3.14)") ]* ) → [None](https://docs.python.org/3.14/library/constants.html#None "(in Python v3.14)") [[source]](../_modules/pypdf/_reader.html#PdfReader.read)
    :   Read and process the PDF stream, extracting necessary data.

        Parameters :
        :   **stream** – The PDF file stream.

    decrypt ( *password : [str](https://docs.python.org/3.14/library/stdtypes.html#str "(in Python v3.14)") | [bytes](https://docs.python.org/3.14/library/stdtypes.html#bytes "(in Python v3.14)")* ) → [PasswordType](#pypdf.PasswordType "pypdf._encryption.PasswordType") [[source]](../_modules/pypdf/_reader.html#PdfReader.decrypt)
    :   When using an encrypted / secured PDF file with the PDF Standard encryption handler, this function will allow the file to be decrypted. It checks the given password against the document’s user password and owner password, and then stores the resulting decryption key if either password is correct.

        It does not matter which password was matched. Both passwords provide the correct decryption key that will allow the document to be used with this library.

        Parameters :
        :   **password** – The password to match.

        Returns :
        :   An indicator if the document was decrypted and whether it was the owner password or the user password.

    *property* is\_encrypted *: [bool](https://docs.python.org/3.14/library/functions.html#bool "(in Python v3.14)")*
    :   Read-only boolean property showing whether this PDF file is encrypted.

        Note that this property, if true, will remain true even after the  [`decrypt()`](#pypdf.PdfReader.decrypt "pypdf.PdfReader.decrypt")  method is called.

    add\_form\_topname ( *name : [str](https://docs.python.org/3.14/library/stdtypes.html#str "(in Python v3.14)")* ) → [DictionaryObject](generic.html#pypdf.generic.DictionaryObject "pypdf.generic._data_structures.DictionaryObject") | [None](https://docs.python.org/3.14/library/constants.html#None "(in Python v3.14)") [[source]](../_modules/pypdf/_reader.html#PdfReader.add_form_topname)
    :   Add a top level form that groups all form fields below it.

        Parameters :
        :   **name** – text string of the “/T” Attribute of the created object

        Returns :
        :   The created object. `None` means no object was created.

    rename\_form\_topname ( *name : [str](https://docs.python.org/3.14/library/stdtypes.html#str "(in Python v3.14)")* ) → [DictionaryObject](generic.html#pypdf.generic.DictionaryObject "pypdf.generic._data_structures.DictionaryObject") | [None](https://docs.python.org/3.14/library/constants.html#None "(in Python v3.14)") [[source]](../_modules/pypdf/_reader.html#PdfReader.rename_form_topname)
    :   Rename top level form field that all form fields below it.

        Parameters :
        :   **name** – text string of the “/T” field of the created object

        Returns :
        :   The modified object. `None` means no object was modified.

    *property* are\_permissions\_valid *: [bool](https://docs.python.org/3.14/library/functions.html#bool "(in Python v3.14)") | [None](https://docs.python.org/3.14/library/constants.html#None "(in Python v3.14)")*
    :   Whether the `/Perms` integrity check passed for this document.

        For AES-256 encrypted documents (R=5/R=6), the `/Perms` field is an encrypted copy of the permissions that can be verified independently. Returns `False` if this check fails (the `/P` permissions may have been tampered with).

        Returns `None` if the document is not encrypted or has not yet been decrypted via  [`decrypt()`](#pypdf.PdfReader.decrypt "pypdf.PdfReader.decrypt")  . Returns `True` for non-AES-256 encryption (no `/Perms` to check).

    *property* attachment\_list *: [Generator](https://docs.python.org/3.14/library/collections.abc.html#collections.abc.Generator "(in Python v3.14)") [ [EmbeddedFile](generic.html#pypdf.generic.EmbeddedFile "pypdf.generic._files.EmbeddedFile") , [None](https://docs.python.org/3.14/library/constants.html#None "(in Python v3.14)") , [None](https://docs.python.org/3.14/library/constants.html#None "(in Python v3.14)") ]*
    :   Iterable of attachment objects.

    *property* attachments *: [Mapping](https://docs.python.org/3.14/library/collections.abc.html#collections.abc.Mapping "(in Python v3.14)") [ [str](https://docs.python.org/3.14/library/stdtypes.html#str "(in Python v3.14)") , [list](https://docs.python.org/3.14/library/stdtypes.html#list "(in Python v3.14)") [ [bytes](https://docs.python.org/3.14/library/stdtypes.html#bytes "(in Python v3.14)") ] ]*
    :   Mapping of attachment filenames to their content.

    decode\_permissions ( *permissions\_code : [int](https://docs.python.org/3.14/library/functions.html#int "(in Python v3.14)")* ) → [NoReturn](https://docs.python.org/3.14/library/typing.html#typing.NoReturn "(in Python v3.14)")
    :   Take the permissions as an integer, return the allowed access.

    get\_destination\_page\_number ( *destination : [Destination](Destination.html#pypdf.generic.Destination "pypdf.generic._data_structures.Destination")* ) → [int](https://docs.python.org/3.14/library/functions.html#int "(in Python v3.14)") | [None](https://docs.python.org/3.14/library/constants.html#None "(in Python v3.14)")
    :   Retrieve page number of a given Destination object.

        Parameters :
        :   **destination** – The destination to get page number.

        Returns :
        :   The page number or None if page is not found

    get\_fields ( *tree : [TreeObject](generic.html#pypdf.generic.TreeObject "pypdf.generic._data_structures.TreeObject") | [None](https://docs.python.org/3.14/library/constants.html#None "(in Python v3.14)") = None* , *retval : [dict](https://docs.python.org/3.14/library/stdtypes.html#dict "(in Python v3.14)") [ [Any](https://docs.python.org/3.14/library/typing.html#typing.Any "(in Python v3.14)") , [Any](https://docs.python.org/3.14/library/typing.html#typing.Any "(in Python v3.14)") ] | [None](https://docs.python.org/3.14/library/constants.html#None "(in Python v3.14)") = None* , *fileobj : [Any](https://docs.python.org/3.14/library/typing.html#typing.Any "(in Python v3.14)") | [None](https://docs.python.org/3.14/library/constants.html#None "(in Python v3.14)") = None* , *stack : [list](https://docs.python.org/3.14/library/stdtypes.html#list "(in Python v3.14)") [ [PdfObject](generic.html#pypdf.generic.PdfObject "pypdf.generic._base.PdfObject") ] | [None](https://docs.python.org/3.14/library/constants.html#None "(in Python v3.14)") = None* ) → [dict](https://docs.python.org/3.14/library/stdtypes.html#dict "(in Python v3.14)") [ [str](https://docs.python.org/3.14/library/stdtypes.html#str "(in Python v3.14)") , [Any](https://docs.python.org/3.14/library/typing.html#typing.Any "(in Python v3.14)") ] | [None](https://docs.python.org/3.14/library/constants.html#None "(in Python v3.14)")
    :   Extract field data if this PDF contains interactive form fields.

        The *tree* , *retval* , *stack* parameters are for recursive use.

        Parameters :
        :   * **tree** – Current object to parse.
            * **retval** – In-progress list of fields.
            * **fileobj** – A file object (usually a text file) to write a report to on all interactive form fields found.
            * **stack** – List of already parsed objects.

        Returns :
        :   A dictionary where each key is a field name, and each value is a  [`Field`](Field.html#pypdf.generic.Field "pypdf.generic.Field")  object. By default, the mapping name is used for keys. `None` if form data could not be located.

    get\_form\_text\_fields ( *full\_qualified\_name : [bool](https://docs.python.org/3.14/library/functions.html#bool "(in Python v3.14)") = False* ) → [dict](https://docs.python.org/3.14/library/stdtypes.html#dict "(in Python v3.14)") [ [str](https://docs.python.org/3.14/library/stdtypes.html#str "(in Python v3.14)") , [Any](https://docs.python.org/3.14/library/typing.html#typing.Any "(in Python v3.14)") ]
    :   Retrieve form fields from the document with textual data.

        Parameters :
        :   **full\_qualified\_name** – to get full name

        Returns :
        :   A dictionary. The key is the name of the form field, the value is the content of the field.

            If the document contains multiple form fields with the same name, the second and following will get the suffix .2, .3, …

    get\_named\_dest\_root ( ) → [ArrayObject](generic.html#pypdf.generic.ArrayObject "pypdf.generic._data_structures.ArrayObject")

    get\_num\_pages ( ) → [int](https://docs.python.org/3.14/library/functions.html#int "(in Python v3.14)")
    :   Calculate the number of pages in this PDF file.

        Returns :
        :   The number of pages of the parsed PDF file.

        Raises :
        :   [**PdfReadError**](errors.html#pypdf.errors.PdfReadError "pypdf.errors.PdfReadError")  – If restrictions prevent this action.

    get\_page ( *page\_number : [int](https://docs.python.org/3.14/library/functions.html#int "(in Python v3.14)")* ) → [PageObject](PageObject.html#pypdf._page.PageObject "pypdf._page.PageObject")
    :   Retrieve a page by number from this PDF file. Most of the time `.pages[page_number]` is preferred.

        Parameters :
        :   **page\_number** – The page number to retrieve (pages begin at zero)

        Returns :
        :   A  [`PageObject`](PageObject.html#pypdf._page.PageObject "pypdf._page.PageObject")  instance.

    get\_page\_number ( *page : [PageObject](PageObject.html#pypdf._page.PageObject "pypdf._page.PageObject")* ) → [int](https://docs.python.org/3.14/library/functions.html#int "(in Python v3.14)") | [None](https://docs.python.org/3.14/library/constants.html#None "(in Python v3.14)")
    :   Retrieve page number of a given PageObject.

        Parameters :
        :   **page** – The page to get page number. Should be an instance of  [`PageObject`](PageObject.html#pypdf._page.PageObject "pypdf._page.PageObject")

        Returns :
        :   The page number or None if page is not found

    get\_pages\_showing\_field ( *field : [Field](Field.html#pypdf.generic.Field "pypdf.generic._data_structures.Field") | [PdfObject](generic.html#pypdf.generic.PdfObject "pypdf.generic._base.PdfObject") | [IndirectObject](generic.html#pypdf.generic.IndirectObject "pypdf.generic._base.IndirectObject")* ) → [list](https://docs.python.org/3.14/library/stdtypes.html#list "(in Python v3.14)") [ [PageObject](PageObject.html#pypdf._page.PageObject "pypdf._page.PageObject") ]
    :   Provides list of pages where the field is called.

        Parameters :
        :   **field** – Field Object, PdfObject or IndirectObject referencing a Field

        Returns :
        :   *List of pages* –

            * Empty list:
              :   The field has no widgets attached (either hidden field or ancestor field).
            * Single page list:
              :   Page where the widget is present (most common).
            * Multi-page list:
              :   Field with multiple kids widgets (example: radio buttons, field repeated on multiple pages).

    *property* metadata *: [DocumentInformation](DocumentInformation.html#pypdf.DocumentInformation "pypdf._doc_common.DocumentInformation") | [None](https://docs.python.org/3.14/library/constants.html#None "(in Python v3.14)")*
    :   Retrieve the PDF file’s document information dictionary, if it exists.

        Note that some PDF files use metadata streams instead of document information dictionaries, and these metadata streams will not be accessed by this function.

    *property* named\_destinations *: [dict](https://docs.python.org/3.14/library/stdtypes.html#dict "(in Python v3.14)") [ [str](https://docs.python.org/3.14/library/stdtypes.html#str "(in Python v3.14)") , [Destination](Destination.html#pypdf.generic.Destination "pypdf.generic._data_structures.Destination") ]*
    :   A read-only dictionary which maps names to destinations.

    *property* open\_destination *: [Destination](Destination.html#pypdf.generic.Destination "pypdf.generic._data_structures.Destination") | [TextStringObject](generic.html#pypdf.generic.TextStringObject "pypdf.generic._base.TextStringObject") | [ByteStringObject](generic.html#pypdf.generic.ByteStringObject "pypdf.generic._base.ByteStringObject") | [None](https://docs.python.org/3.14/library/constants.html#None "(in Python v3.14)")*
    :   Property to access the opening destination ( `/OpenAction` entry in the PDF catalog). It returns `None` if the entry does not exist or is not set.

        Raises :
        :   [**Exception**](https://docs.python.org/3.14/library/exceptions.html#Exception "(in Python v3.14)")  – If a destination is invalid.

    *property* outline *: [list](https://docs.python.org/3.14/library/stdtypes.html#list "(in Python v3.14)") [ [Destination](Destination.html#pypdf.generic.Destination "pypdf.generic._data_structures.Destination") | [list](https://docs.python.org/3.14/library/stdtypes.html#list "(in Python v3.14)") [ [Destination](Destination.html#pypdf.generic.Destination "pypdf.generic._data_structures.Destination") | [list](https://docs.python.org/3.14/library/stdtypes.html#list "(in Python v3.14)") [ [Destination](Destination.html#pypdf.generic.Destination "pypdf.generic._data_structures.Destination") ] ] ]*
    :   Read-only property for the outline present in the document (i.e., a collection of ‘outline items’ which are also known as ‘bookmarks’).

    *property* page\_labels *: [list](https://docs.python.org/3.14/library/stdtypes.html#list "(in Python v3.14)") [ [str](https://docs.python.org/3.14/library/stdtypes.html#str "(in Python v3.14)") ]*
    :   A list of labels for the pages in this document.

        This property is read-only. The labels are in the order that the pages appear in the document.

    *property* page\_layout *: [str](https://docs.python.org/3.14/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3.14/library/constants.html#None "(in Python v3.14)")*
    :   Get the page layout currently being used.

        Valid `layout` values

            |  |  |
        | --- | --- |
        | /NoLayout | Layout explicitly not specified |
        | /SinglePage | Show one page at a time |
        | /OneColumn | Show one column at a time |
        | /TwoColumnLeft | Show pages in two columns, odd-numbered pages on the left |
        | /TwoColumnRight | Show pages in two columns, odd-numbered pages on the right |
        | /TwoPageLeft | Show two pages at a time, odd-numbered pages on the left |
        | /TwoPageRight | Show two pages at a time, odd-numbered pages on the right |

    *property* page\_mode *: [Literal](https://docs.python.org/3.14/library/typing.html#typing.Literal "(in Python v3.14)") [ '/UseNone' , '/UseOutlines' , '/UseThumbs' , '/FullScreen' , '/UseOC' , '/UseAttachments' ] | [None](https://docs.python.org/3.14/library/constants.html#None "(in Python v3.14)")*
    :   Get the page mode currently being used.

        Valid `mode` values

            |  |  |
        | --- | --- |
        | /UseNone | Do not show outline or thumbnails panels |
        | /UseOutlines | Show outline (aka bookmarks) panel |
        | /UseThumbs | Show page thumbnails panel |
        | /FullScreen | Fullscreen view |
        | /UseOC | Show Optional Content Group (OCG) panel |
        | /UseAttachments | Show attachments panel |

    *property* pages *: [Sequence](https://docs.python.org/3.14/library/collections.abc.html#collections.abc.Sequence "(in Python v3.14)") [ [PageObject](PageObject.html#pypdf._page.PageObject "pypdf._page.PageObject") ]*
    :   Property that emulates a list of  [`PageObject`](PageObject.html#pypdf._page.PageObject "pypdf._page.PageObject")  . This property allows to get a page or a range of pages.

        The returned object supports indexing, slicing, `len()` , iteration and (for PdfWriter) `del` , but it is not a  [`list`](https://docs.python.org/3.14/library/stdtypes.html#list "(in Python v3.14)")  - pages are looked up on demand rather than materialised up front, so list-only operations such as `append()` or concatenation with `+` are not available.

        Note

        For PdfWriter only: Provides the capability to remove a page/range of page from the list (using the del operator). Remember: Only the page entry is removed, as the objects beneath can be used elsewhere. A solution to completely remove them - if they are not used anywhere - is to write to a buffer/temporary file and then load it into a new PdfWriter.

    remove\_page ( *page : [int](https://docs.python.org/3.14/library/functions.html#int "(in Python v3.14)") | [PageObject](PageObject.html#pypdf._page.PageObject "pypdf._page.PageObject") | [IndirectObject](generic.html#pypdf.generic.IndirectObject "pypdf.generic._base.IndirectObject")* , *clean : [bool](https://docs.python.org/3.14/library/functions.html#bool "(in Python v3.14)") = False* ) → [None](https://docs.python.org/3.14/library/constants.html#None "(in Python v3.14)")
    :   Remove page from pages list.

        Parameters :
        :   * **page** –

              + [`int`](https://docs.python.org/3.14/library/functions.html#int "(in Python v3.14)")  : Page number to be removed.
              + [`PageObject`](PageObject.html#pypdf._page.PageObject "pypdf._page.PageObject")  : page to be removed. If the page appears many times only the first one will be removed.
              + [`IndirectObject`](generic.html#pypdf.generic.IndirectObject "pypdf.generic.IndirectObject")  : Reference to page to be removed.
            * **clean** – replace PageObject with NullObject to prevent annotations or destinations to reference a detached page.

    *property* threads *: [ArrayObject](generic.html#pypdf.generic.ArrayObject "pypdf.generic._data_structures.ArrayObject") | [None](https://docs.python.org/3.14/library/constants.html#None "(in Python v3.14)")*
    :   Read-only property for the list of threads.

        See §12.4.3 from the PDF 1.7 or 2.0 specification.

        It is an array of dictionaries with “/F” (the first bead in the thread) and “/I” (a thread information dictionary containing information about the thread, such as its title, author, and creation date) properties or None if there are no articles.

        Since PDF 2.0 it can also contain an indirect reference to a metadata stream containing information about the thread, such as its title, author, and creation date.

    *property* user\_access\_permissions *: [UserAccessPermissions](constants.html#pypdf.constants.UserAccessPermissions "pypdf.constants.UserAccessPermissions") | [None](https://docs.python.org/3.14/library/constants.html#None "(in Python v3.14)")*
    :   Get the user access permissions for encrypted documents. Returns None if not encrypted.

        Warning

        For AES-256 encrypted documents (R=5/R=6), the returned permissions are derived from the `/P` field, which is only trustworthy if the `/Perms` integrity check passed. Check  [`are_permissions_valid`](#pypdf.PdfReader.are_permissions_valid "pypdf.PdfReader.are_permissions_valid")  to verify.

    *property* viewer\_preferences *: [ViewerPreferences](generic.html#pypdf.generic.ViewerPreferences "pypdf.generic._viewerpref.ViewerPreferences") | [None](https://docs.python.org/3.14/library/constants.html#None "(in Python v3.14)")*
    :   Returns the existing ViewerPreferences as an overloaded dictionary.

    *property* xfa *: [dict](https://docs.python.org/3.14/library/stdtypes.html#dict "(in Python v3.14)") [ [str](https://docs.python.org/3.14/library/stdtypes.html#str "(in Python v3.14)") , [Any](https://docs.python.org/3.14/library/typing.html#typing.Any "(in Python v3.14)") ] | [None](https://docs.python.org/3.14/library/constants.html#None "(in Python v3.14)")*

*class* pypdf. PasswordType ( *\* values* ) [[source]](../_modules/pypdf/_encryption.html#PasswordType)
:   Bases:  [`IntEnum`](https://docs.python.org/3.14/library/enum.html#enum.IntEnum "(in Python v3.14)")

    NOT\_DECRYPTED *= 0*

    USER\_PASSWORD *= 1*

    OWNER\_PASSWORD *= 2*
