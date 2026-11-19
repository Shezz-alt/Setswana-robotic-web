import tkinter as tk
from tkinter import messagebox


# ============================================================
# MEBALA
# ============================================================

BACKGROUND = "#66A96B"
LIGHT_BLUE = "#BDE7F5"
LIGHT_PINK = "#F8D7E6"
WHITE = "#FFFFFF"
SOFT_GREEN = "#BFE3C0"
SOFT_YELLOW = "#FFE8A3"
BLACK = "#000000"
CREAM = "#FFFDF7"
DEEP_BLUE = "#274C77"


# ============================================================
# DIPOTSO
# ============================================================

QUESTIONS = [

    {
        "question": "1. Roboto ke eng?",

        "options": [

            (
                "Motšhini o o ka rulaganyediwang go dira "
                "ditiro ka go latela ditaelo."
            ),

            "Buka e e dirisiwang go kwala ditaelo.",

            "Sekirini sa khomphuthara.",

            "Mofuta wa motlakase."
        ],

        "answer": 0,

        "explanation": (
            "Roboto ke motšhini o o ka rulaganyediwang "
            "go dira ditiro ka go latela ditaelo "
            "tse e di neilweng."
        )
    },


    {
        "question": (
            "2. Ke karolo efe ya roboto e e amogelang "
            "le go diragatsa ditaelo?"
        ),

        "options": [

            "Motswedi wa maatla",

            "Selaodi",

            "Maoto",

            "Ditsebe"
        ],

        "answer": 1,

        "explanation": (
            "Selaodi se amogela le go diragatsa ditaelo "
            "tse di laolang tsela e roboto e dirang ka yone."
        )
    },


    {
        "question": (
            "3. Disensa di thusa roboto go dira eng?"
        ),

        "options": [

            "Go kwala code fela.",

            (
                "Go lemoga tshedimosetso "
                "mo tikologong."
            ),

            "Go fetola leina la roboto.",

            "Go boloka dithuto mo bukeng."
        ],

        "answer": 1,

        "explanation": (
            "Disensa di thusa roboto go lemoga dilo "
            "tse di jaaka lesedi, bokgakala, "
            "go ama kgotsa motsamao."
        )
    },


    {
        "question": "4. Algorithm ke eng?",

        "options": [

            "Setshwantsho sa roboto.",

            "Motswedi wa maatla.",

            (
                "Tatelano ya dikgato kgotsa ditaelo "
                "go dira tiro."
            ),

            "Leina la sensa."
        ],

        "answer": 2,

        "explanation": (
            "Algorithm ke tatelano ya dikgato kgotsa "
            "ditaelo tse di rulagantsweng go rarabolola "
            "bothata kgotsa go dira tiro."
        )
    },


    {
        "question": (
            "5. Taelo ya 'Sokologela Mojeng' e dira eng?"
        ),

        "options": [

            "E tsamaisa roboto kwa pele.",

            "E tsamaisa roboto kwa morago.",

            (
                "E fetola tsela ya roboto gore "
                "e lebe kwa molemeng."
            ),

            (
                "E fetola tsela ya roboto gore "
                "e lebe kwa mojeng."
            )
        ],

        "answer": 3,

        "explanation": (
            "Sokologela Mojeng e fetola direction ya "
            "roboto gore e lebe kwa mojeng. Roboto ga e "
            "suthe mo seleng fa e sokologa."
        )
    }
]


# ============================================================
# QUIZ MODULE
# ============================================================

class QuizModule:

    def __init__(self, parent):

        self.parent = parent

        self.current_question = 0

        self.score = 0

        self.selected_answer = tk.IntVar(
            value=-1
        )

        self.answer_checked = False


        self.parent.configure(
            bg=BACKGROUND
        )


        self.build_interface()

        self.display_question()


    # ========================================================
    # BUILD INTERFACE
    # ========================================================

    def build_interface(self):

        tk.Label(
            self.parent,
            text="🧠 DIPOTSO TSA DIROBOTO",
            font=("Arial", 24, "bold"),
            fg=BLACK,
            bg=BACKGROUND
        ).pack(
            pady=(22, 4)
        )


        tk.Label(
            self.parent,
            text=(
                "Araba dipotso tse 5 go leka gore "
                "o tlhalogantse dithuto tsa diroboto."
            ),
            font=("Arial", 12, "bold"),
            fg=BLACK,
            bg=BACKGROUND,
            wraplength=720,
            justify="center"
        ).pack(
            pady=(0, 10)
        )


        self.progress_label = tk.Label(
            self.parent,
            text="",
            font=("Arial", 11, "bold"),
            fg=BLACK,
            bg=SOFT_YELLOW
        )

        self.progress_label.pack(
            fill="x",
            padx=140,
            pady=(0, 10),
            ipady=6
        )


        self.quiz_card = tk.Frame(
            self.parent,
            bg=WHITE,
            highlightbackground=BLACK,
            highlightthickness=1
        )

        self.quiz_card.pack(
            fill="both",
            expand=True,
            padx=120,
            pady=(0, 20)
        )


        self.question_label = tk.Label(
            self.quiz_card,
            text="",
            font=("Arial", 16, "bold"),
            fg=BLACK,
            bg=LIGHT_BLUE,
            wraplength=760,
            justify="left",
            anchor="w"
        )

        self.question_label.pack(
            fill="x",
            padx=20,
            pady=(20, 15),
            ipady=10
        )


        self.options_frame = tk.Frame(
            self.quiz_card,
            bg=WHITE
        )

        self.options_frame.pack(
            fill="x",
            padx=35,
            pady=5
        )


        self.option_buttons = []


        for index in range(4):

            button = tk.Radiobutton(
                self.options_frame,
                text="",
                variable=self.selected_answer,
                value=index,
                font=("Arial", 12),
                fg=BLACK,
                bg=CREAM,
                activebackground=LIGHT_BLUE,
                activeforeground=BLACK,
                selectcolor=SOFT_YELLOW,
                anchor="w",
                justify="left",
                wraplength=720,
                padx=12,
                pady=10,
                indicatoron=True
            )

            button.pack(
                fill="x",
                pady=5
            )


            self.option_buttons.append(
                button
            )


        self.feedback_label = tk.Label(
            self.quiz_card,
            text="",
            font=("Arial", 11, "bold"),
            fg=BLACK,
            bg=WHITE,
            wraplength=760,
            justify="left"
        )

        self.feedback_label.pack(
            fill="x",
            padx=35,
            pady=(12, 8)
        )


        button_frame = tk.Frame(
            self.quiz_card,
            bg=WHITE
        )

        button_frame.pack(
            pady=(5, 20)
        )


        self.check_button = tk.Button(
            button_frame,
            text="✓  Netefatsa Karabo",
            font=("Arial", 11, "bold"),
            bg=SOFT_GREEN,
            fg=BLACK,
            activebackground=SOFT_YELLOW,
            activeforeground=BLACK,
            relief="flat",
            cursor="hand2",
            width=20,
            height=2,
            command=self.check_answer
        )

        self.check_button.pack(
            side="left",
            padx=7
        )


        self.next_button = tk.Button(
            button_frame,
            text="E e Latelang →",
            font=("Arial", 11, "bold"),
            bg=LIGHT_PINK,
            fg=BLACK,
            activebackground=SOFT_YELLOW,
            activeforeground=BLACK,
            relief="flat",
            cursor="hand2",
            width=18,
            height=2,
            state="disabled",
            command=self.next_question
        )

        self.next_button.pack(
            side="left",
            padx=7
        )


    # ========================================================
    # DISPLAY QUESTION
    # ========================================================

    def display_question(self):

        question_data = QUESTIONS[
            self.current_question
        ]


        self.selected_answer.set(
            -1
        )

        self.answer_checked = False


        self.feedback_label.config(
            text="",
            bg=WHITE
        )


        self.progress_label.config(
            text=(
                f"Potso {self.current_question + 1} "
                f"ya {len(QUESTIONS)}"
            )
        )


        self.question_label.config(
            text=question_data["question"]
        )


        for index, option in enumerate(
            question_data["options"]
        ):

            self.option_buttons[
                index
            ].config(
                text=option,
                state="normal",
                bg=CREAM
            )


        self.check_button.config(
            state="normal"
        )


        if (
            self.current_question
            == len(QUESTIONS) - 1
        ):

            next_text = (
                "Bona Dipoelo →"
            )

        else:

            next_text = (
                "E e Latelang →"
            )


        self.next_button.config(
            state="disabled",
            text=next_text
        )


    # ========================================================
    # CHECK ANSWER
    # ========================================================

    def check_answer(self):

        if self.answer_checked:

            return


        selected = (
            self.selected_answer.get()
        )


        if selected == -1:

            messagebox.showinfo(
                "Karabo",
                "Tlhopha karabo pele."
            )

            return


        question_data = QUESTIONS[
            self.current_question
        ]


        correct_answer = (
            question_data["answer"]
        )


        self.answer_checked = True


        if selected == correct_answer:

            self.score += 1


            self.feedback_label.config(
                text=(
                    "✓ Karabo e siame!\n\n"
                    f"{question_data['explanation']}"
                ),
                bg=SOFT_GREEN
            )


        else:

            correct_text = (
                question_data[
                    "options"
                ][
                    correct_answer
                ]
            )


            self.feedback_label.config(
                text=(
                    "✗ Karabo ga e a siama.\n\n"
                    f"Karabo e e siameng: "
                    f"{correct_text}\n\n"
                    f"{question_data['explanation']}"
                ),
                bg=LIGHT_PINK
            )


        for button in (
            self.option_buttons
        ):

            button.config(
                state="disabled"
            )


        self.check_button.config(
            state="disabled"
        )


        self.next_button.config(
            state="normal"
        )


    # ========================================================
    # NEXT QUESTION
    # ========================================================

    def next_question(self):

        if not self.answer_checked:

            return


        if (
            self.current_question
            < len(QUESTIONS) - 1
        ):

            self.current_question += 1

            self.display_question()


        else:

            self.show_results()


    # ========================================================
    # RESULTS
    # ========================================================

    def show_results(self):

        for widget in (
            self.quiz_card.winfo_children()
        ):

            widget.destroy()


        percentage = round(
            (
                self.score
                / len(QUESTIONS)
            )
            * 100
        )


        if percentage == 100:

            result_message = (
                "🌟 O dirile sentle thata! "
                "O arabile dipotso tsotlhe ka nepo."
            )


        elif percentage >= 60:

            result_message = (
                "👏 O dirile sentle. "
                "Boela mo dithutong tse o sa "
                "di tlhaloganyeng sentle."
            )


        else:

            result_message = (
                "📘 Tswelela go ithuta. "
                "Boela mo Dithutong mme "
                "o leke dipotso gape."
            )


        tk.Label(
            self.quiz_card,
            text="DIPOelo TSA DIPOTSO",
            font=("Arial", 22, "bold"),
            fg=BLACK,
            bg=LIGHT_BLUE
        ).pack(
            fill="x",
            padx=30,
            pady=(35, 15),
            ipady=10
        )


        tk.Label(
            self.quiz_card,
            text=(
                f"{self.score} / "
                f"{len(QUESTIONS)}"
            ),
            font=("Arial", 38, "bold"),
            fg=BLACK,
            bg=WHITE
        ).pack(
            pady=(15, 5)
        )


        tk.Label(
            self.quiz_card,
            text=f"{percentage}%",
            font=("Arial", 22, "bold"),
            fg=BLACK,
            bg=SOFT_YELLOW
        ).pack(
            ipadx=20,
            ipady=8,
            pady=10
        )


        tk.Label(
            self.quiz_card,
            text=result_message,
            font=("Arial", 12, "bold"),
            fg=BLACK,
            bg=WHITE,
            wraplength=650,
            justify="center"
        ).pack(
            padx=40,
            pady=15
        )


        tk.Label(
            self.quiz_card,
            text=(
                "Dipoelo tsa dipotso tseno ga di fetole "
                "Kgatelopele ya gago ya dithuto "
                "le dikgwetlho."
            ),
            font=("Arial", 10),
            fg=BLACK,
            bg=CREAM,
            wraplength=620,
            justify="center"
        ).pack(
            padx=40,
            pady=(5, 15),
            ipadx=10,
            ipady=8
        )


        tk.Button(
            self.quiz_card,
            text="↻  Leka Gape",
            font=("Arial", 11, "bold"),
            bg=SOFT_GREEN,
            fg=BLACK,
            activebackground=SOFT_YELLOW,
            activeforeground=BLACK,
            relief="flat",
            cursor="hand2",
            width=18,
            height=2,
            command=self.restart_quiz
        ).pack(
            pady=(5, 25)
        )


        self.progress_label.config(
            text="Dipotso di feditswe"
        )


    # ========================================================
    # RESTART QUIZ
    # ========================================================

    def restart_quiz(self):

        self.current_question = 0

        self.score = 0

        self.selected_answer.set(
            -1
        )

        self.answer_checked = False


        for widget in (
            self.quiz_card.winfo_children()
        ):

            widget.destroy()


        self.question_label = tk.Label(
            self.quiz_card,
            text="",
            font=("Arial", 16, "bold"),
            fg=BLACK,
            bg=LIGHT_BLUE,
            wraplength=760,
            justify="left",
            anchor="w"
        )

        self.question_label.pack(
            fill="x",
            padx=20,
            pady=(20, 15),
            ipady=10
        )


        self.options_frame = tk.Frame(
            self.quiz_card,
            bg=WHITE
        )

        self.options_frame.pack(
            fill="x",
            padx=35,
            pady=5
        )


        self.option_buttons = []


        for index in range(4):

            button = tk.Radiobutton(
                self.options_frame,
                text="",
                variable=self.selected_answer,
                value=index,
                font=("Arial", 12),
                fg=BLACK,
                bg=CREAM,
                activebackground=LIGHT_BLUE,
                activeforeground=BLACK,
                selectcolor=SOFT_YELLOW,
                anchor="w",
                justify="left",
                wraplength=720,
                padx=12,
                pady=10,
                indicatoron=True
            )

            button.pack(
                fill="x",
                pady=5
            )


            self.option_buttons.append(
                button
            )


        self.feedback_label = tk.Label(
            self.quiz_card,
            text="",
            font=("Arial", 11, "bold"),
            fg=BLACK,
            bg=WHITE,
            wraplength=760,
            justify="left"
        )

        self.feedback_label.pack(
            fill="x",
            padx=35,
            pady=(12, 8)
        )


        button_frame = tk.Frame(
            self.quiz_card,
            bg=WHITE
        )

        button_frame.pack(
            pady=(5, 20)
        )


        self.check_button = tk.Button(
            button_frame,
            text="✓  Netefatsa Karabo",
            font=("Arial", 11, "bold"),
            bg=SOFT_GREEN,
            fg=BLACK,
            relief="flat",
            cursor="hand2",
            width=20,
            height=2,
            command=self.check_answer
        )

        self.check_button.pack(
            side="left",
            padx=7
        )


        self.next_button = tk.Button(
            button_frame,
            text="E e Latelang →",
            font=("Arial", 11, "bold"),
            bg=LIGHT_PINK,
            fg=BLACK,
            relief="flat",
            cursor="hand2",
            width=18,
            height=2,
            state="disabled",
            command=self.next_question
        )

        self.next_button.pack(
            side="left",
            padx=7
        )


        self.display_question()