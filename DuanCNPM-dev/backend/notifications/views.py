from .forms import ThongBaoForm
from accounts.models import TaiKhoan
from django.shortcuts import redirect
from django.contrib import messages

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import connection

from accounts.models import TaiKhoan
from .models import ThongBao, ThongBaoNhanVien


@login_required
def notification_list(request):
    user: TaiKhoan = request.user

    # join đơn giản bằng raw SQL hoặc ORM
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT t.mathongbao, t.tieude, t.ngaygui,
                   CASE WHEN tn.ngaydoc IS NULL THEN 0 ELSE 1 END AS da_doc
            FROM THONGBAO t
            LEFT JOIN THONGBAO_NHANVIEN tn
              ON t.mathongbao = tn.mathongbao
             AND tn.mataikhoan = %s
            ORDER BY t.ngaygui DESC
        """, [user.mataikhoan])
        rows = cursor.fetchall()

    notifications = [
        {
            'mathongbao': r[0],
            'tieude': r[1],
            'ngaygui': r[2],
            'da_doc': bool(r[3]),
        }
        for r in rows
    ]

    return render(request, 'notifications/list.html', {'notifications': notifications})


@login_required
def notification_detail(request, id):
    user: TaiKhoan = request.user
    notification = get_object_or_404(ThongBao, mathongbao=id)

    # Đánh dấu đã đọc
    now = timezone.now()
    with connection.cursor() as cursor:
        cursor.execute("""
            MERGE THONGBAO_NHANVIEN AS target
            USING (SELECT %s AS mathongbao, %s AS mataikhoan) AS src
            ON (target.mathongbao = src.mathongbao AND target.mataikhoan = src.mataikhoan)
            WHEN MATCHED THEN
                UPDATE SET ngaydoc = COALESCE(target.ngaydoc, src.mathongbao * 0 + ?)
            WHEN NOT MATCHED THEN
                INSERT (mathongbao, mataikhoan, ngaydoc)
                VALUES (src.mathongbao, src.mataikhoan, ?);
        """.replace('?', '%s'), [id, user.mataikhoan, now, now])

    return render(request, 'notifications/detail.html', {'notification': notification})

@login_required
def notification_create(request):
    user: TaiKhoan = request.user
    if user.vaitro != "QUANLY":
        return HttpResponse("Chỉ quản lý mới được gửi thông báo.")

    if request.method == "POST":
        form = ThongBaoForm(request.POST)
        if form.is_valid():
            tb = form.save(commit=False)
            tb.nguoigui = user.mataikhoan
            tb.save()
            messages.success(request, "Đã gửi thông báo.")
            return redirect('notifications:list')
    else:
        form = ThongBaoForm()

    return render(request, 'notifications/create.html', {'form': form})
