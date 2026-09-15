import streamlit as st
from pypdf import PdfReader


# =========================================================
# PDF RAG ASSISTANT
# STEP 3: PDF TEXT EXTRACTION
# =========================================================

st.set_page_config(
    page_title="PDF RAG Assistant",
    page_icon="📚",
    layout="wide"
)


# =========================================================
# HEADER
# =========================================================

st.title("📚 PDF RAG Assistant")

st.subheader(
    "Advanced Document Question Answering System"
)

st.write(
    """
Upload a PDF document and prepare it for the
Retrieval-Augmented Generation pipeline.
"""
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("📄 Document")

    uploaded_file = st.file_uploader(
        "Upload a PDF document",
        type=["pdf"]
    )


# =========================================================
# PDF PROCESSING FUNCTION
# =========================================================

def extract_pdf_pages(uploaded_file):
    """
    Extract text from every page of the PDF.

    Returns:
        list of dictionaries containing:
        - page number
        - page text
    """

    reader = PdfReader(
        uploaded_file
    )

    pages = []

    for page_number, page in enumerate(
        reader.pages,
        start=1
    ):

        text = page.extract_text()

        if text is None:
            text = ""

        pages.append(
            {
                "page_number": page_number,
                "text": text.strip()
            }
        )

    return pages


# =========================================================
# DOCUMENT PROCESSING
# =========================================================

if uploaded_file:

    st.divider()

    st.subheader(
        "📄 Document Information"
    )

    # -----------------------------------------------------
    # Basic file information
    # -----------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "File Name",
            uploaded_file.name
        )

    with col2:

        file_size_kb = (
            uploaded_file.size / 1024
        )

        st.metric(
            "File Size",
            f"{file_size_kb:.2f} KB"
        )

    with col3:

        st.metric(
            "File Type",
            "PDF"
        )


    # -----------------------------------------------------
    # Extract PDF
    # -----------------------------------------------------

    st.divider()

    st.subheader(
        "🔍 PDF Text Extraction"
    )

    try:

        with st.spinner(
            "Reading PDF pages..."
        ):

            pages = extract_pdf_pages(
                uploaded_file
            )


        # -------------------------------------------------
        # Calculate statistics
        # -------------------------------------------------

        total_pages = len(pages)

        pages_with_text = sum(
            1
            for page in pages
            if page["text"]
        )

        total_characters = sum(
            len(page["text"])
            for page in pages
        )


        # -------------------------------------------------
        # Display statistics
        # -------------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Total Pages",
                total_pages
            )

        with col2:

            st.metric(
                "Pages With Text",
                pages_with_text
            )

        with col3:

            st.metric(
                "Characters Extracted",
                f"{total_characters:,}"
            )


        # -------------------------------------------------
        # Check extraction
        # -------------------------------------------------

        if pages_with_text == 0:

            st.error(
                """
                No readable text was found in this PDF.

                This may be a scanned/image-only PDF.
                OCR will be added in a later version.
                """
            )

        else:

            st.success(
                "PDF text extracted successfully."
            )


            # -------------------------------------------------
            # Display each page
            # -------------------------------------------------

            st.divider()

            st.subheader(
                "📖 Extracted Pages"
            )

            for page in pages:

                page_number = page[
                    "page_number"
                ]

                page_text = page[
                    "text"
                ]

                with st.expander(
                    f"Page {page_number}"
                ):

                    if page_text:

                        st.text(
                            page_text
                        )

                    else:

                        st.warning(
                            "No text found on this page."
                        )


    except Exception as e:

        st.error(
            f"Error reading PDF: {e}"
        )


# =========================================================
# RAG PIPELINE STATUS
# =========================================================

st.divider()

st.subheader(
    "RAG Pipeline"
)

col1, col2, col3, col4, col5, col6 = (
    st.columns(6)
)

with col1:

    st.success(
        "✓ Streamlit"
    )

with col2:

    if uploaded_file:

        st.success(
            "✓ PDF Upload"
        )

    else:

        st.info(
            "○ PDF Upload"
        )


with col3:

    if uploaded_file:

        st.success(
            "✓ Extraction"
        )

    else:

        st.info(
            "○ Extraction"
        )


with col4:

    st.info(
        "○ Chunking"
    )

with col5:

    st.info(
        "○ Embeddings"
    )

with col6:

    st.info(
        "○ FAISS"
    )


# =========================================================
# NEXT STAGE
# =========================================================

if uploaded_file:

    st.info(
        """
        **Next stage:**

        Extracted page text will be cleaned and
        converted into intelligent overlapping chunks
        while preserving page metadata.
        """
    )

else:

    st.info(
        "Upload a PDF to begin document processing."
    )
