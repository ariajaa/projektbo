import streamlit as st
from chatbot import ask_gemini
import random

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="FSA Logistics AI",
    page_icon="📦",
    layout="wide"
)

# =========================
# DATABASE SEMENTARA
# =========================
if "data_resi" not in st.session_state:

    st.session_state.data_resi = {

        "FSA001": {
            "status": "Dalam Pengiriman",
            "lokasi": "Bekasi",
            "estimasi": "2 Hari Lagi",
            "pengirim": "Andi",
            "penerima": "Budi",

            "tracking": [
                "Paket diterima di Bandung",
                "Paket tiba di Gudang Bekasi",
                "Paket sedang menuju Jakarta"
            ]
        },

        "FSA002": {
            "status": "Sudah Sampai",
            "lokasi": "Jakarta",
            "estimasi": "Paket Diterima",
            "pengirim": "Sinta",
            "penerima": "Rina",

            "tracking": [
                "Paket diterima di Surabaya",
                "Paket dikirim ke Jakarta",
                "Paket diterima oleh penerima"
            ]
        },

        "FSA003": {
            "status": "Tertunda",
            "lokasi": "Gudang Bekasi",
            "estimasi": "Menunggu Pengiriman",
            "pengirim": "Doni",
            "penerima": "Agus",

            "tracking": [
                "Paket diterima di Bekasi",
                "Cuaca buruk menyebabkan keterlambatan"
            ]
        }
    }

# =========================
# RIWAYAT PENGIRIMAN
# =========================
if "riwayat_pengiriman" not in st.session_state:
    st.session_state.riwayat_pengiriman = []

# =========================
# HITUNG STATUS
# =========================
diproses = 0
terkirim = 0
tertunda = 0

for data in st.session_state.data_resi.values():

    if data["status"] == "Dalam Pengiriman":
        diproses += 1

    elif data["status"] == "Sudah Sampai":
        terkirim += 1

    elif data["status"] == "Tertunda":
        tertunda += 1

# =========================
# SIDEBAR
# =========================
menu = st.sidebar.selectbox(
    "📋 Menu",
    [
        "Dashboard",
        "Tracking Resi",
        "Pengiriman Barang",
        "Update Status Paket",
        "Riwayat Pengiriman",
        "Chatbot AI"
    ]
)

# =========================
# HEADER
# =========================
st.title("📦 FSA Logistics AI")
st.caption("Sistem Logistik dan Pengiriman Barang Berbasis AI")

# =========================
# DASHBOARD
# =========================
if menu == "Dashboard":

    st.subheader("Dashboard Pengiriman")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Paket",
        len(st.session_state.data_resi)
    )

    col2.metric(
        "Diproses",
        diproses
    )

    col3.metric(
        "Terkirim",
        terkirim
    )

    col4.metric(
        "Tertunda",
        tertunda
    )

    st.divider()

    # PAKET DIPROSES
    st.write("## 🚚 Paket Diproses")

    ada_data = False

    for resi, data in st.session_state.data_resi.items():

        if data["status"] == "Dalam Pengiriman":

            ada_data = True

            st.write(f"📦 Resi : {resi}")
            st.write(f"👤 Pengirim : {data['pengirim']}")
            st.write(f"👥 Penerima : {data['penerima']}")
            st.write(f"📍 Lokasi : {data['lokasi']}")

            st.divider()

    if not ada_data:
        st.info("Tidak ada paket diproses")

    # PAKET TERKIRIM
    st.write("## ✅ Paket Terkirim")

    ada_data = False

    for resi, data in st.session_state.data_resi.items():

        if data["status"] == "Sudah Sampai":

            ada_data = True

            st.write(f"📦 Resi : {resi}")
            st.write(f"👤 Pengirim : {data['pengirim']}")
            st.write(f"👥 Penerima : {data['penerima']}")
            st.write(f"📍 Lokasi : {data['lokasi']}")

            st.divider()

    if not ada_data:
        st.info("Tidak ada paket terkirim")

    # PAKET TERTUNDA
    st.write("## ⏳ Paket Tertunda")

    ada_data = False

    for resi, data in st.session_state.data_resi.items():

        if data["status"] == "Tertunda":

            ada_data = True

            st.write(f"📦 Resi : {resi}")
            st.write(f"👤 Pengirim : {data['pengirim']}")
            st.write(f"👥 Penerima : {data['penerima']}")
            st.write(f"📍 Lokasi : {data['lokasi']}")

            st.divider()

    if not ada_data:
        st.info("Tidak ada paket tertunda")

# =========================
# TRACKING RESI
# =========================
elif menu == "Tracking Resi":

    st.subheader("📍 Tracking Resi")

    resi = st.text_input(
        "Masukkan Nomor Resi"
    )

    if st.button("Lacak Paket"):

        if resi:

            if resi in st.session_state.data_resi:

                hasil = st.session_state.data_resi[resi]

                st.success("Resi ditemukan")

                st.write("### Detail Pengiriman")

                st.write(f"📦 Status : {hasil['status']}")
                st.write(f"📍 Lokasi Saat Ini : {hasil['lokasi']}")
                st.write(f"🕒 Estimasi : {hasil['estimasi']}")
                st.write(f"👤 Pengirim : {hasil['pengirim']}")
                st.write(f"👥 Penerima : {hasil['penerima']}")

                st.divider()

                st.write("### 🚚 Riwayat Perjalanan Paket")

                for item in hasil["tracking"]:

                    st.write(f"✅ {item}")

            else:
                st.error("Nomor resi tidak ditemukan")

        else:
            st.warning("Masukkan nomor resi terlebih dahulu")

# =========================
# PENGIRIMAN BARANG
# =========================
elif menu == "Pengiriman Barang":

    st.subheader("📦 Form Pengiriman Barang")

    with st.form("form_pengiriman"):

        pengirim = st.text_input("Nama Pengirim")

        penerima = st.text_input("Nama Penerima")

        kota_asal = st.text_input("Kota Asal")

        kota_tujuan = st.text_input("Kota Tujuan")

        alamat = st.text_area("Alamat Tujuan")

        barang = st.selectbox(
            "Jenis Barang",
            [
                "Elektronik",
                "Pakaian",
                "Makanan",
                "Dokumen",
                "Lainnya"
            ]
        )

        berat = st.number_input(
            "Berat Barang (Kg)",
            min_value=1
        )

        submit = st.form_submit_button(
            "Kirim Barang"
        )

        if submit:

            nomor_resi = "FSA" + str(
                random.randint(100, 999)
            )

            st.session_state.data_resi[nomor_resi] = {

                "status": "Dalam Pengiriman",

                "lokasi": kota_asal,

                "estimasi": "3 Hari Lagi",

                "pengirim": pengirim,

                "penerima": penerima,

                "tracking": [
                    f"Paket diterima di {kota_asal}",
                    f"Paket sedang dikirim menuju {kota_tujuan}"
                ]
            }

            st.session_state.riwayat_pengiriman.append({

                "resi": nomor_resi,

                "pengirim": pengirim,

                "penerima": penerima,

                "barang": barang
            })

            st.success(
                "Pengiriman berhasil dibuat"
            )

            st.info(
                f"Nomor Resi Anda : {nomor_resi}"
            )

# =========================
# UPDATE STATUS PAKET
# =========================
elif menu == "Update Status Paket":

    st.subheader("🛠 Update Status Paket")

    daftar_resi = list(
        st.session_state.data_resi.keys()
    )

    pilih_resi = st.selectbox(
        "Pilih Nomor Resi",
        daftar_resi
    )

    status_baru = st.selectbox(
        "Update Status",
        [
            "Dalam Pengiriman",
            "Sudah Sampai",
            "Tertunda"
        ]
    )

    lokasi_baru = st.text_input(
        "Lokasi Paket Saat Ini"
    )

    if st.button("Update Paket"):

        st.session_state.data_resi[pilih_resi][
            "status"
        ] = status_baru

        st.session_state.data_resi[pilih_resi][
            "lokasi"
        ] = lokasi_baru

        st.session_state.data_resi[pilih_resi][
            "tracking"
        ].append(
            f"Status diperbarui menjadi {status_baru} di {lokasi_baru}"
        )

        st.success(
            "Status paket berhasil diperbarui"
        )

# =========================
# RIWAYAT PENGIRIMAN
# =========================
elif menu == "Riwayat Pengiriman":

    st.subheader("📜 Riwayat Pengiriman")

    if st.session_state.riwayat_pengiriman:

        for item in st.session_state.riwayat_pengiriman:

            st.write(f"📦 Resi : {item['resi']}")
            st.write(f"👤 Pengirim : {item['pengirim']}")
            st.write(f"👥 Penerima : {item['penerima']}")
            st.write(f"🛍 Barang : {item['barang']}")

            st.divider()

    else:
        st.info("Belum ada riwayat pengiriman")

# =========================
# CHATBOT AI
# =========================
elif menu == "Chatbot AI":

    st.subheader("🤖 Chatbot Customer Service AI")

    st.write(
        "Tanyakan seputar pengiriman, estimasi barang, dan layanan logistik."
    )

    prompt = st.text_input(
        "Masukkan Pertanyaan"
    )

    if st.button("Kirim Pertanyaan"):

        if prompt:

            with st.spinner(
                "AI sedang menjawab..."
            ):

                jawaban = ask_gemini(prompt)

                st.success(jawaban)

        else:
            st.warning(
                "Masukkan pertanyaan terlebih dahulu"
            )
