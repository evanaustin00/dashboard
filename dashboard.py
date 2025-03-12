import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Konfigurasi halamans
st.set_page_config(
    page_title="Analisis Data Penyewaan Sepeda",
    page_icon=":bike:",
    layout="wide",
)

url_hour = 'https://raw.githubusercontent.com/evanaustin00/bike-sharing-dataset/refs/heads/main/hour.csv'
url_day = 'https://raw.githubusercontent.com/evanaustin00/bike-sharing-dataset/refs/heads/main/day.csv'
hour_df = pd.read_csv(url_hour)
day_df = pd.read_csv(url_day)



# Ubah tipe data 'dteday' menjadi datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Tambahkan Judul dan Deskripsi
st.title("Analisis Data Penyewaan Sepeda")
st.markdown("""
Dashboard ini menyajikan analisis data penyewaan sepeda berdasarkan dataset `day` dan `hour`.
Gunakan filter di sidebar untuk melakukan eksplorasi data lebih lanjut.
""")

# Sidebar untuk Filter Data
with st.sidebar:
    st.header("Filter Data")
    selected_months = st.multiselect(
        "Pilih Bulan:",
        options=day_df['mnth'].unique(),
        default=day_df['mnth'].unique(),
    )

    # Filter Data Berdasarkan Bulan yang Dipilih
    filtered_day_df = day_df[day_df['mnth'].isin(selected_months)]

# Tampilan Data yang telah difilter
st.subheader("Data yang Difilter Berdasarkan Bulan")
st.dataframe(filtered_day_df)

# Kolom Layout untuk Visualisasi
col1, col2 = st.columns(2)

# Pertanyaan 1: Pengaruh Kondisi Cuaca Terhadap Jumlah Pengguna Terdaftar
with col1:
    st.header("Pengaruh Kondisi Cuaca Terhadap Jumlah Pengguna Terdaftar")

    # Data Preparation untuk Pertanyaan 1
    workingday_jan_2011 = day_df[
        (day_df['mnth'] == 1) & (day_df['yr'] == 0) & (day_df['workingday'] == 1)
    ]
    aggregated_weather = workingday_jan_2011.groupby('weathersit')['registered'].sum().reset_index()

    # Visualisasi Data untuk Pertanyaan 1
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.barplot(x='weathersit', y='registered', data=aggregated_weather, palette='viridis', ax=ax1)
    ax1.set_title('Total Jumlah Pengguna Terdaftar Berdasarkan Kondisi Cuaca di Januari 2011 (Hari Kerja)')
    ax1.set_xlabel('Kondisi Cuaca (1: Cerah, 2: Kabut, 3: Hujan/Salju)')
    ax1.set_ylabel('Total Jumlah Pengguna Terdaftar')
    ax1.set_xticks(range(3))
    ax1.set_xticklabels(['Cerah', 'Kabut', 'Hujan/Salju'])
    ax1.grid(axis='y', linestyle='--')
    st.pyplot(fig1)

# Pertanyaan 2: Hubungan Antara Kecepatan Angin dan Jumlah Total Pengguna
with col2:
    st.header("Hubungan Antara Kecepatan Angin dan Jumlah Total Pengguna")

    # Data Preparation untuk Pertanyaan 2
    weekend_first_week_jan_2011 = hour_df[
        (hour_df['dteday'] <= '2011-01-07') & (hour_df['weekday'].isin([0, 6]))
    ]
    aggregated_windspeed = weekend_first_week_jan_2011.groupby('windspeed')['cnt'].sum().reset_index()

    # Visualisasi Data untuk Pertanyaan 2
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='windspeed', y='cnt', data=aggregated_windspeed, alpha=0.7, color='teal', ax=ax2)
    ax2.set_title('Hubungan Antara Kecepatan Angin dan Total Jumlah Pengguna di Akhir Pekan, Minggu Pertama Januari 2011')
    ax2.set_xlabel('Kecepatan Angin')
    ax2.set_ylabel('Total Jumlah Pengguna')
    ax2.grid(True, linestyle='--')
    st.pyplot(fig2)

# Kesimpulan
st.subheader("Kesimpulan")
st.markdown("""
- Kondisi cuaca memiliki pengaruh signifikan terhadap total jumlah pengguna terdaftar pada hari kerja selama bulan Januari 2011. Cuaca yang lebih baik (kondisi 1: Cerah) cenderung memiliki total jumlah pengguna terdaftar yang lebih tinggi dibandingkan dengan cuaca yang kurang baik.
- Tidak ada hubungan yang kuat antara kecepatan angin dan total jumlah pengguna pada akhir pekan selama minggu pertama Januari 2011.
- Tren penggunaan sepeda bervariasi berdasarkan musim.
""")

# Tambahkan Footer
st.markdown("---")
st.markdown("Dibuat dengan Streamlit")
