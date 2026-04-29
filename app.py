import streamlit as st
import re

st.set_page_config(
    page_title="Spam Email Detection",
    page_icon="📧",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #020617, #0f172a, #111827);
    color: white;
}

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    color: #38bdf8;
    margin-bottom: 5px;
}

.sub-title {
    text-align: center;
    color: #cbd5e1;
    font-size: 17px;
    margin-bottom: 30px;
}

.card {
    background: rgba(15, 23, 42, 0.95);
    padding: 25px;
    border-radius: 20px;
    border: 1px solid rgba(56, 189, 248, 0.25);
    box-shadow: 0 0 25px rgba(56, 189, 248, 0.08);
    margin-bottom: 20px;
}

.result-spam {
    background: linear-gradient(135deg, #7f1d1d, #dc2626);
    padding: 20px;
    border-radius: 18px;
    text-align: center;
    color: white;
    font-size: 28px;
    font-weight: 800;
}

.result-safe {
    background: linear-gradient(135deg, #064e3b, #16a34a);
    padding: 20px;
    border-radius: 18px;
    text-align: center;
    color: white;
    font-size: 28px;
    font-weight: 800;
}

.keyword-box {
    background: #020617;
    color: #67e8f9;
    padding: 15px;
    border-radius: 14px;
    border: 1px solid #334155;
    font-size: 16px;
    line-height: 1.8;
}

.email-box {
    background: #020617;
    padding: 15px;
    border-radius: 15px;
    border-left: 5px solid #38bdf8;
    margin-bottom: 12px;
}

.badge {
    display: inline-block;
    background: #1e293b;
    color: #38bdf8;
    padding: 6px 12px;
    border-radius: 999px;
    margin: 4px;
    font-size: 14px;
    border: 1px solid #334155;
}

.stTextArea textarea {
    background-color: #020617;
    color: white;
    border-radius: 15px;
    border: 1px solid #334155;
}

.stButton button {
    width: 100%;
    border-radius: 14px;
    height: 48px;
    font-weight: 700;
    background: linear-gradient(90deg, #0ea5e9, #2563eb);
    color: white;
    border: none;
}

.stButton button:hover {
    background: linear-gradient(90deg, #38bdf8, #1d4ed8);
    color: white;
}
</style>
""", unsafe_allow_html=True)

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

default_words = ["free", "win", "offer", "money", "prize", "lottery", "urgent", "click"]

def word_exists(word):
    temp = st.session_state.head
    while temp is not None:
        if temp.word == word:
            return True
        temp = temp.next
    return False

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

def get_keywords():
    words = []
    temp = st.session_state.head

    while temp is not None:
        words.append(temp.word)
        temp = temp.next

    return words

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

    for word in spam_keywords:
        if word in words:
            matched_words.append(word)

    for word in words:
        if words.count(word) > 1 and word not in repeated_words:
            repeated_words.append(word)

    for word in repeated_words:
        insert_word(word)

    if matched_words or repeated_words:
        result = "SPAM"
    else:
        result = "NOT SPAM"

    return result, matched_words, repeated_words

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("📧 Spam Detector")
    st.write("Using Singly Linked List")

    st.markdown("---")

    st.metric("Total Keywords", len(get_keywords()))
    st.metric("Emails Checked", len(st.session_state.emails))

    spam_count = sum(1 for email in st.session_state.emails if email["result"] == "SPAM")
    safe_count = sum(1 for email in st.session_state.emails if email["result"] == "NOT SPAM")

    st.metric("Spam Emails", spam_count)
    st.metric("Safe Emails", safe_count)

# ---------------- MAIN UI ----------------
st.markdown("<div class='main-title'>Spam Email Detection System</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='sub-title'>A smart email classifier using Singly Linked List and adaptive keyword learning</div>",
    unsafe_allow_html=True
)

left, right = st.columns([2, 1])

with left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("Enter Email Content")

    email_content = st.text_area(
        "Type or paste the email message below:",
        height=220,
        placeholder="Example: Congratulations! You win a free prize. Click now..."
    )

    c1, c2 = st.columns(2)

    with c1:
        check_btn = st.button("Check Email")

    with c2:
        clear_btn = st.button("Clear All")

    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Detection Rules")
    st.write("1. Checks spam keywords stored in Singly Linked List.")
    st.write("2. Detects repeated words in email content.")
    st.write("3. Repeated words are automatically added to the linked list.")
    st.write("4. Email is marked as spam if any rule matches.")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- BUTTON ACTIONS ----------------
if check_btn:
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
            st.markdown("<div class='result-spam'>RESULT: SPAM EMAIL</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='result-safe'>RESULT: NOT SPAM</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("Matched Spam Words")
            if matched_words:
                for word in matched_words:
                    st.markdown(f"<span class='badge'>{word}</span>", unsafe_allow_html=True)
            else:
                st.write("None")
            st.markdown("</div>", unsafe_allow_html=True)

        with col_b:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("Repeated Words Added")
            if repeated_words:
                for word in repeated_words:
                    st.markdown(f"<span class='badge'>{word}</span>", unsafe_allow_html=True)
            else:
                st.write("None")
            st.markdown("</div>", unsafe_allow_html=True)

if clear_btn:
    st.session_state.emails = []
    st.session_state.head = None

    for w in default_words:
        insert_word(w)

    st.success("All emails cleared and keyword list reset.")

# ---------------- LINKED LIST DISPLAY ----------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("Spam Keywords Stored in Singly Linked List")

keywords = get_keywords()

if keywords:
    linked_list_text = " → ".join(keywords)
    st.markdown(f"<div class='keyword-box'>{linked_list_text}</div>", unsafe_allow_html=True)
else:
    st.write("No keywords available.")

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- CHECKED EMAILS ----------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("Checked Email History")

if len(st.session_state.emails) == 0:
    st.info("No emails checked yet.")
else:
    for i, item in enumerate(st.session_state.emails, start=1):
        result_color = "#dc2626" if item["result"] == "SPAM" else "#22c55e"

        st.markdown(f"""
        <div class='email-box'>
            <h4>Email {i}</h4>
            <p>{item['content']}</p>
            <b style='color:{result_color};'>Result: {item['result']}</b>
        </div>
        """, unsafe_allow_html=True)

        if item["matched"]:
            st.write("Matched spam words:", ", ".join(item["matched"]))

        if item["repeated"]:
            st.write("Repeated words added:", ", ".join(item["repeated"]))

st.markdown("</div>", unsafe_allow_html=True)
