import tkinter as tk
from tkinter import messagebox

from database import complete_lesson, get_completed_lessons


# ============================================================
# MEBALA YA THULAGANYO
# ============================================================

BACKGROUND = "#66A96B"
LIGHT_BLUE = "#BDE7F5"
LIGHT_PINK = "#F8D7E6"
WHITE = "#FFFFFF"
SOFT_GREEN = "#BFE3C0"
SOFT_YELLOW = "#FFE8A3"
BLACK = "#000000"
CREAM = "#FFFDF7"


# ============================================================
# DITHUTO TSA DIROBOTO
# ============================================================

LESSONS = [

    {
        "title": "THUTO 1: MATSENO A DIROBOTO",
        "menu": "1. Matseno a Diroboto",

        "content": """
ROBOTO KE ENG?

Roboto ke motšhini o o ka rulaganyediwang go dira ditiro tse di
rileng ka go latela ditaelo tse e di neilweng.

Roboto e ka dirisiwa go dira ditiro tse di farologaneng. Diroboto
dingwe di kgona go tsamaya, go lemoga dilo tse di di dikologileng
le go dira tiro go ya ka ditaelo tse di rulagantsweng.

DIKAI TSA DIROBOTO

• Diroboto tse di dirisiwang mo madirelong.
• Diroboto tse di dirisiwang mo dikolong go ruta barutwana.
• Diroboto tse di phepafatsang matlo.
• Diroboto tse di dirisiwang mo maokelong.
• Diroboto tse di dirisiwang go batlisisa lefaufau.

GORENG RE ITHUTA KA DIROBOTO?

Go ithuta ka diroboto go ka thusa barutwana go godisa bokgoni jwa:

• Go rarabolola mathata.
• Go akanya ka tatelano ya ditaelo.
• Go ithuta ka programming.
• Go tlhama le go leka megopolo e mešwa.
• Go akanya ka tsela e e rulaganeng.

Mo thulaganyong eno, o tla ithuta gore ditaelo di ka dirisiwa
jang go laola roboto e e etsisiwang mo khomphuthareng.
"""
    },


    {
        "title": "THUTO 2: DIKAROLO TSA ROBOTO",
        "menu": "2. Dikarolo tsa Roboto",

        "content": """
DIKAROLO TSA ROBOTO

Roboto e ka nna le dikarolo tse di farologaneng go ya ka tiro
e e diretsweng go e dira.

1. SELAODI

Selaodi se laola tsela e roboto e dirang ka yone. Se amogela le
go diragatsa ditaelo tse di bolelelang roboto gore e dire eng.

2. DISENSA

Disensa di thusa roboto go lemoga tshedimosetso e e tswang mo
tikologong ya yone.

Ka sekai, sensor e ka lemoga:

• Lesedi
• Bokgakala
• Go ama
• Motsamao

3. ACTUATOR

Actuator ke karolo e e thusang roboto go dira motsamao kgotsa
tiragalo nngwe.

Ka sekai, motor e ka dirisiwa go dikolosa maotwana gore roboto
e kgone go tsamaya.

4. MOTSWEDI WA MAATLA

Roboto e tlhoka maatla gore e kgone go dira.

Diroboto dingwe di dirisa dibeteri, fa tse dingwe di dirisa
metswedi e mengwe ya motlakase.

Dikarolo tseno di dirisana mmogo go thusa roboto go lemoga
tikologo, go amogela ditaelo le go dira tiro.
"""
    },


    {
        "title": "THUTO 3: MOTSAMAO LE DITAELO",
        "menu": "3. Motsamao le Ditaelo",

        "content": """
MOTSAMAO WA ROBOTO

Roboto e tlhoka ditaelo tse di tlhaloganyegang gore e itse gore
e tshwanetse go tsamaya jang.

Mo simulator ya rona, re tla dirisa ditaelo tse di jaaka:

• Tsamaya pele
• Tsamaya morago
• Sokologela molemeng
• Sokologela mojeng
• Ema

TATELANO YA DITAELO

Roboto e tshwanetse go diragatsa ditaelo ka tatelano e e
rulagantsweng.

Ka sekai:

1. Tsamaya pele
2. Tsamaya pele
3. Sokologela mojeng
4. Tsamaya pele
5. Ema

Fa tatelano ya ditaelo e fetolwa, roboto e ka feleletsa e le
mo lefelong le le farologaneng.

Ka jalo, go rulaganya ditaelo ka tatelano e e siameng ke karolo
e e botlhokwa ya programming.

Mo karolong ya programming ya thulaganyo eno, o tla kgona go
tlhopha ditaelo le go bona roboto e di diragatsa.
"""
    },


    {
        "title": "THUTO 4: ALGORITHM LE PROGRAMMING",
        "menu": "4. Algorithm le Programming",

        "content": """
ALGORITHM KE ENG?

Algorithm ke tatelano ya dikgato kgotsa ditaelo tse di
rulagantsweng go rarabolola bothata kgotsa go dira tiro
e e rileng.

Ka sekai, re ka naya roboto algorithm e e latelang:

Kgato 1: Tsamaya pele
Kgato 2: Tsamaya pele
Kgato 3: Sokologela mojeng
Kgato 4: Tsamaya pele
Kgato 5: Ema

PROGRAMMING YA ROBOTO

Programming ke mokgwa wa go naya khomphuthara kgotsa roboto
ditaelo tse e ka di diragatsang.

Mo thulaganyong eno, ga o tlhoke go kwala Python code gore
o kgone go laola roboto.

O tla dirisa diboloko tsa ditaelo tse di bonalang mo sekirining.

Mokgwa ono o tlhotlheleditswe ke Scratch, e e dirisang diboloko
tsa programming go thusa barutwana go ithuta dikgopolo tsa
programming ka tsela e e bonalang.

O tla kgona go:

• Tlhopha ditaelo.
• Rulaganya ditaelo ka tatelano.
• Simolola lenaneo.
• Leba roboto e diragatsa ditaelo.
• Fetola ditaelo fa roboto e sa fitlhe kwa e tshwanetseng go ya teng.

Seno se tla go thusa go tlhaloganya kamano fa gare ga algorithm,
programming le tsela e roboto e dirang ka yone.
"""
    }
]


# ============================================================
# KAROLO YA DITHUTO
# ============================================================

class LessonModule:

    def __init__(self, parent):

        self.parent = parent
        self.current_lesson = 0
        self.lesson_buttons = []

        self.parent.configure(
            bg=BACKGROUND
        )

        self.build_interface()
        self.display_lesson()


    # ========================================================
    # AGA TEBEGO
    # ========================================================

    def build_interface(self):

        tk.Label(
            self.parent,
            text="📘 DITHUTO TSA DIROBOTO",
            font=("Arial", 24, "bold"),
            fg=BLACK,
            bg=BACKGROUND
        ).pack(
            pady=(18, 2)
        )


        tk.Label(
            self.parent,
            text="Ithute ka diroboto le programming",
            font=("Arial", 12, "bold"),
            fg=BLACK,
            bg=BACKGROUND
        ).pack(
            pady=(0, 10)
        )


        lesson_area = tk.Frame(
            self.parent,
            bg=BACKGROUND
        )

        lesson_area.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(5, 15)
        )


        # ====================================================
        # LENANE LA DITHUTO
        # ====================================================

        lesson_menu = tk.Frame(
            lesson_area,
            width=260,
            bg=WHITE,
            highlightbackground=BLACK,
            highlightthickness=1
        )

        lesson_menu.pack(
            side="left",
            fill="y",
            padx=(0, 15)
        )

        lesson_menu.pack_propagate(
            False
        )


        tk.Label(
            lesson_menu,
            text="DITHUTO",
            font=("Arial", 15, "bold"),
            fg=BLACK,
            bg=LIGHT_BLUE
        ).pack(
            fill="x",
            pady=(0, 15),
            ipady=10
        )


        tk.Label(
            lesson_menu,
            text="Tlhopha thuto",
            font=("Arial", 11, "bold"),
            fg=BLACK,
            bg=WHITE
        ).pack(
            pady=(0, 10)
        )


        colours = [
            LIGHT_BLUE,
            LIGHT_PINK,
            LIGHT_BLUE,
            LIGHT_PINK
        ]


        for index, lesson in enumerate(
            LESSONS
        ):

            button = tk.Button(
                lesson_menu,
                text=lesson["menu"],
                font=("Arial", 11, "bold"),
                bg=colours[index],
                fg=BLACK,
                activebackground=SOFT_YELLOW,
                activeforeground=BLACK,
                relief="flat",
                cursor="hand2",
                width=25,
                height=3,
                wraplength=210,
                command=lambda i=index:
                self.select_lesson(i)
            )

            button.pack(
                padx=12,
                pady=7
            )

            self.lesson_buttons.append(
                button
            )


        # ====================================================
        # KAROLO YA DITENG TSA THUTO
        # ====================================================

        content_area = tk.Frame(
            lesson_area,
            bg=WHITE,
            highlightbackground=BLACK,
            highlightthickness=1
        )

        content_area.pack(
            side="right",
            fill="both",
            expand=True
        )


        self.lesson_title = tk.Label(
            content_area,
            font=("Arial", 19, "bold"),
            fg=BLACK,
            bg=LIGHT_PINK,
            wraplength=650
        )

        self.lesson_title.pack(
            fill="x",
            pady=(0, 5),
            ipady=10
        )


        # ====================================================
        # NAVIGATION BUTTONS
        # ====================================================

        navigation = tk.Frame(
            content_area,
            bg=WHITE
        )

        navigation.pack(
            side="bottom",
            fill="x",
            padx=15,
            pady=(8, 12)
        )


        self.previous_button = tk.Button(
            navigation,
            text="← E e Fetileng",
            font=("Arial", 11, "bold"),
            bg=LIGHT_BLUE,
            fg=BLACK,
            activebackground=SOFT_YELLOW,
            activeforeground=BLACK,
            relief="flat",
            cursor="hand2",
            width=16,
            height=2,
            command=self.previous_lesson
        )

        self.previous_button.pack(
            side="left",
            padx=5
        )


        self.complete_button = tk.Button(
            navigation,
            text="✓ Ke Feditse Thuto",
            font=("Arial", 11, "bold"),
            bg=SOFT_GREEN,
            fg=BLACK,
            activebackground=SOFT_YELLOW,
            activeforeground=BLACK,
            relief="flat",
            cursor="hand2",
            width=20,
            height=2,
            command=self.mark_complete
        )

        self.complete_button.pack(
            side="left",
            expand=True,
            padx=5
        )


        self.next_button = tk.Button(
            navigation,
            text="E e Latelang →",
            font=("Arial", 11, "bold"),
            bg=LIGHT_PINK,
            fg=BLACK,
            activebackground=SOFT_YELLOW,
            activeforeground=BLACK,
            relief="flat",
            cursor="hand2",
            width=16,
            height=2,
            command=self.next_lesson
        )

        self.next_button.pack(
            side="right",
            padx=5
        )


        # ====================================================
        # LESSON TEXT
        # ====================================================

        text_frame = tk.Frame(
            content_area,
            bg=WHITE
        )

        text_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(5, 0)
        )


        scrollbar = tk.Scrollbar(
            text_frame
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )


        self.lesson_text = tk.Text(
            text_frame,
            wrap="word",
            font=("Arial", 13),
            bg=CREAM,
            fg=BLACK,
            relief="flat",
            padx=24,
            pady=18,
            spacing1=4,
            spacing3=8,
            yscrollcommand=scrollbar.set
        )

        self.lesson_text.pack(
            side="left",
            fill="both",
            expand=True
        )


        # ====================================================
        # TEXT FORMATTING
        # ====================================================

        self.lesson_text.tag_configure(
            "heading",
            font=("Arial", 14, "bold"),
            spacing1=10,
            spacing3=6
        )


        self.lesson_text.tag_configure(
            "subheading",
            font=("Arial", 13, "bold"),
            spacing1=8,
            spacing3=4
        )


        self.lesson_text.tag_configure(
            "bullet",
            lmargin1=18,
            lmargin2=34
        )


        self.lesson_text.tag_configure(
            "step",
            lmargin1=18,
            lmargin2=34
        )


        scrollbar.config(
            command=self.lesson_text.yview
        )


    # ========================================================
    # INSERT FORMATTED CONTENT
    # ========================================================

    def insert_formatted_content(
        self,
        content
    ):

        for line in content.strip().splitlines():

            stripped = line.strip()


            if not stripped:

                self.lesson_text.insert(
                    tk.END,
                    "\n"
                )

                continue


            if (
                stripped.isupper()
                and len(stripped) > 2
            ):

                tag = "heading"


            elif (
                len(stripped) > 2
                and stripped[0].isdigit()
                and ". " in stripped[:4]
                and stripped.split(
                    ". ",
                    1
                )[1].isupper()
            ):

                tag = "subheading"


            elif stripped.startswith(
                "•"
            ):

                tag = "bullet"


            elif stripped.lower().startswith(
                "kgato "
            ):

                tag = "step"


            else:

                tag = None


            if tag:

                self.lesson_text.insert(
                    tk.END,
                    stripped + "\n",
                    tag
                )

            else:

                self.lesson_text.insert(
                    tk.END,
                    stripped + "\n"
                )


    # ========================================================
    # DISPLAY LESSON
    # ========================================================

    def display_lesson(self):

        lesson = LESSONS[
            self.current_lesson
        ]


        self.lesson_title.config(
            text=lesson["title"]
        )


        self.lesson_text.config(
            state="normal"
        )


        self.lesson_text.delete(
            "1.0",
            tk.END
        )


        self.insert_formatted_content(
            lesson["content"]
        )


        self.lesson_text.config(
            state="disabled"
        )


        self.lesson_text.yview_moveto(
            0
        )


        self.update_lesson_menu()

        self.update_navigation_buttons()

        self.update_complete_button()


    # ========================================================
    # UPDATE LESSON MENU
    # ========================================================

    def update_lesson_menu(self):

        default_colours = [
            LIGHT_BLUE,
            LIGHT_PINK,
            LIGHT_BLUE,
            LIGHT_PINK
        ]


        completed = (
            get_completed_lessons()
        )


        for index, button in enumerate(
            self.lesson_buttons
        ):

            lesson_number = (
                index + 1
            )


            lesson_name = (
                LESSONS[index]["menu"]
            )


            if lesson_number in completed:

                lesson_name = (
                    "✓ " + lesson_name
                )


            button.config(
                text=lesson_name
            )


            if index == self.current_lesson:

                button.config(
                    bg=SOFT_YELLOW
                )

            else:

                button.config(
                    bg=default_colours[index]
                )


    # ========================================================
    # UPDATE PREVIOUS / NEXT
    # ========================================================

    def update_navigation_buttons(self):

        if self.current_lesson == 0:

            self.previous_button.config(
                state="disabled"
            )

        else:

            self.previous_button.config(
                state="normal"
            )


        if (
            self.current_lesson
            == len(LESSONS) - 1
        ):

            self.next_button.config(
                state="disabled"
            )

        else:

            self.next_button.config(
                state="normal"
            )


    # ========================================================
    # UPDATE COMPLETE BUTTON
    # ========================================================

    def update_complete_button(self):

        lesson_number = (
            self.current_lesson + 1
        )


        completed = (
            get_completed_lessons()
        )


        if lesson_number in completed:

            self.complete_button.config(
                text="✓ Thuto e Feditswe",
                bg=SOFT_GREEN,
                state="disabled"
            )

        else:

            self.complete_button.config(
                text="✓ Ke Feditse Thuto",
                bg=SOFT_GREEN,
                state="normal"
            )


    # ========================================================
    # SELECT LESSON
    # ========================================================

    def select_lesson(
        self,
        index
    ):

        self.current_lesson = index

        self.display_lesson()


    # ========================================================
    # PREVIOUS LESSON
    # ========================================================

    def previous_lesson(self):

        if self.current_lesson > 0:

            self.current_lesson -= 1

            self.display_lesson()


    # ========================================================
    # NEXT LESSON
    # ========================================================

    def next_lesson(self):

        if (
            self.current_lesson
            < len(LESSONS) - 1
        ):

            self.current_lesson += 1

            self.display_lesson()


    # ========================================================
    # MARK LESSON COMPLETE
    # ========================================================

    def mark_complete(self):

        lesson_number = (
            self.current_lesson + 1
        )


        complete_lesson(
            lesson_number
        )


        completed = (
            get_completed_lessons()
        )


        if lesson_number in completed:

            self.update_lesson_menu()

            self.update_complete_button()


            messagebox.showinfo(
                "Thuto e Feditswe",
                (
                    f"O feditse Thuto "
                    f"{lesson_number}! "
                    "Kgatelopele ya gago "
                    "e bolokilwe."
                )
            )

        else:

            messagebox.showwarning(
                "Thuto",
                (
                    "Thuto ga e a kgona go bolokwa. "
                    "Netefatsa gore o tsene mo "
                    "thulaganyong jaaka morutwana."
                )
            )