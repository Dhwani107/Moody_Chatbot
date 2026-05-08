from dotenv import load_dotenv

load_dotenv()

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_mistralai import ChatMistralAI


st.set_page_config(page_title="Mood Chatbot UI", page_icon="M", layout="wide")

MOODS = {
    "1": {
        "label": "Happy",
        "subtitle": "Bright, upbeat, and positive.",
        "system": "You are a happy ai agent and reply in a happy tone",
        "gradient": "linear-gradient(135deg, #ffe259 0%, #ffa751 100%)",
        "accent": "#fff7d6",
    },
    "2": {
        "label": "Sad",
        "subtitle": "Soft, calm, and comforting.",
        "system": "You are a sad ai agent and reply in a sad tone",
        "gradient": "linear-gradient(135deg, #1f3c88 0%, #3f72af 48%, #112d4e 100%)",
        "accent": "#d9ecff",
    },
    "3": {
        "label": "Angry",
        "subtitle": "Strong, intense, and bold.",
        "system": "You are an angry ai agent and reply in an angry tone",
        "gradient": "linear-gradient(135deg, #2b0f16 0%, #7f1d1d 42%, #ff6b35 100%)",
        "accent": "#ffe2d0",
    },
    "4": {
        "label": "Funny",
        "subtitle": "Playful, witty, and light.",
        "system": "You are a funny ai agent and reply in a funny tone",
        "gradient": "linear-gradient(135deg, #672d91 0%, #8e44ad 38%, #f39c12 100%)",
        "accent": "#fff0cc",
    },
}

DEFAULT_MOOD = "2"

if "selected_mood" not in st.session_state:
    st.session_state.selected_mood = DEFAULT_MOOD
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_error" not in st.session_state:
    st.session_state.last_error = None


def reset_chat_for_mood(mood_key: str) -> None:
    mood = MOODS[mood_key]
    st.session_state.selected_mood = mood_key
    st.session_state.messages = [
        AIMessage(
            content=f"You selected {mood['label']}. Ask me anything and I’ll reply in that tone."
        )
    ]

selected = MOODS[st.session_state.selected_mood]

st.markdown(
    f"""
    <style>
        .stApp {{
            background: {selected['gradient']};
            color: white;
        }}
        .stApp::before {{
            content: "";
            position: fixed;
            inset: 0;
            background-image: radial-gradient(rgba(255,255,255,0.12) 1px, transparent 1px);
            background-size: 24px 24px;
            opacity: 0.16;
            pointer-events: none;
        }}
        .hero {{
            position: relative;
            padding: 1.5rem 1.6rem;
            border-radius: 28px;
            background: rgba(8, 10, 18, 0.25);
            border: 1px solid rgba(255,255,255,0.16);
            backdrop-filter: blur(16px);
            box-shadow: 0 18px 50px rgba(0,0,0,0.18);
            margin-bottom: 1rem;
        }}
        .hero h1 {{
            margin: 0;
            font-size: 2.35rem;
            line-height: 1;
        }}
        .hero p {{
            margin: 0.45rem 0 0;
            color: {selected['accent']};
            font-size: 1.02rem;
        }}
        .mood-card {{
            padding: 1rem;
            border-radius: 20px;
            background: rgba(255,255,255,0.12);
            border: 1px solid rgba(255,255,255,0.16);
            color: white;
            margin-bottom: 0.85rem;
        }}
        .active-card {{
            box-shadow: 0 0 30px rgba(255,255,255,0.18);
        }}
        div[data-testid="stSidebar"] {{
            background: rgba(8, 10, 18, 0.34);
            backdrop-filter: blur(18px);
            border-right: 1px solid rgba(255,255,255,0.12);
        }}
        .scene {{
            border-radius: 22px;
            padding: 0.9rem 1rem;
            text-align: center;
            letter-spacing: 0.16em;
            background: rgba(255,255,255,0.12);
            border: 1px solid rgba(255,255,255,0.16);
            margin-bottom: 1rem;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="hero">
        <h1>Mood Chatbot UI</h1>
        <p>Pick a mood first, then chat with the bot in that tone. This UI matches your CLI options: Happy, Sad, Angry, and Funny.</p>
    </div>
    <div class="scene">CURRENT MOOD: {selected['label'].upper()}</div>
    """,
    unsafe_allow_html=True,
)

st.markdown("### Choose a mood")
mood_columns = st.columns(4)
for mood_key, column in zip(MOODS.keys(), mood_columns):
    mood = MOODS[mood_key]
    with column:
        is_active = mood_key == st.session_state.selected_mood
        st.markdown(
            f"""
            <div class="mood-card {'active-card' if is_active else ''}" style="
                background: {'rgba(255,255,255,0.22)' if is_active else 'rgba(255,255,255,0.10)'};
                border: 1px solid {'rgba(255,255,255,0.35)' if is_active else 'rgba(255,255,255,0.16)'};
            ">
                <div style="font-weight: 700; font-size: 1.05rem;">{mood['label']}</div>
                <div style="opacity: 0.9; font-size: 0.92rem; margin-top: 0.25rem;">{mood['subtitle']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(f"Use {mood['label']}", key=f"select_{mood_key}", use_container_width=True):
            reset_chat_for_mood(mood_key)
            st.rerun()

selected = MOODS[st.session_state.selected_mood]

left, right = st.columns([1.55, 1])
with left:
    st.markdown("### Chat")
    st.caption("Type a message below. The assistant will respond in the selected mood.")

    if not st.session_state.messages:
        reset_chat_for_mood(st.session_state.selected_mood)

    for message in st.session_state.messages:
        role = "assistant" if isinstance(message, AIMessage) else "user"
        with st.chat_message(role):
            st.markdown(message.content)

    user_prompt = st.chat_input(f"Message for the {selected['label'].lower()} mood bot...")

    if user_prompt:
        st.session_state.messages.append(HumanMessage(content=user_prompt))
        try:
            model = ChatMistralAI(model="mistral-small-2506", temperature=0.9)
            conversation = [SystemMessage(content=selected["system"]), *st.session_state.messages]
            response = model.invoke(conversation)
            st.session_state.messages.append(AIMessage(content=response.content))
        except Exception as error:
            st.session_state.messages.append(
                AIMessage(
                    content=(
                        "I could not reach the model right now. Check your API key and internet connection.\n\n"
                        f"Error: {error}"
                    )
                )
            )
        st.rerun()

with right:
    st.markdown("### Mood guide")
    st.write(f"**Happy:** {MOODS['1']['system']}")
    st.write(f"**Sad:** {MOODS['2']['system']}")
    st.write(f"**Angry:** {MOODS['3']['system']}")
    st.write(f"**Funny:** {MOODS['4']['system']}")
    st.markdown("### How to use")
    st.write("1. Pick a mood button.")
    st.write("2. Type your message in chat.")
    st.write("3. The response follows the selected tone.")
