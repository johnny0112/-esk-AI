import streamlit as st
import openai
import google.generativeai as genai

#replace "openai_api" with name of your file with api key
with open("openai_api", "r") as file:
    api_key = file.read().strip()
openai.api_key = api_key

#replace "gemini_api" with name of your file with api key
with open("gemini_api", "r") as file:
    gemini_api_key = file.read().strip()
genai.configure(api_key=gemini_api_key)

def get_gpt_response(prompt):
    result = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return result


def generate_gemini_response(prompt):
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    response = model.generate_content(prompt)
    return response

def transcribe_audio(audio_file):
    transcript = openai.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )
    return transcript


st.markdown(
    """
    <style>
    body {
        background-color: #f0f2f6;
    }
    .main {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
    }
    .sidebar .sidebar-content h1 {
        color: #4b8bbe;
    }
    .stRadio > div {
        display: flex;
        flex-direction: column;
    }
    .stRadio > div > label {
        background: rgba(75, 139, 190, 0.2);
        color: #4b8bbe;
        border: 1px solid #4b8bbe;
        border-radius: 25px;
        padding: 10px 15px;
        margin-bottom: 10px;
        cursor: pointer;
        transition: background-color 0.3s ease, color 0.3s ease;
        text-align: center;
        width: 100%;
        box-sizing: border-box;
    }
    .stRadio > div > label:hover {
        background-color: rgba(75, 139, 190, 0.4);
    }
    .stRadio > div > label[data-selected="true"] {
        background-color: #4b8bbe;
        color: white;
    }
    .chat-option > div > div > label {
        background: rgba(46, 204, 113, 0.2);
        color: #2ecc71;
        border: 1px solid #2ecc71;
        border-radius: 25px;
        padding: 10px 15px;
        margin-bottom: 10px;
        cursor: pointer;
        transition: background-color 0.3s ease, color 0.3s ease;
        text-align: center;
        width: 100%;
        box-sizing: border-box;
    }
    .chat-option > div > div > label:hover {
        background-color: rgba(46, 204, 113, 0.4);
    }
    .chat-option > div > div > label[data-selected="true"] {
        background-color: #2ecc71;
        color: white;
    }
    h1 {
        color: #4b8bbe;
    }
    h2 {
        color: #4b8bbe;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.title("Česká AI 🤖")


st.sidebar.title("Navigace")
page = st.sidebar.radio("Vyberte stránku", ["Chat", "Nahrát nahrávku"])

if page == "Chat":
    st.header("Chat s Umělou inteligencí 💬")
    st.markdown('<div class="chat-option">', unsafe_allow_html=True)
    service_choice = st.radio("Vyberte službu", ["Chat s GPT", "Chat s Gemini"])
    st.markdown('</div>', unsafe_allow_html=True)

    prompt = st.text_input("Zadej prompt")
    if st.button("Odeslat"):
        if prompt:
            if service_choice == "Chat s GPT":
                response = get_gpt_response(prompt)
                st.subheader("Odpověď od GPT-4:")
                st.write(response.choices[0].message.content)
            else:
                response = generate_gemini_response(prompt)
                st.subheader("Odpověď od Gemini AI:")
                st.write(response.text)
        else:
            st.warning("Zadejte prompt prosím")

elif page == "Nahrát nahrávku":
    st.header("Nahrát a přepsat nahrávku 🎤")
    st.markdown("**Nahrajte audio soubor ve formátu mp3, wav nebo ogg a klikněte na 'Přepsat'.**")
    audio_file = st.file_uploader("Nahrajte audio soubor", type=["mp3", "wav", "ogg"])
    if st.button("Přepsat"):
        if audio_file:
            st.audio(audio_file, format='audio/mp3')
            transcript = transcribe_audio(audio_file)
            st.subheader("Zde je Váš přepis 😊")
            st.write(transcript.text)
        else:
            st.warning("Nahrajte prosím audio soubor.")
