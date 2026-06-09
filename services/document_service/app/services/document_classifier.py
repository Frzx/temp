from pathlib import Path


ALLOWED_DOCUMENT_TYPES = {
    "pdf",
    "excel",
    "image",
    "text",
}


def classify_document_type(*, file_name: str, content_type: str | None) -> str:
    suffix = Path(file_name).suffix.lower()
    normalized_content_type = (content_type or "").lower()

    if suffix == ".pdf" or normalized_content_type == "application/pdf":
        return "pdf"
    if suffix in {".xls", ".xlsx", ".csv"} or "spreadsheet" in normalized_content_type or "excel" in normalized_content_type:
        return "excel"
    if suffix in {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".webp"} or normalized_content_type.startswith("image/"):
        return "image"
    if suffix in {".txt", ".md", ".json", ".xml"} or normalized_content_type.startswith("text/"):
        return "text"

    raise ValueError("Unsupported file type. Allowed types: pdf, excel, image, text")

# Use this later for production

# from typing import Final, Literal

# import magic

# DocumentType = Literal["pdf", "excel", "image", "text"]

# ALLOWED_DOCUMENT_TYPES: Final[set[str]] = {
#     "pdf",
#     "excel",
#     "image",
#     "text",
# }

# _EXCEL_MIME_TYPES: Final[set[str]] = {
#     "application/vnd.ms-excel",
#     "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
#     "application/vnd.oasis.opendocument.spreadsheet",
#     "text/csv",
# }

# _TEXT_MIME_TYPES: Final[set[str]] = {
#     "application/json",
#     "application/xml",
#     "application/x-yaml",
#     "text/plain",
#     "text/markdown",
# }


# class UnsupportedFileTypeError(ValueError):
#     pass


# def classify_document_type(
#     *,
#     file_bytes: bytes,
# ) -> DocumentType:
#     """
#     Classify a document based on its actual file contents.

#     Raises:
#         UnsupportedFileTypeError: If the file type is not supported.
#     """
#     if not file_bytes:
#         raise UnsupportedFileTypeError("File is empty")

#     mime_type = magic.from_buffer(
#         file_bytes,
#         mime=True,
#     ).lower()

#     if mime_type == "application/pdf":
#         return "pdf"

#     if mime_type.startswith("image/"):
#         return "image"

#     if mime_type in _EXCEL_MIME_TYPES:
#         return "excel"

#     if (
#         mime_type.startswith("text/")
#         or mime_type in _TEXT_MIME_TYPES
#     ):
#         return "text"

#     raise UnsupportedFileTypeError(
#         f"Unsupported file type detected: {mime_type}"
#    )