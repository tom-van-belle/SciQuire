import streamlit as st


def render_app_info():

        # Adding custom HTML and CSS for an improved hover-over tooltip
    st.markdown("""
        <style>
        .tooltip {
            position: left;
            display: inline-block;
            border-bottom: 1px dotted black; /* Style for the hoverable text */
        }

        .tooltip .tooltiptext {
            visibility: hidden;
            width: 800px; /* Width to fit content */
            background-color: #f9f9f9;
            color: #000;
            text-align: left;
            border-radius: 6px;
            padding: 15px;
            position: absolute;
            z-index: 1;
            bottom: 100;
            right: 10px; /* Positioning slightly offset */
            opacity: 0;
            transition: opacity 0.5s;
            box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.8); /* Adding some shadow for better visibility */
        }

        .tooltip:hover .tooltiptext {
            visibility: visible;
            opacity: 1;
        }
        </style>
        <div class="tooltip">ℹ️ App info
            <span class="tooltiptext">
                <strong>App info:</strong>
                <ul>
                    <li>Chat with PubMed is an AI-powered insight generator using biomedical abstracts from PubMed.</li>
                    <li>When you ask a question, the app will retrieve relevant abstracts from PubMed and generate insights based on them.</li>
                    <li>Next you can ask follow-up questions to refine the insights, i.e. you can chat with the downloaded abstracts</li>
                </ul>
            </span>
        </div>
        <div class="tooltip">🔍 Example Questions
            <span class="tooltiptext">
                <strong>Example scientific questions:</strong>
                <ul>
                    <li>How can advanced imaging techniques and biomarkers be leveraged for early diagnosis and monitoring of disease progression in neurodegenerative disorders?</li>
                    <li>What are the potential applications of stem cell technology and regenerative medicine in the treatment of neurodegenerative diseases, and what are the associated challenges?</li>
                    <li>What are the roles of gut microbiota and the gut-brain axis in the pathogenesis of type 1 and type 2 diabetes, and how can these interactions be modulated for therapeutic benefit?</li>
                    <li>What are the molecular mechanisms underlying the development of resistance to targeted cancer therapies, and how can these resistance mechanisms be overcome?</li>
                </ul>
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    st.text("")