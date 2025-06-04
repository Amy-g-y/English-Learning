import streamlit as st

from datetime import datetime, timedelta
import os
from translator import translate
import pandas as pd
import streamlit as st
st.set_page_config(page_title="Hey!", page_icon="🚀", layout="centered")
import random



st.title("Let's start learning English!")
VIDEO_URL = "https://www.youtube.com/watch?v=R5Bds2GcCdk"
st.video(VIDEO_URL)
VIDEO_URL = "https://www.youtube.com/watch?v=Whwyu09a8KE"
st.video(VIDEO_URL)
# ---------------- SESSION STATE ----------------



# external css
def local_css(file_name: str):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style.css")


def update_flashcards(new_flashcard_df: pd.DataFrame):
    if not new_flashcard_df.empty:
        st.session_state.flashcards_df = concat_df(
            st.session_state.flashcards_df, new_flashcard_df
        )
        save_flashcards(st.session_state.flashcards_df)


def update_next_appearance(id: int, next_appearance: datetime):
    if next_appearance is not None:
        st.session_state.flashcards_df.loc[
            st.session_state.flashcards_df[ID] == id, NEXT_APPEARANCE
        ] = next_appearance
        save_flashcards(st.session_state.flashcards_df)

def restart_flashcards():
    st.session_state.flashcards_df[NEXT_APPEARANCE] = datetime.now() - timedelta(days=1)
    save_flashcards(st.session_state.flashcards_df)
    st.success("All flashcards have been reset!")
    st.rerun()

# ---------------- Start Flash ----------------
# code for flashcard taken from https://github.com/raman-r-4978/flashcard/blob/main/utils.py
from utils import (
    ANSWER,
    DATE_ADDED,
    DEFAULT_TAGS,
    ID,
    NEXT_APPEARANCE,
    QUESTION,
    TAGS,
    concat_df,
    get_question,
    load_all_flashcards,
    prepare_flashcard_df,
    save_flashcards,
    search,
    view_flashcards, reset_flashcards,
)

if "flashcards_df" not in st.session_state:
    st.session_state.flashcards_df = load_all_flashcards()

try:
    q_no, row = next(get_question())

    st.write (row[QUESTION])
    with st.expander("Show Answer"):
        st.write(row[ANSWER])

    next_appearance = None
    col1, col2, col3 = st.columns(3, gap="large")
    now = datetime.now()
    timestamp = int(now.timestamp())
    with col1:
        easy_submit_button: bool = st.button(label="Easy", use_container_width=True)
        if easy_submit_button:
            prev_time_diff = int(row[NEXT_APPEARANCE]) - int(row[DATE_ADDED])
            next_appearance_days = min(prev_time_diff + 2, 60)
            next_appearance = timestamp + 1000000
    with col2:
        medium_submit_button: bool = st.button(
            label="Medium", use_container_width=True
        )
        if medium_submit_button:
            next_appearance = timestamp + 500000
    with col3:
        hard_submit_button: bool = st.button(label="Hard", use_container_width=True)
        if hard_submit_button:
            next_appearance = timestamp + 1

    if next_appearance is not None:
        update_next_appearance(row[ID], next_appearance)
        st.info(
            f"""Next Apperance of this card will be {next_appearance} days!""",
            icon="🎉",
        )
        st.rerun()
except StopIteration:
    st.info("Hey! You have completed all the flashcards. Good Job!", icon="🙌")

with st.expander("⚙️ Settings"):
    if st.button("🔁 Restart All Flashcards"):
        restart_flashcards()
        reset_flashcards()


st.write("Vocabulary List 1")
st.write("angry")
st.write("animal")
st.write("answer")
st.write("")
st.write("")

st.write("#"), st.write("##")
tab1, tab2, tab3 = st.tabs(["Translator", "Matching Game", "Chatbot"])


with tab1:
    st.header("Translator")
    translate()


with tab2:

    st.header("Matching Game")
    # Example word-image pairs (use your own images!)
    pairs = {
        "Cat": "https://upload.wikimedia.org/wikipedia/commons/3/3a/Cat03.jpg",
        "Dog": "https://upload.wikimedia.org/wikipedia/commons/d/d9/Collage_of_Nine_Dogs.jpg",
        "Elephant": "https://upload.wikimedia.org/wikipedia/commons/3/37/African_Bush_Elephant.jpg",
        "Computer": "images/computer.jpg",
        "Mountain": "images/mountain.jpg",
        "Pillow": "images/pillow.jpg",
        "Ice": "images/ice.jpg",
        "Noodle": "images/noodle.jpg",
        "Rainy": "images/rainy.jpg",
        "Window": "images/window.jpg",
        "Piano": "images/piano.jpg",
        "Violin": "images/violin.jpg",
        "Umbrella": "images/umbrella.jpg",
        "Chair": "images/chair.jpg",
        "Flashlight": "images/flashlight.jpg",
        "Bus": "images/bus.jpg",
        "Table": "images/table.webp",
        "Cloud": "images/cloud.webp",
        "Sunshine": "images/sunshine.jpg",
    }

    # Initialize session state
    if "selected_word" not in st.session_state:
        st.session_state.selected_word = None
    if "matched" not in st.session_state:
        st.session_state.matched = []
    st.header("🔤 Select a word to match with an image")

    from itertools import islice


    # Function to split list into chunks
    def chunk_list(lst, size):
        for i in range(0, len(lst), size):
            yield lst[i:i + size]


    # Split word buttons into rows (5 per row)
    words = list(pairs.keys())
    for word_chunk in chunk_list(words, 5):
        cols = st.columns(len(word_chunk))
        for i, word in enumerate(word_chunk):
            if word in st.session_state.matched:
                cols[i].button(word, disabled=True)
            elif cols[i].button(word):
                st.session_state.selected_word = word
    st.subheader("🖼️ Select the matching image")

    from itertools import islice


    # Function to chunk dictionary
    def chunk_dict(d, size):
        it = iter(d.items())
        for _ in range(0, len(d), size):
            yield dict(islice(it, size))


    for chunk in chunk_dict(pairs, 5):
        img_cols = st.columns(len(chunk))
        for i, (word, img_url) in enumerate(chunk.items()):
            if word in st.session_state.matched:
                img_cols[i].image(img_url, caption="✅ Matched", use_container_width=True)
            else:
                img_cols[i].image(img_url, use_container_width=True)
                if img_cols[i].button("Select", key=f"img_{word}"):
                    selected_word = st.session_state.selected_word
                    if selected_word is None:
                        st.warning("Please select a word first.")
                    elif word == selected_word:
                        st.success(f"🎉 Correct! {selected_word} matches.")
                        st.session_state.matched.append(word)
                        st.session_state.selected_word = None
                    else:
                        st.error(f"❌ Oops! {selected_word} doesn't match this image.")
                        st.session_state.selected_word = None

    if len(st.session_state.matched) == len(pairs):
        st.balloons()
        st.success("You've matched all the pairs! 🎉")

with tab3:
    st.header("Chatbot")
    if st.button ("Chatbot"):
        st.switch_page("pages/page_ai_chatbot.py")


left, middle, right = st.columns(3)
if left.button("Reading Resources", use_container_width=True):
    left.markdown()
















