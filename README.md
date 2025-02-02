# PCB Expert System

A Streamlit-based expert system that recommends Printed Circuit Boards (PCBs) based on user inputs like type, application, and price range. Built with Python, Streamlit, and the Experta rule engine, this tool helps users find the most suitable PCB for their needs.

## Features
- **Interactive Chat Interface**: Users can input their preferences for PCB type, application, and price range.
- **PCB Recommendations**: The system recommends PCBs based on user inputs and provides detailed information about each recommendation.
- **Rule-Based Logic**: Uses the Experta library to implement rule-based decision-making for accurate recommendations.

## Dataset
The system uses a predefined dataset of PCBs with the following attributes:
- **Name**: PCB type (e.g., Single Sided, Double Sided, Multi-Layer, etc.)
- **Type**: Category (e.g., Basic, Advanced, Flexible, etc.)
- **Applications**: Common uses (e.g., Medical, Consumer electronics, etc.)
- **Price**: Cost range (Low, Moderate, High)
- **Description**: Detailed description of the PCB.
- **Image URL**: Visual representation of the PCB.

## How It Works
1. The user interacts with the chat interface to specify their preferences for PCB type, application, and price range.
2. The system uses rule-based logic to match the user's inputs with the dataset.
3. The system displays the best PCB recommendations along with detailed information and images.


   git clone https://github.com/your-username/pcb-expert-system.git
