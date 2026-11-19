import tkinter as tk
from tkinter import messagebox

from database import record_activity_attempt


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


# ============================================================
# TIMING
# ============================================================

EXECUTION_DELAY = 1200


# ============================================================
# COMMAND HELP
# ============================================================

COMMAND_HELP = {

    "Tsamaya Pele": {
        "setswana": (
            "Tsamaisa roboto kwa pele go ya kwa e lebileng teng. "
            "Lebelela motsu mo robotong go itse gore pele ke kae."
        ),
        "english": (
            "Move the robot forward in the direction it is facing."
        )
    },

    "Tsamaya Morago": {
        "setswana": (
            "Tsamaisa roboto kwa morago, kgatlhanong le tsela "
            "e e lebileng teng."
        ),
        "english": (
            "Move the robot backward."
        )
    },

    "Sokologela Molemeng": {
        "setswana": (
            "Fetola tsela ya roboto gore e lebe kwa molemeng. "
            "Roboto ga e suthe mo seleng; e fetola fela tsela "
            "e e lebileng."
        ),
        "english": (
            "Turn the robot to the left without moving "
            "to another square."
        )
    },

    "Sokologela Mojeng": {
        "setswana": (
            "Fetola tsela ya roboto gore e lebe kwa mojeng. "
            "Roboto ga e suthe mo seleng; e fetola fela tsela "
            "e e lebileng."
        ),
        "english": (
            "Turn the robot to the right without moving "
            "to another square."
        )
    }
}


# ============================================================
# ACTIVITY MODULE
# ============================================================

class ActivityModule:

    def __init__(self, parent):

        self.parent = parent

        self.cell_size = 50

        self.start_x = 3
        self.start_y = 5

        self.robot_x = self.start_x
        self.robot_y = self.start_y

        self.direction = "N"

        self.commands = []

        self.current_command = 0

        self.running = False

        self.current_activity = 1

        self.parent.configure(
            bg=BACKGROUND
        )

        self.build_interface()

        self.load_activity(1)


    # ========================================================
    # BUILD INTERFACE
    # ========================================================

    def build_interface(self):

        tk.Label(
            self.parent,
            text="🎯 DITIRO TSA DIROBOTO",
            font=("Arial", 23, "bold"),
            fg=BLACK,
            bg=BACKGROUND
        ).pack(
            pady=(12, 3)
        )


        tk.Label(
            self.parent,
            text="Dirisa ditaelo go rarabolola dikgwetlho",
            font=("Arial", 12, "bold"),
            fg=BLACK,
            bg=BACKGROUND
        ).pack(
            pady=(0, 8)
        )


        main_area = tk.Frame(
            self.parent,
            bg=BACKGROUND
        )

        main_area.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=8
        )


        self.build_left_panel(
            main_area
        )

        self.build_middle_panel(
            main_area
        )

        self.build_right_panel(
            main_area
        )


    # ========================================================
    # LEFT PANEL
    # ========================================================

    def build_left_panel(
        self,
        parent
    ):

        left_frame = tk.Frame(
            parent,
            width=270,
            bg=WHITE,
            highlightbackground=BLACK,
            highlightthickness=1
        )

        left_frame.pack(
            side="left",
            fill="y",
            padx=(0, 10)
        )

        left_frame.pack_propagate(
            False
        )


        tk.Label(
            left_frame,
            text="DIKGWETLHO",
            font=("Arial", 14, "bold"),
            fg=BLACK,
            bg=LIGHT_BLUE
        ).pack(
            fill="x",
            pady=(0, 5),
            ipady=7
        )


        challenge_colours = [

            LIGHT_BLUE,
            LIGHT_PINK,
            SOFT_YELLOW,
            LIGHT_BLUE,
            LIGHT_PINK

        ]


        for number in range(
            1,
            6
        ):

            tk.Button(
                left_frame,
                text=f"🤖  Kgwetlho {number}",
                width=20,
                height=2,
                font=("Arial", 10, "bold"),
                bg=challenge_colours[
                    number - 1
                ],
                fg=BLACK,
                activebackground=SOFT_YELLOW,
                activeforeground=BLACK,
                relief="flat",
                cursor="hand2",
                command=lambda n=number:
                    self.load_activity(n)
            ).pack(
                pady=3
            )


        # ====================================================
        # COMMANDS
        # ====================================================

        tk.Label(
            left_frame,
            text="DITAELO",
            font=("Arial", 13, "bold"),
            fg=BLACK,
            bg=LIGHT_PINK
        ).pack(
            fill="x",
            pady=(8, 3),
            ipady=6
        )


        tk.Label(
            left_frame,
            text=(
                "Tobetsa ? go bona "
                "tlhaloso ya taelo."
            ),
            font=("Arial", 9),
            fg=BLACK,
            bg=WHITE,
            wraplength=235,
            justify="center"
        ).pack(
            pady=(2, 3)
        )


        self.create_command_button(
            left_frame,
            "🤖👆 Tsamaya Pele",
            "Tsamaya Pele",
            LIGHT_BLUE
        )


        self.create_command_button(
            left_frame,
            "🤖👇 Tsamaya Morago",
            "Tsamaya Morago",
            LIGHT_PINK
        )


        self.create_command_button(
            left_frame,
            "🤖👈 Sokologela Molemeng",
            "Sokologela Molemeng",
            SOFT_YELLOW,
            9
        )


        self.create_command_button(
            left_frame,
            "🤖👉 Sokologela Mojeng",
            "Sokologela Mojeng",
            LIGHT_PINK,
            9
        )


    # ========================================================
    # COMMAND BUTTON
    # ========================================================

    def create_command_button(
        self,
        parent,
        button_text,
        command_name,
        colour,
        font_size=10
    ):

        row = tk.Frame(
            parent,
            bg=WHITE
        )

        row.pack(
            fill="x",
            padx=8,
            pady=2
        )


        tk.Button(
            row,
            text=button_text,
            width=19,
            height=2,
            font=("Arial", font_size, "bold"),
            bg=colour,
            fg=BLACK,
            activebackground=SOFT_YELLOW,
            activeforeground=BLACK,
            relief="flat",
            cursor="hand2",
            command=lambda:
                self.add_command(
                    command_name
                )
        ).pack(
            side="left",
            fill="x",
            expand=True
        )


        tk.Button(
            row,
            text="?",
            width=3,
            height=2,
            font=("Arial", 10, "bold"),
            bg=SOFT_GREEN,
            fg=BLACK,
            activebackground=SOFT_YELLOW,
            activeforeground=BLACK,
            relief="flat",
            cursor="hand2",
            command=lambda:
                self.show_command_help(
                    command_name
                )
        ).pack(
            side="right",
            padx=(6, 0)
        )


    # ========================================================
    # COMMAND HELP
    # ========================================================

    def show_command_help(
        self,
        command_name
    ):

        help_info = COMMAND_HELP.get(
            command_name
        )


        if help_info is None:
            return


        messagebox.showinfo(
            "Tlhaloso ya Taelo",
            (
                f"{command_name}\n\n"

                f"Setswana:\n"
                f"{help_info['setswana']}\n\n"

                f"English help:\n"
                f"{help_info['english']}"
            )
        )


    # ========================================================
    # MIDDLE PANEL
    # ========================================================

    def build_middle_panel(
        self,
        parent
    ):

        middle_frame = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=BLACK,
            highlightthickness=1
        )

        middle_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )


        self.activity_title = tk.Label(
            middle_frame,
            font=("Arial", 16, "bold"),
            fg=BLACK,
            bg=LIGHT_PINK,
            wraplength=320
        )

        self.activity_title.pack(
            fill="x",
            pady=(0, 3),
            ipady=8
        )


        self.activity_instruction = tk.Label(
            middle_frame,
            font=("Arial", 10, "bold"),
            fg=BLACK,
            bg=SOFT_YELLOW,
            wraplength=310,
            justify="center"
        )

        self.activity_instruction.pack(
            fill="x",
            padx=10,
            pady=(5, 4),
            ipady=6
        )


        self.activity_tip = tk.Label(
            middle_frame,
            text="",
            font=("Arial", 9),
            fg=BLACK,
            bg=WHITE,
            wraplength=310,
            justify="left"
        )

        self.activity_tip.pack(
            fill="x",
            padx=15,
            pady=(2, 7)
        )


        tk.Label(
            middle_frame,
            text="DITAELO TSA GAGO",
            font=("Arial", 12, "bold"),
            fg=BLACK,
            bg=LIGHT_BLUE
        ).pack(
            fill="x",
            pady=(3, 3),
            ipady=7
        )


        self.command_list = tk.Listbox(
            middle_frame,
            font=("Arial", 11),
            height=11,
            bg=CREAM,
            fg=BLACK,
            selectbackground=SOFT_YELLOW,
            selectforeground=BLACK,
            highlightbackground=BLACK,
            highlightthickness=1,
            relief="flat"
        )

        self.command_list.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=8
        )


        command_controls = tk.Frame(
            middle_frame,
            bg=WHITE
        )

        command_controls.pack(
            pady=8
        )


        tk.Button(
            command_controls,
            text="Tlosa Taelo",
            font=("Arial", 9, "bold"),
            bg=LIGHT_BLUE,
            fg=BLACK,
            activebackground=SOFT_YELLOW,
            activeforeground=BLACK,
            relief="flat",
            cursor="hand2",
            width=13,
            height=2,
            command=self.remove_command
        ).pack(
            side="left",
            padx=5
        )


        tk.Button(
            command_controls,
            text="Phimola Tsotlhe",
            font=("Arial", 9, "bold"),
            bg=LIGHT_PINK,
            fg=BLACK,
            activebackground=SOFT_YELLOW,
            activeforeground=BLACK,
            relief="flat",
            cursor="hand2",
            width=15,
            height=2,
            command=self.clear_commands
        ).pack(
            side="left",
            padx=5
        )


    # ========================================================
    # RIGHT PANEL
    # ========================================================

    def build_right_panel(
        self,
        parent
    ):

        right_frame = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=BLACK,
            highlightthickness=1
        )

        right_frame.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(10, 0)
        )


        tk.Label(
            right_frame,
            text="LEFELO LA KGWETLHO",
            font=("Arial", 13, "bold"),
            fg=BLACK,
            bg=LIGHT_BLUE
        ).pack(
            fill="x",
            pady=(0, 3),
            ipady=8
        )


        self.direction_label = tk.Label(
            right_frame,
            text="Roboto e lebile: Bokone ↑",
            font=("Arial", 12, "bold"),
            fg=BLACK,
            bg=SOFT_YELLOW
        )

        self.direction_label.pack(
            fill="x",
            padx=15,
            pady=(5, 5),
            ipady=5
        )


        self.canvas = tk.Canvas(
            right_frame,
            width=350,
            height=350,
            bg=WHITE,
            highlightthickness=1,
            highlightbackground=BLACK
        )

        self.canvas.pack(
            padx=10,
            pady=5
        )


        controls = tk.Frame(
            right_frame,
            bg=WHITE
        )

        controls.pack(
            pady=8
        )


        self.run_button = tk.Button(
            controls,
            text="▶  Simolola",
            width=13,
            height=2,
            font=("Arial", 10, "bold"),
            bg=SOFT_GREEN,
            fg=BLACK,
            activebackground=SOFT_YELLOW,
            activeforeground=BLACK,
            relief="flat",
            cursor="hand2",
            command=self.run_activity
        )

        self.run_button.pack(
            side="left",
            padx=5
        )


        tk.Button(
            controls,
            text="↻  Simolola Gape",
            width=15,
            height=2,
            font=("Arial", 10, "bold"),
            bg=LIGHT_PINK,
            fg=BLACK,
            activebackground=SOFT_YELLOW,
            activeforeground=BLACK,
            relief="flat",
            cursor="hand2",
            command=self.reset_robot
        ).pack(
            side="left",
            padx=5
        )


        self.status_label = tk.Label(
            right_frame,
            text="Roboto e siametse.",
            font=("Arial", 10, "bold"),
            fg=BLACK,
            bg=SOFT_YELLOW,
            wraplength=330
        )

        self.status_label.pack(
            fill="x",
            padx=15,
            pady=(3, 10),
            ipady=6
        )


    # ========================================================
    # LOAD ACTIVITY
    # ========================================================

    def load_activity(
        self,
        number
    ):

        if self.running:
            return


        self.current_activity = number


        self.commands.clear()

        self.refresh_commands()


        self.robot_x = self.start_x
        self.robot_y = self.start_y

        self.direction = "N"


        # ====================================================
        # KGWETLHO 1
        # ====================================================

        if number == 1:

            self.target_x = 3
            self.target_y = 2

            self.obstacles = []


            self.activity_title.config(
                text="KGWETLHO 1: MOTSAMAO WA PELE"
            )


            self.activity_instruction.config(
                text=(
                    "Tsamaisa roboto go fitlha kwa lefelong "
                    "le le tshwailweng FITLHA."
                )
            )


            self.activity_tip.config(
                text=(
                    "Tataiso: Roboto e simolola e lebile Bokone ↑. "
                    "Lebelela motsu pele ga o tlhopha taelo."
                )
            )


        # ====================================================
        # KGWETLHO 2
        # ====================================================

        elif number == 2:

            self.target_x = 5
            self.target_y = 3

            self.obstacles = []


            self.activity_title.config(
                text=(
                    "KGWETLHO 2: "
                    "MOTSAMAO LE GO SOKOLOGA"
                )
            )


            self.activity_instruction.config(
                text=(
                    "Dirisa motsamao le go sokologa "
                    "go fitlhisa roboto kwa FITLHA."
                )
            )


            self.activity_tip.config(
                text=(
                    "Tataiso: Lebelela gore roboto e lebile kae. "
                    "Fa o sokologa, motsu wa roboto o tla fetoga."
                )
            )


        # ====================================================
        # KGWETLHO 3
        # ====================================================

        elif number == 3:

            self.target_x = 5
            self.target_y = 1

            self.obstacles = [

                (3, 3),
                (4, 3)

            ]


            self.activity_title.config(
                text=(
                    "KGWETLHO 3: "
                    "DITAELO LE DIKGORELETSI"
                )
            )


            self.activity_instruction.config(
                text=(
                    "Fitlhisa roboto kwa FITLHA mme "
                    "o se ka wa tsena mo dikarolong "
                    "tse di nang le sekgoreletsi."
                )
            )


            self.activity_tip.config(
                text=(
                    "Tataiso: X e raya sekgoreletsi. "
                    "Rulaganya tsela ya gago mme "
                    "o sokologe fa go tlhokega."
                )
            )


        # ====================================================
        # KGWETLHO 4
        # ====================================================

        elif number == 4:

            self.target_x = 1
            self.target_y = 1

            self.obstacles = [

                (3, 3),
                (2, 3),
                (2, 2)

            ]


            self.activity_title.config(
                text=(
                    "KGWETLHO 4: "
                    "RULAGANYA TSELA"
                )
            )


            self.activity_instruction.config(
                text=(
                    "Fitlhisa roboto kwa FITLHA "
                    "ka go rulaganya tsela e e nang "
                    "le diphetogo tsa direction."
                )
            )


            self.activity_tip.config(
                text=(
                    "Tataiso: O tla tlhoka go tsamaya, "
                    "go sokologa, mme o fetole direction "
                    "gape gore o fitlhe kwa FITLHA."
                )
            )


        # ====================================================
        # KGWETLHO 5
        # ====================================================

        else:

            self.target_x = 6
            self.target_y = 0

            self.obstacles = [

                (3, 4),
                (4, 4),
                (4, 3),
                (5, 3),
                (5, 2),
                (4, 2),
                (3, 2),
                (3, 1)

            ]


            self.activity_title.config(
                text=(
                    "KGWETLHO 5: "
                    "TSELA E E RARAGANENG"
                )
            )


            self.activity_instruction.config(
                text=(
                    "Fitlhisa roboto kwa FITLHA ka go tila "
                    "dikgoreletsi tsotlhe. Rulaganya ditaelo "
                    "ka kelotlhoko pele ga o simolola."
                )
            )


            self.activity_tip.config(
                text=(
                    "Tataiso: Se potlake. Lebelela lefelo lotlhe, "
                    "direction ya roboto le dikarolo tse di nang le X."
                )
            )


        self.update_direction_label()

        self.draw_activity()


        self.status_label.config(
            text=(
                f"Kgwetlho {number}: "
                "Tlhopha ditaelo go simolola."
            )
        )


    # ========================================================
    # DRAW ACTIVITY
    # ========================================================

    def draw_activity(self):

        self.canvas.delete(
            "all"
        )


        for position in range(
            0,
            351,
            self.cell_size
        ):

            self.canvas.create_line(
                position,
                0,
                position,
                350,
                fill="#B0B0B0"
            )


            self.canvas.create_line(
                0,
                position,
                350,
                position,
                fill="#B0B0B0"
            )


        # ====================================================
        # FITLHA
        # ====================================================

        x1 = (
            self.target_x
            * self.cell_size
        )

        y1 = (
            self.target_y
            * self.cell_size
        )


        self.canvas.create_rectangle(
            x1 + 3,
            y1 + 3,
            x1 + self.cell_size - 3,
            y1 + self.cell_size - 3,
            fill=SOFT_GREEN,
            outline=BLACK,
            width=2
        )


        self.canvas.create_text(
            x1 + 25,
            y1 + 25,
            text="FITLHA",
            font=("Arial", 9, "bold"),
            fill=BLACK
        )


        # ====================================================
        # OBSTACLES
        # ====================================================

        for obstacle_x, obstacle_y in (
            self.obstacles
        ):

            ox = (
                obstacle_x
                * self.cell_size
            )

            oy = (
                obstacle_y
                * self.cell_size
            )


            self.canvas.create_rectangle(
                ox + 3,
                oy + 3,
                ox + self.cell_size - 3,
                oy + self.cell_size - 3,
                fill="#B0B0B0",
                outline=BLACK
            )


            self.canvas.create_text(
                ox + 25,
                oy + 25,
                text="X",
                font=("Arial", 16, "bold"),
                fill=BLACK
            )


        self.draw_robot()


    # ========================================================
    # DRAW ROBOT
    # ========================================================

    def draw_robot(self):

        self.canvas.delete(
            "robot"
        )


        center_x = (
            self.robot_x
            * self.cell_size
            + self.cell_size // 2
        )


        center_y = (
            self.robot_y
            * self.cell_size
            + self.cell_size // 2
        )


        # Direction arrow
        self.canvas.create_text(
            center_x,
            center_y - 28,
            text=self.get_direction_arrow(),
            font=("Arial", 16, "bold"),
            fill=BLACK,
            tags="robot"
        )


        # Head
        self.canvas.create_oval(
            center_x - 7,
            center_y - 20,
            center_x + 7,
            center_y - 6,
            fill=LIGHT_BLUE,
            outline=BLACK,
            width=2,
            tags="robot"
        )


        # Eyes
        self.canvas.create_oval(
            center_x - 4,
            center_y - 16,
            center_x - 2,
            center_y - 14,
            fill=BLACK,
            outline=BLACK,
            tags="robot"
        )


        self.canvas.create_oval(
            center_x + 2,
            center_y - 16,
            center_x + 4,
            center_y - 14,
            fill=BLACK,
            outline=BLACK,
            tags="robot"
        )


        # Body
        self.canvas.create_rectangle(
            center_x - 9,
            center_y - 5,
            center_x + 9,
            center_y + 10,
            fill=LIGHT_BLUE,
            outline=BLACK,
            width=2,
            tags="robot"
        )


        # Arms
        self.canvas.create_line(
            center_x - 9,
            center_y,
            center_x - 18,
            center_y + 7,
            fill=BLACK,
            width=3,
            tags="robot"
        )


        self.canvas.create_line(
            center_x + 9,
            center_y,
            center_x + 18,
            center_y + 7,
            fill=BLACK,
            width=3,
            tags="robot"
        )


        # Legs
        self.canvas.create_line(
            center_x - 5,
            center_y + 10,
            center_x - 10,
            center_y + 20,
            fill=BLACK,
            width=3,
            tags="robot"
        )


        self.canvas.create_line(
            center_x + 5,
            center_y + 10,
            center_x + 10,
            center_y + 20,
            fill=BLACK,
            width=3,
            tags="robot"
        )


        self.canvas.create_text(
            center_x,
            center_y + 2,
            text=self.get_direction_arrow(),
            font=("Arial", 11, "bold"),
            fill=BLACK,
            tags="robot"
        )


    # ========================================================
    # DIRECTION
    # ========================================================

    def get_direction_arrow(self):

        arrows = {

            "N": "↑",
            "E": "→",
            "S": "↓",
            "W": "←"

        }


        return arrows[
            self.direction
        ]


    def update_direction_label(self):

        names = {

            "N": "Bokone ↑",
            "E": "Botlhaba →",
            "S": "Borwa ↓",
            "W": "Bophirima ←"

        }


        self.direction_label.config(
            text=(
                f"Roboto e lebile: "
                f"{names[self.direction]}"
            )
        )


    # ========================================================
    # COMMANDS
    # ========================================================

    def add_command(
        self,
        command
    ):

        if self.running:
            return


        self.commands.append(
            command
        )


        self.refresh_commands()


    def remove_command(self):

        if self.running:
            return


        selection = (
            self.command_list.curselection()
        )


        if not selection:

            messagebox.showinfo(
                "Taelo",
                (
                    "Tlhopha taelo e o "
                    "batlang go e tlosa."
                )
            )

            return


        self.commands.pop(
            selection[0]
        )


        self.refresh_commands()


    def clear_commands(self):

        if self.running:
            return


        self.commands.clear()

        self.refresh_commands()


        self.status_label.config(
            text=(
                "Ditaelo tsotlhe "
                "di phimotswe."
            )
        )


    def refresh_commands(self):

        self.command_list.delete(
            0,
            tk.END
        )


        for index, command in enumerate(
            self.commands,
            start=1
        ):

            self.command_list.insert(
                tk.END,
                f"{index}. {command}"
            )


    # ========================================================
    # RUN ACTIVITY
    # ========================================================

    def run_activity(self):

        if self.running:
            return


        if not self.commands:

            messagebox.showinfo(
                "Kgwetlho",
                "Tlhopha ditaelo pele."
            )

            return


        self.robot_x = self.start_x
        self.robot_y = self.start_y

        self.direction = "N"


        self.update_direction_label()

        self.draw_activity()


        self.current_command = 0

        self.running = True


        self.run_button.config(
            state="disabled"
        )


        self.status_label.config(
            text=(
                f"Kgwetlho {self.current_activity}: "
                "Roboto e simolola go diragatsa ditaelo..."
            )
        )


        self.parent.after(
            500,
            self.execute_next
        )


    # ========================================================
    # EXECUTE COMMANDS
    # ========================================================

    def execute_next(self):

        if not self.running:
            return


        if self.current_command >= len(
            self.commands
        ):

            self.finish_activity()

            return


        command = self.commands[
            self.current_command
        ]


        self.command_list.selection_clear(
            0,
            tk.END
        )


        self.command_list.selection_set(
            self.current_command
        )


        self.command_list.see(
            self.current_command
        )


        command_number = (
            self.current_command + 1
        )


        total_commands = len(
            self.commands
        )


        self.status_label.config(
            text=(
                f"Kgwetlho {self.current_activity} | "
                f"Taelo {command_number}/{total_commands}: "
                f"{command}"
            )
        )


        if command == "Tsamaya Pele":

            if not self.move_forward():

                return


        elif command == "Tsamaya Morago":

            if not self.move_backward():

                return


        elif command == "Sokologela Molemeng":

            self.turn_left()


        elif command == "Sokologela Mojeng":

            self.turn_right()


        self.current_command += 1


        self.parent.after(
            EXECUTION_DELAY,
            self.execute_next
        )


    # ========================================================
    # MOVE FORWARD
    # ========================================================

    def move_forward(self):

        new_x = self.robot_x

        new_y = self.robot_y


        if self.direction == "N":

            new_y -= 1


        elif self.direction == "E":

            new_x += 1


        elif self.direction == "S":

            new_y += 1


        elif self.direction == "W":

            new_x -= 1


        return self.attempt_move(
            new_x,
            new_y
        )


    # ========================================================
    # MOVE BACKWARD
    # ========================================================

    def move_backward(self):

        new_x = self.robot_x

        new_y = self.robot_y


        if self.direction == "N":

            new_y += 1


        elif self.direction == "E":

            new_x -= 1


        elif self.direction == "S":

            new_y -= 1


        elif self.direction == "W":

            new_x += 1


        return self.attempt_move(
            new_x,
            new_y
        )


    # ========================================================
    # CHECK MOVEMENT
    # ========================================================

    def attempt_move(
        self,
        new_x,
        new_y
    ):

        if (
            new_x < 0
            or new_x > 6
            or new_y < 0
            or new_y > 6
        ):

            self.fail_activity(
                (
                    "Roboto e lekile go tswa "
                    "mo lefelong la kgwetlho."
                )
            )

            return False


        if (
            new_x,
            new_y
        ) in self.obstacles:

            self.fail_activity(
                (
                    "Roboto e thulane "
                    "le sekgoreletsi."
                )
            )

            return False


        self.robot_x = new_x

        self.robot_y = new_y


        self.draw_activity()


        return True


    # ========================================================
    # TURN LEFT
    # ========================================================

    def turn_left(self):

        directions = [

            "N",
            "W",
            "S",
            "E"

        ]


        index = directions.index(
            self.direction
        )


        self.direction = directions[
            (index + 1) % 4
        ]


        self.update_direction_label()

        self.draw_activity()


    # ========================================================
    # TURN RIGHT
    # ========================================================

    def turn_right(self):

        directions = [

            "N",
            "E",
            "S",
            "W"

        ]


        index = directions.index(
            self.direction
        )


        self.direction = directions[
            (index + 1) % 4
        ]


        self.update_direction_label()

        self.draw_activity()


    # ========================================================
    # FINISH ACTIVITY
    # ========================================================

    def finish_activity(self):

        self.running = False


        self.run_button.config(
            state="normal"
        )


        self.command_list.selection_clear(
            0,
            tk.END
        )


        successful = (
            self.robot_x == self.target_x
            and self.robot_y == self.target_y
        )


        record_activity_attempt(
            self.current_activity,
            successful
        )


        if successful:

            self.status_label.config(
                text=(
                    f"Kgwetlho {self.current_activity}: "
                    "O atlegile! Roboto e fitlhile kwa FITLHA."
                )
            )


            messagebox.showinfo(
                "O Atlegile!",
                (
                    f"O feditse Kgwetlho "
                    f"{self.current_activity} "
                    "ka katlego!"
                )
            )


        else:

            self.status_label.config(
                text=(
                    f"Kgwetlho {self.current_activity}: "
                    "Roboto ga e ise e fitlhe kwa FITLHA. "
                    "Leka gape."
                )
            )


            messagebox.showinfo(
                "Leka Gape",
                (
                    "Roboto ga e a fitlha kwa FITLHA. "
                    "Leba direction le tatelano ya ditaelo, "
                    "mme o leke gape."
                )
            )


    # ========================================================
    # FAILED ACTIVITY
    # ========================================================

    def fail_activity(
        self,
        reason
    ):

        self.running = False


        self.run_button.config(
            state="normal"
        )


        self.command_list.selection_clear(
            0,
            tk.END
        )


        record_activity_attempt(
            self.current_activity,
            False
        )


        self.status_label.config(
            text=(
                f"Kgwetlho {self.current_activity}: "
                f"{reason}"
            )
        )


        messagebox.showinfo(
            "Leka Gape",
            reason
        )


    # ========================================================
    # RESET ROBOT
    # ========================================================

    def reset_robot(self):

        self.running = False

        self.current_command = 0


        self.robot_x = self.start_x

        self.robot_y = self.start_y

        self.direction = "N"


        self.run_button.config(
            state="normal"
        )


        self.command_list.selection_clear(
            0,
            tk.END
        )


        self.update_direction_label()

        self.draw_activity()


        self.status_label.config(
            text=(
                f"Kgwetlho {self.current_activity}: "
                "Roboto e buseditswe kwa tshimologong."
            )
        )