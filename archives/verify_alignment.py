import cv2
import matplotlib.pyplot as plt

def verify_alignment(image_path):
    warped_img = cv2.imread(image_path)
    if warped_img is None:
        raise FileNotFoundError(f"Could not read image at {image_path}")

    # Convert BGR to RGB for matplotlib
    rgb_img = cv2.cvtColor(warped_img, cv2.COLOR_BGR2RGB)
    
    plt.figure(figsize=(14, 10))
    plt.imshow(rgb_img)
    
    # Force a detailed grid onto the plot canvas
    plt.grid(color='cyan', linestyle='-', linewidth=0.5)
    
    # Add major tickers every 50 pixels to easily inspect alignment
    plt.xticks(range(0, warped_img.shape[1], 100))
    plt.yticks(range(0, warped_img.shape[0], 100))
    
    plt.title("Alignment Check: Ensure milepost lines run parallel to the cyan grid lines")
    plt.show()

# Call this with the map image in assets/
verify_alignment("assets/Eurorails Map Fixed.jpg")