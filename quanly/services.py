from django.db.models import Q
from .models import CT_DatPhong, DatPhong, Phong, HoaDon, CT_HoaDon, DoiNha
from decimal import Decimal
from django.utils import timezone
from django.db import transaction

def check_booking_conflict(phong_id, ngaynhan, ngaytra):
    """
    Kiểm tra xem phòng đã có booking overlapping hay không.
    Trả về True nếu có conflict.
    Logic: overlap nếu (existing.ngaynhan <= ngaytra_new) and (existing.ngaytra >= ngaynhan_new)
    """
    conflicts = CT_DatPhong.objects.filter(
        phong_id=phong_id,
        datphong__trangthai__in=['CHO','XAC_NHAN','DANG_O']  # các trạng thái chiếm phòng
    ).filter(
        Q(datphong__ngaynhan__lte=ngaytra) & Q(datphong__ngaytra__gte=ngaynhan)
    )
    return conflicts.exists()

@transaction.atomic
def do_checkin(datphong_id, nhanvien_id):
    """
    Chuyển booking sang DANG_O, cập nhật trạng thái phòng sang DANG_THUE
    tạo record housekeeping 'Cần dọn' nếu cần
    """
    dp = DatPhong.objects.select_for_update().get(pk=datphong_id)
    dp.trangthai = 'DANG_O'
    dp.save()
    for ct in dp.chitiet.all():
        p = ct.phong
        p.trangthai = 'DANG_THUE'
        p.save()
    # Ghi audit log: tạo bằng model AuditLog (bạn có thể thêm)
    return True

@transaction.atomic
def do_checkout(datphong_id, nhanvien_id):
    """
    Tính tiền phòng theo ngày, tổng hợp dịch vụ (ứng dụng phải thêm dịch vụ vào HD)
    Tạo Hóa đơn tạm, cập nhật trạng thái phòng = TRONG, tạo housekeeping task
    """
    dp = DatPhong.objects.select_for_update().get(pk=datphong_id)
    # tính số đêm
    ngaynhan = dp.ngaynhan
    ngaytra = dp.ngaytra
    so_dem = (ngaytra - ngaynhan).days or 1
    # tạo hoá đơn
    hd = HoaDon.objects.create(datphong=dp, khach=dp.khach, ngaylap=timezone.now(), tongtien=0)
    tong = Decimal(0)
    for ct in dp.chitiet.all():
        giaphong = ct.giaphong * so_dem
        CT_HoaDon.objects.create(hoadon=hd, loai='PHONG', mathamchieu=ct.phong.id, mota=f'Phòng {ct.phong.sophong} x {so_dem} đêm', soluong=so_dem, dongia=ct.giaphong)
        tong += Decimal(giaphong)
        # set phòng trống & tạo task dọn
        p = ct.phong
        p.trangthai = 'TRONG'
        p.save()
        DoiNha.objects.create(phong=p, nhanvien_id=nhanvien_id, trangthai='CANDON')
    # (Giả sử các dịch vụ đã được thêm vào HD trước đó)
    hd.tongtien = tong
    hd.trangthai = 'CHUA'
    hd.save()
    # cập nhật booking
    dp.trangthai = 'HOAN_TAT'
    dp.save()
    return hd
