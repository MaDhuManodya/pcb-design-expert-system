import streamlit as st
from experta import *
from typing import Dict, List
from PIL import Image
from io import BytesIO

# ==========================
# PCB Data
# ==========================
pcbs = [
    {
        "name": "Single Sided PCBs",
        "type": "Basic",
        "applications": ["Power sensors", "Relays", "Sensors", "Electronic toys"],
        "price": "Low",
        "description": "Single sided PCBs are the most basic type, featuring only one layer of substrate and a copper layer for conductivity. These PCBs are cost-effective and suitable for low-density designs.",
        "image_url": "https://matchingelec.com/templates/yootheme/cache/d5/Single-Sided_PCB-d540cec0.jpeg"
    },
    {
        "name": "Double Sided PCBs",
        "type": "Advanced",
        "applications": ["Mobile phone systems", "Power monitoring", "Test equipment", "Amplifiers"],
        "price": "Moderate",
        "description": "Double sided PCBs feature conductive layers on both sides, allowing for increased circuit density and more complex designs. They use through-hole or surface mount technology.",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQlhOM5Jt2fft1pzNeVFnw5EhkZCSneZ2TPr39CvsQ-o6UbbdCzlzNQ3R2ffYVK8bD6yrY&usqp=CAU"
    },
    {
        "name": "Multi-Layer PCBs",
        "type": "Complex",
        "applications": ["Computers", "Medical equipment", "GPS trackers", "Mobile phones"],
        "price": "High",
        "description": "Multi-layer PCBs are designed with multiple layers of copper for high-speed circuits. They offer high design flexibility and are suitable for compact, high-performance applications.",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSCSa0LkIT0RpnopYDW7IwA_BA3ck9yKIluhw&s"
    },
    {
        "name": "Rigid PCBs",
        "type": "Rigid",
        "applications": ["GPS equipment", "X-ray systems", "Heart monitors", "Control tower instrumentation"],
        "price": "Moderate",
        "description": "Rigid PCBs are made from solid substrate material, making them strong and non-flexible. They are used in a wide range of applications where compactness and reliability are needed.",
        "image_url": "pcb;s\Rigid PCBs.jpg"
    },
    {
        "name": "Flexible PCBs",
        "type": "Flexible",
        "applications": ["OLED fabrication", "Automotive electronics", "Mobile phones", "Cameras"],
        "price": "Moderate",
        "description": "Flexible PCBs are built on flexible substrates, enabling them to be bent or folded. These are used in applications that require compactness and high flexibility, such as wearable electronics.",
        "image_url": "https://cdn.prod.website-files.com/6038a4e3907dbd2e3e7b4046/6687ac9acf79da3be4a85475_pikaso_reimagine_A-closeup-view-of-a-flexible-LED-pcb.jpg"
    },
    {
        "name": "Rigid-Flex PCBs",
        "type": "Hybrid",
        "applications": ["Aerospace", "Medical devices", "Consumer electronics"],
        "price": "High",
        "description": "Rigid-Flex PCBs combine the properties of rigid and flexible circuit boards. They are lightweight and compact, making them ideal for high-performance, space-constrained applications.",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQKzLCEluv3Xc1DtejwOQ4ej5L-zzkoPU78IA&s"
    }
]

# ==========================
# PCB Expert System
# ==========================
class PCBExpert(KnowledgeEngine):
    def __init__(self, pcb_type=None, application=None, price=None):
        super().__init__()
        self.pcb_type = pcb_type
        self.application = application
        self.price = price
        self.pcb_recommendations = []

    def calculate_match_score(self, pcb: Dict) -> Dict:
        score = 0
        match_reasons = []
        if self.pcb_type and self.pcb_type.lower() in pcb['type'].lower():
            score += 30
            match_reasons.append(f"✓ Matches {self.pcb_type} type")
        if self.application:
            for app in pcb['applications']:
                if self.application.lower() in app.lower():
                    score += 30
                    match_reasons.append(f"✓ Suitable for {app}")
                    break
        if self.price and self.price.lower() == pcb['price'].lower():
            score += 40
            match_reasons.append(f"✓ Matches {self.price} price range")
        return {
            'pcb': pcb,
            'score': score,
            'match_reasons': match_reasons
        }

    @Rule(Fact(action='recommend'))  # Make sure this is followed by an indented block
    def recommend_pcbs(self):
        scoring_results = []
        perfect_matches = []
        for pcb in pcbs:
            match_data = self.calculate_match_score(pcb)
            if match_data['score'] == 100:
                perfect_matches.append(match_data)
            elif match_data['score'] > 0:
                scoring_results.append(match_data)
        if perfect_matches:
            self.pcb_recommendations = sorted(perfect_matches, key=lambda x: x['pcb']['name'])
        else:
            self.pcb_recommendations = sorted(scoring_results, key=lambda x: x['score'], reverse=True)

# ==========================
# Format PCB Recommendations
# ==========================
def format_pcb_recommendation(recommendation: Dict) -> str:
    pcb = recommendation['pcb']
    return (
        f"### PCB Recommendation: **{pcb['name']}**\n"
        f"🔍 **Match Score:** {recommendation['score']}%\n\n"
        f"![PCB Image]({pcb['image_url']})\n\n"
        f"#### 🔧 Key Details:\n"
        f"- **Type:** {pcb['type']}\n"
        f"- **Price:** {pcb['price']}\n\n"
        f"#### 📋 Description:\n"
        f"{pcb['description']}\n\n"
        f"#### 🤔 Why This PCB?\n"
        + "".join(f"- {reason}\n" for reason in recommendation['match_reasons'])
    )


# ==========================
# Streamlit UI Code
# ==========================
st.title("🔧 PCB Expert System")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "What type of PCB are you interested in? (e.g., Basic, Advanced, Flexible, Complex)"}
    ]
    st.session_state["current_step"] = "recommend_type"

# Display chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if user_input := st.chat_input("Ask me anything about PCBs!"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    response = None
    user_input_lower = user_input.lower()

    valid_types = ["basic", "advanced", "flexible", "complex"]
    valid_price = ["low", "moderate", "high"]

    if st.session_state.get("current_step") == "recommend_type":
        if user_input_lower in valid_types:
            st.session_state["pcb_type"] = user_input.title()
            st.session_state["current_step"] = "recommend_application"
            response = "What applications are you focusing on? (e.g., Medical, Consumer electronics, Power sensors, etc.)"
        else:
            st.session_state["pcb_type"] = "Basic"  # Default to 'Basic' if no input is provided
            st.session_state["current_step"] = "recommend_application"
            response = "What applications are you focusing on? (e.g., Medical, Consumer electronics, Power sensors, etc.)"
    elif st.session_state.get("current_step") == "recommend_application":
        if user_input:
            st.session_state["application"] = user_input
        else:
            st.session_state["application"] = "Medical"  # Default to 'Medical' if no input is provided
        st.session_state["current_step"] = "recommend_price"
        response = "What price range are you looking for? (Low, Moderate, High)"
    elif st.session_state.get("current_step") == "recommend_price":
        if user_input_lower in valid_price:
            st.session_state["price"] = user_input.capitalize()
            st.session_state["current_step"] = None
            engine = PCBExpert(
                pcb_type=st.session_state.get("pcb_type"),
                application=st.session_state.get("application"),
                price=st.session_state.get("price")
            )
            engine.reset()
            engine.declare(Fact(action="recommend"))
            engine.run()
            recommendations = engine.pcb_recommendations

            if recommendations:
                response = "Here are some PCB recommendations based on your preferences:\n"
                for recommendation in recommendations:
                    response += format_pcb_recommendation(recommendation) + "\n"
            else:
                response = "Sorry, no PCBs matched your preferences. Try adjusting your inputs."
        else:
            st.session_state["price"] = "Low"  # Default to 'Low' if no input is provided
            st.session_state["current_step"] = None
            engine = PCBExpert(
                pcb_type=st.session_state.get("pcb_type"),
                application=st.session_state.get("application"),
                price=st.session_state.get("price")
            )
            engine.reset()
            engine.declare(Fact(action="recommend"))
            engine.run()
            recommendations = engine.pcb_recommendations

            if recommendations:
                response = "Here are some PCB recommendations based on your preferences:\n"
                for recommendation in recommendations:
                    response += format_pcb_recommendation(recommendation) + "\n"
            else:
                response = "Sorry, no PCBs matched your preferences. Try adjusting your inputs."

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)

