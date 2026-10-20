
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
