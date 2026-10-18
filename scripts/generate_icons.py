import math
import os
from PIL import Image, ImageDraw, ImageFilter

def create_gradient_bg(size, start_color=(79, 70, 229), mid_color=(124, 58, 237), end_color=(236, 72, 153)):
    """Creates a smooth diagonal linear gradient."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    for y in range(size):
        for x in range(size):
            t = (x + y) / (2.0 * size)
            if t < 0.5:
                sub_t = t * 2.0
                r = int(start_color[0] + (mid_color[0] - start_color[0]) * sub_t)
                g = int(start_color[1] + (mid_color[1] - start_color[1]) * sub_t)
                b = int(start_color[2] + (mid_color[2] - start_color[2]) * sub_t)
            else:
                sub_t = (t - 0.5) * 2.0
                r = int(mid_color[0] + (end_color[0] - mid_color[0]) * sub_t)
                g = int(mid_color[1] + (end_color[1] - mid_color[1]) * sub_t)
                b = int(mid_color[2] + (end_color[2] - mid_color[2]) * sub_t)
            img.putpixel((x, y), (r, g, b, 255))
    return img

def draw_rounded_finder(draw, x, y, size, color=(255, 255, 255, 255), radius=None):
    if radius is None:
        radius = size * 0.22
    # Outer box
    draw.rounded_rectangle([x, y, x + size, y + size], radius=radius, fill=color)
    # Inner cutout (using clear or background color simulation; here we draw inner gap then inner dot)
    gap = size * 0.22
    dot_size = size - 2 * gap
    draw.rounded_rectangle([x + gap, y + gap, x + size - gap, y + size - gap], radius=radius * 0.6, fill=(0, 0, 0, 0))
    # Center dot
    center_inset = size * 0.35
    draw.rounded_rectangle([x + center_inset, y + center_inset, x + size - center_inset, y + size - center_inset], 
                           radius=radius * 0.5, fill=color)

def generate_qr_icon(size=512, is_round=False, is_foreground_only=False):
    # Oversample 2x for anti-aliasing
    scale = 2
    actual_size = size * scale
    
    if is_foreground_only:
        base = Image.new("RGBA", (actual_size, actual_size), (0, 0, 0, 0))
    else:
        # Full icon with gradient background
        gradient = create_gradient_bg(actual_size)
        base = Image.new("RGBA", (actual_size, actual_size), (0, 0, 0, 0))
        mask = Image.new("L", (actual_size, actual_size), 0)
        mask_draw = ImageDraw.Draw(mask)
        
        margin = int(actual_size * 0.04)
        if is_round:
            mask_draw.ellipse([margin, margin, actual_size - margin, actual_size - margin], fill=255)
        else:
            radius = int(actual_size * 0.22)
            mask_draw.rounded_rectangle([margin, margin, actual_size - margin, actual_size - margin], radius=radius, fill=255)
        
        base.paste(gradient, (0, 0), mask)
        
        # Add subtle glass/inner shadow border
        border_overlay = Image.new("RGBA", (actual_size, actual_size), (0, 0, 0, 0))
        border_draw = ImageDraw.Draw(border_overlay)
        border_width = int(actual_size * 0.015)
        if is_round:
            border_draw.ellipse([margin, margin, actual_size - margin, actual_size - margin], 
                                outline=(255, 255, 255, 60), width=border_width)
        else:
            border_draw.rounded_rectangle([margin, margin, actual_size - margin, actual_size - margin], 
                                          radius=radius, outline=(255, 255, 255, 60), width=border_width)
        base = Image.alpha_composite(base, border_overlay)

    # Now draw the stylized QR code
    qr_layer = Image.new("RGBA", (actual_size, actual_size), (0, 0, 0, 0))
    qr_draw = ImageDraw.Draw(qr_layer)
    
    # Safe zone dimensions
    if is_foreground_only:
        # Foreground for adaptive icon needs to fit within central 66% safe area
        box_area = actual_size * 0.58
    else:
        box_area = actual_size * 0.64

    left = (actual_size - box_area) / 2
    top = (actual_size - box_area) / 2
    
    # Grid coordinates (7x7 blocks style)
    unit = box_area / 7.0
    finder_size = unit * 2.4
    
    # Corner Finders
    # Top-Left
    draw_rounded_finder(qr_draw, left, top, finder_size, (255, 255, 255, 245))
    # Top-Right
    draw_rounded_finder(qr_draw, left + box_area - finder_size, top, finder_size, (255, 255, 255, 245))
    # Bottom-Left
    draw_rounded_finder(qr_draw, left, top + box_area - finder_size, finder_size, (255, 255, 255, 245))
    
    # Additional data modules (stylized rounded dots / pills)
    def draw_dot(grid_x, grid_y, w_units=1.0, h_units=1.0):
        px = left + grid_x * unit + unit * 0.12
        py = top + grid_y * unit + unit * 0.12
        pw = unit * w_units - unit * 0.24
        ph = unit * h_units - unit * 0.24
        r = min(pw, ph) * 0.35
        qr_draw.rounded_rectangle([px, py, px + pw, py + ph], radius=r, fill=(255, 255, 255, 235))

    # Decorative functional data dots inside the grid
    # Timing strips
    draw_dot(3, 0.5, 1, 0.8)
    draw_dot(3, 1.8, 1, 0.8)
    draw_dot(0.5, 3, 0.8, 1)
    draw_dot(1.8, 3, 0.8, 1)

    # Center module cluster
    draw_dot(3, 3, 1, 1)
    draw_dot(4.2, 3, 0.8, 1)
    draw_dot(3, 4.2, 1, 0.8)

    # Right side and bottom clusters
    draw_dot(5.8, 3.2, 1.0, 1.0)
    draw_dot(4.5, 4.5, 1.2, 1.2)
    draw_dot(3.2, 5.8, 1.0, 1.0)
    draw_dot(5.8, 5.8, 1.0, 1.0)
    draw_dot(5.8, 4.5, 1.0, 1.0)
    draw_dot(4.5, 5.8, 1.0, 1.0)

    # In center or accent area, add a stylish sparkling diamond / star badge
    sparkle_center_x = left + box_area * 0.5
    sparkle_center_y = top + box_area * 0.5
    sparkle_size = unit * 0.9
    sparkle_points = [
        (sparkle_center_x, sparkle_center_y - sparkle_size),
        (sparkle_center_x + sparkle_size * 0.3, sparkle_center_y - sparkle_size * 0.3),
        (sparkle_center_x + sparkle_size, sparkle_center_y),
        (sparkle_center_x + sparkle_size * 0.3, sparkle_center_y + sparkle_size * 0.3),
        (sparkle_center_x, sparkle_center_y + sparkle_size),
        (sparkle_center_x - sparkle_size * 0.3, sparkle_center_y + sparkle_size * 0.3),
        (sparkle_center_x - sparkle_size, sparkle_center_y),
        (sparkle_center_x - sparkle_size * 0.3, sparkle_center_y - sparkle_size * 0.3),
    ]
    # Center accent glow
    qr_draw.polygon(sparkle_points, fill=(255, 235, 120, 250))

    # Add subtle soft shadow behind QR elements
    shadow = qr_layer.filter(ImageFilter.GaussianBlur(actual_size * 0.015))
    shadow_colored = Image.new("RGBA", (actual_size, actual_size), (0, 0, 0, 70))
    final_shadow = Image.new("RGBA", (actual_size, actual_size), (0, 0, 0, 0))
    final_shadow.paste(shadow_colored, (0, int(actual_size * 0.01)), shadow.split()[3])

    if not is_foreground_only:
        composite = Image.alpha_composite(base, final_shadow)
        composite = Image.alpha_composite(composite, qr_layer)
    else:
        composite = Image.alpha_composite(final_shadow, qr_layer)

    # Downsample with high quality Lanczos filter
    final_img = composite.resize((size, size), Image.Resampling.LANCZOS)
    return final_img

def main():
    os.makedirs("app/src/main/res/mipmap-mdpi", exist_ok=True)
    os.makedirs("app/src/main/res/mipmap-hdpi", exist_ok=True)
    os.makedirs("app/src/main/res/mipmap-xhdpi", exist_ok=True)
    os.makedirs("app/src/main/res/mipmap-xxhdpi", exist_ok=True)
    os.makedirs("app/src/main/res/mipmap-xxxhdpi", exist_ok=True)
    os.makedirs("app/src/main/res/drawable-nodpi", exist_ok=True)

    densities = {
        "mipmap-mdpi": 48,
        "mipmap-hdpi": 72,
        "mipmap-xhdpi": 96,
        "mipmap-xxhdpi": 144,
        "mipmap-xxxhdpi": 192,
    }

    print("Generating app icons...")
    # Standard square-rounded and round launcher icons
    for folder, px in densities.items():
        icon = generate_qr_icon(size=px, is_round=False)
        icon.save(f"app/src/main/res/{folder}/ic_launcher.png", "PNG")

        icon_round = generate_qr_icon(size=px, is_round=True)
        icon_round.save(f"app/src/main/res/{folder}/ic_launcher_round.png", "PNG")

        # Adaptive icon foreground (standard is 108dp: 108, 162, 216, 324, 432 px)
        fg_px = int(px * (108 / 48))
        icon_fg = generate_qr_icon(size=fg_px, is_foreground_only=True)
        icon_fg.save(f"app/src/main/res/{folder}/ic_launcher_foreground.png", "PNG")
        print(f"Generated {folder}: {px}px, foreground {fg_px}px")

    # High-res store icon
    store_icon = generate_qr_icon(size=512, is_round=False)
    store_icon.save("app/src/main/ic_launcher-playstore.png", "PNG")
    store_icon.save("app/src/main/res/drawable-nodpi/ic_launcher_playstore.png", "PNG")
    print("Generated 512x512 playstore icon.")

if __name__ == "__main__":
    main()
