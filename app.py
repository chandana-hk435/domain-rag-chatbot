import streamlit as st
from pypdf import PdfReader

st.set_page_config(
    page_title="PDF Chatbot",
    page_icon="📚"
)

st.title("📚 Domain-Specific RAG Chatbot")
st.write("Upload a PDF and ask questions about its content.")

uploaded_file = st.file_uploader(
    "Upload your PDF document",
    type=["pdf"]
)

if uploaded_file is not None:
    reader = PdfReader(uploaded_file)

    document_text = ""
    page_texts = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        if text.strip():
            document_text += text + "\n"
            page_texts.append({
                "page": page_number,
                "text": text
            })

    st.success("PDF uploaded and text extracted successfully!")

    st.write("Number of pages:", len(reader.pages))

    question = st.text_input("Enter your question")

    if st.button("Search PDF"):
        if question.strip():
            words = question.lower().split()
            results = []

            for page in page_texts:
                score = sum(
                    1 for word in words
                    if word in page["text"].lower()
                )

                if score > 0:
                    results.append((score, page))

            results.sort(key=lambda item: item[0], reverse=True)

            if results:
                st.subheader("Relevant information")

                for score, page in results[:3]:
                    st.write(f"**Source: Page {page['page']}**")
                    st.write(page["text"])
                    st.divider()
            else:
                st.warning(
                    "I could not find this information "
                    "in the uploaded document."
                )
        else:
            st.warning("Please enter a question.")