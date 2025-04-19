import streamlit as st
import psycopg2 
import pandas as pd

def get_connection():
    return psycopg2.connect(
    host="localhost",
    database="sportsradar",
    user="MySQL",
    password="3306"
    )
tag=st.sidebar.selectbox('# **ExploreSports**:slot_machine:',['Home','Search Data','Competitor View','Country Wise','Leader Board','Conclusion'])
if tag=='Home':     
    page_by_img_1 = """
    <style>
    [data-testid="stAppViewContainer"]{
    background: rgb(0,128,128);
    background: linear-gradient(159deg, rgba(0,128,128,1) 0%, rgba(0,153,144,1) 100%);
    [data-testid="stSidebar"]{
    background-color: #fffd80;
    background-image: linear-gradient(315deg, #7ed6df 0%, #000000 74%);;
    }
    }
    </style>
    """
    st.markdown(page_by_img_1, unsafe_allow_html=True)
    st.title(" Sport Radar-API:tennis::dart::sports_medal::trophy:")
    st.caption("## -Game Analytics: Unlocking Tennis Data with SportRadar")
    st.markdown("""### Welcome to the Game Analytics application! This tool is designed to manage, visualize, and analyze tennis competition data using the SportRadar API. Explore the world of tennis through  dynamic insights and visualizations,powered by Python, MYSQL, and StreamlitAPI:Tennis:""")
    st.markdown("### **Work Done By**::crown:_Anandhi Pandian_")
    queries = {
        "total_competitors": "SELECT COUNT(*) FROM competitor_df;",
        "countries_represented": "SELECT COUNT(DISTINCT country) FROM competitor_df;",
        "Top_5_Rank":"""select c.name as competitor_name , c.country , cr.rank,cr.points from competitor_df c join competitor_ranking_df cr on c.competitor_id = cr.competitor_id order by cr.rank_id limit 5;  """,
        "High_Competitons_played":"""SELECT c.name AS competitor_name, c.country, cr.competitions_played FROM competitor_df c JOIN competitor_ranking_df cr ON c.competitor_id = cr.competitor_id ORDER BY cr.competitions_played DESC LIMIT 10;""",
        "Top_Complex":"SELECT co.complex_name, COUNT(v.venue_id) AS venue_count FROM complexes_df co JOIN venues_df v ON co.complex_id = v.complex_id GROUP BY co.complex_name ORDER BY venue_count DESC LIMIT 5;"                    
    }
    def fetch_statistics():
        stats = {}
        connection = get_connection()
        cursor = connection.cursor()
        try:
            for key, query in queries.items():
                cursor.execute(query)
                stats[key] = cursor.fetchone()[0] 
        finally:
            cursor.close()
            connection.close()
        return stats

    
    st.title("Game Analytics: Summary Statistics")
    stats = fetch_statistics()
    st.metric("Total Number of Competitors", stats["total_competitors"])
    st.metric("Number of Countries Represented", stats["countries_represented"])
    st.metric("Top 2 Competitors", stats["Top_5_Rank"])
    st.metric("Top 2 Competitors Most Competitions Played",stats["High_Competitons_played"])
    st.metric(" Top Complexes",stats["Top_Complex"])

    
if tag=="Search Data":
    page_by_img_1 = """
    <style>
    [data-testid="stAppViewContainer"]{
    background-color: #fffd80;
    background-image: linear-gradient(315deg, #7ed6df 0%, #000000 74%);
    }
    [data-testid="stSidebar"]{
    background: rgb(46,139,87);
    background: linear-gradient(159deg, rgba(46,139,87,1) 0%, rgba(64,224,208,1) 100%);
    }
    </style>
    """
    st.markdown(page_by_img_1, unsafe_allow_html=True)


    def get_countries():
        query = "SELECT DISTINCT country FROM Competitor_df ORDER BY country ASC;"
        conn=get_connection()
        cursor=conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        countries = ["All"] + [row[0] for row in results]
        return countries

    def get_filter(search_name=None, country=None, rank_range=None, points=None):
        query = """
        SELECT c.name, c.country, cr.rank, cr.points
        FROM Competitor_df c
        JOIN Competitor_Ranking_df cr ON c.competitor_id = cr.competitor_id
        WHERE 1=1
        """
        params = []

        if search_name:
            query += " AND c.name ILIKE %s"
            params.append(f"%{search_name}%")
        

        if country and country != "All":
            query += " AND c.country = %s"
            params.append(country)
        
        if rank_range:
            query += " AND cr.rank BETWEEN %s AND %s"
            params.extend(rank_range)
        
        if points:
            query += " AND cr.points >= %s"
            params.append(points)
        
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                results = cursor.fetchall()
        
        return results

    st.title("Search and Filter Competitors")

    with st.sidebar:
        st.header("Filters")
        
        search_name = st.text_input("Search by Name", value="", placeholder="Enter competitor name...", help="Search competitors globally by name.")

        countries = get_countries()
        selected_country = st.selectbox(
            "Filter by Country", 
            countries, 
            help="Select a country to filter competitors by location."
        )

        rank_min, rank_max = st.slider(
            "Rank Range", 
            min_value=1, 
            max_value=1000, 
            value=(1, 100), 
            step=1,
            help="Select a range to filter competitors by rank."
        )
        
        points = st.number_input(
            "Points Threshold", 
            min_value=0, 
            value=0, 
            step=10,
            help="Set a minimum points threshold to filter competitors."
        )

    if st.sidebar.button("Search"):
        filters = {
            "search_name": search_name.strip() if search_name else None,
            "country": selected_country if selected_country != "All" else None,
            "rank_range": (rank_min, rank_max),
            "points": points if points > 0 else None,
        }

        competitors = get_filter(
            search_name=filters["search_name"],
            country=filters["country"],
            rank_range=filters["rank_range"],
            points=filters["points"],
        )

        if competitors:
            st.write("Filtered Results:")
            df = pd.DataFrame(competitors, columns=["Name", "Country", "Rank", "Points"])
            st.dataframe(df, use_container_width=True)
        else:
            st.write("No competitors found.")
if tag=="Competitor View":
    page_by_img_1 ="""<style>
    [data-testid="stAppViewContainer"]{
    background: rgb(46,139,87);
    background: linear-gradient(159deg, rgba(46,140,87,1) 0%, rgba(64,225,208,1) 100%);
    [data-testid="stSidebar"]{
    background: rgb(0,84,180);
    background: linear-gradient(159deg, rgba(0,84,180,1) 0%, rgba(64,225,208,1) 100%);    
    }
    }
    </style>"""
    st.markdown(page_by_img_1, unsafe_allow_html=True)

    def fetch_competitors():
        query = "SELECT competitor_id, name FROM Competitor_df;"
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                competitors = cursor.fetchall()
        return competitors

    def fetch_competitor_details(competitor_id):
        query = """
        SELECT 
            c.name, 
            c.country, 
            r.rank, 
            r.movement, 
            r.competitions_played 
        FROM Competitor_df c
        JOIN Competitor_Ranking_df r
        ON c.competitor_id = r.competitor_id
        WHERE c.competitor_id = %s;
        """
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (competitor_id,))
                details = cursor.fetchone()
        return details

    st.title("Competitor Details Viewer")

    competitors = fetch_competitors()
    competitor_options = {name: competitor_id for competitor_id, name in competitors}
    selected_competitor = st.selectbox("Select a Competitor", options=list(competitor_options.keys()))

    if selected_competitor:
        competitor_id = competitor_options[selected_competitor]
        details = fetch_competitor_details(competitor_id)
        
        if details:
            st.subheader(f"Details for {details[0]}")
            st.write(f"**Country:** {details[1]}")
            st.write(f"**Rank:** {details[2]}")
            st.write(f"**Movement:** {details[3]}")
            st.write(f"**Competitions Played:** {details[4]}")
        else:
            st.write("No details available for the selected competitor.")
if tag=="Country Wise":
    page_by_img_1 ="""<style>
    [data-testid="stAppViewContainer"]{
    background: rgb(0,84,180);
    background: linear-gradient(159deg, rgba(0,84,180,1) 0%, rgba(64,224,208,1) 100%);
    [data-testid="stSidebar"]{
    background-color: #607123;
    background-image: linear-gradient(314deg, #607123 0%, #95b54c 74%)    
    }
    }
    </style>"""
    st.markdown(page_by_img_1, unsafe_allow_html=True)

    def fetch_country_analysis():
        query = """
        SELECT 
            c.country, 
            COUNT(c.competitor_id) AS total_competitors, 
            AVG(r.points) AS average_points
        FROM Competitor_df c
        JOIN Competitor_Ranking_df r
        ON c.competitor_id = r.competitor_id
        GROUP BY c.country
        ORDER BY c.country;
        """
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                data = cursor.fetchall()
        return data

    st.title("Country-Wise Analysis")

    country_analysis = fetch_country_analysis()

    if country_analysis:
        df = pd.DataFrame(
            country_analysis, 
            columns=["Country", "Total Competitors", "Average Points"]
        )
        
        st.subheader("Country-Wise Competitor Analysis")
        st.dataframe(df, use_container_width=True)
    else:
        st.write("No data available for country-wise analysis.")

if tag=="Leader Board":
    page_by_img_1 ="""<style>
    [data-testid="stAppViewContainer"]{
    background-color: #607123;
    background-image: linear-gradient(314deg, #607123 0%, #95b54c 74%);
    
    }
    </style>"""
    st.markdown(page_by_img_1, unsafe_allow_html=True)
    def fetch_top_ranked():
        query = """
        SELECT 
            c.name, 
            c.country, 
            r.rank, 
            r.points 
        FROM Competitor_df c
        JOIN Competitor_Ranking_df r
        ON c.competitor_id = r.competitor_id
        ORDER BY r.rank ASC 
        LIMIT 10;
        """
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                data = cursor.fetchall()
        return data

    def fetch_highest_points():
        query = """
        SELECT 
            c.name, 
            c.country, 
            r.rank, 
            r.points 
        FROM Competitor_df c
        JOIN Competitor_Ranking_df r
        ON c.competitor_id = r.competitor_id
        ORDER BY r.points DESC 
        LIMIT 10;
        """
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                data = cursor.fetchall()
        return data
    st.title("Leaderboards")

    tab1, tab2 = st.tabs(["Top-Ranked Competitors", "Competitors with Highest Points"])

    with tab1:
        top_ranked = fetch_top_ranked()
        if top_ranked:
            df_top_ranked = pd.DataFrame(
                top_ranked, 
                columns=["Name", "Country", "Rank", "Points"]
            )
            df_top_ranked.index += 1  
            st.subheader("Top-Ranked Competitors")
            st.dataframe(df_top_ranked, use_container_width=True)
        else:
            st.write("No data available for top-ranked competitors.")

    with tab2:
        highest_points = fetch_highest_points()
        if highest_points:
            df_highest_points = pd.DataFrame(
                highest_points, 
                columns=["Name", "Country", "Rank", "Points"]
            )
            df_highest_points.index += 1  
            st.subheader("Competitors with Highest Points")
            st.dataframe(df_highest_points, use_container_width=True)
        else:
            st.write("No data available for competitors with the highest points.")

if tag=='Conclusion':
    st.markdown("""
    ### Conclusion

    Thank you :sparkles: for using the **Competitor Performance Dashboard**:rocket:  
    This application demonstrates how data can be leveraged to provide meaningful insights into competitor performance, rankings, and country-wise analysis. With features like detailed competitor information, leaderboards, and analytical summaries, this tool serves as a comprehensive solution for exploring performance metrics.

    Built with **MYSQL** for robust data management and **Streamlit** for an interactive user experience, this project highlights the power of modern data visualization tools in making data-driven decisions accessible to everyone.

    We hope this dashboard helps you uncover valuable insights and enhances your understanding of the data. Feel free to explore further and adapt the tool to suit your specific needs.  

     :smile: To Analyzing! 
    """)


