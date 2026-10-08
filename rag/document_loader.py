import os


DOCUMENTS_DIR = "documents"


def load_documents():
    documents = []

    if not os.path.exists(DOCUMENTS_DIR):
        os.makedirs(DOCUMENTS_DIR)

    for filename in os.listdir(DOCUMENTS_DIR):

        filepath = os.path.join(
            DOCUMENTS_DIR,
            filename
        )

        if not os.path.isfile(filepath):
            continue

        if not filename.lower().endswith(
            (".txt", ".md")
        ):
            continue

        try:
            with open(
                filepath,
                "r",
                encoding="utf-8"
            ) as file:

                content = file.read()

            documents.append({
                "filename": filename,
                "content": content
            })

        except Exception as error:
            print(
                f"Could not read {filename}: {error}"
            )

    return documents


def chunk_text(
    text,
    chunk_size=1000,
    overlap=200
):
    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks