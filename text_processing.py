## NLP
## For FURTHER TEXT PROCESSING (after text extraction)
## Not Required for hackathon.








# import re
# from bs4 import BeautifulSoup
# import nltk
# from nltk.tokenize import sent_tokenize
# nltk.download('punkt')
# from text_extraction import extract_text
# import contractions



# pages = extract_text("./Sample/selectable1.pdf")

# print("Extracted text: ")
# print(pages[0])


# # STAGE 1
# def stage1_text_repair(text):
#     text = BeautifulSoup(text, "html.parser").get_text()
#     text = re.sub(r'(.)\1{4,}', r'\1', text)   # Fix bold text (5x+ repetition)
#     text = re.sub(r'\s+', ' ', text).strip()
#     return text

# repaired_text = [stage1_text_repair(page) for page in pages]
# print("\n--- Stage 1: Text Repair ---\n")
# print(repaired_text[0])

# # STAGE 2
# def stage2_structure_preserve(text):
#     # Minimal cleanup only
#     text = re.sub(r'\u00ad', '', text)  # Remove soft hyphens
#     return text

# structured_text = [stage2_structure_preserve(page) for page in repaired_text]
# print("\n--- Stage 2: Structure Preserved ---\n")
# print(structured_text[0])


# # STAGE 3
# def stage3_sentence_split(text):
#     return sent_tokenize(text)

# sentences = [stage3_sentence_split(page) for page in structured_text]
# print("\n--- Stage 3: Sentence Split ---\n")
# print(sentences[0])


# # STAGE 4
# def stage4_light_normalize(sentence):
#     return contractions.fix(sentence)

# normalized_sentences = [
#     [stage4_light_normalize(s) for s in page]
#     for page in sentences
# ]

# print("\n--- Stage 4: Light Normalization ---\n")
# print(normalized_sentences[0])


# # STAGE 5
# def stage5_qp_ready(sentences):
#     return [s.strip() for s in sentences if len(s.strip()) > 10]

# qp_ready_text = [stage5_qp_ready(page) for page in normalized_sentences]

# print("\n--- Final QP-Ready Text ---\n")
# print(qp_ready_text[0])




# ### CHUNKING  ( 1 chunk = max 150/200  words)
# def chunk_page(sentences, max_words=150):
#     chunks = []
#     current_chunk = []
#     current_words = 0

#     for s in sentences:
#         words = s.split()
#         if current_words + len(words) > max_words:
#             chunks.append(" ".join(current_chunk))
#             current_chunk = []
#             current_words = 0

#         current_chunk.append(s)
#         current_words += len(words)

#     if current_chunk:
#         chunks.append(" ".join(current_chunk))

#     return chunks

# def build_chunks_with_metadata(qp_ready_text, source_name, max_words=150):
#     all_chunks = []
#     chunk_counter = 0

#     for page_idx, page_sentences in enumerate(qp_ready_text):
#         page_number = page_idx + 1  # user-facing page number

#         page_chunks = chunk_page(page_sentences, max_words)

#         for c in page_chunks:
#             chunk_obj = {
#                 "chunk_id": f"{source_name}_p{page_number}_c{chunk_counter}",
#                 "text": c,
#                 "page_start": page_number,
#                 "page_end": page_number,
#                 "source": source_name
#             }

#             all_chunks.append(chunk_obj)
#             chunk_counter += 1

#     return all_chunks


# # Flatten all sentences from all pages into a single list
# all_sentences = [sentence for page in qp_ready_text for sentence in page]

# # # Chunk the sentences
# # chunks = chunk_page(all_sentences, 150)

# chunks_with_metadata = build_chunks_with_metadata(
#     qp_ready_text=qp_ready_text,
#     source_name="Document.pdf",
#     max_words=150
# )

# print("\n--- Sample Chunks with Metadata ---\n")
# for ch in chunks_with_metadata[:5]:
#     print(ch["chunk_id"])
#     print(f"Page: {ch['page_start']}")
#     print(f"Words: {len(ch['text'].split())}")
#     print(ch["text"])
#     print("-" * 50)


