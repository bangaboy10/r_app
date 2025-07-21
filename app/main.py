import streamlit as st
import processor
import database
import models
import utils
import tempfile

st.title("📄 Receipt & Bill Analyzer")

# Initialize database
database.init_db()

# File uploader
uploaded_file = st.file_uploader("Upload receipt (.jpg, .png, .pdf)", type=["jpg", "png", "pdf"])

if uploaded_file:
    file_ext = uploaded_file.name.split(".")[-1].lower()
    text = ""

    # For image files
    if file_ext in ['jpg', 'png']:
        text = processor.extract_text_from_image(uploaded_file)

    # For PDF files
    elif file_ext == 'pdf':
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name

        # ✅ Pass file path (not BytesIO) to processor
        st.info(f"Processing PDF from: {temp_file_path}")
        text = processor.extract_text_from_pdf(temp_file_path)

    st.subheader("🔍 Extracted Text")
    st.text(text)

    # Parse extracted text
    parsed = processor.parse_receipt_text(text)
    st.subheader("📦 Parsed Data")
    st.write(parsed)

    # Save to DB
    try:
        receipt = models.ReceiptData(**parsed)
        database.insert_receipt(receipt)
        st.success("✅ Receipt saved!")
    except Exception as e:
        st.error(f"❌ Error saving receipt: {e}")

# Fetch and display data
data = database.get_all_receipts()
if data:
    df = utils.receipts_to_df(data)

    st.subheader("📋 All Receipts")
    st.dataframe(df)

    st.subheader("📊 Summary Statistics")
    stats = utils.aggregate_stats(df)
    st.json(stats)

    st.subheader("📈 Monthly Trend")
    trend = utils.monthly_trend(df)
    st.line_chart(trend)
else:
    st.info("No receipts uploaded yet.")
