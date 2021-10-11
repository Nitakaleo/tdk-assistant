from GUI.gui import ChatBotGUI
import nltk

if __name__ == "__main__":
    nltk.download('punkt')
    nltk.download('wordnet')
    nltk.download('averaged_perceptron_tagger')

    chatbot = ChatBotGUI()
    chatbot.run()
