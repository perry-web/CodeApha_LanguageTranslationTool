
---

#  AI Translation Desktop App (Python 3.13+)

A modern, user-friendly **AI Translator Desktop Application** built with **Python and Tkinter**.  
It supports **text translation**, **speech recognition**, and **speech-to-speech translation**, powered by **Google Translate API**.  
The app automatically detects the source language or lets users choose one, offers real-time translation, and stores translation history in a CSV file.

---

##  Features

-  **Auto Language Detection** - automatically detect input language.
-  **Translate to Any Language** - users can choose their target language.
-  **Speech Recognition** - convert spoken words to text.
-  **Speech-to-Speech Translation** - speak in one language, hear the translation in another.
-  **Text-to-Speech Output** - listen to translated text via `gTTS`.
-  **Real-time Translation** - instant translation as you type.
-  **History Logging** - saves all translations with timestamps in `translation_history.csv`.
-  **Modern GUI** - clean, minimal, and user-friendly Tkinter interface.

---

##  Tech Stack

| Library | Purpose |
|----------|----------|
| `tkinter` | Graphical User Interface |
| `googletrans==4.0.0-rc1` | Translation (unofficial Google Translate API) |
| `speech_recognition` | Speech-to-text conversion |
| `gtts` | Text-to-speech (Google Text-to-Speech) |
| `playsound` | Play translated audio |
| `datetime`, `csv` | Manage timestamps & translation history |
| `threading` | Real-time translation and background tasks |

---

##  Installation

### 1. Clone the repository
```bash
git clone https://github.com/perry-web/CodeApha_LanguageTranslationTool.git
cd AI-Translation-App
````

### 2. Install dependencies

```bash
pip install googletrans==4.0.0-rc1 gtts playsound SpeechRecognition
```

### 2. Run the app

```bash
python app.py
```

---

##  How to Use

### 1. **Launch the App**

Start the app - the Tkinter window will appear with mode buttons at the top.

### 2. **Select Translation Mode**

Choose one of:

* **Text Translation** - type text and translate it.
* **Speech → Text** - speak to convert voice to text.
* **Speech → Speech** - speak and hear the translated version aloud.

### 3. **Set Target Language**

Pick your target language (e.g., French, German, Swahili, etc.)
If no source language is selected, the app **auto-detects** it.

### 4. **Translate**

Type text (or speak), then press **Translate**.
Optionally enable **Auto Translate** for real-time translation.

### 5. **Listen to Translation**

Click **Speak Output** to hear the translated text spoken aloud.

### 6. **View Translation History**

All translations are saved automatically to:

```
translation_history.csv
```

---

##  Example of Translation History

| timestamp           | mode | source_lang | target_lang | source_text  | translated_text |
| ------------------- | ---- | ----------- | ----------- | ------------ | --------------- |
| 2025-10-23 14:44:54 | text | fr          | en          | bonjour      | hello           |
| 2025-10-23 14:45:10 | text | en          | de          | good morning | Guten Morgen    |

---

##  Project Structure

```
AI_Translation_App/
│
├── ai_translator.py           # Main application (standalone executable)
├── ai_translator.ipynb        # Jupyter Notebook version for demo/testing
├── translation_history.csv    # Logs of all translations
├── translated_audio.mp3       # Temporary audio file (auto-deleted)
└── README.md                  # Documentation
```

---

##  Notes & Limitations

* `googletrans` uses an **unofficial API**; it may occasionally break if Google updates endpoints.
* For commercial/production environments, use the **official Google Cloud Translation API**.
* Internet connection is required.
* Background noise may affect speech recognition accuracy.

---


##  Author

 [perrykoko@engineer.com](mailto:perrykoko@engineer.com)
 [LinkedIn](https://linkedin.com/in/perry-koko-cybersecurity-ml-engineer)

---

##  License

This project is released under the **MIT License**  you are free to use, modify, and distribute it for educational or personal projects.

---

##  Acknowledgments

* [Google Translate](https://translate.google.com) for translation service
* [gTTS](https://pypi.org/project/gTTS/) for speech synthesis
* [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) for audio input handling

---
