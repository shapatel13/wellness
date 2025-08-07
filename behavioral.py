"""
Soul Space Wellness Assistant - A Streamlit app for yoga studio members
Provides evidence-based mental health and wellness support.

Run `pip install streamlit agno` to install dependencies.
"""

import streamlit as st
import os
import datetime
from typing import List, Optional

from agno.agent import Agent
from agno.models.groq import Groq

# Set page configuration
st.set_page_config(
    page_title="Soul Space Wellness Assistant",
    page_icon="🧘‍♀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better aesthetics
st.markdown("""
<style>
    .main {
        background-color: #f5f5f5;
    }
    .stApp {
        background-image: linear-gradient(to bottom right, #e6f7ff, #f0f8ff);
    }
    .css-18e3th9 {
        padding-top: 2rem;
    }
    .sidebar-content {
        padding: 1rem;
        background-color: rgba(255, 255, 255, 0.7);
        border-radius: 0.5rem;
    }
    h1, h2, h3 {
        color: #2C3333;
    }
    .stButton button {
        background-color: #66BFBF;
        color: white;
        font-weight: bold;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background-color: #4F9D9D;
        transform: translateY(-2px);
    }
    footer {
        font-size: 0.8rem;
        text-align: center;
        color: #666;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

class SoulSpaceWellnessBot:
    def __init__(self):
        # Initialize agent with Groq model and built-in memory
        self.agent = Agent(
            model=Groq(
                id="openai/gpt-oss-120b", 
                temperature=0.6, 
                max_tokens=2048,  # Set max tokens to 2048
                top_p=0.95,
                api_key=st.secrets["GROQ_API_KEY"]
            ),
            description="An expert clinical psychologist specializing in evidence-based wellness approaches with deep knowledge of research literature.",
            instructions=self._get_instructions(),
            add_history_to_messages=True,
            markdown=True,  # Enable markdown formatting
        )
    
    def _get_instructions(self) -> List[str]:
        """Define the behavior and guardrails for the Soul Space wellness assistant."""
        return [
            "You are Dr. Maya, a clinical psychologist with expertise in anxiety treatment, mindfulness, and evidence-based wellness approaches.",
            
            "EXPERTISE & COMMUNICATION STYLE:",
            "- Provide detailed, substantive responses (300-500 words) that demonstrate deep expertise",
            "- Balance technical knowledge with accessible language for educated non-specialists",
            "- Use a warm, thoughtful tone that feels like speaking with a knowledgeable mentor",
            "- Draw from both scientific literature and clinical experience",
            "- Address the complexity of psychological experiences rather than oversimplifying",
            "- Include specific scientific references (author, publication year, key finding) for any claims",
            "- Acknowledge nuance and individual differences in treatment responses",
            "- Provide concrete, actionable advice that is evidence-based",
            
            "CONTENT GUIDELINES:",
            "- Begin responses by validating and normalizing the person's experience",
            "- Explain the neurobiological or psychological mechanisms at work (with references)",
            "- Describe 1-2 evidence-based techniques in specific, actionable detail",
            "- Include scientific rationale for why these techniques work",
            "- Suggest how to integrate practices into daily life",
            "- Do NOT use overly formulaic structures (avoid labeled sections like 'Validation,' 'Insight,' etc.)",
            "- Do NOT explicitly promote Soul Space services - only mention if directly relevant",
            
            "REFERENCES:",
            "- Include 2-3 specific scientific references in each response",
            "- Format as (Author, Year) in the text",
            "- Reference both classic foundational research and recent studies",
            "- Draw from peer-reviewed psychology, neuroscience, and behavioral medicine literature",
            "- Be specific about findings rather than making vague claims",
            
            "GUARDRAILS:",
            "- No medical diagnoses or treatment recommendations",
            "- Redirect crisis situations to appropriate resources",
            "- Stay within wellness, mental health topics",
            "- No medication advice",
            
            "Remember to be thorough but conversational, and to ground recommendations in specific research findings with proper citations."
        ]
    
    def run(self, prompt: str):
        """Get a response from the agent using the run method."""
        return self.agent.run(prompt)

def get_wellness_suggestions():
    """Return a list of suggested wellness topics with emojis."""
    return [
        "😴 Sleep",
        "🗣️ Social anxiety",
        "📱 Digital habits",
        "💓 Stress",
        "🧠 ADHD focus",
        "🔉 Inner critic",
        "⚡ Burnout",
        "😰 Worrying",
        "🧘 Meditation",
        "🫁 Breathing",
        "❓ Normal anxiety",
        "🛟 Grounding"
    ]

def initialize_chat_history():
    """Initialize session state variables for chat history."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "suggestion_clicked" not in st.session_state:
        st.session_state.suggestion_clicked = None

def main():
    # App title and description
    st.title("🧘‍♀️ Wellness Guide | Evidence-Based Mental Health Support")
    st.markdown("""
    > Combining modern psychology, neuroscience, and mindfulness to help you navigate anxiety, stress, and digital wellbeing.
    """)
    
    # Initialize chat history
    initialize_chat_history()
    
    # Initialize bot if not already done
    if 'bot' not in st.session_state:
        st.session_state.bot = SoulSpaceWellnessBot()
        
    # Sidebar with information and controls
    with st.sidebar:
        st.image("https://img.icons8.com/dusk/64/000000/lotus.png", width=100)
        
        st.markdown("<div class='sidebar-content'>", unsafe_allow_html=True)
        st.header("About Dr. Maya")
        st.markdown("""
        I specialize in evidence-based approaches for:
        - Anxiety management
        - Sleep optimization
        - Mindfulness practices
        - Digital wellness
        - Stress resilience
        
        My approach integrates cognitive-behavioral techniques, neuroscience, and contemplative traditions—all grounded in current research.
        """)
        
        st.subheader("Session")
        if st.button("🔄 Start Fresh", key="new_session"):
            st.session_state.messages = []
            # Create a new agent instance to clear memory
            st.session_state.bot = SoulSpaceWellnessBot()
            st.rerun()
        
        st.subheader("Common Concerns")
        st.markdown("What would you like help with?")
        
        # Display suggestion buttons in groups of 3 (more compact)
        suggestions = get_wellness_suggestions()
        for i in range(0, len(suggestions), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(suggestions):
                    suggestion = suggestions[i + j]
                    if cols[j].button(suggestion, key=f"suggestion_{i+j}"):
                        st.session_state.suggestion_clicked = suggestion
                        st.rerun()
        
        st.markdown("""
        <footer>
            Evidence-based wellness support
        </footer>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Chat interface
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Handle suggestion clicks (this happens before welcome message to avoid duplicates)
    if st.session_state.suggestion_clicked is not None:
        suggestion = st.session_state.suggestion_clicked
        st.session_state.suggestion_clicked = None  # Reset after handling
        
        # Add user message to display
        with st.chat_message("user"):
            st.markdown(suggestion)
        st.session_state.messages.append({"role": "user", "content": suggestion})
        
        # Generate response with context (agent manages history internally)
        with st.chat_message("assistant"):
            with st.spinner("Researching evidence-based approaches..."):
                response = st.session_state.bot.run(suggestion)
                st.markdown(response.content)
                
        # Add assistant response to UI history
        st.session_state.messages.append({"role": "assistant", "content": response.content})
    
    # If there are no messages yet, display a welcome message
    if not st.session_state.messages:
        with st.chat_message("assistant"):
            welcome_message = """
            Welcome! I'm Dr. Maya, and I specialize in evidence-based approaches to anxiety, sleep, and mental wellbeing. 

            My background combines clinical psychology, neuroscience research, and mindfulness training to provide you with practical, science-backed strategies tailored to your specific concerns.

            What would you like support with today? Feel free to ask about anything from managing anxiety symptoms to improving sleep, building mindfulness practices, or creating healthier digital boundaries.
            """
            st.markdown(welcome_message)
            # Add this initial message to the history
            st.session_state.messages.append({"role": "assistant", "content": welcome_message})
            # Send to agent memory
            st.session_state.bot.run("Just say 'Hello' to start our conversation")
    
    # Chat input
    if prompt := st.chat_input("What would you like support with?"):
        # Add user message to display
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Generate response with context
        with st.chat_message("assistant"):
            with st.spinner("Researching evidence-based approaches..."):
                response = st.session_state.bot.run(prompt)
                st.markdown(response.content)
                
        # Add assistant response to UI history
        st.session_state.messages.append({"role": "assistant", "content": response.content})
    
    st.markdown("---")
    st.markdown(
        "*Where modern psychology meets ancient wisdom*"
    )

if __name__ == "__main__":
    main()


