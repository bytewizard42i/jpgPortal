# 1st attempt at creating a jpg with an iperceptible QR code overlayed.  

# pip install pillow qrcode

from PIL import Image, ImageDraw, ImageOps
import qrcode

def create_fluorescent_border_with_qr(image_path, qr_data, output_path):
    # Load the image
    base_image = Image.open(image_path)

    # Create a QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_code = qr.make_image(fill_color="black", back_color="white").convert("RGBA")

    # Resize QR code to be smaller than the base image
    qr_size = min(base_image.size) // 4  # QR size is 1/4 of the smallest dimension of the image
    qr_code = qr_code.resize((qr_size, qr_size), Image.ANTIALIAS)

    # Make the QR code semi-transparent
    qr_code.putalpha(128)  # Adjust alpha to make it more or less transparent

    # Add the QR code to the base image
    base_image.paste(qr_code, (10, 10), qr_code)  # Adjust position as needed

    # Add a fluorescent green border
    border_size = 10  # Adjust thickness of the border
    border_color = "#39FF14"  # Fluorescent green
    bordered_image = ImageOps.expand(base_image, border=border_size, fill=border_color)

    # Draw squares in each corner
    draw = ImageDraw.Draw(bordered_image)
    square_size = 20  # Adjust size of the corner squares
    for x in [0, bordered_image.width - square_size]:
        for y in [0, bordered_image.height - square_size]:
            draw.rectangle([x, y, x + square_size, y + square_size], fill=border_color)

    # Save the final image
    bordered_image.save(output_path)

# Example usage
create_fluorescent_border_with_qr("path_to_your_photo.jpg", "Your QR Data Here", "output_photo.jpg")
