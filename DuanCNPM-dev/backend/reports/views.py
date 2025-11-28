from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection
from datetime import date


@login_required
def revenue_report(request):
    data = []
    tu_ngay = den_ngay = None

    if request.method == 'POST':
        tu_ngay = request.POST.get('tu_ngay')
        den_ngay = request.POST.get('den_ngay')
        if tu_ngay and den_ngay:
            with connection.cursor() as cursor:
                cursor.callproc('sp_BaoCaoDoanhThuKhoangNgay', [tu_ngay, den_ngay])
                rows = cursor.fetchall()
            data = [
                {
                    'Ngay': r[0],
                    'DoanhThuPhong': r[1],
                    'DoanhThuDichVu': r[2],
                    'TongDoanhThu': r[3],
                }
                for r in rows
            ]

    return render(request, 'reports/revenue_report.html', {'data': data})


@login_required
def customer_report(request):
    data = []
    if request.method == 'POST':
        tu_ngay = request.POST.get('tu_ngay')
        den_ngay = request.POST.get('den_ngay')
        if tu_ngay and den_ngay:
            with connection.cursor() as cursor:
                cursor.callproc('sp_TraCuuKhachKhoangNgay', [tu_ngay, den_ngay])
                rows = cursor.fetchall()
            # mapping theo SELECT trong sp_TraCuuKhachKhoangNgay
            for r in rows:
                data.append({
                    'madatphong': r[0],
                    'makhachhang': r[1],
                    'ten_khach': r[2],
                    'loaikhach': r[3],
                    'maphong': r[4],
                    'loaiphong': r[5],
                    'ngaynhan': r[6],
                    'ngaytra': r[7],
                    'tongtien_phong': r[8],
                    'madichvu': r[9],
                    'tendichvu': r[10],
                    'soluong': r[11],
                    'tien_dichvu': r[12],
                })

    return render(request, 'reports/customer_report.html', {'data': data})
