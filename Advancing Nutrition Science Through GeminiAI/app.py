import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image

# ------------------ CONFIG ------------------
st.set_page_config(
    page_title="Advancing Nutrition Science Through Gemini AI",
    layout="wide"
)

# Main Heading
st.markdown("<h1 style='text-align: center;'>🥗 NutriAssist AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Smart Nutrition Powered by Gemini 2.5 Flash</p>", unsafe_allow_html=True)
st.markdown("---")

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ✅ FIXED MODEL - Supports vision (images + text)
model = genai.GenerativeModel("models/gemini-2.5-flash")

# ------------------ DEBUG INFO (REMOVE AFTER TESTING) ------------------
#st.sidebar.markdown("### 🔍 Debug Models (remove after)")
#try:
 #   models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
  #  st.sidebar.code(f"Available models:\n" + "\n".join(models), language="text")
#except:
 #   st.sidebar.error("Check API key")

# ------------------ SIDEBAR ------------------
# st.sidebar.title("Nutrition AI Scenarios")

# option = st.sidebar.radio(
#     "Choose what you want to do:",
#     (
#         "Dynamic Nutritional Insights",
#         "Tailored Meal Planning",
#         "Virtual Nutrition Coaching"
#     )
# )

st.markdown("""
<style>

/* Sidebar buttons */
section[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    text-align: left;
    padding: 10px 14px;
    margin-bottom: 8px;
    border-radius: 8px;
    border: 1px solid #e0e0e0;
    background-color: #f8f9fa;
    font-weight: 500;
    transition: all 0.2s ease-in-out;
}

/* Hover */
section[data-testid="stSidebar"] .stButton > button:hover {
    background-color: #1a8cff;
    color: white;
}

/* Active (primary button) */
section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    border-left: 5px solid #0033cc;
    background-color: #eeeeee;
    color: black;
    font-weight: 600;
}

            
</style>
""", unsafe_allow_html=True)






# Initialize page
if "page" not in st.session_state:
    st.session_state.page = "Dynamic Nutritional Insights"

st.sidebar.markdown("###  Nutrition AI Scenario")

pages = [
    "Dynamic Nutritional Insights",
    "Tailored Meal Planning",
    "Virtual Nutrition Coaching"
]

for page in pages:
    def set_page(p=page):
        st.session_state.page = p

    st.sidebar.button(
        page,
        key=f"btn_{page}",
        use_container_width=True,
        type="primary" if st.session_state.page == page else "secondary",
        on_click=set_page
    )

option = st.session_state.page



# ------------------ PAGE 1 ------------------
if option == "Dynamic Nutritional Insights":
    st.title("📸 Dynamic Nutritional Insights")
    st.write(
        "Upload an image of food or enter its name for detailed nutritional analysis."
    )

    col1, col2 = st.columns([2, 3])
    with col1:
        food_name = st.text_input("Food item name (optional)")
    with col2:
        uploaded_image = st.file_uploader(
            "Upload an image",
            type=["jpg", "jpeg", "png"]
        )

    image = None
    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", width=500)

    if st.button("🔬 Analyze Nutrition", type="primary"):
        if not image and not food_name:
            st.warning("Please provide food name or image!")
        else:
            with st.spinner("Analyzing nutrition using Gemini AI..."):
                prompt = f"""
You are a nutrition expert.

Analyze the food based on the following information:
Food name: {food_name if food_name else "Image only"}

Provide:
• Calories (per 100g/serving)
• Macronutrients (carbs, protein, fat in grams)
• Key micronutrients (vitamins/minerals)
• Health considerations & benefits
• Serving suggestions

**Mention clearly that values are approximate estimates.**
                """
                
                try:
                    # IMAGE + TEXT
                    if image:
                        response = model.generate_content([prompt, image])
                    else:
                        response = model.generate_content(prompt)
                    
                    st.success("✅ Analysis complete!")
                    st.subheader("🍎 Nutrition Analysis")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.info("Try: 1) New API key 2) Check models above")

# ------------------ PAGE 2 ------------------
elif option == "Tailored Meal Planning":
    st.markdown('<div class="page-container">', unsafe_allow_html=True)
    st.title("🍽️ Tailored Meal Planning")
    st.write("Provide your dietary details for a personalized 1-day plan.")

    col1, col2 = st.columns(2)
    with col1:
        diet = st.text_input("Dietary restrictions/allergies", placeholder="e.g., vegetarian, nut-free")
        activity = st.selectbox("Activity level", ["Sedentary", "Moderate", "Active", "Athlete"])
    with col2:
        condition = st.text_input("Health conditions", placeholder="e.g., diabetes, weight loss")
        taste = st.text_input("Taste preferences", placeholder="e.g., spicy, Indian")

    if st.button("🍽️ Generate Meal Plan", type="primary"):
        with st.spinner("Creating your meal plan..."):
            prompt = f"""
Create a **1-day balanced meal plan** (3 meals + 2 snacks) for:

• Diet/Restrictions: {diet or 'None'}
• Health condition: {condition or 'General health'}
• Activity level: {activity}
• Taste preferences: {taste or 'Balanced flavors'}

Requirements:
• Total ~2000 calories (adjust for activity)
• Balanced macros (45-65% carbs, 20-30% protein, 20-30% fat)
• Include portion sizes, prep time, calories per meal
• Indian/home-friendly ingredients
• Nutritional benefits per meal

Format as markdown with emojis.
            """
            
            try:
                response = model.generate_content(prompt)
                st.subheader("📋 Your Personalized Meal Plan")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error: {str(e)}")

# ------------------ PAGE 3 ------------------
elif option == "Virtual Nutrition Coaching":
    st.markdown('<div class="page-container">', unsafe_allow_html=True)
    st.title("💬 Virtual Nutrition Coaching")
    st.write("Ask any nutrition question - get expert advice!")

    question = st.text_area("Your question:", height=100, 
                           placeholder="e.g., Best protein sources for vegetarians? How much water daily?")

    if st.button("💬 Ask Coach", type="primary"):
        if question:
            with st.spinner("Coach is responding..."):
                prompt = f"""
You are a friendly, expert nutrition coach with 15+ years experience.

Answer this question clearly, practically, and encouragingly:

**Question:** {question}

Structure:
1. Direct answer
2. Practical tips/action steps
3. Common mistakes to avoid
4. Follow-up question for user

Keep it conversational and supportive.
                """
                
                try:
                    response = model.generate_content(prompt)
                    st.markdown("### 🧑‍⚕️ Coach Says:")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# ------------------ FOOTER ------------------
st.markdown("---")
st.info(
    "⚠️ **Disclaimer:** All values are AI-generated estimates. "
    "Consult a registered dietitian for personalized medical advice. "
    "Data based on general nutritional databases."
)
st.caption("Powered by Gemini 2.5 Flash • Feb 2026")
