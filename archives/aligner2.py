import cv2
import numpy as np
import sys
import os

# =====================================================================
# 🛠️ USER CONFIGURATION: PASTE YOUR CORNER PIXEL COORDINATES HERE
# =====================================================================
# Open your raw image in an editor and find the (X, Y) pixel coordinates
# of the four corners of the gold border.
CORNER_TOP_LEFT     = [127, 32]     # Replace with your actual [X, Y]
CORNER_TOP_RIGHT    = [1345, 30]    # Replace with your actual [X, Y]
CORNER_BOTTOM_LEFT = [114, 1047]  # Replace with your actual [X, Y]
CORNER_BOTTOM_RIGHT  = [1352, 1055]   # Replace with your actual [X, Y]

# --- File Paths ---
INPUT_IMAGE_PATH = "assets/Eurorails Map Original.jpg"  # Path to your raw image
OUTPUT_IMAGE_PATH = "assets/map2.jpg" # Where to save output

# --- Desired Output Dimensions ---
# Standard crisp resolution maintaining a clean aspect ratio for the board
OUTPUT_WIDTH = 2400 
OUTPUT_HEIGHT = 1800 
# =====================================================================

def main():
    print("=== Eurorails Hardcoded Map Pre-Processor ===")
    
    # 1. Load Raw Image
    img = cv2.imread(INPUT_IMAGE_PATH)
    if img is None:
        print(f"ERROR: Could not load image from '{INPUT_IMAGE_PATH}'")
        print("Please check that the file name matches your workspace exactly.")
        sys.exit()
        
    print(f"Loaded source image successfully ({img.shape[1]}x{img.shape[0]}px).")

    # 2. Package Source Coordinates
    # The order must map perfectly to the destination rectangle layout
    src_points = np.float32([
        CORNER_TOP_LEFT,
        CORNER_TOP_RIGHT,
        CORNER_BOTTOM_RIGHT,
        CORNER_BOTTOM_LEFT
    ])
    
    # 3. Define Destination Target Layout
    dst_points = np.float32([
        [0, 0],                            # Target Top-Left
        [OUTPUT_WIDTH, 0],                 # Target Top-Right
        [OUTPUT_WIDTH, OUTPUT_HEIGHT],     # Target Bottom-Right
        [0, OUTPUT_HEIGHT]                 # Target Bottom-Left
    ])

    print("\nProcessing perspective transformation matrix...")
    print(f"Source Coordinates:\n{src_points}")
    
    # 4. Calculate Homography Matrix & Apply Warp
    M_transform = cv2.getPerspectiveTransform(src_points, dst_points)
    
    aligned_img = cv2.warpPerspective(
        img, 
        M_transform, 
        (OUTPUT_WIDTH, OUTPUT_HEIGHT),
        flags=cv2.INTER_CUBIC  # High-quality bicubic interpolation for clean lines
    )

    # 5. Save the Aligned Output
    output_dir = os.path.dirname(OUTPUT_IMAGE_PATH)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cv2.imwrite(OUTPUT_IMAGE_PATH, aligned_img)
    print(f"\nSUCCESS! Pristine, squared map saved to: {OUTPUT_IMAGE_PATH}")
    print(f"New Dimensions: {OUTPUT_WIDTH}x{OUTPUT_HEIGHT} pixels.")

    # 6. Quick Visual Verification
    # Opens a window showing your output file so you can double check the crop accuracy.
    cv2.namedWindow("Verification Window", cv2.WINDOW_NORMAL)
    cv2.imshow("Verification Window", aligned_img)
    print("\nPress 'q' inside the display window to exit.")
    
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
            
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()