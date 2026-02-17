from django.shortcuts import render
from django.http import HttpResponse
import qrcode
from io import BytesIO
import base64

def home(request):
    qr_image = None
    qr_text = None

    if request.method == "POST":
        batch = request.POST.get("batch")
        group = request.POST.get("group")
        plant = request.POST.get("plant")
        description = request.POST.get("description")

        students = []

        for i in range(1, 16):
            name = request.POST.get(f"student{i}")
            enroll = request.POST.get(f"enroll{i}")

            if name and enroll:
                students.append(f"{len(students)+1}. {name} - {enroll}")

        # QR text
        qr_text = f"""
Batch Name: {batch}
Group Name: {group}

Plant Name: {plant}

Plant Description:
{description}

Total Students: {len(students)}

Students:
""" + "\n".join(students)

        # Generate fresh QR every time
        qr = qrcode.make(qr_text)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        qr_image = base64.b64encode(buffer.getvalue()).decode()

        # store text in session for download
        request.session["qr_text"] = qr_text

    return render(request, "home.html", {
        "qr": qr_image
    })


def download_qr(request):
    qr_text = request.session.get("qr_text")

    if not qr_text:
        return HttpResponse("No QR data found")

    qr = qrcode.make(qr_text)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")

    response = HttpResponse(buffer.getvalue(), content_type="image/png")
    response["Content-Disposition"] = 'attachment; filename="plant_qr.png"'
    return response