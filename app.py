import streamlit as st
import pandas as pd

# -------------------------------------------------
# Customer → Health System Name mapping
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
# Helper: add Health System Name
# -------------------------------------------------
def add_health_system(df):
    if "customer" not in df.columns:
        raise ValueError("❌ 'customer' column is mandatory")
    df = df.copy()
    df.insert(
        1,
        "Health System Name",
        df["customer"].map(mapping).fillna("")
    )
    return df

# -------------------------------------------------
# Aggregated Mode
# -------------------------------------------------
def process_aggregated(files):
    dfs = [pd.read_csv(f) for f in files]
    df = pd.concat(dfs, ignore_index=True)

    numeric_cols = df.select_dtypes(include="number").columns
    final_df = df.groupby("customer", as_index=False)[numeric_cols].sum()
    final_df = add_health_system(final_df)
    return final_df

# -------------------------------------------------
# Streamlit UI
# -------------------------------------------------
st.set_page_config(page_title="DER CSV Processor", layout="wide")
st.title("📦 DER CSV Processor")

mode = st.selectbox(
    "Select processing mode",
    [
        "Aggregated (Customer level)",
        "Use this for more than 2 columns present per csv"
    ]
)

uploaded_files = st.file_uploader(
    "Upload CSV files (multiple allowed)",
    type=["csv"],
    accept_multiple_files=True
)

if uploaded_files:
    try:
        # -------------------------------------------------
        # AGGREGATED MODE
        # -------------------------------------------------
        if mode == "Aggregated (Customer level)":
            with st.spinner("Processing files..."):
                final_df = process_aggregated(uploaded_files)

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

        # -------------------------------------------------
        # MULTI-COLUMN / ROW-LEVEL MODE
        # -------------------------------------------------
        else:
            st.success("Files loaded ✅")

            for idx, file in enumerate(uploaded_files, start=1):
                st.divider()
                st.subheader(f"📄 File {idx}: {file.name}")

                df = pd.read_csv(file)
                df = add_health_system(df)

                # -------- Base Preview --------
                st.markdown("**Base Preview**")
                st.dataframe(df, use_container_width=True)

                # -------- Pivot Builder --------
                st.markdown("### 🔄 Pivot Builder")

                all_cols = df.columns.tolist()
                numeric_cols = df.select_dtypes(include="number").columns.tolist()

                rows = st.multiselect(
                    "Rows",
                    all_cols,
                    key=f"rows_{idx}"
                )
                columns = st.multiselect(
                    "Columns",
                    all_cols,
                    key=f"cols_{idx}"
                )
                values = st.multiselect(
                    "Values (numeric only)",
                    numeric_cols,
                    key=f"vals_{idx}"
                )

                agg_func = st.selectbox(
                    "Aggregation Function",
                    ["sum", "mean", "count", "min", "max"],
                    key=f"agg_{idx}"
                )

                if rows and values:
                    pivot_df = pd.pivot_table(
                        df,
                        index=rows,
                        columns=columns if columns else None,
                        values=values,
                        aggfunc=agg_func,
                        fill_value=0
                    ).reset_index()

                    st.markdown("**Pivot Preview**")
                    st.dataframe(pivot_df, use_container_width=True)

                    pivot_csv = pivot_df.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        f"⬇️ Download Pivot CSV (File {idx})",
                        pivot_csv,
                        file_name=f"pivot_{file.name}",
                        mime="text/csv"
                    )

                # -------- Download Base --------
                base_csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    f"⬇️ Download Base CSV (File {idx})",
                    base_csv,
                    file_name=file.name,
                    mime="text/csv"
                )

    except Exception as e:
        st.error("❌ Error processing files")
        st.exception(e)
