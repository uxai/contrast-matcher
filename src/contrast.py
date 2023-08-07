#!/usr/bin/env python3

# Set the threshold for how far your new color can deviate from the original contrast
THRESHOLD = 0.01

# convert HSL to RGB
def HSLtoRGB(H, S, L):
    C = (1 - abs(2 * L - 1)) * S
    X = C * (1 - (abs(((H / 60) % 2) - 1)))
    m = L - C / 2

    if 0 <= H < 60:
        (Rx, Gx, Bx) = (C, X, 0)
    elif 60 <= H < 120:
        (Rx, Gx, Bx) = (X, C, 0)
    elif 120 <= H < 180:
        (Rx, Gx, Bx) = (0, C, X)
    elif 180 <= H < 240:
        (Rx, Gx, Bx) = (0, X, C)
    elif 240 <= H < 300:
        (Rx, Gx, Bx) = (X, 0, C)
    else:
        (Rx, Gx, Bx) = (C, 0, X)

    R, G, B = (Rx + m) * 255, (Gx + m) * 255, (Bx + m) * 255
    RGB = [R, G, B]
    return RGB

#Luminance for both calculated and perceived contrasts according to WCAG standards
def luminance(rgb, method):
    rgbcc = rgb.copy()
    for v in range(0, len(rgbcc)):
        rgbcc[v] = rgbcc[v] / 255
        if rgbcc[v] <= 0.03928:
            rgbcc[v] = rgbcc[v] / 12.92
        else:
            rgbcc[v] = pow((rgbcc[v] + 0.055) / 1.055, 2.4)
    
    if method == 1:
        return (rgbcc[0] * 0.2126 + rgbcc[1] * 0.7152 + rgbcc[2] * 0.0722)
    else:
        return (rgbcc[0] * 0.299 + rgbcc[1] * 0.587 + rgbcc[2] * 0.114)

# Calculate the color contrast
def contrast(rgb1, rgb2, method):
    lum1 = luminance(rgb1, method)
    lum2 = luminance(rgb2, method)

    if lum1 > lum2:
        return (lum1 + 0.05) / (lum2 + 0.05)
    else:
        return (lum2 + 0.05) / (lum1 + 0.05)

# Function to search range function and expand the range until matches are found
def match_contrast(S1, H3, RGB2, contrast_origin, method):
    nearest_col = {}

    start = int(S1 * 100)
    finish = int(S1 * 100)

    while not nearest_col:
        nearest_col = search_range(H3, RGB2, contrast_origin, start, finish, method)
        if start == 0 and finish == 100:
            return False
        start -= 1
        if start < 0:
            start = 0
        finish += 1
        if finish > 100:
            finish = 100

    return nearest_col
        
# Search range of colors prioritizing Saturation (sat) and light as secondary, search light from 0-100 and continue looping.
def search_range(H3, RGB2, contrast_origin, start, finish, method):
    nearest_col = {}
    for sat in range(start, finish+1):
        for light in range(0, 101):
            RGB3 = HSLtoRGB(H3, sat / 100, light / 100)
            contrast_new = round(contrast(RGB3, RGB2, method), 3)
            diff = round(abs(contrast_origin - contrast_new), 3)
            if diff <= THRESHOLD:
                nearest_col["H"] = H3
                nearest_col["S"] = sat
                nearest_col["L"] = light
                nearest_col["contrast"] = contrast_new
                nearest_col["difference"] = diff
                return nearest_col
    
    return False

def print_output(nearest_col, method):
    print("--------------------------------------")
    print(f"{method} contrast match:")
    print("--------------------------------------")
    print(f"H:{nearest_col['H']}, S:{nearest_col['S']}, L:{nearest_col['L']}")
    print(f"Contrast ratio: {nearest_col['contrast']}")
    print(f"Contrast difference from origin: {nearest_col['difference']}")


if __name__ == "__main__":
    HSL1 = input("Please enter the foreground color HSL values (0, 0, 0): ").replace(" ", "")
    HSL1 = HSL1.split(',')
    H1, S1, L1 = int(HSL1[0]), int(HSL1[1])/100, int(HSL1[2])/100
    RGB1 = HSLtoRGB(H1, S1, L1)

    HSL2 = input("Please enter the background color HSL values (0, 0, 0): ").replace(" ", "")
    HSL2 = HSL2.split(',')
    H2, S2, L2 = int(HSL2[0]), int(HSL2[1])/100, int(HSL2[2])/100
    RGB2 = HSLtoRGB(H2, S2, L2)

    contrast_calculated = round(contrast(RGB1, RGB2, 1), 3)
    contrast_perceived =  round(contrast(RGB1, RGB2, 2), 3)
    print("+------------------------------------+")
    print("|         First pair results         |")
    print("+------------------------------------+")
    print(f"Contrast calculated is: {contrast_calculated}")
    print(f"Contrast perceived is:  {contrast_perceived}")

    print("--------------------------------------")
    H3 = int(input("Please enter the new foreground Hue to match (0 - 359): "))
    nearest_col = match_contrast(S1, H3, RGB2, contrast_calculated, 1)
    if(nearest_col == False):
        print("No match found, possibly out of range")
    else:
        print_output(nearest_col, "Calculated")
    nearest_col = match_contrast(S1, H3, RGB2, contrast_perceived, 2)
    if(nearest_col == False):
        print("No match found, possibly out of range")
    else:
        print_output(nearest_col, "Perceived")