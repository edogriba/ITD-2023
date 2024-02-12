from utils.utils import *
import pandas as pd

def create_graph(graphs):
    with graphs[0].expander("Bar chart"):
        tot = execute_query(st.session_state["connection"], "SELECT StartTime, COUNT(*) AS 'Lesson Number' FROM Schedule GROUP BY StartTime;")
        chart1_lessons = pd.DataFrame(
            tot
        )
        st.bar_chart(chart1_lessons, x='StartTime', y='Lesson Number')
    with graphs[0].expander("Line chart"):
        tot = execute_query(st.session_state["connection"], "SELECT COUNT(*) AS 'Number of Lessons per day' FROM Schedule GROUP BY Day")
        chart2_lessons = pd.DataFrame(
            tot, index=["1_Monday", "2_Tuesday", "3_Wednesday", "4_Thursday", "5_Friday"]
        )
        st.line_chart(chart2_lessons)

if __name__ == "__main__":
    st.title("📈 Charts")
    # creation of one single tab
    graphs = st.tabs(["Charts"])
    if check_connection():
        create_graph(graphs=graphs)