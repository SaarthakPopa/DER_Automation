import streamlit as st
import zipfile
import pandas as pd
import io

# -------------------------------------------------
# Customer → Health System Name mapping (FINAL)
# -------------------------------------------------
mapping = {
    "adventist-prod": "Adventist Healthcare",
    "alo-prod": "Alo solutions",
    "ascension-preprod": "Ascension Health (Env 1)",
    "ascension-prod": "Ascension Health (Env 2)",
    "atlantichealth-prod": "Atlantic Health",
    "bannerapollo-prod": "Banner Health",
    "bhsf-prod": "Baptist Health South Florida",
    "careabout-prod": "CareAbout Health",
    "ccmcn-prod": "Colorado Community Managed Care Network",
    "ccnc-prod": "Community Care of North Carolina",
    "chessapollo-prod": "CHESS Health Solutions",
    "childrenshealthapollo-prod": "Children Health Alliance",
    "christianacare-prod": "Christiana Care Health System",
    "cmhcapollo-prod": "Central Maine Healthcare",
    "cmicsapollo-prod": "Childrens Mercy Hospital And Clinics",
    "coa-prod": "Colorado Access",
    "concare-prod": "ConcertoCare",
    "connecticutchildrens-prod": "Connecticut Children’s Health",
    "cshnational-prod": "CSH National (Env 2)",
    "curana-prod": "Curana Health",
    "dhmsapollo-prod": "Dignity Health",
    "dock-cmicsapollo-prod": "Childrens Mercy Hospital And Clinics (Nexus)",
    "dock-embrightapollo-prod": "Embright (Nexus)",
    "dock-nemoursapollo-prod": "Nemours Childrens Health System (Nexus)",
    "dock-risehealth-prod": "Rise Health (Nexus)",
    "dock-tccn-prod": "Childrens Healthcare Of Atlanta (Nexus)",
    "evergreen-prod": "Evergreen Nephrology",
    "falliance-prod": "Franciscan Health",
    "flmedicaid-prod": "Florida Medicaid",
    "impacthealth-prod": "Impact Primary Care Network/Impact Health",
    "innolhp-prod": "Longevity Health Plan(LHP) - Core)",
    "innovaetna-prod": "Longevity Health Plan(LHP) - Aetna",
    "mercyoneapollo-prod": "MercyOne",
    "mercypit-prod": "Trinity Health Pittsburgh",
    "mgm-prod": "Mgm Resorts",
    "mhcn-prod": "Chi Memorial",
    "nwm-prod": "Northwestern Medicine",
    "orlandoapollo-prod": "Orlando Health",
    "pedassoc-prod": "Pediatric Associates",
    "phlc-prod": "Population Health Learning Center",
    "php-prod": "P3 Health Partners",
    "prismah-prod": "Prisma Health",
    "pswapollo-prod": "Physicians Of Southwest Washington",
    "sacramentoshie-prod": "Sacramento SHIE (Env 2)",
    "sentara-prod": "Sentara Health",
    "smch-prod": "San Mateo County Health",
    "strivehealth-prod": "Strive Health",
    "thnapollo-prod": "Cone Health",
    "trinity-prod": "Trinity Health National",
    "usrc-prod": "US RenalCare",
    "advantasureapollo-prod": "Advantasure (Env 2)",
    "alameda-prod": "Alameda County",
    "bsim-prod": "BSIM Healthcare services",
    "cshnational-new-prod": "CSH National (Env 1)",
    "dock-olyortho-prod": "Oly Ortho (Nexus)",
    "franciscan-staging": "Franciscan Health (staging)",
    "govcloud-prod": "govcloud-prod",
    "innohumana-prod": "Longevity Health Plan(LHP) - HUMANA",
    "integration-preprod": "internal env",
    "longitudegvt-prod": "LongitudeRx (Env 1)",
    "longituderx-prod": "LongitudeRx (Env 2)",
    "mcs-prod": "Medical Card System",
    "stewardapollo-prod": "Steward Health Care System",
    "walgreens-prod": "Walgreens"
}

# -------------------------------------------------
# Core processing function (UNCHANGED logic)
# -------------------------------------------------
def process_zip(uploaded_zip):
    dfs = []

    with zipfile.ZipFile(uploaded_zip) as z:
        for file in z.namelist():
            if file.lower().endswith(".csv"):
                with z.open(file) as f:
                    dfs.append(pd.read_csv(f))

    combined_df = pd.concat(dfs, ignore_index=True)

    metric_cols = combined_df.columns.drop("customer")

    final_df = (
        combined_df
        .groupby("customer", as_index=False)[metric_cols]
        .sum()
    )

    final_df.insert(
        1,
        "Health System Name",
        final_df["customer"].map(mapping).fillna("")
    )

    return final_df

# -------------------------------------------------
# Streamlit UI
# -------------------------------------------------
st.set_page_config(page_title="DER ZIP Processor", layout="wide")

st.title("📦 DER ZIP → Final Aggregated Table")
st.write("Upload a **DER zip file** containing CSVs to generate the final consolidated table.")

uploaded_zip = st.file_uploader(
    "Drag & drop or upload ZIP file",
    type=["zip"]
)

if uploaded_zip:
    try:
        with st.spinner("Processing ZIP file..."):
            final_df = process_zip(uploaded_zip)

        st.success("Processing complete ✅")

        st.subheader("📊 Preview Result")
        st.dataframe(final_df, use_container_width=True)

        # Convert to CSV for download
        csv_bytes = final_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="⬇️ Download Final CSV",
            data=csv_bytes,
            file_name="final.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error("❌ Error processing ZIP file")
        st.exception(e)
