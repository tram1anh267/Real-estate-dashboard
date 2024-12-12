import streamlit as st
import pandas as pd
import os
import warnings
import plotly.express as px

warnings.filterwarnings('ignore')

# Cấu hình giao diện Streamlit
st.set_page_config(page_title="Bất động sản!!", page_icon=":house:", layout="wide")

st.title(":house: Bất động sản")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# Upload file
fl = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    if filename.endswith(".csv") or filename.endswith(".txt"):
        df = pd.read_csv(fl, encoding="ISO-8859-1")
    else:
        df = pd.read_excel(fl)
else:
    os.chdir(r"/Users/hoangtramanh/Desktop/Streamlit")
    df = pd.read_csv("data_clean_DBA7.csv", encoding="utf-8", sep=";")

# Kiểm tra các cột cần thiết
required_columns = ["KieuNha", "Gia(ty)", "DienTich", "Quan", "Phuong", "Duong"]
for col in required_columns:
    if col not in df.columns:
        st.error(f"Cột '{col}' không tồn tại trong dữ liệu. Vui lòng kiểm tra lại.")
        st.stop()

# Tạo các bộ lọc
st.sidebar.header("Chọn bộ lọc:")

# Bộ lọc kiểu nhà
KieuNha = st.sidebar.multiselect("Chọn kiểu nhà bạn muốn:", options=df["KieuNha"].unique())
if KieuNha:
    df = df[df["KieuNha"].isin(KieuNha)]

# Bộ lọc giá
def categorize_price(price):
    if price < 0.5:
        return "Dưới 500 triệu"
    elif 0.5 <= price < 0.8:
        return "500 - 800 triệu"
    elif 0.8 <= price < 1:
        return "800 triệu - 1 tỷ"
    elif 1 <= price < 2:
        return "1 - 2 tỷ"
    elif 2 <= price < 3:
        return "2 - 3 tỷ"
    elif 3 <= price < 5:
        return "3 - 5 tỷ"
    elif 5 <= price < 7:
        return "5 - 7 tỷ"
    elif 7 <= price < 10:
        return "7 - 10 tỷ"
    elif 10 <= price < 20:
        return "10 - 20 tỷ"
    elif 20 <= price < 30:
        return "20 - 30 tỷ"
    elif 30 <= price < 40:
        return "30 - 40 tỷ"
    elif 40 <= price < 60:
        return "40 - 60 tỷ"
    else:
        return "Trên 60 tỷ"

df["KhoangGia"] = df["Gia(ty)"].apply(categorize_price)
KhoangGia = st.sidebar.multiselect("Chọn khoảng giá bạn muốn:", options=df["KhoangGia"].unique())
if KhoangGia:
    df = df[df["KhoangGia"].isin(KhoangGia)]

# Bộ lọc diện tích
def categorize_area(area):
    if area < 30:
        return "Dưới 30 m²"
    elif 30 <= area < 50:
        return "30 - 50 m²"
    elif 50 <= area < 80:
        return "50 - 80 m²"
    elif 80 <= area < 100:
        return "80 - 100 m²"
    elif 100 <= area < 150:
        return "100 - 150 m²"
    elif 150 <= area < 200:
        return "150 - 200 m²"
    elif 200 <= area < 250:
        return "200 - 250 m²"
    elif 250 <= area < 300:
        return "250 - 300 m²"
    elif 300 <= area < 500:
        return "300 - 500 m²"
    else:
        return "Trên 500 m²"

df["KhoangDienTich"] = df["DienTich"].apply(categorize_area)
DienTich = st.sidebar.multiselect("Diện tích căn nhà mơ ước ^^", options=df["KhoangDienTich"].unique())
if DienTich:
    df = df[df["KhoangDienTich"].isin(DienTich)]

# Bộ lọc quận
Quan = st.sidebar.multiselect("Quận bạn muốn:", options=df["Quan"].unique())
if Quan:
    df = df[df["Quan"].isin(Quan)]

# Bộ lọc phường
Phuong = st.sidebar.multiselect("Phường bạn muốn:", options=df["Phuong"].unique())
if Phuong:
    df = df[df["Phuong"].isin(Phuong)]

# Bộ lọc đường
Duong = st.sidebar.multiselect("Đường bạn muốn:", options=df["Duong"].unique())
if Duong:
    df = df[df["Duong"].isin(Duong)]

# Hiển thị dữ liệu sau khi lọc
st.dataframe(df)

# Vẽ biểu đồ
# Tính số lượng nhà theo kiểu
df_so_tang = df["SoTang"].value_counts().reset_index(name='count')
df_so_tang.columns = ['SoTang', 'count']

fig_so_tang = px.bar(df_so_tang, x="SoTang", y="count", title="Số lượng nhà theo số tầng")
st.plotly_chart(fig_so_tang)

# Biểu đồ phân tán với màu sắc theo kiểu nhà và kích thước theo diện tích
fig = px.scatter(df, 
                 x="Gia(ty)", 
                 y="DienTich", 
                 color="KieuNha",  # Màu sắc theo kiểu nhà
                 size="DienTich",  # Kích thước điểm theo diện tích
                 hover_name="TenDuAn", 
                 hover_data=["Quan", "Phuong", "Duong"],
                 title="Biểu đồ phân tán: Giá vs Diện tích",
                 labels={"Gia(ty)": "Giá (tỷ)", "DienTich": "Diện tích (m²)"}
                )

# Hiển thị biểu đồ
st.plotly_chart(fig)

# Biểu đồ Box Plot cho giá trị theo kiểu nhà
fig = px.box(df, 
             x="KieuNha", 
             y="Gia(ty)", 
             color="KieuNha", 
             title="Box Plot: Giá theo Kiểu nhà",
             labels={"Gia(ty)": "Giá (tỷ)", "KieuNha": "Kiểu nhà"})

# Hiển thị biểu đồ Box Plot
st.plotly_chart(fig)
# Biểu đồ phân tán 3D với Số tầng, Mặt tiền, và Đường vào
fig = px.scatter_3d(df, 
                    x="SoTang",           # Số tầng
                    y="MatTien",          # Mặt tiền
                    z="DuongVao",         # Đường vào
                    color="KieuNha",      # Màu sắc theo kiểu nhà
                    size="DienTich",      # Kích thước điểm theo diện tích
                    hover_name="TenDuAn", 
                    hover_data=["Quan", "Phuong"],
                    title="Biểu đồ phân tán 3D: Số tầng, Mặt tiền và Đường vào",
                    labels={"SoTang": "Số tầng", "MatTien": "Mặt tiền", "DuongVao": "Đường vào"})

# Hiển thị biểu đồ 3D
st.plotly_chart(fig)




import plotly.express as px
import streamlit as st

# Biểu đồ phân tán Mặt tiền
fig_mat_tien = px.scatter(df,
                          x="MatTien", 
                          y="Gia(ty)",
                          color="KieuNha", 
                          size="DienTich", 
                          hover_name="TenDuAn",
                          hover_data=["Quan", "Phuong"],
                          title="Biểu đồ phân tán: Mặt tiền vs Giá",
                          labels={"MatTien": "Mặt tiền", "Gia(ty)": "Giá (tỷ)"})
st.plotly_chart(fig_mat_tien)

# Biểu đồ phân tán Đường vào
fig_duong_vao = px.scatter(df,
                           x="DuongVao", 
                           y="Gia(ty)",
                           color="KieuNha", 
                           size="DienTich", 
                           hover_name="TenDuAn",
                           hover_data=["Quan", "Phuong"],
                           title="Biểu đồ phân tán: Đường vào vs Giá",
                           labels={"DuongVao": "Đường vào", "Gia(ty)": "Giá (tỷ)"})
st.plotly_chart(fig_duong_vao)

# Biểu đồ Pie thể hiện tỷ lệ có/không nội thất
# Giả sử trường "NoiThat" là có (1) và không có (0) nội thất
fig_pie = px.pie(df, 
                 names="NoiThat", 
                 title="Nội thất",
                 labels={"NoiThat": "Nội thất"},
                 color="NoiThat", 
                 color_discrete_map={1: "green", 0: "red"})
st.plotly_chart(fig_pie)




# Khởi tạo Geolocator
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="my_application_name")

# Hàm để tạo địa chỉ và geocode
from time import sleep

# Chuyển đổi địa chỉ thành tọa độ và chờ giữa các lần gọi
def get_coordinates(row):
    address = f"{row['Duong']}, {row['Phuong']}, {row['Quan']}, TP.HCM"
    location = geolocator.geocode(address)
    sleep(1)  # Tạm dừng 1 giây giữa các lần gọi để tránh bị giới hạn
    return location.latitude if location else None, location.longitude if location else None

# Áp dụng hàm để tạo tọa độ
df[['Latitude', 'Longitude']] = df.apply(get_coordinates, axis=1, result_type="expand")

# Vẽ bản đồ
fig = px.scatter_mapbox(df, lat='Latitude', lon='Longitude', hover_name='TenDuAn',
                        title="Dự án Bất động sản TP.HCM", zoom=10)

fig.update_layout(mapbox_style="carto-positron")  # Chọn kiểu bản đồ

# Hiển thị bản đồ
fig.show()
