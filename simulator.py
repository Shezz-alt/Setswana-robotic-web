import tkinter as tk
from tkinter import messagebox

BACKGROUND = "#66A96B"
LIGHT_BLUE = "#BDE7F5"
LIGHT_PINK = "#F8D7E6"
WHITE = "#FFFFFF"
SOFT_GREEN = "#BFE3C0"
SOFT_YELLOW = "#FFE8A3"
BLACK = "#000000"

# ============================================================
# SIMULATOR TIMING
# ============================================================

EXECUTION_DELAY = 1200
WAIT_DELAY = 1800

# ============================================================
# COMMAND HELP
# ============================================================

COMMAND_HELP = {
    "Tsamaya Pele": {
        "setswana": (
            "Tsamaisa roboto kwa pele go ya kwa e lebileng teng."
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
            "Robot ga e suthe mo seleng; e fetola fela tsela "
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
    },

    "Leta": {
        "setswana": (
            "Roboto e leta nakwana pele ga lenaneo le tswelela "
            "ka taelo e e latelang."
        ),
        "english": (
            "Wait briefly before continuing to the next command."
        )
    },

    "Ema": {
        "setswana": (
            "Emisa go diragadiwa ga ditaelo tsa robot."
        ),
        "english": (
            "Stop the robot program."
        )
    }
}


class RobotSimulator:

    def __init__(self, parent):

        self.parent = parent
        self.program_commands = []
        self.current_command = 0
        self.program_running = False
        self.direction = "N"

        self.start_x = 3
        self.start_y = 3

        self.robot_x = self.start_x
        self.robot_y = self.start_y

        self.cell_size = 50

        self.parent.configure(
            bg=BACKGROUND
        )

        self.build_interface()


    # ========================================================
    # MAIN INTERFACE
    # ========================================================

    def build_interface(self):

        tk.Label(
            self.parent,
            text="🤖 LENANEO LA ROBOTO",
            font=("Arial", 23, "bold"),
            fg=BLACK,
            bg=BACKGROUND
        ).pack(
            pady=(15, 3)
        )


        tk.Label(
            self.parent,
            text="Rulaganya ditaelo go laola roboto",
            font=("Arial", 12, "bold"),
            fg=BLACK,
            bg=BACKGROUND
        ).pack(
            pady=(0, 10)
        )


        main_area = tk.Frame(
            self.parent,
            bg=BACKGROUND
        )

        main_area.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )


        self.build_command_panel(
            main_area
        )

        self.build_program_panel(
            main_area
        )

        self.build_simulator_panel(
            main_area
        )


    # ========================================================
    # DIBOLOKO TSA DITAELO
    # ========================================================

    def build_command_panel(
        self,
        parent
    ):

        frame = tk.Frame(
            parent,
            width=270,
            bg=WHITE,
            highlightbackground=BLACK,
            highlightthickness=1
        )

        frame.pack(
            side="left",
            fill="y",
            padx=(0, 10)
        )

        frame.pack_propagate(
            False
        )


        tk.Label(
            frame,
            text="DIBOLOKO TSA DITAELO",
            font=("Arial", 13, "bold"),
            fg=BLACK,
            bg=LIGHT_BLUE,
            wraplength=240
        ).pack(
            fill="x",
            pady=(0, 10),
            ipady=10
        )


        tk.Label(
            frame,
            text="Tlhopha taelo",
            font=("Arial", 10, "bold"),
            fg=BLACK,
            bg=WHITE
        ).pack(
            pady=(3, 3)
        )


        tk.Label(
            frame,
            text="Tobetsa ? go bona tlhaloso ya taelo.",
            font=("Arial", 9),
            fg=BLACK,
            bg=WHITE,
            wraplength=235,
            justify="center"
        ).pack(
            pady=(0, 8)
        )


        self.command_button(
            frame,
            "🤖👆 Tsamaya Pele",
            "Tsamaya Pele",
            LIGHT_BLUE
        )


        self.command_button(
            frame,
            "🤖👇 Tsamaya Morago",
            "Tsamaya Morago",
            LIGHT_PINK
        )


        self.command_button(
            frame,
            "🤖👈 Sokologela Molemeng",
            "Sokologela Molemeng",
            SOFT_YELLOW,
            9
        )


        self.command_button(
            frame,
            "🤖👉 Sokologela Mojeng",
            "Sokologela Mojeng",
            LIGHT_PINK,
            9
        )


        self.command_button(
            frame,
            "🤖⏱ Leta",
            "Leta",
            LIGHT_BLUE
        )


        self.command_button(
            frame,
            "🤖✋ Ema",
            "Ema",
            LIGHT_PINK
        )


    def command_button(
        self,
        parent,
        label,
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
            pady=4
        )


        tk.Button(
            row,
            text=label,
            width=20,
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
    # DITAELO TSA GAGO
    # ========================================================

    def build_program_panel(
        self,
        parent
    ):

        frame = tk.Frame(
            parent,
            width=300,
            bg=WHITE,
            highlightbackground=BLACK,
            highlightthickness=1
        )

        frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )


        tk.Label(
            frame,
            text="DITAELO TSA GAGO",
            font=("Arial", 13, "bold"),
            fg=BLACK,
            bg=LIGHT_PINK
        ).pack(
            fill="x",
            pady=(0, 5),
            ipady=10
        )


        tk.Label(
            frame,
            text=(
                "Ditaelo di tla diragadiwa "
                "ka tatelano, nngwe ka nngwe."
            ),
            font=("Arial", 10, "bold"),
            fg=BLACK,
            bg=WHITE,
            wraplength=260
        ).pack(
            pady=(8, 5)
        )


        self.command_list = tk.Listbox(
            frame,
            font=("Arial", 12),
            height=15,
            bg="#FFFDF7",
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
            pady=10
        )


        controls = tk.Frame(
            frame,
            bg=WHITE
        )

        controls.pack(
            fill="x",
            padx=10,
            pady=10
        )


        tk.Button(
            controls,
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
            controls,
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
            side="right",
            padx=5
        )


    # ========================================================
    # ROBOT SIMULATOR
    # ========================================================

    def build_simulator_panel(
        self,
        parent
    ):

        frame = tk.Frame(
            parent,
            width=390,
            bg=WHITE,
            highlightbackground=BLACK,
            highlightthickness=1
        )

        frame.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(10, 0)
        )


        tk.Label(
            frame,
            text="ROBOTO",
            font=("Arial", 13, "bold"),
            fg=BLACK,
            bg=LIGHT_BLUE
        ).pack(
            fill="x",
            pady=(0, 3),
            ipady=10
        )


        self.direction_label = tk.Label(
            frame,
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
            frame,
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


        self.draw_grid()
        self.draw_robot()


        controls = tk.Frame(
            frame,
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
            command=self.run_program
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
            frame,
            text="Roboto e siametse go simolola.",
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
    # GRID
    # ========================================================

    def draw_grid(self):

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


    # ========================================================
    # HUMANOID ROBOT
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


        # Larger direction arrow above robot
        self.canvas.create_text(
            center_x,
            center_y - 28,
            text=self.get_direction_arrow(),
            font=("Arial", 16, "bold"),
            fill=BLACK,
            tags="robot"
        )


        # Tlhogo
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


        # Matlho
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


        # Mmele
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


        # Mabogo
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


        # Maoto
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
    # ROBOT DIRECTION
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
                f"Robot e lebile: "
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

        if self.program_running:
            return


        self.program_commands.append(
            command
        )


        self.refresh_command_list()


    def remove_command(self):

        if self.program_running:
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


        self.program_commands.pop(
            selection[0]
        )


        self.refresh_command_list()


    def clear_commands(self):

        if self.program_running:
            return


        self.program_commands.clear()


        self.refresh_command_list()


        self.status_label.config(
            text=(
                "Ditaelo tsotlhe "
                "di phimotswe."
            )
        )


    def refresh_command_list(self):

        self.command_list.delete(
            0,
            tk.END
        )


        for index, command in enumerate(
            self.program_commands,
            start=1
        ):

            self.command_list.insert(
                tk.END,
                f"{index}. {command}"
            )


    # ========================================================
    # RUN PROGRAM
    # ========================================================

    def run_program(self):

        if self.program_running:
            return


        if not self.program_commands:

            messagebox.showinfo(
                "Lenaneo",
                (
                    "Tlhopha ditaelo pele "
                    "ga o simolola."
                )
            )

            return


        self.current_command = 0

        self.program_running = True


        self.run_button.config(
            state="disabled"
        )


        self.status_label.config(
            text=(
                "Robot e simolola go diragatsa "
                "ditaelo ka tatelano..."
            )
        )


        self.parent.after(
            500,
            self.execute_next_command
        )


    def execute_next_command(self):

        if not self.program_running:
            return


        if self.current_command >= len(
            self.program_commands
        ):

            self.finish_program()

            return


        command = self.program_commands[
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
            self.program_commands
        )


        self.status_label.config(
            text=(
                f"Taelo {command_number}/{total_commands}: "
                f"{command}"
            )
        )


        delay = EXECUTION_DELAY


        if command == "Tsamaya Pele":

            self.move_forward()


        elif command == "Tsamaya Morago":

            self.move_backward()


        elif command == "Sokologela Molemeng":

            self.turn_left()


        elif command == "Sokologela Mojeng":

            self.turn_right()


        elif command == "Leta":

            delay = WAIT_DELAY


        elif command == "Ema":

            self.status_label.config(
                text=(
                    f"Taelo {command_number}/{total_commands}: "
                    "Roboto e emisitswe."
                )
            )


            self.program_running = False


            self.run_button.config(
                state="normal"
            )


            return


        self.current_command += 1


        self.parent.after(
            delay,
            self.execute_next_command
        )


    # ========================================================
    # MOVEMENT
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


        self.attempt_move(
            new_x,
            new_y
        )


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


        self.attempt_move(
            new_x,
            new_y
        )


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

            self.status_label.config(
                text=(
                    "Roboto ga e kgone go tswa "
                    "mo lefelong la motsamao."
                )
            )

            return


        self.robot_x = new_x
        self.robot_y = new_y


        self.draw_robot()


    # ========================================================
    # TURNING
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

        self.draw_robot()


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

        self.draw_robot()


    # ========================================================
    # FINISH / RESET
    # ========================================================

    def finish_program(self):

        self.program_running = False


        self.run_button.config(
            state="normal"
        )


        self.command_list.selection_clear(
            0,
            tk.END
        )


        self.status_label.config(
            text=(
                "Roboto e feditse "
                "ditaelo tsotlhe."
            )
        )


    def reset_robot(self):

        self.program_running = False

        self.current_command = 0


        self.robot_x = self.start_x
        self.robot_y = self.start_y


        self.direction = "N"


        self.update_direction_label()

        self.draw_robot()


        self.command_list.selection_clear(
            0,
            tk.END
        )


        self.run_button.config(
            state="normal"
        )


        self.status_label.config(
            text=(
                "Roboto e buseditswe "
                "kwa tshimologong."
            )
        )