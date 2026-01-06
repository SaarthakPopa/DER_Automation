import streamlit as st
import zipfile
import pandas as pd

# -------------------------------------------------
# Customer → Health System Name mapping
# -------------------------------------------------
# -------------------------------------------------
# Customer → Health System Name mapping
# -------------------------------------------------
mapping = {'advantasure-prod': 'Advantasure (Env 1)',
 'advantasureapollo-prod': 'Advantasure (Env 2)',
 'adventist-prod': 'Adventist Healthcare',
 'alameda-prod': 'Alameda County',
 'alo-prod': 'Alo solutions',
 'arkansashealth-prod': 'Chi St Vincent',
 'ascension-preprod': 'Ascension Health (Env 1)',
 'ascension-prod': 'Ascension Health (Env 2)',
 'atlantichealth-prod': 'Atlantic Health',
 'bannerapollo-prod': 'Banner Health',
 'bhsf-prod': 'Baptist Health South Florida',
 'bsim-prod': 'BSIM Healthcare services',
 'careabout-prod': 'CareAbout Health',
 'ccmcn-prod': 'Colorado Community Managed Care Network',
 'ccnc-prod': 'Community Care of North Carolina',
 'chessapollo-prod': 'CHESS Health Solutions',
 'childrenshealthapollo-prod': 'Children Health Alliance',
 'christianacare-prod': 'Christiana Care Health System',
 'cmhcapollo-prod': 'Central Maine Healthcare',
 'cmicsapollo-prod': 'Childrens Mercy Hospital And Clinics',
 'coa-prod': 'Colorado Access',
 'concare-prod': 'ConcertoCare',
 'connecticutchildrens-prod': "Connecticut Children's Health",
 'cshnational-new-prod': 'CSH National (Env 1)',
 'cshnational-prod': 'CSH National (Env 2)',
 'curana-prod': 'Curana Health',
 'dhmsapollo-prod': 'Dignity Health',
 'dock-cmicsapollo-prod': 'Childrens Mercy Hospital And Clinics (Nexus)',
 'dock-embrightapollo-prod': 'Embright (Nexus)',
 'dock-nemoursapollo-prod': 'Nemours Childrens Health System (Nexus)',
 'dock-risehealth-prod': 'Rise Health (Nexus)',
 'dock-tccn-prod': 'Childrens Healthcare Of Atlanta (Nexus)',
 'embrightapollo-prod': 'Embright',
 'evergreen-prod': 'Evergreen Nephrology',
 'falliance-prod': 'Franciscan Health',
 'flmedicaid-prod': 'Florida Medicaid',
 'franciscan-staging': 'Franciscan Health (staging)',
 'govcloud-prod': 'govcloud-prod',
 'gravitydemo-prod': 'Gravity',
 'impacthealth-prod': 'Impact Primary Care Network/Impact Health',
 'innohumana-prod': 'Longevity Health Plan(LHP) - HUMANA',
 'innolhp-prod': 'Longevity Health Plan(LHP) - Core)',
 'innovaetna-prod': 'Longevity Health Plan(LHP) - Aetna',
 'integration-preprod': 'internal env',
 'integris-prod': 'integris-prod',
 'intjuly-prod': 'internal account',
 'longitudegvt-prod': 'LongitudeRx (Env 1)',
 'longituderx-prod': 'LongitudeRx (Env 2)',
 'mcs-prod': 'Medical Card System',
 'mercyoneapollo-prod': 'MercyOne',
 'mercypit-prod': 'Trinity Health Pittsburgh',
 'mgm-prod': 'Mgm Resorts',
 'mhcn-prod': 'Chi Memorial',
 'nemoursapollo-prod': 'Nemours Childrens Health System',
 'novanthealth-prod':'Novant Health',
 'nwm-prod': 'Northwestern Medicine',
 'orlandoapollo-prod': 'Orlando Health',
 'pedassoc-prod': 'Pediatric Associates',
 'phlc-prod': 'Population Health Learning Center',
 'php-prod': 'P3 Health Partners',
 'pophealthcare-prod': 'Emcara / POP Health / Guidewell Mutual Holding Company',
 'prismah-prod': 'Prisma Health',
 'pswapollo-prod': 'Physicians Of Southwest Washington',
 'risehealth-prod': 'Rise Health',
 'sacramento-prod': 'Sacramento SHIE (Env 1)',
 'sacramentoshie-prod': 'Sacramento SHIE (Env 2)',
 'sentara-prod': 'Sentara Health',
 'smch-prod': 'San Mateo County Health ',
 'stewardapollo-prod': 'Steward Health Care System',
 'strivehealth-prod': 'Strive Health',
 'tccn-prod': 'Childrens Healthcare Of Atlanta',
 'thnapollo-prod': 'Cone Health',
 'trinity-prod': 'Trinity Health National',
 'uninet-prod': 'CHI Health Partners',
 'usrc-prod': 'US RenalCare',
 'walgreens-prod': 'Walgreens'}

# -------------------------------------------------
# Load ZIP
# -------------------------------------------------
def load_zip(uploaded_zip):
    dfs = []
    with zipfile.ZipFile(uploaded_zip) as z:
        for file in z.namelist():
            if file.lower().endswith(".csv"):
                with z.open(file) as f:
                    df = pd.read_csv(f)
                    df["_source_file"] = file.replace(".csv", "")
                    dfs.append(df)
    return dfs

# -------------------------------------------------
# Row-level horizontal concat (CORRECT)
# -------------------------------------------------
def process_row_level_horizontal(dfs):
    merged_df = None

    for df in dfs:
        if "customer" not in df.columns:
            raise ValueError("customer column is mandatory")

        source = df["_source_file"].iloc[0]

        # Rename all columns except customer
        rename_map = {
            col: f"{col}_{source}"
            for col in df.columns
            if col not in ["customer", "_source_file"]
        }
        df = df.rename(columns=rename_map)
        df = df.drop(columns=["_source_file"])

        if merged_df is None:
            merged_df = df
        else:
            merged_df = merged_df.merge(
                df,
                on="customer",
                how="outer"
            )

    # Add Health System Name once
    merged_df.insert(
        1,
        "Health System Name",
        merged_df["customer"].map(mapping).fillna("")
    )

    return merged_df

# -------------------------------------------------
# Streamlit UI
# -------------------------------------------------
st.set_page_config(page_title="DER ZIP Processor", layout="wide")
st.title("📦 DER ZIP Processor")

mode = st.selectbox(
    "Select processing mode",
    [
        "Aggregated (Customer level)",
        "Row-level (Horizontal concat on customer)"
    ]
)

uploaded_zip = st.file_uploader(
    "Upload ZIP file containing CSVs",
    type=["zip"]
)

if uploaded_zip:
    try:
        with st.spinner("Processing ZIP file..."):
            dfs = load_zip(uploaded_zip)

            if mode == "Aggregated (Customer level)":
                base_df = pd.concat(dfs, ignore_index=True)
                numeric_cols = base_df.select_dtypes(include="number").columns
                final_df = base_df.groupby("customer", as_index=False)[numeric_cols].sum()
                final_df.insert(
                    1,
                    "Health System Name",
                    final_df["customer"].map(mapping).fillna("")
                )
            else:
                final_df = process_row_level_horizontal(dfs)

        st.success("Processing complete ✅")

        st.subheader("📊 Preview Result")
        st.dataframe(final_df, use_container_width=True)

        csv_bytes = final_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download Final CSV",
            csv_bytes,
            file_name="final.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error("❌ Error processing ZIP")
        st.exception(e)
