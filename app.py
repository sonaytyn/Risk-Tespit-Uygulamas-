import streamlit as st

st.set_page_config(page_title="Sağlık ve Risk Değerlendirme Aracı", page_icon="🫀", layout="centered")

st.title("🫀 Sağlık ve Risk Değerlendirme Asistanı")
st.markdown("Gazi Üniversitesi Sağlık Bilimleri Fakültesi • Stand Etkinliği")
st.write("Lütfen bilgilerinizi girerek Vücut Kitle İndeksinizi (BKİ), Bel/Boy oranınızı ve güncel klinik risk sınıflamalarınızı öğrenin.")

with st.form("risk_form"):
    col1, col2 = st.columns(2)
    with col1:
        yas = st.number_input("Yaşınız", min_value=10, max_value=100, value=22)
        cinsiyet = st.selectbox("Cinsiyet", ["Kadın", "Erkek"])
        kilo = st.number_input("Vücut Ağırlığı (kg)", min_value=30.0, max_value=200.0, value=60.0)
    with col2:
        boy = st.number_input("Boy Uzunluğu (cm)", min_value=100.0, max_value=220.0, value=165.0)
        bel_cevresi = st.number_input("Bel Çevresi (cm)", min_value=50.0, max_value=180.0, value=75.0)
    
    submitted = st.form_submit_button("Risk Durumumu Detaylı Hesapla")

if submitted:
    # Hesaplamalar
    boy_m = boy / 100.0
    bki = kilo / (boy_m ** 2)
    bel_boy_orani = bel_cevresi / boy
    
    st.divider()
    st.subheader("📊 Değerlendirme Sonuçlarınız")
    
    # 1. BKİ Değerlendirmesi
    st.metric("Vücut Kitle İndeksi (BKİ)", f"{bki:.1f} kg/m²")
    if bki < 18.5:
        st.info("BKİ Durumu: Zayıf (Normal ağırlığa ulaşmak için beslenmenizi dengeleyebilirsiniz.)")
    elif 18.5 <= bki < 25:
        st.success("BKİ Durumu: Normal Kilolu (Harika! Sağlıklı aralıktasınız.)")
    elif 25 <= bki < 30:
        st.warning("BKİ Durumu: Hafif Şişman / Fazla Kilolu (Kardiyovasküler risk yönetimi için dikkat edilmeli.)")
    else:
        st.error("BKİ Durumu: Obezite Sınıfı (Metabolik riskler artış gösterebilir, uzman desteği önerilir.)")
        
    # 2. Bel / Boy Oranı Değerlendirmesi (Sınır değer net gösteriliyor)
    sinir_bel_boy = 0.50 if cinsiyet == "Kadın" else 0.53
    st.metric("Bel / Boy Oranı", f"{bel_boy_orani:.2f}", help=f"Sağlıklı üst sınır: {sinir_bel_boy}")
    
    if cinsiyet == "Kadın":
        st.write(f"ℹ️ **Değerlendirme Kriteri:** Kadınlar için güvenli üst sınır **0.50**'dir.")
    else:
        st.write(f"ℹ️ **Değerlendirme Kriteri:** Erkekler için güvenli üst sınır **0.53**'tür.")
        
    if bel_boy_orani < sinir_bel_boy:
        st.success(f"Bel/Boy Oranı Durumu: Sağlıklı aralıkta (Sınır olan {sinir_bel_boy}'in altındasınız, merkezi obezite riski düşük).")
    else:
        st.error(f"⚠️ Bel/Boy Oranı Durumu: Riskli sınırın üzerinde! (Hesaplanan oran: {bel_boy_orani:.2f} | Güvenli Sınır: {sinir_bel_boy}). Karın bölgesi yağlanması kardiyovasküler hastalıklar için risk faktörüdür.")

    # 3. Hocanın İstediği Bel Çevresi Risk Sınıflaması
    st.markdown("---")
    st.subheader("📌 Bel Çevresi ve Kardiyovasküler Risk Analizi")
    
    if cinsiyet == "Kadın":
        st.write(f"**Girilen Bel Çevresi:** {bel_cevresi} cm (Kadın Kriterleri)")
        if bel_cevresi >= 88:
            st.error("🚨 **Yüksek Risk Grubu:** Bel çevreniz 88 cm ve üzerindedir. Tip 2 Diyabet, hipertansiyon ve kardiyovasküler hastalık riski **yüksektir**.")
        elif bel_cevresi >= 80:
            st.warning("⚠️ **Risk Grubu:** Bel çevreniz 80 cm - 87.9 cm arasındadır. Artmış metabolik risk söz konusudur, önlem almanız önerilir.")
        else:
            st.success("✅ **Düşük Risk / Normal:** Bel çevreniz 80 cm'nin altındadır, sağlıklı aralıktasınız.")
    else: # Erkek
        st.write(f"**Girilen Bel Çevresi:** {bel_cevresi} cm (Erkek Kriterleri)")
        if bel_cevresi >= 104:
            st.error("🚨 **Yüksek Risk Grubu:** Bel çevreniz 104 cm ve üzerindedir. Tip 2 Diyabet, hipertansiyon ve kardiyovasküler hastalık riski **yüksektir**.")
        elif bel_cevresi >= 92:
            st.warning("⚠️ **Risk Grubu:** Bel çevreniz 92 cm - 103.9 cm arasındadır. Artmış metabolik risk söz konusudur, önlem almanız önerilir.")
        else:
            st.success("✅ **Düşük Risk / Normal:** Bel çevreniz 92 cm'nin altındadır, sağlıklı aralıktasınız.")

    # Özet Tavsiye
    st.markdown("---")
    st.markdown("### 💡 Uzman Tavsiyesi ve Önemli Uyarılar")
    st.markdown("""
    * **Paketli Gıda ve Şeker Tuzağı:** İşlenmiş ve paketli gıdaların gizli şeker, yüksek yağ ve yüksek kalori içeriği obezite ve diyabet riskini artırır. Etiket okuma alışkanlığı edinin!
    * **Gizli Tuz:** Tuz sadece yemek masasında eklediğimiz değildir; atıştırmalıklarda, krakerlerde ve hazır gıdalarda da gizli sodyum bulunur. 
    * **Aktivite:** Haftada en az 5 gün 30 dakika tempolu yürüyüş yaparak insülin duyarlılığınızı ve kalp sağlığınızı destekleyin.
    """)
