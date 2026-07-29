import fitz  # PyMuPDF


class PDFService:

    @staticmethod
    def extract_text(file_path: str) -> str:
        """
        Extract text from a PDF file using PyMuPDF.

        Args:
            file_path: Path to the PDF file.

        Returns:
            Extracted text content as a string.

        Raises:
            RuntimeError: If the PDF cannot be opened or read.
        """
        try:
            document = fitz.open(file_path)
        except Exception as e:
            raise RuntimeError(f"Cannot open PDF file: {e}")

        text = ""
        try:
            for page in document:
                text += page.get_text()
        finally:
            document.close()

        return text.strip()