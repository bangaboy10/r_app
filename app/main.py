import streamlit as st
import processor
import database
import models
import utils
import tempfile

st.title("📄 Receipt & Bill Analyzer")

# Initialize database
database.init_db()

# Upload file
uploaded_file = st.file_uploader("Upload receipt (.jpg, .png, .pdf)", type=["jpg", "png", "pdf"])

if uploaded_file:
    file_ext = uploaded_file.name.split(".")[-1].lower()
    text = ""

    # Handle image
    if file_ext in ['jpg', 'png']:
        text = processor.extract_text_from_image(uploaded_file)

    # Handle PDF
    elif file_ext == 'pdf':
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name

        text = processor.extract_text_from_pdf(temp_file_path)

    # Show extracted text
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
        st.success("✅ Receipt saved to database!")
    except Exception as e:
        st.error(f"❌ Error saving receipt: {e}")

# Fetch and display all records
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
