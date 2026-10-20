import html
import time
import streamlit as st

from web_database import (
    register_user,
    login_user,
    complete_lesson,
    get_completed_lessons,
    record_activity_attempt,
    get_activity_progress,
    calculate_progress,
    get_all_learners_progress,
)

st.set_page_config(
    page_title="Setswana Robotics",
    page_icon="🤖",
    layout="wide",
)

# ============================================================
# COLOURS / STYLE
# ============================================================
BACKGROUND = "#2E7D32"
LIGHT_BLUE = "#BDE7F5"
LIGHT_PINK = "#F8D7E6"
DEEP_BLUE = "#274C77"
WHITE = "#FFFFFF"
SOFT_GREEN = "#BFE3C0"
SOFT_YELLOW = "#FFE8A3"
BLACK = "#000000"
CREAM = "#FFFDF7"

st.markdown(
    f"""
    <style>
    .stApp {{ background: {BACKGROUND}; }}
    [data-testid="stSidebar"] {{ background: {WHITE}; }}
    .main-title {{
        text-align:center;
        font-size:2.2rem;
        font-weight:800;
        color:{BLACK};
        margin-bottom:.4rem;
    }}
    .subtitle {{
        text-align:center;
        font-weight:700;
        color:{BLACK};
        margin-bottom:1rem;
    }}
    .card {{
        background:{WHITE};
        padding:1rem 1.2rem;
        border-radius:14px;
        border:2px solid #D5E5EA;
        color:{BLACK};
        margin-bottom:.8rem;
    }}
    .info {{
        background:{SOFT_YELLOW};
        padding:.8rem 1rem;
        border-radius:10px;
        color:{BLACK};
        font-weight:600;
    }}
    div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stMarkdownContainer"] li {{ color:{BLACK}; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# LESSONS
# ============================================================
LESSONS = [
    {
        "title": "THUTO 1: MATSENO A DIROBOTO",
        "menu": "1. Matseno a Diroboto",
        "content": """ROBOT KE ENG?

Robot ke motšhini o o ka rulaganyediwang go dira ditiro tse di rileng
ka go latela ditaelo tse e di neilweng.

Robot e ka dirisiwa go dira ditiro tse di farologaneng.
Diroboto dingwe di kgona go tsamaya, go lemoga dilo tse di
di dikologileng le go dira tiro go ya ka ditaelo tse di rulagantsweng.

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
jang go laola robot e e etsisiwang mo khomphuthareng.""",
    },
    {
        "title": "THUTO 2: DIKAROLO TSA ROBOT",
        "menu": "2. Dikarolo tsa Robot",
        "content": """DIKAROLO TSA ROBOT

Robot e ka nna le dikarolo tse di farologaneng go ya ka tiro
e e diretsweng go e dira.

1. SELAODI
Selaodi se laola tsela e robot e dirang ka yone.
Se amogela le go diragatsa ditaelo tse di bolelelang robot
gore e dire eng.

2. DISENSA
Disensa di thusa robot go lemoga tshedimosetso e e tswang
mo tikologong ya yone.
Ka sekai, sensor e ka lemoga:
• Lesedi
• Bokgakala
• Go ama
• Motsamao

3. ACTUATOR
Actuator ke karolo e e thusang robot go dira motsamao
kgotsa tiragalo nngwe.
Ka sekai, motor e ka dirisiwa go dikolosa maotwana
gore robot e kgone go tsamaya.

4. MOTSWEDI WA MAATLA
Robot e tlhoka maatla gore e kgone go dira.
Diroboto dingwe di dirisa dibeteri, fa tse dingwe di dirisa
metswedi e mengwe ya motlakase.

Dikarolo tseno di dirisana mmogo go thusa robot go lemoga
tikologo, go amogela ditaelo le go dira tiro.""",
    },
    {
        "title": "THUTO 3: MOTSAMAO LE DITAELO",
        "menu": "3. Motsamao le Ditaelo",
        "content": """MOTSAMAO WA ROBOT

Robot e tlhoka ditaelo tse di tlhaloganyegang gore e itse
gore e tshwanetse go tsamaya jang.

Mo simulator ya rona, re tla dirisa ditaelo tse di jaaka:
• Tsamaya pele
• Tsamaya morago
• Sokologela molemeng
• Sokologela mojeng
• Ema

TATELANO YA DITAELO

Robot e tshwanetse go diragatsa ditaelo ka tatelano
e e rulagantsweng.

Ka sekai:
1. Tsamaya pele
2. Tsamaya pele
3. Sokologela mojeng
4. Tsamaya pele
5. Ema

Fa tatelano ya ditaelo e fetolwa, robot e ka feleletsa
e le mo lefelong le le farologaneng.

Ka jalo, go rulaganya ditaelo ka tatelano e e siameng
ke karolo e e botlhokwa ya programming.""",
    },
    {
        "title": "THUTO 4: ALGORITHM LE PROGRAMMING",
        "menu": "4. Algorithm le Programming",
        "content": """ALGORITHM KE ENG?

Algorithm ke tatelano ya dikgato kgotsa ditaelo tse di
rulagantsweng go rarabolola bothata kgotsa go dira tiro e e rileng.

Ka sekai, re ka naya robot algorithm e e latelang:
Kgato 1: Tsamaya pele
Kgato 2: Tsamaya pele
Kgato 3: Sokologela mojeng
Kgato 4: Tsamaya pele
Kgato 5: Ema

PROGRAMMING YA ROBOT

Programming ke mokgwa wa go naya khomphuthara kgotsa robot
ditaelo tse e ka di diragatsang.

Mo thulaganyong eno, ga o tlhoke go kwala Python code
gore o kgone go laola robot.

O tla dirisa diboloko tsa ditaelo tse di bonalang mo sekirining.

Mokgwa ono o tlhotlheleditswe ke Scratch, e e dirisang
diboloko tsa programming go thusa barutwana go ithuta
dikgopolo tsa programming ka tsela e e bonalang.""",
    },
]

# ============================================================
# ROBOT PARTS
# ============================================================
ROBOT_PARTS = {
    "Tlhogo": (
        "TLHOGO (Head)",
        "Tlhogo ke karolo e e kwa godimo ya robot. E ka tshola disensa le dikarolo tse di thusang robot go amogela tshedimosetso.",
    ),
    "Matlho": (
        "MATLHO / DISENSA TSA PONO",
        "Matlho a robot a ka emela disensa tsa pono. Disensa di thusa robot go lemoga lesedi, dilo kgotsa tikologo e e e dikologileng.",
    ),
    "Ditsebe": (
        "DITSEBE / SENSA YA MODUMO",
        "Ditsebe di ka emela sensor ya modumo kgotsa microphone. Karolo eno e thusa robot go lemoga medumo mo tikologong.",
    ),
    "Mmele": (
        "MMELE (Body)",
        "Mmele o tshola le go sireletsa dikarolo tsa robot. Mo teng go ka nna le selaodi, mehala le dikarolo tse dingwe tsa elektroniki.",
    ),
    "Selaodi": (
        "SELAODI (Controller)",
        "Selaodi se amogela le go diragatsa ditaelo. Se thusa go laola tsela e robot e arabelang le go dira ditiro ka yone.",
    ),
    "Maatla": (
        "MOTSWEDI WA MAATLA",
        "Motswedi wa maatla o naya robot maatla a go dira. Sekai ke beteri e e nayang dikarolo tsa robot motlakase.",
    ),
    "Mabogo": (
        "MABOGO (Arms)",
        "Mabogo a robot a ka tsamaisiwa ke dimotor kgotsa diactuator. A thusa robot go tsamaisa kgotsa go fitlhelela dilo.",
    ),
    "Diatla": (
        "DIATLA (Hands)",
        "Diatla di ka thusa robot go tshwara kgotsa go sutisa dilo fa robot e na le mokgwa wa go dira jalo.",
    ),
    "Maoto": (
        "MAOTO (Legs)",
        "Maoto a thusa robot go ema le go tsamaya. Dimotor kgotsa diactuator di ka laola motsamao wa maoto.",
    ),
}

# ============================================================
# COMMANDS / ACTIVITIES
# ============================================================
COMMANDS = [
    "Tsamaya Pele",
    "Tsamaya Morago",
    "Sokologela Molemeng",
    "Sokologela Mojeng",
    "Leta",
    "Ema",
]

ACTIVITIES = {
    1: {
        "title": "KGWETLHO 1",
        "instruction": "Tsamaisa robot go fitlha kwa lefelong le le tshwailweng FITLHA.",
        "target": (3, 2),
        "obstacles": [],
    },
    2: {
        "title": "KGWETLHO 2",
        "instruction": "Dirisa motsamao le go sokologa go fitlhisa robot kwa FITLHA.",
        "target": (5, 3),
        "obstacles": [],
    },
    3: {
        "title": "KGWETLHO 3",
        "instruction": "Fitlhisa robot kwa FITLHA mme o se ka wa tsena mo dikarolong tse di nang le sekgoreletsi.",
        "target": (5, 1),
        "obstacles": [(3, 3), (4, 3)],
    },
}

# ============================================================
# SESSION STATE
# ============================================================
DEFAULTS = {
    "role_choice": None,
    "user_role": None,
    "user_id": None,
    "user_name": None,
    "page": "Gae",
    "sim_commands": [],
    "sim_x": 3,
    "sim_y": 3,
    "sim_direction": "N",
    "activity_number": 1,
    "activity_commands": [],
    "activity_x": 3,
    "activity_y": 5,
    "activity_direction": "N",
    "selected_part": "Tlhogo",
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value.copy() if isinstance(value, list) else value


def reset_session():
    for key, value in DEFAULTS.items():
        st.session_state[key] = value.copy() if isinstance(value, list) else value


def active_learner_id():
    if st.session_state.user_role == "learner":
        return st.session_state.user_id
    return None


# ============================================================
# DIRECTION / MOVEMENT LOGIC
# ============================================================
ARROWS = {"N": "↑", "E": "→", "S": "↓", "W": "←"}
NAMES = {
    "N": "Bokone ↑",
    "E": "Botlhaba →",
    "S": "Borwa ↓",
    "W": "Bophirima ←",
}


def move_state(x, y, direction, command, obstacles=None):
    obstacles = obstacles or []
    new_x, new_y, new_direction = x, y, direction

    if command == "Tsamaya Pele":
        if direction == "N":
            new_y -= 1
        elif direction == "E":
            new_x += 1
        elif direction == "S":
            new_y += 1
        else:
            new_x -= 1

    elif command == "Tsamaya Morago":
        if direction == "N":
            new_y += 1
        elif direction == "E":
            new_x -= 1
        elif direction == "S":
            new_y -= 1
        else:
            new_x += 1

    elif command == "Sokologela Molemeng":
        directions = ["N", "W", "S", "E"]
        new_direction = directions[(directions.index(direction) + 1) % 4]

    elif command == "Sokologela Mojeng":
        directions = ["N", "E", "S", "W"]
        new_direction = directions[(directions.index(direction) + 1) % 4]

    # Leta and Ema intentionally keep position/direction unchanged.

    if not (0 <= new_x <= 6 and 0 <= new_y <= 6):
        return x, y, direction, "boundary"

    if (new_x, new_y) in obstacles:
        return x, y, direction, "obstacle"

    return new_x, new_y, new_direction, "ok"


# ============================================================
# ROBUST HTML RENDERERS
# Important: generated HTML contains no Markdown indentation.
# ============================================================
def grid_html(x, y, direction, target=None, obstacles=None):
    obstacles = obstacles or []
    cells = []

    for row in range(7):
        for column in range(7):
            label = "&nbsp;"
            colour = WHITE
            border = "#9E9E9E"

            if (column, row) in obstacles:
                label = "✖"
                colour = "#D0D0D0"

            if target == (column, row):
                label = "FITLHA"
                colour = SOFT_GREEN

            if (column, row) == (x, y):
                label = f"🤖<br><span style='font-size:20px'>{ARROWS[direction]}</span>"
                colour = LIGHT_BLUE
                border = DEEP_BLUE

            cells.append(
                "<div style='"
                f"background:{colour};"
                f"border:2px solid {border};"
                "min-height:52px;"
                "display:flex;"
                "align-items:center;"
                "justify-content:center;"
                "text-align:center;"
                "font-weight:800;"
                "font-size:11px;"
                "border-radius:6px;"
                "color:#000000;"
                "'>"
                f"{label}"
                "</div>"
            )

    return (
        "<div style='background:#FFFFFF;padding:12px;border-radius:14px;"
        "border:2px solid #D5E5EA;max-width:480px;margin:0 auto;'>"
        "<div style='display:grid;grid-template-columns:repeat(7,minmax(38px,1fr));"
        "gap:3px;width:100%;'>"
        + "".join(cells)
        + "</div></div>"
    )


def robot_svg():
    # Kept on one HTML line so Streamlit does not interpret SVG as a Markdown code block.
    return (
        f"<div style='background:{CREAM};border:2px solid {LIGHT_BLUE};border-radius:14px;"
        "padding:10px;text-align:center;max-width:420px;margin:0 auto;'>"
        "<svg width='300' height='405' viewBox='0 0 300 405' xmlns='http://www.w3.org/2000/svg' "
        "style='max-width:100%;height:auto;'>"
        "<line x1='150' y1='10' x2='150' y2='30' stroke='black' stroke-width='4'/>"
        f"<circle cx='150' cy='9' r='7' fill='{SOFT_YELLOW}' stroke='black' stroke-width='2'/>"
        f"<rect x='95' y='30' width='110' height='85' rx='8' fill='{LIGHT_BLUE}' stroke='black' stroke-width='3'/>"
        f"<ellipse cx='84' cy='70' rx='11' ry='20' fill='{LIGHT_PINK}' stroke='black' stroke-width='2'/>"
        f"<ellipse cx='216' cy='70' rx='11' ry='20' fill='{LIGHT_PINK}' stroke='black' stroke-width='2'/>"
        "<circle cx='125' cy='68' r='10' fill='white' stroke='black'/>"
        "<circle cx='175' cy='68' r='10' fill='white' stroke='black'/>"
        "<circle cx='125' cy='68' r='3' fill='black'/>"
        "<circle cx='175' cy='68' r='3' fill='black'/>"
        "<line x1='128' y1='96' x2='172' y2='96' stroke='black' stroke-width='3'/>"
        f"<rect x='132' y='115' width='36' height='18' fill='{SOFT_YELLOW}' stroke='black'/>"
        f"<rect x='102' y='133' width='96' height='126' rx='8' fill='{LIGHT_BLUE}' stroke='black' stroke-width='3'/>"
        f"<rect x='120' y='150' width='60' height='40' fill='{SOFT_YELLOW}' stroke='black'/>"
        "<text x='150' y='175' text-anchor='middle' font-size='12' font-weight='700' fill='black'>SELAODI</text>"
        f"<rect x='126' y='210' width='48' height='36' fill='{SOFT_GREEN}' stroke='black'/>"
        "<text x='150' y='233' text-anchor='middle' font-size='12' font-weight='700' fill='black'>MAATLA</text>"
        f"<rect x='55' y='145' width='47' height='28' fill='{LIGHT_PINK}' stroke='black'/>"
        f"<rect x='30' y='168' width='28' height='80' fill='{LIGHT_BLUE}' stroke='black'/>"
        f"<rect x='198' y='145' width='47' height='28' fill='{LIGHT_PINK}' stroke='black'/>"
        f"<rect x='242' y='168' width='28' height='80' fill='{LIGHT_BLUE}' stroke='black'/>"
        f"<circle cx='44' cy='262' r='17' fill='{SOFT_YELLOW}' stroke='black'/>"
        f"<circle cx='256' cy='262' r='17' fill='{SOFT_YELLOW}' stroke='black'/>"
        f"<rect x='110' y='259' width='80' height='22' fill='{LIGHT_PINK}' stroke='black'/>"
        f"<rect x='115' y='281' width='32' height='78' fill='{LIGHT_BLUE}' stroke='black'/>"
        f"<rect x='153' y='281' width='32' height='78' fill='{LIGHT_BLUE}' stroke='black'/>"
        f"<rect x='102' y='356' width='45' height='26' fill='{SOFT_YELLOW}' stroke='black'/>"
        f"<rect x='153' y='356' width='45' height='26' fill='{SOFT_YELLOW}' stroke='black'/>"
        "</svg></div>"
    )


# ============================================================
# ROLE SELECTION / LOGIN
# ============================================================
def role_selection():
    st.markdown('<div class="main-title">🤖 SETSWANA ROBOTICS</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">Tlhopha gore o tsena jaaka Morutabana kgotsa Morutwana.</div>',
        unsafe_allow_html=True,
    )

    teacher_column, learner_column = st.columns(2)

    with teacher_column:
        st.markdown(
            "<div class='card' style='text-align:center'><div style='font-size:3rem'>👩‍🏫</div>"
            "<h3>MORUTABANA</h3><p>Dirisa dithuto, dikarolo tsa robot, Pogoramo le Ditiro go ruta barutwana.</p></div>",
            unsafe_allow_html=True,
        )
        if st.button("👩‍🏫 Tsena jaaka Morutabana", use_container_width=True):
            st.session_state.role_choice = "teacher"
            st.rerun()

    with learner_column:
        st.markdown(
            "<div class='card' style='text-align:center'><div style='font-size:3rem'>🧑‍🎓</div>"
            "<h3>MORUTWANA</h3><p>Ithute dithuto, dikarolo tsa robot, Pogoramo le Ditiro.</p></div>",
            unsafe_allow_html=True,
        )
        if st.button("🧑‍🎓 Tsena jaaka Morutwana", use_container_width=True):
            st.session_state.role_choice = "learner"
            st.rerun()


def login_page():
    role = st.session_state.role_choice
    if role == "teacher":
        title = "👩‍🏫 MORUTABANA"
    else:
        title = "🧑‍🎓 MORUTWANA"

    st.markdown(f'<div class="main-title">{title}</div>', unsafe_allow_html=True)

    if st.button("← Boela morago"):
        st.session_state.role_choice = None
        st.rerun()

    name = st.text_input("Kwala leina kgotsa khoutu ya teko", placeholder="Sekai: P001")
    login_column, register_column = st.columns(2)

    with login_column:
        if st.button("🔓 Tsena", use_container_width=True):
            result = login_user(role, name)
            if result:
                st.session_state.user_id = result[0]
                st.session_state.user_name = result[1]
                st.session_state.user_role = role
                st.session_state.page = "Gae"
                st.rerun()
            else:
                st.warning("Leina kgotsa khoutu eno ga e ise e ikwadise. Dirisa Ikwadise go simolola.")

    with register_column:
        if st.button("👤 Ikwadise", use_container_width=True):
            success, status, user_id = register_user(role, name)
            if success:
                st.session_state.user_id = user_id
                st.session_state.user_name = name.strip()
                st.session_state.user_role = role
                st.session_state.page = "Gae"
                st.rerun()
            elif status == "exists":
                st.warning("Leina kgotsa khoutu eno e setse e ikwadisitse. Dirisa Tsena.")
            elif status == "teacher":
                st.warning("Khoutu eno e setse e le ya Morutabana.")
            else:
                st.warning("Tsweetswee, kwala leina kgotsa khoutu ya teko.")


# ============================================================
# NAVIGATION
# ============================================================
def navigation():
    role = st.session_state.user_role
    icon = "👩‍🏫" if role == "teacher" else "🧑‍🎓"
    role_text = "Morutabana" if role == "teacher" else "Morutwana"

    st.sidebar.markdown("## 🤖 SETSWANA ROBOTICS")
    st.sidebar.markdown(f"**{icon} {role_text}: {st.session_state.user_name}**")
    st.sidebar.markdown("---")

    pages = ["Gae", "Dithuto", "Dikarolo tsa Robot", "Pogoramo", "Ditiro", "Kgatelopele"]
    st.session_state.page = st.sidebar.radio(
        "LENANEO",
        pages,
        index=pages.index(st.session_state.page),
    )

    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Tswaya", use_container_width=True):
        reset_session()
        st.rerun()


# ============================================================
# HOME
# ============================================================
def home():
    role = st.session_state.user_role
    name = html.escape(st.session_state.user_name or "")

    st.markdown('<div class="main-title">🤖 SETSWANA ROBOTICS</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">Re a go amogela, {name}! 🌟</div>', unsafe_allow_html=True)

    if role == "teacher":
        heading = "👩‍🏫 MOKGWA WA MORUTABANA"
        text = (
            "Dirisa Dithuto go ruta barutwana, Dikarolo tsa Robot go tlhalosa robot, "
            "Pogoramo go bontsha motsamao le ditaelo, le Ditiro go bontsha dikgwetlho."
        )
        note = "Pontsho ya morutabana ga e boloki kgatelopele ya morutwana."
    else:
        heading = "🧑‍🎓 MOKGWA WA MORUTWANA"
        text = (
            "Ithute ka diroboto, tlhotlhomisa dikarolo tsa robot, aga ditaelo mo Pogoramo, "
            "mme o rarabolole dikgwetlho."
        )
        note = "Dithuto le ditiro tse o di fetsang di tla bonala mo Kgatelopele."

    st.markdown(
        f"<div class='card'><h3>{heading}</h3><p>{text}</p><p><b>{note}</b></p></div>",
        unsafe_allow_html=True,
    )


# ============================================================
# LESSONS PAGE
# ============================================================
def lessons_page():
    role = st.session_state.user_role
    learner_id = active_learner_id()
    completed = get_completed_lessons(learner_id) if learner_id else []

    st.header("📘 DITHUTO TSA DIROBOTO")

    labels = []
    for number, lesson in enumerate(LESSONS, start=1):
        prefix = "✓ " if number in completed else ""
        labels.append(prefix + lesson["menu"])

    selected = st.selectbox("Tlhopha thuto", labels)
    index = labels.index(selected)
    lesson = LESSONS[index]

    st.markdown(
        f"<div class='card'><h3>{lesson['title']}</h3></div>",
        unsafe_allow_html=True,
    )
    st.text(lesson["content"])

    if role == "learner":
        lesson_number = index + 1
        if lesson_number in completed:
            st.success("✓ Thuto e Feditswe")
        elif st.button("✓ Ke Feditse Thuto", type="primary"):
            complete_lesson(learner_id, lesson_number)
            st.success(f"O feditse Thuto {lesson_number}! Kgatelopele ya gago e bolokilwe.")
            st.rerun()


# ============================================================
# ROBOT PARTS PAGE
# ============================================================
def parts_page():
    st.header("🦾 DIKAROLO TSA ROBOT")
    st.caption("Tlhopha karolo ya robot go bona leina le tlhaloso ya yone.")

    robot_column, info_column = st.columns([1.15, 1], gap="large")

    with robot_column:
        # The no-indentation SVG fixes the raw <svg> text problem seen in deployment.
        st.markdown(robot_svg(), unsafe_allow_html=True)

    with info_column:
        keys = list(ROBOT_PARTS)
        columns = st.columns(3)
        for index, key in enumerate(keys):
            with columns[index % 3]:
                if st.button(key, key=f"part_{key}", use_container_width=True):
                    st.session_state.selected_part = key
                    st.rerun()

        name, description = ROBOT_PARTS[st.session_state.selected_part]
        st.markdown(
            f"<div class='card'><h2>{name}</h2><div class='info'>{description}</div></div>",
            unsafe_allow_html=True,
        )


# ============================================================
# SIMULATOR
# ============================================================
def simulator_page():
    st.header("🤖 LENANEO LA ROBOT")
    st.caption("Rulaganya ditaelo go laola robot")

    command_column, sequence_column, robot_column = st.columns([1, 1.1, 1.45], gap="medium")

    with command_column:
        st.subheader("DIBOLOKO TSA DITAELO")
        for command in COMMANDS:
            if st.button(f"➕ {command}", key=f"sim_{command}", use_container_width=True):
                st.session_state.sim_commands.append(command)
                st.rerun()

    with sequence_column:
        st.subheader("DITAELO TSA GAGO")
        if not st.session_state.sim_commands:
            st.write("Ga go na ditaelo.")
        else:
            for index, command in enumerate(st.session_state.sim_commands, start=1):
                st.write(f"{index}. {command}")

        remove_column, clear_column = st.columns(2)
        with remove_column:
            if st.button("Tlosa Taelo", key="sim_remove", use_container_width=True):
                if st.session_state.sim_commands:
                    st.session_state.sim_commands.pop()
                st.rerun()
        with clear_column:
            if st.button("Phimola Tsotlhe", key="sim_clear", use_container_width=True):
                st.session_state.sim_commands = []
                st.rerun()

    with robot_column:
        st.subheader("ROBOT")
        st.write(f"Robot e lebile: **{NAMES[st.session_state.sim_direction]}**")

        placeholder = st.empty()
        placeholder.markdown(
            grid_html(
                st.session_state.sim_x,
                st.session_state.sim_y,
                st.session_state.sim_direction,
            ),
            unsafe_allow_html=True,
        )

        run_column, reset_column = st.columns(2)

        with run_column:
            if st.button("▶ Simolola", key="sim_run", type="primary", use_container_width=True):
                if not st.session_state.sim_commands:
                    st.warning("Tlhopha ditaelo pele ga o simolola.")
                else:
                    x = st.session_state.sim_x
                    y = st.session_state.sim_y
                    direction = st.session_state.sim_direction
                    status = "Robot e feditse ditaelo tsotlhe."

                    for command in st.session_state.sim_commands:
                        new_x, new_y, new_direction, result = move_state(x, y, direction, command)

                        if result == "boundary":
                            status = "Robot ga e kgone go tswa mo lefelong la motsamao."
                            break

                        x, y, direction = new_x, new_y, new_direction
                        status = f"Taelo: {command}"

                        placeholder.markdown(
                            grid_html(x, y, direction),
                            unsafe_allow_html=True,
                        )
                        time.sleep(0.35)

                        if command == "Ema":
                            status = "Robot e emisitswe."
                            break

                    st.session_state.sim_x = x
                    st.session_state.sim_y = y
                    st.session_state.sim_direction = direction
                    st.success(status)

        with reset_column:
            if st.button("↻ Simolola Gape", key="sim_reset", use_container_width=True):
                st.session_state.sim_commands = []
                st.session_state.sim_x = 3
                st.session_state.sim_y = 3
                st.session_state.sim_direction = "N"
                st.rerun()


# ============================================================
# ACTIVITIES
# ============================================================
def load_activity(activity_number):
    st.session_state.activity_number = activity_number
    st.session_state.activity_commands = []
    st.session_state.activity_x = 3
    st.session_state.activity_y = 5
    st.session_state.activity_direction = "N"


def activities_page():
    st.header("🎯 DITIRO TSA DIROBOTO")
    st.caption("Dirisa ditaelo go rarabolola dikgwetlho")

    activity_columns = st.columns(3)
    for activity_number in range(1, 4):
        with activity_columns[activity_number - 1]:
            if st.button(
                f"🤖 Kgwetlho {activity_number}",
                key=f"choose_activity_{activity_number}",
                use_container_width=True,
            ):
                load_activity(activity_number)
                st.rerun()

    activity_number = st.session_state.activity_number
    configuration = ACTIVITIES[activity_number]

    command_column, sequence_column, grid_column = st.columns([1, 1.1, 1.45], gap="medium")

    with command_column:
        st.subheader("DITAELO")
        for command in COMMANDS[:4]:
            if st.button(f"➕ {command}", key=f"act_{command}", use_container_width=True):
                st.session_state.activity_commands.append(command)
                st.rerun()

    with sequence_column:
        st.subheader(configuration["title"])
        st.write(configuration["instruction"])
        st.markdown("**DITAELO TSA GAGO**")

        if not st.session_state.activity_commands:
            st.write("Ga go na ditaelo.")
        else:
            for index, command in enumerate(st.session_state.activity_commands, start=1):
                st.write(f"{index}. {command}")

        remove_column, clear_column = st.columns(2)
        with remove_column:
            if st.button("Tlosa Taelo", key="act_remove", use_container_width=True):
                if st.session_state.activity_commands:
                    st.session_state.activity_commands.pop()
                st.rerun()
        with clear_column:
            if st.button("Phimola Tsotlhe", key="act_clear", use_container_width=True):
                st.session_state.activity_commands = []
                st.rerun()

    with grid_column:
        st.subheader("LEFELO LA KGWETLHO")
        placeholder = st.empty()
        placeholder.markdown(
            grid_html(
                st.session_state.activity_x,
                st.session_state.activity_y,
                st.session_state.activity_direction,
                configuration["target"],
                configuration["obstacles"],
            ),
            unsafe_allow_html=True,
        )

        run_column, reset_column = st.columns(2)

        with run_column:
            if st.button("▶ Simolola", key="act_run", type="primary", use_container_width=True):
                if not st.session_state.activity_commands:
                    st.warning("Tlhopha ditaelo pele.")
                else:
                    x, y, direction = 3, 5, "N"
                    reason = None

                    for command in st.session_state.activity_commands:
                        new_x, new_y, new_direction, result = move_state(
                            x,
                            y,
                            direction,
                            command,
                            configuration["obstacles"],
                        )

                        if result == "boundary":
                            reason = "Robot e lekile go tswa mo lefelong la kgwetlho."
                            break
                        if result == "obstacle":
                            reason = "Robot e thulane le sekgoreletsi."
                            break

                        x, y, direction = new_x, new_y, new_direction

                        placeholder.markdown(
                            grid_html(
                                x,
                                y,
                                direction,
                                configuration["target"],
                                configuration["obstacles"],
                            ),
                            unsafe_allow_html=True,
                        )
                        time.sleep(0.35)

                    st.session_state.activity_x = x
                    st.session_state.activity_y = y
                    st.session_state.activity_direction = direction

                    success = reason is None and (x, y) == configuration["target"]

                    if active_learner_id() is not None:
                        record_activity_attempt(active_learner_id(), activity_number, success)

                    if reason:
                        st.warning(reason)
                    elif success:
                        st.success(
                            f"O atlegile! Robot e fitlhile kwa FITLHA. O feditse Kgwetlho {activity_number} ka katlego!"
                        )
                    else:
                        st.warning(
                            "Robot ga e a fitlha kwa FITLHA. Leba tatelano ya ditaelo mme o leke gape."
                        )

        with reset_column:
            if st.button("↻ Simolola Gape", key="act_reset", use_container_width=True):
                load_activity(activity_number)
                st.rerun()


# ============================================================
# PROGRESS PAGE
# ============================================================
def progress_page():
    if st.session_state.user_role == "teacher":
        st.header("📊 KGATELOPELE YA BARUTWANA")
        rows = get_all_learners_progress()
        st.metric("Palo ya Barutwana", len(rows))
        if rows:
            st.dataframe(rows, use_container_width=True, hide_index=True)
        else:
            st.write("Ga go na barutwana ba ba ikwadisitseng.")
        return

    learner_id = active_learner_id()
    st.header("⭐ KGATELOPELE YA MORUTWANA")
    st.write(f"🧑‍🎓 Morutwana: **{st.session_state.user_name}**")

    percentage = calculate_progress(learner_id)
    st.metric("Kgatelopele Yotlhe", f"{percentage}%")
    st.progress(percentage / 100)

    lessons = get_completed_lessons(learner_id)
    activity_data = get_activity_progress(learner_id)
    activities = {
        activity_number: (attempts, completed)
        for activity_number, attempts, completed in activity_data
    }

    lesson_column, activity_column = st.columns(2)

    with lesson_column:
        st.subheader("📘 DITHUTO")
        lesson_names = [
            "Thuto 1: Matseno a Diroboto",
            "Thuto 2: Dikarolo tsa Robot",
            "Thuto 3: Motsamao le Ditaelo",
            "Thuto 4: Algorithm le Pogoramo",
        ]
        for number, name in enumerate(lesson_names, start=1):
            status = "✓ E Feditswe" if number in lessons else "○ Ga e Ise e Fediwe"
            st.write(f"**{name}** — {status}")

    with activity_column:
        st.subheader("🎯 DIKGWETLHO")
        for number in range(1, 4):
            attempts, completed = activities.get(number, (0, 0))
            status = "✓ E Feditswe" if completed else "○ Ga e Ise e Fediwe"
            st.write(f"**Kgwetlho {number}** — {status} — Maiteko: {attempts}")


# ============================================================
# MAIN APPLICATION
# ============================================================
if st.session_state.user_role is None:
    if st.session_state.role_choice is None:
        role_selection()
    else:
        login_page()
else:
    navigation()
    page = st.session_state.page

    if page == "Gae":
        home()
    elif page == "Dithuto":
        lessons_page()
    elif page == "Dikarolo tsa Robot":
        parts_page()
    elif page == "Pogoramo":
        simulator_page()
    elif page == "Ditiro":
        activities_page()
    elif page == "Kgatelopele":
        progress_page()
