import streamlit as st
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from PIL import Image
import io

# CONFIGURACIÓN
subscription_key = st.secrets["AZURE_VISION_KEY"]
endpoint = st.secrets["AZURE_VISION_ENDPOINT"]

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

st.title("🧠 Análisis de imágenes con Azure Computer Vision")
uploaded_file = st.file_uploader("Sube una imagen", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='Imagen subida', use_column_width=True)

    # Convertir imagen a bytes
    image_bytes = uploaded_file.read()

    # Llamada a Azure
    analysis = computervision_client.analyze_image_in_stream(
        io.BytesIO(image_bytes),
        visual_features=["Description", "Tags"]
    )

    # Mostrar descripción
    if analysis.description and analysis.description.captions:
        st.subheader("📝 Descripción:")
        for caption in analysis.description.captions:
            st.write(f"- {caption.text} (Confianza: {caption.confidence:.2f})")

    # Mostrar tags
    if analysis.tags:
        st.subheader("🏷️ Etiquetas:")
        st
