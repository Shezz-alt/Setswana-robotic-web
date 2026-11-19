import tkinter as tk
from tkinter import messagebox

from lessons import LessonModule, LESSONS
from simulator import RobotSimulator
from activities import ActivityModule
from quiz import QuizModule
from database import (
    login_learner, register_learner, get_learner,
    login_teacher, register_teacher, get_teacher,
    get_active_user_role, get_active_user_name,
    get_completed_lessons, get_activity_progress,
    calculate_progress, get_all_learners_progress,
    reset_learner_pin, clear_active_user,
    learner_is_active, teacher_is_active,
)

# ============================================================
# MEBALA
# ============================================================

BACKGROUND = "#2E7D32"
LIGHT_BLUE = "#BDE7F5"
LIGHT_PINK = "#F8D7E6"
DEEP_BLUE = "#274C77"
WHITE = "#FFFFFF"
SOFT_GREEN = "#BFE3C0"
SOFT_YELLOW = "#FFE8A3"
BLACK = "#000000"
BORDER = "#D5E5EA"
BUTTON_HOVER = "#A7D9EB"
CREAM = "#FFFDF7"


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title(
    "Setswana Robotics Learning System"
)

root.geometry(
    "1250x760"
)

root.minsize(
    1100,
    680
)

root.configure(
    bg=BACKGROUND
)


navigation = None
content_frame = None


# ============================================================
# HELPERS
# ============================================================

def clear_root():

    for widget in root.winfo_children():
        widget.destroy()


def clear_content():

    if content_frame is None:
        return

    for widget in content_frame.winfo_children():
        widget.destroy()


def require_active_user():

    if get_active_user_role() is None:

        messagebox.showwarning(
            "Tsena",
            "Tsweetswee, tsena pele."
        )

        show_role_selection()

        return False

    return True


def make_button(
    parent,
    text,
    command,
    bg,
    width=20,
    height=2,
    font_size=11
):

    return tk.Button(
        parent,
        text=text,
        command=command,
        font=("Arial", font_size, "bold"),
        bg=bg,
        fg=BLACK,
        activebackground=BUTTON_HOVER,
        activeforeground=BLACK,
        relief="flat",
        cursor="hand2",
        width=width,
        height=height,
    )


# ============================================================
# ROLE SELECTION
# ============================================================

def show_role_selection():

    clear_active_user()

    clear_root()

    root.configure(
        bg=BACKGROUND
    )


    tk.Label(
        root,
        text="🤖",
        font=("Arial", 55),
        bg=BACKGROUND,
        fg=BLACK
    ).pack(
        pady=(45, 5)
    )


    tk.Label(
        root,
        text="SETSWANA ROBOTICS",
        font=("Arial", 32, "bold"),
        bg=BACKGROUND,
        fg=BLACK
    ).pack()


    tk.Label(
        root,
        text=(
            "Tlhopha gore o tsena jaaka "
            "Morutabana kgotsa Morutwana."
        ),
        font=("Arial", 13, "bold"),
        bg=BACKGROUND,
        fg=BLACK
    ).pack(
        pady=(5, 20)
    )


    cards = tk.Frame(
        root,
        bg=BACKGROUND
    )

    cards.pack(
        pady=10
    )


    role_cards = [

        (
            "teacher",
            "👩‍🏫",
            "MORUTABANA",
            LIGHT_BLUE,
            (
                "Dirisa dithuto, dikarolo tsa roboto, "
                "Pogoramo le Ditiro go ruta barutwana "
                "le go bona kgatelopele ya bone."
            ),
            "👩‍🏫  Tsena jaaka Morutabana",
        ),

        (
            "learner",
            "🧑‍🎓",
            "MORUTWANA",
            LIGHT_PINK,
            (
                "Ithute ka diroboto, dirisa Pogoramo, "
                "rarabolola dikgwetlho, araba Dipotso "
                "mme o bone kgatelopele ya gago."
            ),
            "🧑‍🎓  Tsena jaaka Morutwana",
        ),
    ]


    for (
        role,
        icon,
        title,
        colour,
        description,
        button_text
    ) in role_cards:


        card = tk.Frame(
            cards,
            bg=WHITE,
            highlightbackground=colour,
            highlightthickness=2,
            width=360,
            height=300,
        )

        card.pack(
            side="left",
            padx=15
        )

        card.pack_propagate(
            False
        )


        tk.Label(
            card,
            text=icon,
            font=("Arial", 45),
            bg=WHITE
        ).pack(
            pady=(18, 5)
        )


        tk.Label(
            card,
            text=title,
            font=("Arial", 19, "bold"),
            bg=colour,
            fg=BLACK
        ).pack(
            fill="x",
            padx=20,
            ipady=8
        )


        tk.Label(
            card,
            text=description,
            font=("Arial", 11, "bold"),
            bg=WHITE,
            fg=BLACK,
            wraplength=290,
            justify="center",
        ).pack(
            padx=20,
            pady=15
        )


        make_button(
            card,
            button_text,
            lambda r=role: show_login(r),
            colour,
            width=26
        ).pack(
            pady=5
        )


# ============================================================
# LOGIN / REGISTRATION
# ============================================================

def show_login(role):

    clear_active_user()

    clear_root()

    root.configure(
        bg=BACKGROUND
    )


    if role == "teacher":

        icon = "👩‍🏫"

        role_title = "MORUTABANA"

        name_title = (
            "LEINA LA MORUTABANA"
        )

        colour = LIGHT_BLUE

        login_function = (
            login_teacher
        )

        register_function = (
            register_teacher
        )

        get_name_function = (
            get_teacher
        )

    else:

        icon = "🧑‍🎓"

        role_title = "MORUTWANA"

        name_title = (
            "LEINA LA MORUTWANA"
        )

        colour = LIGHT_PINK

        login_function = (
            login_learner
        )

        register_function = (
            register_learner
        )

        get_name_function = (
            get_learner
        )


    make_button(
        root,
        "← Boela Morago",
        show_role_selection,
        SOFT_YELLOW,
        width=14
    ).place(
        x=20,
        y=20
    )


    tk.Label(
        root,
        text=icon,
        font=("Arial", 52),
        bg=BACKGROUND,
        fg=BLACK
    ).pack(
        pady=(50, 5)
    )


    tk.Label(
        root,
        text="SETSWANA ROBOTICS",
        font=("Arial", 30, "bold"),
        bg=BACKGROUND,
        fg=BLACK
    ).pack()


    tk.Label(
        root,
        text=f"TSENA JAAKA {role_title}",
        font=("Arial", 17, "bold"),
        bg=BACKGROUND,
        fg=BLACK
    ).pack(
        pady=(3, 15)
    )


    card = tk.Frame(
        root,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=2
    )

    card.pack(
        ipadx=75,
        ipady=25,
        pady=10
    )


    tk.Label(
        card,
        text=f"{icon}  {name_title}",
        font=("Arial", 15, "bold"),
        bg=colour,
        fg=BLACK
    ).pack(
        fill="x",
        pady=(0, 20),
        ipady=10
    )


    tk.Label(
        card,
        text="Kwala leina la gago",
        font=("Arial", 11, "bold"),
        bg=WHITE,
        fg=BLACK
    ).pack(
        pady=(0, 7)
    )


    name_entry = tk.Entry(
        card,
        font=("Arial", 15),
        width=30,
        justify="center",
        relief="solid",
        bd=1
    )

    name_entry.pack(
        pady=8,
        ipady=6
    )

    name_entry.focus_set()


    def attempt_login():

        name = (
            name_entry.get().strip()
        )


        if not name:

            messagebox.showwarning(
                "Leina",
                "Tsweetswee, kwala leina la gago."
            )

            return


        if login_function(name):

            messagebox.showinfo(
                "Tsena",
                (
                    f"Re a go amogela, "
                    f"{get_name_function()}!"
                )
            )

            build_main_system()

        else:

            messagebox.showwarning(
                "Ga go a Atlega",
                (
                    "Ga re a kgona go tsena. "
                    "Netefatsa leina le PIN ya gago."
                )
            )


    def attempt_registration():

        name = (
            name_entry.get().strip()
        )


        if not name:

            messagebox.showwarning(
                "Leina",
                "Tsweetswee, kwala leina la gago."
            )

            return


        successful, status = (
            register_function(name)
        )


        if successful:

            messagebox.showinfo(
                "Ikwadiso",
                (
                    f"O ikwadisitse ka katlego, "
                    f"{get_name_function()}!"
                )
            )

            build_main_system()

            return


        if status == "exists":

            messagebox.showinfo(
                "Leina le teng",
                (
                    "Leina leno le setse le ikwadisitse. "
                    "Dirisa Tsena mme o kwale PIN."
                )
            )


        elif status == "cancelled":

            return


        elif status in (
            "teacher",
            "learner"
        ):

            messagebox.showwarning(
                "Leina",
                (
                    "Leina leno le setse le dirisiwa "
                    "mo karolong e nngwe ya system."
                )
            )


        else:

            messagebox.showwarning(
                "Leina",
                "Ikwadiso ga e a atlega."
            )


    buttons = tk.Frame(
        card,
        bg=WHITE
    )

    buttons.pack(
        pady=(15, 5)
    )


    make_button(
        buttons,
        "🔓  Tsena",
        attempt_login,
        SOFT_GREEN,
        width=16
    ).pack(
        side="left",
        padx=7
    )


    make_button(
        buttons,
        "👤  Ikwadise",
        attempt_registration,
        colour,
        width=16
    ).pack(
        side="left",
        padx=7
    )


    tk.Label(
        card,
        text=(
            "Fa o le mosha, dirisa Ikwadise mme o tlhame PIN.\n"
            "Fa o setse o ikwadisitse, dirisa Tsena."
        ),
        font=("Arial", 10),
        bg=WHITE,
        fg=BLACK,
        justify="center",
    ).pack(
        pady=(15, 0)
    )


    name_entry.bind(
        "<Return>",
        lambda event:
            attempt_login()
    )


# ============================================================
# MAIN SYSTEM / NAVIGATION
# ============================================================

def build_main_system():

    global navigation
    global content_frame


    if not require_active_user():
        return


    clear_root()


    role = (
        get_active_user_role()
    )

    name = (
        get_active_user_name()
    )


    icon = (
        "👩‍🏫"
        if role == "teacher"
        else "🧑‍🎓"
    )


    role_text = (
        "Morutabana"
        if role == "teacher"
        else "Morutwana"
    )


    header = tk.Frame(
        root,
        height=85,
        bg=DEEP_BLUE
    )

    header.pack(
        fill="x"
    )

    header.pack_propagate(
        False
    )


    tk.Label(
        header,
        text="🤖  SETSWANA ROBOTICS",
        font=("Arial", 23, "bold"),
        fg=WHITE,
        bg=DEEP_BLUE
    ).pack(
        side="left",
        padx=30,
        pady=20
    )


    tk.Label(
        header,
        text=(
            f"{icon} {role_text}: {name}"
        ),
        font=("Arial", 12, "bold"),
        fg=WHITE,
        bg=DEEP_BLUE
    ).pack(
        side="right",
        padx=30
    )


    body = tk.Frame(
        root,
        bg=BACKGROUND
    )

    body.pack(
        fill="both",
        expand=True
    )


    navigation = tk.Frame(
        body,
        width=250,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    navigation.pack(
        side="left",
        fill="y"
    )

    navigation.pack_propagate(
        False
    )


    tk.Label(
        navigation,
        text="LENANEO",
        font=("Arial", 16, "bold"),
        bg=WHITE,
        fg=BLACK
    ).pack(
        pady=(16, 3)
    )


    tk.Label(
        navigation,
        text=f"{icon} {role_text}",
        font=("Arial", 10, "bold"),
        bg=WHITE,
        fg=BLACK
    ).pack(
        pady=(0, 10)
    )


    nav_items = [

        (
            "🏠  Gae",
            show_home,
            LIGHT_BLUE
        ),

        (
            "📘  Dithuto",
            show_lessons,
            LIGHT_PINK
        ),

        (
            "🦾  Dikarolo tsa Roboto",
            show_robot_parts,
            SOFT_YELLOW
        ),

        (
            "🤖  Pogoramo",
            show_programming,
            LIGHT_BLUE
        ),

        (
            "🎯  Ditiro",
            show_activities,
            LIGHT_PINK
        ),
    ]


    if role == "teacher":

        nav_items.extend(
            [

                (
                    "📊  Kgatelopele",
                    show_teacher_progress,
                    LIGHT_BLUE
                ),

                (
                    "🔐  Laola PIN",
                    show_learner_pin_management,
                    SOFT_YELLOW
                ),
            ]
        )

    else:

        nav_items.extend(
            [

                (
                    "🧠  Dipotso",
                    show_quiz,
                    SOFT_YELLOW
                ),

                (
                    "⭐  Kgatelopele",
                    show_learner_progress,
                    LIGHT_BLUE
                ),
            ]
        )


    for (
        text,
        command,
        colour
    ) in nav_items:

        make_button(
            navigation,
            text,
            command,
            colour,
            width=23
        ).pack(
            pady=5,
            padx=16
        )


    tk.Label(
        navigation,
        text="",
        bg=WHITE
    ).pack(
        expand=True
    )


    make_button(
        navigation,
        "🚪  Tswaya",
        logout_user,
        "#F4E1E6",
        width=23
    ).pack(
        pady=5,
        padx=16
    )


    tk.Label(
        navigation,
        text="Setswana Robotics",
        font=("Arial", 9),
        bg=WHITE,
        fg=BLACK
    ).pack(
        pady=(3, 8)
    )


    content_frame = tk.Frame(
        body,
        bg=BACKGROUND
    )

    content_frame.pack(
        side="right",
        fill="both",
        expand=True
    )


    show_home()


# ============================================================
# BEGINNER GUIDE - FULL EXPLANATIONS
# ============================================================

def show_beginner_guide():

    if not require_active_user():
        return


    role = (
        get_active_user_role()
    )


    window = tk.Toplevel(
        root
    )

    window.title(
        "Tataiso ya Tshimologo"
    )

    window.geometry(
        "930x720"
    )

    window.minsize(
        850,
        650
    )

    window.configure(
        bg=BACKGROUND
    )

    window.transient(
        root
    )

    window.grab_set()


    tk.Label(
        window,
        text="🧭 TATAISO YA TSHIMOLOGO",
        font=("Arial", 24, "bold"),
        bg=BACKGROUND,
        fg=BLACK
    ).pack(
        pady=(18, 5)
    )


    if role == "teacher":

        intro = (
            "Tataiso eno e tlhalosa karolo nngwe le nngwe ya system "
            "gore Morutabana a itse gore a simolole kae, "
            "a dirise karolo efe, le gore karolo eo e thusa jang "
            "mo thutong."
        )


        steps = [

            (
                "1. 📘 DITHUTO",
                (
                    "Simolola ka Dithuto. Go na le dithuto tse nne "
                    "tse di tlhalosang gore roboto ke eng, dikarolo "
                    "tsa roboto, motsamao le ditaelo, le algorithm "
                    "le programming. Bula thuto nngwe le nngwe, "
                    "e bale le barutwana, mme o tlhalose dikakanyo "
                    "pele ga Pogoramo kgotsa Ditiro. Pontsho ya "
                    "Morutabana ga e boloki completion jaaka "
                    "kgatelopele ya Morutwana."
                )
            ),

            (
                "2. 🦾 DIKAROLO TSA ROBOTO",
                (
                    "Bula Dikarolo tsa Roboto go bontsha roboto "
                    "e e tletseng. Tobetsa tlhogo, matlho, ditsebe, "
                    "mmele, selaodi, motswedi wa maatla, mabogo, "
                    "diatla kgotsa maoto. Fa karolo e tobetswa, "
                    "tlhaloso ya leina le tiro ya yone e bonala "
                    "mo letlhakoreng. Dirisa seno go ruta dikarolo "
                    "tsa motheo tsa roboto ka tsela e e bonalang."
                )
            ),

            (
                "3. 🤖 POGORAMO",
                (
                    "Bula Pogoramo go bontsha kafa ditaelo di "
                    "laolang roboto ka teng. Tlhopha Tsamaya Pele, "
                    "Tsamaya Morago, Sokologela Molemeng kgotsa "
                    "Sokologela Mojeng. Ditaelo di tsena mo lenaneng "
                    "mme roboto e di diragatsa ka tatelano. Lebelela "
                    "motsu wa direction pele le morago ga go sokologa. "
                    "Tobetsa ? fa tlhaloso ya taelo e tlhokega."
                )
            ),

            (
                "4. 🎯 DITIRO",
                (
                    "Bula Ditiro go dirisa dikgwetlho tse tlhano. "
                    "Kgwetlho nngwe le nngwe e na le FITLHA, mme "
                    "dingwe di na le dikgoreletsi tse di tshwailweng "
                    "ka X. Bontsha barutwana kafa ba ka rulaganyang "
                    "tatelano ya ditaelo, kafa ba ka sokologang le "
                    "kafa ba ka tilang dikgoreletsi ka teng. Ditiro "
                    "tsa Morutabana ke pontsho fela mme ga di fetole "
                    "kgatelopele ya Morutwana."
                )
            ),

            (
                "5. 📊 KGATELOPELE",
                (
                    "Bula Kgatelopele go bona barutwana ba ba "
                    "ikwadisitseng. O tla bona gore morutwana mongwe "
                    "le mongwe o feditse Dithuto tse kae mo go 4, "
                    "Dikgwetlho tse kae mo go 5, le percentage ya "
                    "kgatelopele. Seno se thusa go lemoga barutwana "
                    "ba ba tlhokang tlhaloso kgotsa thuso e nngwe."
                )
            ),

            (
                "6. 🔐 LAOLA PIN",
                (
                    "Fa Morutwana a lebetse PIN, bula Laola PIN. "
                    "Tlhopha leina la Morutwana, kwala PIN e ntšha "
                    "ya dinomoro tse 4 go ya go 6, mme o e netefatse. "
                    "Go fetola PIN ga go phimole dithuto, maiteko "
                    "kgotsa dikgwetlho tse Morutwana a setseng "
                    "a di dirile."
                )
            ),
        ]


        footer = (
            "Morutabana o dirisa system go ruta le go tlhokomela "
            "kgatelopele. Pontsho ya Morutabana ga e tshwanetse "
            "go fetola rekoto ya Morutwana."
        )


    else:

        intro = (
            "Tataiso eno e tla go tsamaisa kgato ka kgato. "
            "Fa o le lekgetlho la ntlha o dirisa system, "
            "latela dikgato tsotlhe ka tatelano gore o se ka "
            "wa tlhakana kgotsa wa tlogela karolo nngwe "
            "e sa dirisiwa."
        )


        steps = [

            (
                "1. 📘 DITHUTO",
                (
                    "Simolola ka Dithuto pele ga Ditiro. Go na le "
                    "dithuto tse nne. Thuto 1 e tlhalosa gore roboto "
                    "ke eng. Thuto 2 e tlhalosa dikarolo tsa roboto. "
                    "Thuto 3 e tlhalosa motsamao le ditaelo. "
                    "Thuto 4 e tlhalosa algorithm le programming. "
                    "Bala thuto ka kelotlhoko, dirisa scroll fa "
                    "diteng di le dintsi, mme fa o feditse tobetsa "
                    "'Ke Feditse Thuto' gore system e boloke "
                    "completion ya gago."
                )
            ),

            (
                "2. 🦾 DIKAROLO TSA ROBOTO",
                (
                    "Bula Dikarolo tsa Roboto morago ga go bala "
                    "dithuto. O tla bona roboto e e nang le antenna, "
                    "tlhogo, matlho, ditsebe, molomo, molala, mmele, "
                    "selaodi, motswedi wa maatla, mabogo, diatla, "
                    "maoto le dinao. Tobetsa dikarolo tse di bonalang. "
                    "Mo letlhakoreng le le jang o tla bona leina "
                    "la karolo le tlhaloso ya gore e dira eng. "
                    "Leka dikarolo tsotlhe gore o di itse pele "
                    "ga o tswelela."
                )
            ),

            (
                "3. 🤖 POGORAMO",
                (
                    "Mo Pogoramo o ithuta go laola roboto ka ditaelo. "
                    "Tsamaya Pele e tsamaisa roboto kwa e lebileng teng. "
                    "Tsamaya Morago e e busetsa kwa morago. Sokologela "
                    "Molemeng kgotsa Mojeng e fetola direction. "
                    "Lebelela motsu o o fa godimo ga roboto ka dinako "
                    "tsotlhe. Ditaelo di tsena mo lenaneng mme di "
                    "diragadiwa ka tatelano. Tobetsa ? fa taelo "
                    "e sa tlhaloganyesege."
                )
            ),

            (
                "4. 🎯 DITIRO",
                (
                    "Mo Ditiro go na le Kgwetlho 1 go ya go 5. "
                    "Maikaelelo ke go fitlhisa roboto kwa FITLHA. "
                    "Tlhopha ditaelo ka tatelano e e siameng, lebelele "
                    "direction, mme o tile dikgoreletsi tse di "
                    "tshwailweng ka X. Kgwetlho 1 e bonolo, mme tse "
                    "dingwe di tlhoka go sokologa le go rulaganya tsela. "
                    "Fa roboto e sa fitlhe kwa FITLHA, fetola ditaelo "
                    "mme o leke gape. Maiteko le completion di bolokiwa "
                    "mo Kgatelopele."
                )
            ),

            (
                "5. 🧠 DIPOTSO",
                (
                    "Morago ga Dithuto le Ditiro, bula Dipotso go leka "
                    "kitso ya gago. Go na le dipotso tse 5 tsa multiple "
                    "choice. Tlhopha karabo e le nngwe mme o tobetsa "
                    "'Netefatsa Karabo'. System e go bolelela gore "
                    "karabo e siame kgotsa nnyaa le go tlhalosa lebaka. "
                    "Fa o feditse, o bona score mo go 5 le percentage. "
                    "'Leka Gape' e go letla go simolola dipotso gape. "
                    "Dipotso ga di fetole percentage ya Kgatelopele."
                )
            ),

            (
                "6. ⭐ KGATELOPELE",
                (
                    "Bula Kgatelopele go bona se o setseng o se dirile. "
                    "O tla bona Dithuto /4 le Dikgwetlho /5. Thuto kgotsa "
                    "Kgwetlho e e feditsweng e bontsha ✓. Kgatelopele "
                    "Yotlhe e balwa ka dithuto tse 4 le dikgwetlho tse 5, "
                    "ka jalo tsotlhe ke dilo tse 9. Fa sengwe se sa bontshe "
                    "se feditswe, boela mo karolong eo mme o e fetse "
                    "ka akhaonto ya gago."
                )
            ),
        ]


        footer = (
            "Tsena ka leina la gago le PIN ya gago fela gore "
            "kgatelopele e bolokwe mo akhaontong e e siameng. "
            "Fa o lebetse PIN, kopa Morutabana go go thusa."
        )


    tk.Label(
        window,
        text=intro,
        font=("Arial", 12, "bold"),
        bg=SOFT_YELLOW,
        fg=BLACK,
        wraplength=820,
        justify="center"
    ).pack(
        fill="x",
        padx=40,
        pady=(5, 10),
        ipady=9
    )


    outer = tk.Frame(
        window,
        bg=WHITE
    )

    outer.pack(
        fill="both",
        expand=True,
        padx=40,
        pady=5
    )


    canvas = tk.Canvas(
        outer,
        bg=WHITE,
        highlightthickness=0
    )


    scrollbar = tk.Scrollbar(
        outer,
        orient="vertical",
        command=canvas.yview
    )


    cards_frame = tk.Frame(
        canvas,
        bg=WHITE
    )


    cards_frame.bind(
        "<Configure>",
        lambda event:
            canvas.configure(
                scrollregion=canvas.bbox("all")
            )
    )


    canvas.create_window(
        (0, 0),
        window=cards_frame,
        anchor="nw",
        width=815
    )


    canvas.configure(
        yscrollcommand=scrollbar.set
    )


    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )


    scrollbar.pack(
        side="right",
        fill="y"
    )


    for index, (
        title,
        description
    ) in enumerate(steps):


        colour = (
            LIGHT_BLUE
            if index % 2 == 0
            else LIGHT_PINK
        )


        card = tk.Frame(
            cards_frame,
            bg=colour,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        card.pack(
            fill="x",
            padx=8,
            pady=6
        )


        tk.Label(
            card,
            text=title,
            font=("Arial", 11, "bold"),
            bg=colour,
            fg=BLACK,
            width=25,
            anchor="nw",
            justify="left"
        ).pack(
            side="left",
            padx=(12, 8),
            pady=10
        )


        tk.Label(
            card,
            text=description,
            font=("Arial", 10),
            bg=colour,
            fg=BLACK,
            wraplength=590,
            justify="left",
            anchor="w"
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 12),
            pady=10
        )


    tk.Label(
        window,
        text=footer,
        font=("Arial", 10, "bold"),
        bg=SOFT_YELLOW,
        fg=BLACK,
        wraplength=820,
        justify="center"
    ).pack(
        fill="x",
        padx=40,
        pady=(8, 5),
        ipady=7
    )


    make_button(
        window,
        "✓  Ke a tlhaloganya",
        window.destroy,
        SOFT_GREEN,
        width=20
    ).pack(
        pady=(5, 15)
    )


# ============================================================
# HOME
# ============================================================

def show_home():

    if not require_active_user():
        return


    clear_content()


    role = (
        get_active_user_role()
    )

    name = (
        get_active_user_name()
    )


    tk.Label(
        content_frame,
        text="🤖",
        font=("Arial", 44),
        bg=BACKGROUND,
        fg=BLACK
    ).pack(
        pady=(30, 3)
    )


    tk.Label(
        content_frame,
        text="SETSWANA ROBOTICS",
        font=("Arial", 29, "bold"),
        bg=BACKGROUND,
        fg=BLACK
    ).pack()


    tk.Label(
        content_frame,
        text=f"Re a go amogela, {name}! 🌟",
        font=("Arial", 17, "bold"),
        bg=BACKGROUND,
        fg=BLACK
    ).pack(
        pady=(8, 12)
    )


    card = tk.Frame(
        content_frame,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=2
    )

    card.pack(
        fill="x",
        padx=100,
        pady=10,
        ipady=12
    )


    if role == "teacher":

        heading = (
            "👩‍🏫 MOKGWA WA MORUTABANA"
        )

        colour = LIGHT_BLUE

        description = (
            "Dirisa Dithuto, Dikarolo tsa Roboto, "
            "Pogoramo le Ditiro go ruta barutwana. "
            "Dirisa Kgatelopele go bona gore ba gatetse pele jang."
        )

        note = (
            "Pontsho ya Morutabana ga e boloki kgatelopele "
            "ya Morutwana. Dirisa Laola PIN fa Morutwana "
            "a lebetse PIN."
        )

    else:

        heading = (
            "🧑‍🎓 MOKGWA WA MORUTWANA"
        )

        colour = LIGHT_PINK

        description = (
            "Simolola ka Dithuto, ithute dikarolo tsa roboto, "
            "dirisa Pogoramo, rarabolola Dikgwetlho, "
            "mme morago o leke Dipotso."
        )

        note = (
            "Dithuto le Ditiro tse o di fetsang di bonala "
            "mo Kgatelopele. Dipotso ke tsa go leka kitso "
            "mme ga di fetole percentage."
        )


    tk.Label(
        card,
        text=heading,
        font=("Arial", 15, "bold"),
        bg=colour,
        fg=BLACK
    ).pack(
        fill="x",
        padx=20,
        ipady=8
    )


    tk.Label(
        card,
        text=description,
        font=("Arial", 12, "bold"),
        bg=WHITE,
        fg=BLACK,
        wraplength=720,
        justify="center"
    ).pack(
        padx=35,
        pady=12
    )


    tk.Label(
        card,
        text=note,
        font=("Arial", 11, "bold"),
        bg=SOFT_YELLOW,
        fg=BLACK,
        wraplength=720,
        justify="center"
    ).pack(
        fill="x",
        padx=30,
        pady=10,
        ipady=7
    )


    guide_card = tk.Frame(
        content_frame,
        bg=WHITE,
        highlightbackground=SOFT_YELLOW,
        highlightthickness=2
    )

    guide_card.pack(
        fill="x",
        padx=150,
        pady=(8, 15),
        ipady=8
    )


    tk.Label(
        guide_card,
        text="🧭 A KE LE LANTLHA O DIRISA SYSTEM?",
        font=("Arial", 13, "bold"),
        bg=SOFT_YELLOW,
        fg=BLACK
    ).pack(
        fill="x",
        padx=20,
        pady=(0, 8),
        ipady=7
    )


    tk.Label(
        guide_card,
        text=(
            "Bula Tataiso ya Tshimologo go bona tlhaloso "
            "e e feletseng ya karolo nngwe le nngwe le tsela "
            "ya go dirisa system kgato ka kgato."
        ),
        font=("Arial", 11),
        bg=WHITE,
        fg=BLACK,
        wraplength=650,
        justify="center"
    ).pack(
        padx=25,
        pady=(2, 8)
    )


    make_button(
        guide_card,
        "🧭  Bona Tataiso ya Tshimologo",
        show_beginner_guide,
        SOFT_GREEN,
        width=28
    ).pack(
        pady=(2, 8)
    )


# ============================================================
# LESSONS
# ============================================================

def show_lessons():

    if not require_active_user():
        return


    if teacher_is_active():

        show_teacher_lessons()

    else:

        clear_content()

        LessonModule(
            content_frame
        )


def show_teacher_lessons():

    clear_content()


    tk.Label(
        content_frame,
        text="📘 DITHUTO TSA DIROBOTO",
        font=("Arial", 24, "bold"),
        bg=BACKGROUND,
        fg=BLACK
    ).pack(
        pady=(18, 3)
    )


    tk.Label(
        content_frame,
        text=(
            "👩‍🏫 Mokgwa wa Morutabana - bula thuto nngwe "
            "le nngwe go e bala le go e tlhalosetsa barutwana."
        ),
        font=("Arial", 12, "bold"),
        bg=SOFT_YELLOW,
        fg=BLACK,
        wraplength=850
    ).pack(
        fill="x",
        padx=45,
        pady=(3, 10),
        ipady=7
    )


    main = tk.Frame(
        content_frame,
        bg=BACKGROUND
    )

    main.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=(0, 15)
    )


    menu = tk.Frame(
        main,
        width=250,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    menu.pack(
        side="left",
        fill="y",
        padx=(0, 10)
    )

    menu.pack_propagate(
        False
    )


    tk.Label(
        menu,
        text="DITHUTO",
        font=("Arial", 15, "bold"),
        bg=LIGHT_BLUE,
        fg=BLACK
    ).pack(
        fill="x",
        ipady=10
    )


    lesson_area = tk.Frame(
        main,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    lesson_area.pack(
        side="right",
        fill="both",
        expand=True
    )


    title = tk.Label(
        lesson_area,
        text="",
        font=("Arial", 18, "bold"),
        bg=LIGHT_PINK,
        fg=BLACK,
        wraplength=700
    )

    title.pack(
        fill="x",
        ipady=10
    )


    text_frame = tk.Frame(
        lesson_area,
        bg=WHITE
    )

    text_frame.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=10
    )


    scrollbar = tk.Scrollbar(
        text_frame
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )


    text = tk.Text(
        text_frame,
        wrap="word",
        font=("Arial", 13),
        bg=CREAM,
        fg=BLACK,
        relief="flat",
        padx=20,
        pady=15,
        spacing1=3,
        spacing3=7,
        yscrollcommand=scrollbar.set
    )

    text.pack(
        side="left",
        fill="both",
        expand=True
    )


    scrollbar.config(
        command=text.yview
    )


    def display(index):

        lesson = (
            LESSONS[index]
        )


        title.config(
            text=lesson.get(
                "title",
                f"Thuto {index + 1}"
            )
        )


        text.config(
            state="normal"
        )

        text.delete(
            "1.0",
            tk.END
        )

        text.insert(
            "1.0",
            lesson.get(
                "content",
                ""
            )
        )

        text.config(
            state="disabled"
        )

        text.yview_moveto(
            0
        )


    for index, lesson in enumerate(
        LESSONS
    ):

        make_button(
            menu,
            lesson.get(
                "menu",
                f"Thuto {index + 1}"
            ),
            lambda i=index:
                display(i),
            (
                LIGHT_BLUE
                if index % 2 == 0
                else LIGHT_PINK
            ),
            width=22,
            height=3,
            font_size=10
        ).pack(
            pady=7,
            padx=12
        )


    display(0)


# ============================================================
# ROBOT PARTS - FULL ROBOT
# ============================================================

def show_robot_parts():

    if not require_active_user():
        return


    clear_content()


    role = (
        get_active_user_role()
    )


    subtitle = (
        "👩‍🏫 Tobetsa karolo ya roboto go e tlhalosetsa barutwana."
        if role == "teacher"
        else
        "🧑‍🎓 Tobetsa karolo ya roboto go ithuta leina le tiro ya yone."
    )


    tk.Label(
        content_frame,
        text="🦾 DIKAROLO TSA ROBOTO",
        font=("Arial", 24, "bold"),
        bg=BACKGROUND,
        fg=BLACK
    ).pack(
        pady=(15, 3)
    )


    tk.Label(
        content_frame,
        text=subtitle,
        font=("Arial", 12, "bold"),
        bg=SOFT_YELLOW,
        fg=BLACK
    ).pack(
        fill="x",
        padx=45,
        pady=(3, 8),
        ipady=7
    )


    main = tk.Frame(
        content_frame,
        bg=BACKGROUND
    )

    main.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=(0, 15)
    )


    robot_frame = tk.Frame(
        main,
        bg=WHITE,
        highlightbackground=LIGHT_BLUE,
        highlightthickness=2
    )

    robot_frame.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(0, 10)
    )


    tk.Label(
        robot_frame,
        text="TOBETSA KAROLO YA ROBOTO",
        font=("Arial", 14, "bold"),
        bg=LIGHT_BLUE,
        fg=BLACK
    ).pack(
        fill="x",
        ipady=9
    )


    canvas = tk.Canvas(
        robot_frame,
        width=430,
        height=470,
        bg=CREAM,
        highlightthickness=0,
        cursor="hand2"
    )

    canvas.pack(
        pady=8
    )


    info = tk.Frame(
        main,
        width=350,
        bg=WHITE,
        highlightbackground=LIGHT_PINK,
        highlightthickness=2
    )

    info.pack(
        side="right",
        fill="both",
        padx=(10, 0)
    )

    info.pack_propagate(
        False
    )


    tk.Label(
        info,
        text="TSHEDIMOSETSO YA KAROLO",
        font=("Arial", 14, "bold"),
        bg=LIGHT_PINK,
        fg=BLACK
    ).pack(
        fill="x",
        ipady=9
    )


    part_name = tk.Label(
        info,
        text="🤖 Tlhopha karolo ya roboto",
        font=("Arial", 17, "bold"),
        bg=WHITE,
        fg=BLACK,
        wraplength=300
    )

    part_name.pack(
        padx=20,
        pady=(35, 15)
    )


    part_description = tk.Label(
        info,
        text=(
            "Tobetsa karolo e e bonalang ya roboto "
            "go bona leina le tlhaloso ya tiro ya yone."
        ),
        font=("Arial", 12, "bold"),
        bg=SOFT_YELLOW,
        fg=BLACK,
        wraplength=300,
        justify="left"
    )

    part_description.pack(
        fill="x",
        padx=20,
        pady=10,
        ipady=12
    )


    parts = {

        "head": (
            "TLHOGO",
            (
                "Tlhogo ke karolo e e kwa godimo ya roboto. "
                "E ka tshola disensa, matlho le ditsebe tse "
                "di thusang roboto go amogela tshedimosetso."
            )
        ),

        "eyes": (
            "MATLHO / DISENSA TSA PONO",
            (
                "Matlho a roboto a ka emela disensa tsa pono. "
                "Disensa tseno di thusa roboto go lemoga lesedi, "
                "dilo kgotsa tikologo e e e dikologileng."
            )
        ),

        "ears": (
            "DITSEBE / SENSA YA MODUMO",
            (
                "Ditsebe di ka emela sensa ya modumo e e thusang "
                "roboto go lemoga medumo mo tikologong."
            )
        ),

        "body": (
            "MMELE",
            (
                "Mmele o tshola le go sireletsa dikarolo tsa roboto. "
                "Mo teng go ka nna le selaodi, mehala le dikarolo "
                "tse dingwe tsa elektroniki."
            )
        ),

        "controller": (
            "SELAODI",
            (
                "Selaodi se amogela le go diragatsa ditaelo. "
                "Se thusa go laola tsela e roboto e arabelang "
                "le go dira ditiro ka yone."
            )
        ),

        "power": (
            "MOTSWEDI WA MAATLA",
            (
                "Motswedi wa maatla o naya roboto maatla a go dira. "
                "Sekai ke beteri e e nayang dikarolo tsa roboto motlakase."
            )
        ),

        "arms": (
            "MABOGO",
            (
                "Mabogo a roboto a ka tsamaisiwa ke dimotor kgotsa "
                "diactuator. A thusa roboto go fitlhelela kgotsa "
                "go sutisa dilo."
            )
        ),

        "hands": (
            "DIATLA",
            (
                "Diatla di ka thusa roboto go tshwara, "
                "go tlogela kgotsa go sutisa dilo."
            )
        ),

        "legs": (
            "MAOTO LE DINAO",
            (
                "Maoto le dinao di thusa roboto go ema le go tsamaya. "
                "Dimotor kgotsa diactuator di ka laola motsamao wa maoto."
            )
        ),
    }


    def select_part(key):

        name, description = (
            parts[key]
        )

        part_name.config(
            text=name
        )

        part_description.config(
            text=description
        )


    # ANTENNA
    canvas.create_line(
        215, 35,
        215, 55,
        width=4,
        fill=BLACK,
        tags=("head",)
    )

    canvas.create_oval(
        208, 25,
        222, 39,
        fill=SOFT_YELLOW,
        outline=BLACK,
        width=2,
        tags=("head",)
    )


    # HEAD
    canvas.create_rectangle(
        155, 55,
        275, 145,
        fill=LIGHT_BLUE,
        outline=BLACK,
        width=3,
        tags=("head",)
    )


    # EARS
    canvas.create_oval(
        138, 78,
        160, 120,
        fill=LIGHT_PINK,
        outline=BLACK,
        width=2,
        tags=("ears",)
    )

    canvas.create_oval(
        270, 78,
        292, 120,
        fill=LIGHT_PINK,
        outline=BLACK,
        width=2,
        tags=("ears",)
    )


    # EYES
    canvas.create_oval(
        178, 82,
        198, 102,
        fill=WHITE,
        outline=BLACK,
        width=2,
        tags=("eyes",)
    )

    canvas.create_oval(
        232, 82,
        252, 102,
        fill=WHITE,
        outline=BLACK,
        width=2,
        tags=("eyes",)
    )

    canvas.create_oval(
        185, 89,
        192, 96,
        fill=BLACK,
        outline=BLACK,
        tags=("eyes",)
    )

    canvas.create_oval(
        239, 89,
        246, 96,
        fill=BLACK,
        outline=BLACK,
        tags=("eyes",)
    )


    # MOUTH - RESTORED
    canvas.create_line(
        190, 120,
        240, 120,
        width=3,
        fill=BLACK,
        tags=("head",)
    )


    # NECK - RESTORED
    canvas.create_rectangle(
        195, 145,
        235, 165,
        fill=SOFT_YELLOW,
        outline=BLACK,
        width=2,
        tags=("body",)
    )


    # BODY
    canvas.create_rectangle(
        160, 165,
        270, 300,
        fill=LIGHT_BLUE,
        outline=BLACK,
        width=3,
        tags=("body",)
    )


    # CONTROLLER
    canvas.create_rectangle(
        180, 185,
        250, 230,
        fill=SOFT_YELLOW,
        outline=BLACK,
        width=2,
        tags=("controller",)
    )

    canvas.create_text(
        215,
        207,
        text="SELAODI",
        font=("Arial", 9, "bold"),
        fill=BLACK,
        tags=("controller",)
    )


    # POWER SOURCE
    canvas.create_rectangle(
        188, 245,
        242, 285,
        fill=SOFT_GREEN,
        outline=BLACK,
        width=2,
        tags=("power",)
    )

    canvas.create_text(
        215,
        265,
        text="MAATLA",
        font=("Arial", 9, "bold"),
        fill=BLACK,
        tags=("power",)
    )


    # LEFT ARM
    canvas.create_rectangle(
        115, 175,
        160, 205,
        fill=LIGHT_PINK,
        outline=BLACK,
        width=2,
        tags=("arms",)
    )

    canvas.create_rectangle(
        90, 195,
        120, 275,
        fill=LIGHT_BLUE,
        outline=BLACK,
        width=2,
        tags=("arms",)
    )


    # RIGHT ARM
    canvas.create_rectangle(
        270, 175,
        315, 205,
        fill=LIGHT_PINK,
        outline=BLACK,
        width=2,
        tags=("arms",)
    )

    canvas.create_rectangle(
        310, 195,
        340, 275,
        fill=LIGHT_BLUE,
        outline=BLACK,
        width=2,
        tags=("arms",)
    )


    # HANDS
    canvas.create_oval(
        86, 268,
        124, 305,
        fill=SOFT_YELLOW,
        outline=BLACK,
        width=2,
        tags=("hands",)
    )

    canvas.create_oval(
        306, 268,
        344, 305,
        fill=SOFT_YELLOW,
        outline=BLACK,
        width=2,
        tags=("hands",)
    )


    # HIPS
    canvas.create_rectangle(
        170, 300,
        260, 325,
        fill=LIGHT_PINK,
        outline=BLACK,
        width=2,
        tags=("body",)
    )


    # LEGS
    canvas.create_rectangle(
        175, 325,
        210, 410,
        fill=LIGHT_BLUE,
        outline=BLACK,
        width=2,
        tags=("legs",)
    )

    canvas.create_rectangle(
        220, 325,
        255, 410,
        fill=LIGHT_BLUE,
        outline=BLACK,
        width=2,
        tags=("legs",)
    )


    # FEET - RESTORED
    canvas.create_rectangle(
        160, 405,
        210, 435,
        fill=SOFT_YELLOW,
        outline=BLACK,
        width=2,
        tags=("legs",)
    )

    canvas.create_rectangle(
        220, 405,
        270, 435,
        fill=SOFT_YELLOW,
        outline=BLACK,
        width=2,
        tags=("legs",)
    )


    for tag_name in parts:

        canvas.tag_bind(
            tag_name,
            "<Button-1>",
            lambda event, key=tag_name:
                select_part(key)
        )


# ============================================================
# PROGRAMMING
# ============================================================

def show_programming():

    if not require_active_user():
        return


    clear_content()


    if teacher_is_active():

        tk.Label(
            content_frame,
            text=(
                "👩‍🏫 Mokgwa wa Morutabana: Dirisa Pogoramo "
                "go bontsha motsamao le tatelano ya ditaelo. "
                "Pontsho eno ga e boloki kgatelopele."
            ),
            font=("Arial", 11, "bold"),
            bg=SOFT_YELLOW,
            fg=BLACK,
            wraplength=850
        ).pack(
            fill="x",
            padx=20,
            pady=(8, 0),
            ipady=6
        )


    RobotSimulator(
        content_frame
    )


# ============================================================
# ACTIVITIES
# ============================================================

def show_activities():

    if not require_active_user():
        return


    clear_content()


    if teacher_is_active():

        tk.Label(
            content_frame,
            text=(
                "👩‍🏫 Mokgwa wa Morutabana: Dirisa dikgwetlho "
                "go bontsha gore ditaelo di tsamaisa roboto jang. "
                "Pontsho eno ga e boloki kgatelopele."
            ),
            font=("Arial", 11, "bold"),
            bg=SOFT_YELLOW,
            fg=BLACK,
            wraplength=850
        ).pack(
            fill="x",
            padx=20,
            pady=(8, 0),
            ipady=6
        )


    ActivityModule(
        content_frame
    )


# ============================================================
# QUIZ
# ============================================================

def show_quiz():

    if not learner_is_active():

        messagebox.showwarning(
            "Dipotso",
            "Karolo eno ke ya morutwana."
        )

        return


    clear_content()


    QuizModule(
        content_frame
    )


# ============================================================
# TEACHER PIN MANAGEMENT
# ============================================================

def show_learner_pin_management():

    if not teacher_is_active():

        messagebox.showwarning(
            "Tshireletso",
            (
                "Karolo eno e ka dirisiwa "
                "ke morutabana fela."
            )
        )

        return


    clear_content()


    tk.Label(
        content_frame,
        text="🔐 LAOLA PIN YA MORUTWANA",
        font=("Arial", 24, "bold"),
        bg=BACKGROUND,
        fg=BLACK
    ).pack(
        pady=(30, 5)
    )


    tk.Label(
        content_frame,
        text=(
            "Morutabana a ka fetola PIN ya Morutwana fa a e lebetse. "
            "Kgatelopele ga e phimolwe fa PIN e fetolwa."
        ),
        font=("Arial", 12, "bold"),
        bg=SOFT_YELLOW,
        fg=BLACK,
        wraplength=700
    ).pack(
        fill="x",
        padx=100,
        pady=(5, 15),
        ipady=8
    )


    card = tk.Frame(
        content_frame,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=2
    )

    card.pack(
        padx=150,
        pady=10,
        ipadx=55,
        ipady=25
    )


    learners = [

        item["name"]

        for item in get_all_learners_progress()

    ]


    if not learners:

        tk.Label(
            card,
            text=(
                "Ga go na barutwana "
                "ba ba ikwadisitseng."
            ),
            font=("Arial", 12, "bold"),
            bg=WHITE,
            fg=BLACK
        ).pack(
            pady=30
        )

        return


    tk.Label(
        card,
        text="Tlhopha Morutwana",
        font=("Arial", 12, "bold"),
        bg=WHITE,
        fg=BLACK
    ).pack(
        pady=(5, 7)
    )


    selected = tk.StringVar(
        value=learners[0]
    )


    menu = tk.OptionMenu(
        card,
        selected,
        *learners
    )

    menu.config(
        font=("Arial", 11),
        width=28,
        bg=LIGHT_BLUE,
        fg=BLACK,
        relief="flat"
    )

    menu.pack(
        pady=(0, 18)
    )


    tk.Label(
        card,
        text="PIN e Ntšha",
        font=("Arial", 11, "bold"),
        bg=WHITE,
        fg=BLACK
    ).pack(
        pady=(5, 5)
    )


    pin_entry = tk.Entry(
        card,
        show="*",
        font=("Arial", 14),
        width=20,
        justify="center"
    )

    pin_entry.pack(
        pady=(0, 12),
        ipady=5
    )


    tk.Label(
        card,
        text="Netefatsa PIN",
        font=("Arial", 11, "bold"),
        bg=WHITE,
        fg=BLACK
    ).pack(
        pady=(5, 5)
    )


    confirm_entry = tk.Entry(
        card,
        show="*",
        font=("Arial", 14),
        width=20,
        justify="center"
    )

    confirm_entry.pack(
        pady=(0, 15),
        ipady=5
    )


    tk.Label(
        card,
        text=(
            "PIN e tshwanetse go nna "
            "dinomoro tse 4 go ya go 6."
        ),
        font=("Arial", 9),
        bg=SOFT_YELLOW,
        fg=BLACK
    ).pack(
        fill="x",
        padx=20,
        pady=8,
        ipady=5
    )


    def reset_pin():

        learner_name = (
            selected.get().strip()
        )


        new_pin = (
            pin_entry.get().strip()
        )


        confirm = (
            confirm_entry.get().strip()
        )


        if not new_pin:

            messagebox.showwarning(
                "PIN",
                "Kwala PIN e ntšha."
            )

            return


        if new_pin != confirm:

            messagebox.showwarning(
                "PIN",
                (
                    "Di-PIN ga di tshwane. "
                    "Leka gape."
                )
            )

            return


        if (
            not new_pin.isdigit()
            or not 4 <= len(new_pin) <= 6
        ):

            messagebox.showwarning(
                "PIN",
                (
                    "PIN e tshwanetse go nna "
                    "dinomoro tse 4 go ya go 6."
                )
            )

            return


        if not messagebox.askyesno(
            "Netefatsa",
            (
                f"A o batla go fetola "
                f"PIN ya {learner_name}?"
            )
        ):

            return


        success, status = (
            reset_learner_pin(
                learner_name,
                new_pin
            )
        )


        if success:

            pin_entry.delete(
                0,
                tk.END
            )

            confirm_entry.delete(
                0,
                tk.END
            )


            messagebox.showinfo(
                "PIN e Fetotswe",
                (
                    f"PIN ya {learner_name} "
                    "e fetotswe ka katlego.\n\n"
                    "Kgatelopele ya Morutwana "
                    "ga e a fetolwa."
                )
            )


        elif status == "not_found":

            messagebox.showwarning(
                "Morutwana",
                "Morutwana ga a bonale."
            )


        elif status == "invalid_pin":

            messagebox.showwarning(
                "PIN",
                "PIN ga e a siama."
            )


        else:

            messagebox.showwarning(
                "Tshireletso",
                (
                    "PIN ga e a kgona "
                    "go fetolwa."
                )
            )


    make_button(
        card,
        "🔐  Fetola PIN",
        reset_pin,
        SOFT_GREEN,
        width=20
    ).pack(
        pady=(10, 5)
    )


# ============================================================
# LEARNER PROGRESS
# ============================================================

def show_learner_progress():

    if not learner_is_active():

        messagebox.showwarning(
            "Kgatelopele",
            "Karolo eno ke ya morutwana."
        )

        return


    clear_content()


    name = (
        get_learner()
    )

    completed_lessons = (
        get_completed_lessons()
    )

    activity_data = (
        get_activity_progress()
    )

    percentage = (
        calculate_progress()
    )


    tk.Label(
        content_frame,
        text="⭐ KGATELOPELE YA MORUTWANA",
        font=("Arial", 24, "bold"),
        bg=BACKGROUND,
        fg=BLACK
    ).pack(
        pady=(22, 6)
    )


    tk.Label(
        content_frame,
        text=f"🧑‍🎓 Morutwana: {name}",
        font=("Arial", 15, "bold"),
        bg=BACKGROUND,
        fg=BLACK
    ).pack(
        pady=4
    )


    summary = tk.Frame(
        content_frame,
        bg=LIGHT_BLUE
    )

    summary.pack(
        fill="x",
        padx=90,
        pady=10
    )


    tk.Label(
        summary,
        text="Kgatelopele Yotlhe",
        font=("Arial", 14, "bold"),
        bg=LIGHT_BLUE,
        fg=BLACK
    ).pack(
        pady=(8, 2)
    )


    tk.Label(
        summary,
        text=f"{percentage}%",
        font=("Arial", 30, "bold"),
        bg=LIGHT_BLUE,
        fg=BLACK
    ).pack(
        pady=(2, 8)
    )


    tk.Label(
        summary,
        text=(
            "Dithuto tse 4 + "
            "Dikgwetlho tse 5"
        ),
        font=("Arial", 10, "bold"),
        bg=LIGHT_BLUE,
        fg=BLACK
    ).pack(
        pady=(0, 8)
    )


    details = tk.Frame(
        content_frame,
        bg=BACKGROUND
    )

    details.pack(
        fill="both",
        expand=True,
        padx=55,
        pady=6
    )


    lessons_box = tk.Frame(
        details,
        bg=WHITE
    )

    lessons_box.pack(
        side="left",
        fill="both",
        expand=True,
        padx=8
    )


    tk.Label(
        lessons_box,
        text="📘 DITHUTO /4",
        font=("Arial", 14, "bold"),
        bg=LIGHT_BLUE,
        fg=BLACK
    ).pack(
        fill="x",
        ipady=8
    )


    lesson_names = [

        "Thuto 1: Matseno a Diroboto",

        "Thuto 2: Dikarolo tsa Roboto",

        "Thuto 3: Motsamao le Ditaelo",

        "Thuto 4: Algorithm le Pogoramo",
    ]


    for number, title in enumerate(
        lesson_names,
        1
    ):

        complete = (
            number in completed_lessons
        )


        status = (
            "✓ E Feditswe"
            if complete
            else
            "○ Ga e Ise e Fediwe"
        )


        colour = (
            SOFT_GREEN
            if complete
            else
            "#F8F9FA"
        )


        tk.Label(
            lessons_box,
            text=(
                f"{title}\n"
                f"{status}"
            ),
            font=("Arial", 11),
            bg=colour,
            fg=BLACK,
            justify="left",
            anchor="w"
        ).pack(
            fill="x",
            padx=12,
            pady=4,
            ipady=4
        )


    activities_box = tk.Frame(
        details,
        bg=WHITE
    )

    activities_box.pack(
        side="right",
        fill="both",
        expand=True,
        padx=8
    )


    tk.Label(
        activities_box,
        text="🎯 DIKGWETLHO /5",
        font=("Arial", 14, "bold"),
        bg=LIGHT_PINK,
        fg=BLACK
    ).pack(
        fill="x",
        ipady=8
    )


    activity_map = {

        number: (
            attempts,
            complete
        )

        for (
            number,
            attempts,
            complete
        ) in activity_data

    }


    for number in range(
        1,
        6
    ):

        attempts, complete = (
            activity_map.get(
                number,
                (0, 0)
            )
        )


        status = (
            "✓ E Feditswe"
            if complete == 1
            else
            "○ Ga e Ise e Fediwe"
        )


        colour = (
            SOFT_GREEN
            if complete == 1
            else
            "#F8F9FA"
        )


        tk.Label(
            activities_box,
            text=(
                f"Kgwetlho {number}\n"
                f"{status}   |   "
                f"Maiteko: {attempts}"
            ),
            font=("Arial", 10),
            bg=colour,
            fg=BLACK,
            justify="left",
            anchor="w"
        ).pack(
            fill="x",
            padx=12,
            pady=3,
            ipady=4
        )


    if percentage == 100:

        message = (
            "🌟 O feditse dithuto "
            "le dikgwetlho tsotlhe!"
        )


    elif percentage >= 70:

        message = (
            "👏 O dira sentle thata. "
            "Tswelela pele!"
        )


    elif percentage >= 40:

        message = (
            "🚀 O gatetse pele. "
            "Tswelela ka dithuto le dikgwetlho!"
        )


    elif percentage > 0:

        message = (
            "🤖 O simolotse sentle. "
            "Tswelela pele!"
        )


    else:

        message = (
            "📘 Simolola ka dithuto "
            "le dikgwetlho."
        )


    tk.Label(
        content_frame,
        text=message,
        font=("Arial", 12, "bold"),
        bg=SOFT_YELLOW,
        fg=BLACK
    ).pack(
        fill="x",
        padx=90,
        pady=(3, 12),
        ipady=6
    )


# ============================================================
# TEACHER PROGRESS
# ============================================================

def show_teacher_progress():

    if not teacher_is_active():

        messagebox.showwarning(
            "Kgatelopele",
            "Karolo eno ke ya morutabana."
        )

        return


    clear_content()


    data = (
        get_all_learners_progress()
    )


    tk.Label(
        content_frame,
        text="📊 KGATELOPELE YA BARUTWANA",
        font=("Arial", 24, "bold"),
        bg=BACKGROUND,
        fg=BLACK
    ).pack(
        pady=(22, 5)
    )


    tk.Label(
        content_frame,
        text=(
            "Kgatelopele e balwa ka "
            "Dithuto tse 4 le Dikgwetlho tse 5."
        ),
        font=("Arial", 11, "bold"),
        bg=SOFT_YELLOW,
        fg=BLACK
    ).pack(
        fill="x",
        padx=70,
        pady=(3, 6),
        ipady=6
    )


    tk.Label(
        content_frame,
        text=(
            f"Palo ya Barutwana: "
            f"{len(data)}"
        ),
        font=("Arial", 14, "bold"),
        bg=LIGHT_BLUE,
        fg=BLACK
    ).pack(
        fill="x",
        padx=70,
        pady=(4, 10),
        ipady=8
    )


    table = tk.Frame(
        content_frame,
        bg=WHITE
    )

    table.pack(
        fill="both",
        expand=True,
        padx=70,
        pady=10
    )


    header = tk.Frame(
        table,
        bg=DEEP_BLUE
    )

    header.pack(
        fill="x",
        padx=10,
        pady=(10, 4)
    )


    headings = [

        (
            "Morutwana",
            28,
            "w"
        ),

        (
            "Dithuto /4",
            16,
            "center"
        ),

        (
            "Ditiro /5",
            16,
            "center"
        ),

        (
            "Kgatelopele",
            14,
            "center"
        ),
    ]


    for (
        text,
        width,
        anchor
    ) in headings:

        tk.Label(
            header,
            text=text,
            width=width,
            anchor=anchor,
            font=("Arial", 11, "bold"),
            fg=WHITE,
            bg=DEEP_BLUE
        ).pack(
            side="left",
            padx=(
                10
                if text == "Morutwana"
                else 0
            ),
            pady=8
        )


    if not data:

        tk.Label(
            table,
            text=(
                "Ga go na barutwana "
                "ba ba ikwadisitseng."
            ),
            font=("Arial", 12, "bold"),
            bg=WHITE,
            fg=BLACK
        ).pack(
            pady=30
        )

        return


    for index, learner in enumerate(
        data
    ):

        colour = (
            "#F8F9FA"
            if index % 2 == 0
            else WHITE
        )


        row = tk.Frame(
            table,
            bg=colour
        )

        row.pack(
            fill="x",
            padx=10,
            pady=2
        )


        tk.Label(
            row,
            text=learner["name"],
            width=28,
            anchor="w",
            font=("Arial", 11, "bold"),
            bg=colour,
            fg=BLACK
        ).pack(
            side="left",
            padx=10,
            pady=8
        )


        tk.Label(
            row,
            text=(
                f'{learner["completed_lessons"]}/4'
            ),
            width=16,
            font=("Arial", 11),
            bg=colour,
            fg=BLACK
        ).pack(
            side="left"
        )


        tk.Label(
            row,
            text=(
                f'{learner["completed_activities"]}/5'
            ),
            width=16,
            font=("Arial", 11),
            bg=colour,
            fg=BLACK
        ).pack(
            side="left"
        )


        percentage = (
            learner["percentage"]
        )


        tk.Label(
            row,
            text=f"{percentage}%",
            width=14,
            font=("Arial", 11, "bold"),
            bg=(
                SOFT_GREEN
                if percentage == 100
                else colour
            ),
            fg=BLACK
        ).pack(
            side="left"
        )


# ============================================================
# LOGOUT / START
# ============================================================

def logout_user():

    if messagebox.askyesno(
        "Tswaya",
        "A o batla go tswaya?"
    ):

        clear_active_user()

        show_role_selection()


show_role_selection()

root.mainloop()