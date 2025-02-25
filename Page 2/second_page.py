import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(
    layout='wide',
    page_title='Life Expectancy Stats',
    page_icon='📊'
)

df = pd.read_csv("cleaned_life_expectancy.csv")
df.drop(columns=['Unnamed: 0'], inplace=True, errors='ignore')

# Sidebar navigation
st.sidebar.success('Select Page Above!')

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs([ "🌍 Geographical Insights",'📈 Stats Over Years', "💡 Key Metrics & Insights", "📌 Conclusion & Key Takeaways"])

with tab1:
    st.title("🌍 Geographical Insights")
    st.write("Explore the distribution of countries and regions, and compare key factors across income groups and regions.")
    
    # Distribution of Countries by Region
    fig = px.pie(df, names="Region", hole=0.2, width=1000, height=500, 
                 title="Distribution of Countries by Region", 
                 color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig, use_container_width=True)

    # Distribution of Income Groups
    fig = px.histogram(df, x="IncomeGroup", title="Distribution of Income Groups", 
                        text_auto=True, width=1000, height=500, color="IncomeGroup", color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig, use_container_width=True)

#########################################
#########################################

with tab2:
    st.title("📊 Data Overview")
    st.write("This is the Data Overview page.")

    option = st.selectbox(
    "Select your measure",
    ("None", "Life expectancy", "Health expenditure", "Stats of CO2 emission", "Unemployment rate"))
    
    st.write("You selected:", option)
    
    if option != "None": 
        
        if option == "Life expectancy":
            min_year, max_year = 2001, 2019

            year_range = st.slider("📅 Select Year Range:", min_year, max_year, (min_year, max_year))

            filtered_df = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]

            data = filtered_df.groupby("Year")["Life Expectancy World Bank"].mean().reset_index()

        # Generate plot
            fig = px.line(data, x="Year", y="Life Expectancy World Bank", markers=True, 
                          color_discrete_sequence=["firebrick"], width=1000, height=500,  
                          title=f"Average Life Expectancy ({year_range[0]} - {year_range[1]})",
                          text="Year")
            fig.update_traces(textposition="bottom right")
            st.plotly_chart(fig, use_container_width=True)

# **Key Metrics**
            st.subheader("🔎 Key Insights")
            st.write(f"📆 **Data Range:** {year_range[0]} - {year_range[1]}")
            st.write(f"📈 **Average Life Expectancy:** {round(filtered_df['Life Expectancy World Bank'].mean(), 2)}")

            st.subheader("Visual Insight:")
            st.write("The line plot of average life expectancy across multiple years showed a general increasing trend over time. This indicates a positive correlation between the passage of years and increased life expectancy.")
######################################
            st.divider()  
            st.header("🟥 *Trends of Life Expectancy*")

            container = st.container()  # Corrected here, removed 'border=True'
            with container:
                option2 = st.radio("Select your scale", ["***None***", '***Over Countries based on Income scale***', '***Over Regions***'])                

            if option2 != "None":
                if option2 == "***Over Countries based on Income scale***":
                    
                    data = df.groupby("IncomeGroup")["Life Expectancy World Bank"].mean().reset_index()
                    fig = px.histogram(data, y="Life Expectancy World Bank", x="IncomeGroup", 
                                       labels={"Life Expectancy World Bank": "Life Expectancy"},
                                       text_auto=True, width=1000, height=500, color="IncomeGroup", 
                                       title="Effect of Income on Life Expectancy")
                    st.plotly_chart(fig, use_container_width=True)
                    st.subheader("Visual Insight:")
                    st.write("Higher-income groups generally exhibit longer life expectancies compared to lower-income groups. This difference highlights the impact of socioeconomic factors, including access to healthcare, education, and overall living conditions, on health outcomes. It underscores the importance of comprehensive strategies to reduce health disparities and improve overall population health.")
                    

                elif option2 == "***Over Regions***":
                    fig = px.scatter(df, x="Life Expectancy World Bank", y="Education Expenditure %", 
                                     color="Region", width=1200, height=600, 
                                     title="Life Expectancy by Education Expenditure in different Regions")
                    st.plotly_chart(fig, use_container_width=True)
                    st.subheader("Visual Insight:")
                    st.write("Europe and Central Asia showed higher health expenditure and life expectancy, indicating a positive correlation. In contrast, South Asia had outliers with low life expectancy despite high health spending, possibly due to inefficiencies or social factors. Long-term trends suggest that regions with rising life expectancy also increased healthcare investments, highlighting the impact of effective healthcare interventions.")
#########################################                    
        elif option == "Health expenditure":

            min_year, max_year = 2001, 2019
            year_range = st.slider("📅 Select Year Range:", min_year, max_year, (min_year, max_year))
            filtered_df = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]
            data = filtered_df.groupby('Year')['Health Expenditure %'].mean().reset_index()

        # Generate plot
            fig = px.line(data, x="Year", y="Health Expenditure %", markers=True, 
                          color_discrete_sequence=["firebrick"], width=1000, height=500,  
                          title=f"Average Health Expenditure({year_range[0]} - {year_range[1]})",
                          text="Year")
            fig.update_traces(textposition="bottom right")
            st.plotly_chart(fig, use_container_width=True)

# **Key Metrics**
            st.subheader("🔎 Key Insights")
            st.write(f"📆 **Data Range:** {year_range[0]} - {year_range[1]}")
            st.write(f"📈 **Average Life Expectancy:** {round(filtered_df['Life Expectancy World Bank'].mean(), 2)}")

            st.subheader("Visual Insight:")
            st.write("In this visualization, it is seen that health expenditure has been increasing over the years.")

            
#########################################  
            st.divider()  
            st.header("🟦 *Trends of Health expenditure*")

            container = st.container()  # Corrected here, removed 'border=True'
            with container:
                show = st.button("Show Trend")  
                hide = st.button("Hide Trend")  
                if show:
                    st.session_state["show_trend"] = True
                elif hide:
                    st.session_state["show_trend"] = False 
            if st.session_state.get("show_trend", False):
                fig = px.scatter(df, x="Life Expectancy World Bank", y="Health Expenditure %", 
                color="Region", width=1200, height=600,title="Life Expectancy by Health Expenditure in Different Regions")
                st.plotly_chart(fig, use_container_width=True)
                
                st.subheader("Visual Insight:")
                st.write("Europe and Central Asia showed higher health expenditure and life expectancy, indicating a positive correlation. In contrast, South Asia had outliers with low life expectancy despite high health spending, possibly due to inefficiencies or social factors. Long-term trends suggest that regions with rising life expectancy also increased healthcare investments, highlighting the impact of effective healthcare interventions.")
                    
########################################
        
        elif option == "Stats of CO2 emission":

            min_year, max_year = 2001, 2019
            year_range = st.slider("📅 Select Year Range:", min_year, max_year, (min_year, max_year))
            filtered_df = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]
            
            data = filtered_df.groupby(["IncomeGroup", "Year"])['CO2'].mean().reset_index()
            fig = px.line(data, x="Year", y="CO2", color="IncomeGroup", 
                          title="Trends in CO2 Emissions Over Time", line_shape="spline")
            st.plotly_chart(fig, use_container_width=True)

# **Key Metrics**
            st.subheader("🔎 Key Insights")
            st.write(f"📆 **Data Range:** {year_range[0]} - {year_range[1]}")
            st.write(f"📈 **Average Life Expectancy:** {round(filtered_df['Life Expectancy World Bank'].mean(), 2)}")

            st.subheader("Visual Insight:")
            st.write("Higher-income countries exhibit higher CO2 emissions, likely due to larger economies, higher industrialization, and greater energy consumption compared to lower-income countries.")
            
########################################
            st.divider()  
            st.header("☣ *Trends of CO2 emission")

            container = st.container()  # Corrected here, removed 'border=True'
            with container:
                option2 = st.radio("Select your scale", ["***None***", '***Over Countries based on Income scale***', '***Over Regions***'])

            if option2 != "None":
                
                if option2 == "***Over Countries based on Income scale***":
                    data = df.groupby('IncomeGroup')['CO2'].mean().reset_index()
                    fig= px.bar(data, x= "IncomeGroup", y= "CO2", color= "IncomeGroup", title= "Stats of CO2 over income groups", width= 800, height= 600)
                    st.plotly_chart(fig, use_container_width=True)
                    st.subheader("Visual Insight:")
                    st.write("This analysis reveals a disparity in CO2 emissions, with higher-income countries producing more emissions due to their larger economies, greater industrialization, and higher energy consumption. In contrast, lower-income nations have lower emissions, reflecting differences in economic and industrial activity.")
                    

                elif option2 == "***Over Regions***":
                    data= df.groupby('Region')['CO2'].mean().reset_index()
                    fig =px.bar(data, x= "Region", y= "CO2", color="Region",  title= "Stats of CO2 emission over regions", width= 1000, height= 600)
                    fig.update_layout(xaxis_title= "Regions", yaxis_title= "Average CO2", font=dict(size=12))
                    st.plotly_chart(fig, use_container_width=True)
                    st.subheader("Visual Insight:")
                    st.write("The analysis of global CO2 emissions reveals an increasing trend, providing insights into climate change. This information helps policymakers and stakeholders assess the effectiveness of emission reduction efforts and shape strategies to address global warming and ensure sustainability.")

########################################        
        
        elif option == "Unemployment rate":

            min_year, max_year = 2001, 2019
            year_range = st.slider("📅 Select Year Range:", min_year, max_year, (min_year, max_year))
            filtered_df = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]
            data= df.groupby("Year")["Unemployment"].mean().reset_index()

            fig= px.bar(data, x='Year', y="Unemployment", color="Year",  height= 600, width= 1000, 
            title= "Unemployment Rate Over the years")
            st.plotly_chart(fig, use_container_width=True)
            st.subheader("Visual Insight:")
            st.write("In this visulaization, it was observed that the trends show periods of stable unemployment rates over the years, reflecting broader economic conditions.")      
            
            
#########################################
#########################################

with tab3:
    st.title("💡 Key Metrics & Insights")
    st.write("Get a deeper look at correlations and relationships between key metrics.")

    # Correlation of Life Expectancy and Health Factors
    health_df = df[['Life Expectancy World Bank', 'Prevelance of Undernourishment', 'Health Expenditure %', 'Sanitation']]
    corr_matrix = health_df.corr()
    fig = px.imshow(corr_matrix, 
                    labels=dict(color="Correlation"),
                    x=corr_matrix.columns, 
                    y=corr_matrix.columns, 
                    color_continuous_scale="RdBu_r",  
                    title="Correlation of Life Expectancy and Health Factors", text_auto=True, width=700, height=600)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Visual Insight:")
    st.write("Analyzing the relationship between the prevalence of undernourishment and life expectancy reveals a positive correlation, indicating that undernourishment may play a significant role in reducing life expectancy. Additionally, the correlation between undernourishment prevalence and health expenditure showed values close to zero, suggesting no clear linear relationship between the two variables.")

    # Correlation of Life Expectancy and Environmental Factors
    Env_df = df[['Life Expectancy World Bank', 'CO2', 'Prevelance of Undernourishment']]
    corr_matrix = Env_df.corr()
    fig = px.imshow(corr_matrix, 
                    labels=dict(color="Correlation"),
                    x=corr_matrix.columns, 
                    y=corr_matrix.columns, 
                    color_continuous_scale="RdBu_r",  
                    text_auto=True, width=700, height=600,
                    title="Correlation of Life Expectancy and Environmental Factors")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Visual Insight:")
    st.write("It was observed that there are little correlations between life expectancy and CO2 seen in the heatmap and this may suggest that factors other than CO2 emissions play a more significant role in determining life expectancy.") 

    # Relationship Between Income Groups, Education Expenditure, and Unemployment Rates
    fig = px.scatter(df, x="Education Expenditure %", y="Unemployment", color="IncomeGroup", size="Life Expectancy World Bank", title="Relationship Between Income Groups, Education Expenditure, and Unemployment Rates")
    st.plotly_chart(fig, use_container_width=True)

#########################################
#########################################


with tab4:
    st.title("📌 Conclusion & Key Takeaways")
    st.write("Summarizing the insights from our analysis to highlight key findings and recommendations.")

    # Custom Styling
    st.markdown("""
        <style>
        .stMarkdown { font-size: 18px; }
        .stTitle { font-size: 26px !important; font-weight: bold; color: #2E86C1; }
        .stSubheader { font-size: 22px !important; font-weight: bold; color: #117A65; }
        </style>
    """, unsafe_allow_html=True)

    # Interactive Summary Selection
    st.subheader("🔍 Select a Key Finding to Explore")
    key_finding = st.selectbox(
        "Choose a category:",
        ["Life Expectancy & Health", "Environmental Factors", "Income Groups & Socioeconomic", "Overall Insights"],
        index=0
    )

    if key_finding == "Life Expectancy & Health":
        st.markdown("""
        - **📉 Negative Correlation:** Higher **Prevalence of Undernourishment** is linked to lower **Life Expectancy**, reinforcing the need for better nutrition programs.  
        - **💰 Health Spending vs. Impact:** A weaker link between **Health Expenditure %** and **Life Expectancy** suggests that **funding allocation** is more important than just increasing spending.
        """)

    elif key_finding == "Environmental Factors":
        st.markdown("""
        - 🌍 **CO2 Emissions:** Showed **little correlation** with **Life Expectancy**, indicating that other determinants such as **healthcare and sanitation** have a larger impact.  
        - 🚰 **Sanitation as a Key Factor:** Access to **clean water and sanitation** may have a significant role in improving life expectancy.
        """)

    elif key_finding == "Income Groups & Socioeconomic":
        st.markdown("""
        - **📚 Education & Employment:** Higher **Education Expenditure %** correlates with **lower Unemployment Rates**, especially in high-income regions.  
        - **💲 Economic Stability & Health:** Countries with **higher income levels** tend to experience better health outcomes, emphasizing the role of economic policies.
        """)

    else:
        st.markdown("""
        - ✅ **Prioritize nutrition and sanitation** to improve life expectancy.  
        - 📈 **Strengthen economic & education policies** for better public health outcomes.  
        - 🔍 **Further research needed** on regional disparities and policy interventions.
        """)

    # Checkbox for key insights
    st.subheader("✅ Key Insights Checklist")
    insights = [
        "Prevalence of undernourishment significantly impacts life expectancy.",
        "CO2 emissions have a weaker effect on life expectancy than expected.",
        "Health expenditure alone does not guarantee better outcomes.",
        "Education and employment policies can drive economic and health improvements.",
    ]
    for insight in insights:
        st.checkbox(insight)

    # User feedback section
    st.subheader("📢 Your Feedback")
    feedback = st.text_area("What are your thoughts on this analysis?")
    if st.button("Submit Feedback"):
        st.success("Thank you for your input! 🚀")

    # Next Steps
    st.subheader("🚀 Next Steps & Recommendations")
    st.markdown("""
    - **Government policies** should focus on improving **nutrition and sanitation**.  
    - **Economic & education initiatives** are crucial for **long-term health improvements**.  
    - **Further data exploration** is needed to understand the indirect factors influencing life expectancy.
    """)
