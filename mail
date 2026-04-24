import streamlit as st
import re

st.set_page_config(page_title="Spam Email Detection", page_icon="📧", layout="centered")

# ---------------- SINGLY LINKED LIST ----------------
class Node:
    pass

def create_node(word):
    node = Node()
    node.word = word
    node.next = None
    return node

# ---------------- SESSION STORAGE ----------------
if "head" not in st.session_state:
    st.session_state.head = None

if "emails" not in st.session_state:
    st.session_state.emails = []

# initial spam keywords
default_words = ["free", "win", "offer", "money", "prize", "lottery", "urgent", "click"]

# insert word into linked list
def insert_word(word):
    word = word.lower().strip()
    if word == "":
        return

    if word_exists(word):
        return

    new_node = create_node(word)

    if st.session_state.head is None:
        st.session_state.head = new_node
    else:
        temp = st.session_state.head
        while temp.next is not None:
            temp = temp.next
        temp.next = new_node

# check if word already exists
def word_exists(word):
    temp = st.session_state.head
    while temp is not None:
        if temp.word == word:
            return True
        temp = temp.next
    return False

# get all words from linked list
def get_keywords():
    words = []
    temp = st.session_state.head
    while temp is not None:
        words.append(temp.word)
        temp = temp.next
    return words

# load default words once
if st.session_state.head is None:
    for w in default_words:
        insert_word(w)

# ---------------- SPAM CHECK LOGIC ----------------
def extract_words(text):
    return re.findall(r"[a-zA-Z]+", text.lower())

def detect_spam(email_text):
    words = extract_words(email_text)
    spam_keywords = get_keywords()

    matched_words = []
    repeated_words = []

    # check words from linked list in email
    for word in spam_keywords:
        if word in words:
            matched_words.append(word)

    # check repeated words in email
    for word in words:
        if words.count(word) > 1 and word not in repeated_words:
            repeated_words.append(word)

    # if any repeated word is found, add it to linked list
    for word in repeated_words:
        insert_word(word)

    # final decision
    if matched_words or repeated_words:
        result = "SPAM"
    else:
        result = "NOT SPAM"

    return result, matched_words, repeated_words

# ---------------- UI ----------------
st.title("Spam Email Detection")

st.write(
    "The app stores spam keywords in a singly linked list, checks whether those words are present "
    "in the email, and also marks the email as spam if any word repeats more than once."
)

email_content = st.text_area("Enter Email Content")

col1, col2 = st.columns(2)

with col1:
    if st.button("Check Email"):
        if email_content.strip() == "":
            st.warning("Please enter email content.")
        else:
            result, matched_words, repeated_words = detect_spam(email_content)

            st.session_state.emails.append({
                "content": email_content,
                "result": result,
                "matched": matched_words,
                "repeated": repeated_words
            })

            if result == "SPAM":
                st.error("Result: SPAM")
            else:
                st.success("Result: NOT SPAM")

            if matched_words:
                st.write("Spam words found in linked list:", ", ".join(matched_words))
            else:
                st.write("Spam words found in linked list: None")

            if repeated_words:
                st.write("Repeated word(s) added to linked list:", ", ".join(repeated_words))
            else:
                st.write("Repeated word(s): None")

with col2:
    if st.button("Clear All"):
        st.session_state.emails = []
        st.session_state.head = None
        for w in default_words:
            insert_word(w)
        st.info("All emails cleared and keyword list reset.")

# ---------------- DISPLAY LINKED LIST ----------------
st.subheader("Spam Keywords in Singly Linked List")
keywords = get_keywords()
st.write(" → ".join(keywords))

# ---------------- STORED EMAILS ----------------
st.subheader("Checked Emails")
if len(st.session_state.emails) == 0:
    st.write("No emails checked yet.")
else:
    for i, item in enumerate(st.session_state.emails, start=1):
        st.markdown(f"**Email {i}:** {item['content']}")
        st.write(f"Result: {item['result']}")

        if item["matched"]:
            st.write("Matched spam words:", ", ".join(item["matched"]))

        if item["repeated"]:
            st.write("Repeated words added:", ", ".join(item["repeated"]))

        st.markdown("---")
