import streamlit as st
import processor
import database
import models
import utils
from io import BytesIO

st.title("📄 Receipt & Bill Analyzer")
database.init_db()

uploaded_file = st.file_uploader("Upload receipt (.jpg, .png, .pdf)", type=["jpg", "png", "pdf"])

if uploaded_file:
    file_ext = uploaded_file.name.split(".")[-1].lower()
    text = ""
    if file_ext in ['jpg', 'png']:
        text = processor.extract_text_from_image(uploaded_file)
    elif file_ext == 'pdf':
        with BytesIO(uploaded_file.read()) as f:
            text = processor.extract_text_from_pdf(f)

    parsed = processor.parse_receipt_text(text)
    st.write("Parsed Data:", parsed)

    try:
        receipt = models.ReceiptData(**parsed)
        database.insert_receipt(receipt)
        st.success("✅ Receipt saved!")
    except Exception as e:
        st.error(f"❌ Error: {e}")

# Show all data
data = database.get_all_receipts()
if data:
    df = utils.receipts_to_df(data)
    st.subheader("📋 All Receipts")
    st.dataframe(df)

    stats = utils.aggregate_stats(df)
    st.subheader("📊 Summary")
    st.json(stats)

    st.subheader("📈 Monthly Trends")
    trend = utils.monthly_trend(df)
    st.line_chart(trend)
