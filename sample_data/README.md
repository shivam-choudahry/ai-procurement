# Sample Vendor Documents

This folder contains ready-to-use vendor proposal files for testing the Upload screen
of the RFQ AI Procurement Copilot.

## Files

| File | Vendor | Total Price | Notes |
|------|--------|-------------|-------|
| `vendor_apex_creative.txt` | Apex Creative Co. | INR 4,20,00,000 | Full-service FMCG agency; all 8 line items covered; detailed and well-structured response |
| `vendor_spark_digital.txt` | Spark Digital Agency | INR 1,75,00,000 | Digital-native agency; partial scope on Line Items 3 & 7; mixed INR/USD pricing; broadcast TVC not included |
| `vendor_brandsmith_group.txt` | Brandsmith Group | INR 3,90,00,000 | Full-service agency; Hindi-only TVC; itemized total (3,64,00,000) vs. stated total (3,90,00,000) conflict; 6-8 week claim contradicted in timeline |

## How to Use

1. Run the Streamlit app: `streamlit run app.py`
2. Navigate to the **📤 Upload** screen
3. Upload any of these `.txt` files using the file uploader
4. Click **Upload & Process** to run extraction

The system will parse the vendor proposal, run the AI extraction agent (or use demo
mode if no API key is set), and display the structured extraction results in the
**🔍 Extraction Review** screen.

## Complexity Notes

These files are intentionally realistic and messy:

- **Apex Creative** is the most complete response but includes several assumptions
  and notes a 10% media buying commission that sits outside the proposal total
- **Spark Digital** quotes some influencer fees in USD rather than INR (violates RFQ
  instructions), cannot confirm broadcast TVC production cost, and provides only 45
  days validity vs. the expected 90
- **Brandsmith Group** has a direct numerical conflict: itemized line items sum to
  INR 3,64,00,000 but the stated total is INR 3,90,00,000 (INR 26L unexplained
  "contingency reserve"); the executive summary claims "6-8 week go-live" but the
  detailed timeline shows 15-16 weeks for full TVC campaign

These complexity cases are designed to test the extraction agent's ability to detect
missing, unclear, and conflicting information.

