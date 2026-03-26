Metal Surface Defect Detection System
An AI-powered industrial quality control tool that identifies 8 different types of metallic surface defects using Deep Learning (ResNet-18) and Computer Vision.
Overview
  Manual inspection of metal surfaces is slow and prone to human error. This project automates the process by:
  Image Classification: Using a fine-tuned ResNet-18 model to categorize defects.
  Multi-Class Detection: Identifying defects like Crazing, Inclusion, Pitted surfaces, Scratches, etc.
  Real-time Dashboard: A Streamlit interface where users can upload surface images and get instant predictions.

 Project Structure
  Defect_detection.ipynb: The main notebook containing the training logic and dashboard launcher.
  app.py: The Streamlit web application script.
  best_model.pth: (Automatically downloaded on run) The trained weights for the ResNet-18 model.

 Installation & Setup
  1. Model Weights
  Because the trained model (best_model.pth) exceeds GitHub's file size limit, it is hosted on Google Drive. The notebook is pre-configured to download it automatically using its File ID.
  Note: If you are the owner, ensure the file in your Drive is set to "Anyone with the link can view."
  
  2. Configure Ngrok
  To view the web dashboard from Google Colab:
  Sign up at ngrok.com to get your free authtoken.
  In Colab, go to the Secrets tab (Key icon 🔑).
  Add a secret named NGROK_TOKEN and paste your token.
  Toggle Notebook access to ON.
  
  3. Run on Google Colab
  Upload Defect_detection.ipynb to your Google Colab.
  Run the cells in order.
  The notebook will:
  Install necessary libraries (torch, streamlit, pyngrok).
  Download the model weights from Google Drive.
  Start a secure tunnel and provide a Public URL.

 Defect Categories
The model is trained to recognize the following:
Crazing
Inclusion
Normal (No defect)
Patches
Pitted
Rolled
Rust
Scratches

 Tech Stack
PyTorch: Model architecture and inference.
Torchvision: Image preprocessing and ResNet-18 backbone.
Streamlit: Web UI/Dashboard.
Ngrok: Secure tunneling for local hosting.
