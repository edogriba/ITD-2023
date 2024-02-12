from utils.utils import *
import pandas as pd

def create_courses_tab(courses_tab):
    col1, col2, col3 = courses_tab[0].columns(3)
    courses_info = execute_query(st.session_state["connection"],
                                 "SELECT COUNT(*) AS 'Total Amount', COUNT(DISTINCT Type) AS 'Number of Types' FROM Course;")
    # create a suitable data structure from the query result
    courses_info_dict = [dict(zip(courses_info.keys(), result)) for result in courses_info]
    col1.metric('Total amount of courses', f"{compact_format(courses_info_dict[0]['Total Amount'])}")
    col2.metric('Number of types of courses', f"{compact_format(courses_info_dict[0]['Number of Types'])}")

    query = "SELECT MIN(Level), MAX(Level) FROM Course"
    result = execute_query(st.session_state["connection"], query)
    min_max = result.first()
    course_types = get_info("Type", "Course")


    with courses_tab[0].expander("Courses Overview", True):

        filter_param = st.radio("Type of course", course_types)
        level_range = st.slider("Select the level range:", value=(min_max[0], min_max[1]), min_value=min_max[0], max_value=min_max[1])
        if st.button("Show", type='primary'):
            # break the query into two strings to facilitate readability of the code: one fixed and the other that adapts to the options you choose
            query_base = "SELECT CId AS 'code', Name AS 'name', Type AS type, Level AS level FROM Course"
            secondquery = f"WHERE Level >={level_range[0]} AND Level <= {level_range[1]} AND Type = '{filter_param}'"
            products = execute_query(st.session_state["connection"], query_base + " " + secondquery)
            # automatic dataframe creation
            df_products = pd.DataFrame(products)

            if df_products.empty:
                st.warning("No data found.", icon='⚠️')
            else:
                st.write("Range level", level_range[0], '-', level_range[1])
                st.dataframe(df_products, use_container_width=True)

    with courses_tab[0].expander("Lessons Overview", True):
        query_base2 = "SELECT CId, Day, StartTime, Duration, GymRoom, SSN FROM Schedule"
        secondquery2 = f"WHERE CId IN (SELECT CId FROM Course WHERE Level >={level_range[0]} AND Level <= {level_range[1]} AND Type = '{filter_param}')"
        query_sort2 = f"ORDER BY CId;"
        lessons = execute_query(st.session_state["connection"], query_base2 + " " + secondquery2 + " " + query_sort2)
        # automatic dataframe creation
        df_lessons = pd.DataFrame(lessons)

        if df_lessons.empty:
            st.warning("No data found.", icon='⚠️')
        else:
            st.write(f"The type of courses selected: {filter_param}")
            st.write("The range level selected:", level_range[0], '-', level_range[1])
            st.dataframe(df_lessons, use_container_width=True)


if __name__ == "__main__":
    st.title("💻 Courses")
    # creation of one single tab
    courses_tab = st.tabs(["Courses"])
    if check_connection():
        create_courses_tab(courses_tab=courses_tab)
