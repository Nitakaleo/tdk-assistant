from tkinter import *
import json
from network.network import ChatbotDNN
from network.data_preprocessing import get_train_and_test
import tkinter.ttk as ttk
from GUI.gui_settings import *
import random
import os

BACKGROUND_COLOR = "white"


def load_data_model(intents_path):
    data = open(intents_path).read()
    intents = json.loads(data)
    if not os.path.isfile(r"model/model.h5"):

        x_train, y_test = get_train_and_test(intents)
        dnn_chatbot = ChatbotDNN(x_train, y_test)
        dnn_chatbot.fit()

    else:
        dnn_chatbot = ChatbotDNN()

    return intents, dnn_chatbot


class ChatBotGUI(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("Medibot: Medical-bot Assistant")
        self.geometry(str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT))
        self.resizable(width=FALSE, height=FALSE)
        self.configure(bg=BACKGROUND_COLOR)

        self._ANSWER_TO_BOT = False
        self.tag_for_answer_to_bot = ""

        # add iconphoto

        self.bot_photo = PhotoImage(file="GUI/icons/bot.png")
        self.iconphoto(False, self.bot_photo)
        self.click_btn = PhotoImage(file='GUI/icons/send_btn.png')

        self.bg_logo = Label(self, bg=HEADER_BACKGROUD_COLOR, fg="white")
        self.head_title_label = Label(self, bg=HEADER_BACKGROUD_COLOR, fg="white",
                                      text="Medical-Bot Assistant", font="Helvetica "
                                                                         "16 bold")
        # Header
        self.bot_logo_label = Label(self, bg=HEADER_BACKGROUD_COLOR, image=self.bot_photo)

        # Create Chat window
        self.chat_log_window = self.create_chat_log_window()

        # Bind scrollbar to Chat window
        self.scrollbar = Scrollbar(self, command=self.chat_log_window.yview)
        self.chat_log_window['yscrollcommand'] = self.scrollbar.set

        # Create button "SEND"
        self.send_button = self.create_send_button()
        # Create the box to enter message
        self.entry_box = self.create_entry_box()

        # enter key to send message
        self.entry_box.bind("<Return>", self.chat_callback)

        ttk.Separator(self, orient=HORIZONTAL).place(x=11, y=481, relwidth=0.9)

        # Place all components on the main window
        self.place_all_components()

        self.chat_log_window_config()
        self.intents, self.dnn_chatbot = load_data_model(r"intents.json")
        self.default_entry_box(default_message=" Write your question here being as specific as possible...")
        self.default_chat_log()

    def place_all_components(self):
        self.bg_logo.place(x=0, y=0, height=HEAD_LABEL_HEIGHT, width=WINDOW_WIDTH)
        self.head_title_label.place(x=70, y=(HEAD_LABEL_HEIGHT // 2.5), height=20, width=250)
        self.bot_logo_label.place(x=(WINDOW_WIDTH - 100), y=2, height=60, width=40)
        self.scrollbar.place(x=WINDOW_WIDTH - 21, y=HEAD_LABEL_HEIGHT, height=CHAT_LOG_WINDOW_HEIGHT)
        self.chat_log_window.place(x=1, y=63, height=CHAT_LOG_WINDOW_HEIGHT - 5, width=WINDOW_WIDTH - 22)
        self.entry_box.place(x=10, y=(HEAD_LABEL_HEIGHT + CHAT_LOG_WINDOW_HEIGHT + 5),
                             height=ENTRY_BOX_HEIGHT,
                             width=WINDOW_WIDTH - 45)
        self.send_button.place(x=420, y=520, height=25, width=25)

    def chat_log_window_config(self):
        self.chat_log_window.tag_config('you', foreground="red", background="#ECF6FF")
        self.chat_log_window.tag_config('you2', foreground="black", background="#ECF6FF")
        self.chat_log_window.tag_config('bot', foreground="Blue", background="#D7ECFF")
        self.chat_log_window.tag_config('bot2', foreground="Black", background="#D7ECFF")

    def default_chat_log(self):
        self.chat_log_window.config(foreground="#442265", font=(FONT_CHAT, FONT_SIZE_CHAT))
        self.chat_log_window.config(state=NORMAL, exportselection=0)
        self.chat_log_window.insert(END, "\nMEDIBOT:  ", "bot")
        self.chat_log_window.insert(END,
                                    "Welcome! I'm your personal virtual medical assistant. How can I help you?" + '\n\n',
                                    "bot2")
        self.chat_log_window.config(state=DISABLED, exportselection=0, wrap=WORD)

    def default_entry_box(self, default_message="Type here a message..."):
        self.entry_box.config(fg='grey', font=(FONT_CHAT, FONT_SIZE_CHAT))
        self.entry_box.insert(END, default_message)

        self.entry_box.bind("<FocusIn>", lambda event: self.entry_box_focus_in(event, default_message))
        self.entry_box.bind("<FocusOut>", lambda event: self.entry_box_focus_out(event, default_message))

    def entry_box_focus_in(self, event, default_message):
        if self.entry_box.get() == default_message or self.entry_box.get() == "":
            self.entry_box.delete(0, END)
            self.entry_box.config(fg='black', font=(FONT_CHAT, FONT_SIZE_CHAT))

    def entry_box_focus_out(self, event, default_message):

        if self.entry_box.get() == default_message or self.entry_box.get() == "":
            self.entry_box.delete(0, END)
            self.entry_box.config(fg='grey', font=(FONT_CHAT, FONT_SIZE_CHAT))
            self.entry_box.insert(0, default_message)

    def get_bot_answer(self, user_question):

        predicted_class = self.dnn_chatbot.predict(user_question)
        for row in self.intents["intents"]:
            if row["tag"] == predicted_class:
                return row["tag"], random.choice(row["responses"])
        return None, "Something went wrong!"

    def get_responses_from_tag(self, tag):
        for row in self.intents["intents"]:
            if row["tag"] == tag:
                return row["responses"]
        return None

    # sometimes is the bot to ask question
    def insert_bot_message(self, question):
        self.chat_log_window.insert(END, "\nMEDIBOT:  ", "bot")
        self.chat_log_window.insert(END, question + '\n\n', "bot2")

    def insert_user_message(self, message):
        self.chat_log_window.insert(END, "\nYOU:  ", "you")
        self.chat_log_window.insert(END, message + '\n\n', "you2")

    def chat_callback(self, event):
        self.chat()

    def check_need_bot_question(self, res, question, tag):
        if res[0] == tag:
            self.insert_bot_message(question)
            self._ANSWER_TO_BOT = True
            self.tag_for_answer_to_bot = tag

    def chat(self):

        message = self.entry_box.get()
        self.entry_box.delete("0", END)

        covid_checker_tag = ["flu_symptoms", "covid-19_suggestions", "covid-19_symptoms"]

        asthma_checker_tag = ["asthma-symptoms", "asthma-suggestion"]

        if message != '':
            self.chat_log_window.config(foreground="#442265", font=(FONT_CHAT, FONT_SIZE_CHAT))

            self.chat_log_window.config(state=NORMAL, exportselection=0, wrap=WORD)

            self.insert_user_message(message)

            res = self.get_bot_answer(message)
            if self._ANSWER_TO_BOT is False:

                self.insert_bot_message(res[1])

                for tag_covid in covid_checker_tag:
                    self.check_need_bot_question(res=res, question="Do you want more information about the covid-19 "
                                                                   "symptoms ?", tag=tag_covid)
                for tag_asthma in asthma_checker_tag:
                    self.check_need_bot_question(res=res, question="Do you want more information about the asthma "
                                                                   "symptoms ?", tag=tag_asthma)

                self.check_need_bot_question(res=res, question="Do you want more information about the appendicitis "
                                                               "symptoms ?", tag="appendicitis_symptoms")

                self.check_need_bot_question(res=res, question="Do you want more information about the blood pressure "
                                                               "values?",
                                             tag="blood_pressure")

                self.check_need_bot_question(res=res,
                                             question="Do you want more information about the common cold symptoms?",
                                             tag="common_cold_symptoms")

            else:

                if message.lower() == "yes":

                    # flu and covid-19
                    if self.tag_for_answer_to_bot in covid_checker_tag:
                        bot_answ = self.get_responses_from_tag("covid-19")[0]

                    elif self.tag_for_answer_to_bot in asthma_checker_tag:
                        bot_answ = self.get_responses_from_tag("asthma-attack")[0]

                    elif self.tag_for_answer_to_bot == "appendicitis_symptoms":
                        bot_answ = self.get_responses_from_tag("appendicitis")[0]

                    elif self.tag_for_answer_to_bot == "blood_pressure":
                        bot_answ = self.get_responses_from_tag("blood_pressure_reference")[0]

                    elif self.tag_for_answer_to_bot == "common_cold_symptoms":
                        bot_answ = self.get_responses_from_tag("common_cold_information")[0]
                    else:
                        bot_answ = "Something missing..."

                    self.insert_bot_message(bot_answ)

                elif message.lower() == "no":
                    self.insert_bot_message("OK, as you want.")

                else:
                    self.insert_bot_message(random.choice(["I did not understand your choice."]))

                self._ANSWER_TO_BOT = False

            self.chat_log_window.config(state=DISABLED, exportselection=0)
            self.chat_log_window.update_idletasks()
            self.chat_log_window.yview(END)

    def create_chat_log_window(self):
        return Text(self, bd=0, bg="white", font=FONT_CHAT)

    def create_send_button(self):
        return Button(master=self, image=self.click_btn, height=30, width=30, command=self.chat, relief="flat",
                      highlightthickness=0, bd=0, bg=BACKGROUND_COLOR, activebackground=BACKGROUND_COLOR)

    def create_entry_box(self):
        return Entry(self, bd=0, bg="#ECF6FF", width="29", font=FONT_CHAT)

    def run(self):
        self.mainloop()
