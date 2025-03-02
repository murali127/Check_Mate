import cv2
import numpy as np
import os

class ChequeBorderProcessor:
    def __init__(self, output_size=(600, 300), save_intermediate=False):
        """
        Initialize cheque border processor
        :param output_size: Tuple (width, height) for resizing
        :param save_intermediate: Boolean to save processing steps
        """
        self.output_size = output_size
        self.save_intermediate = save_intermediate
    
    def process_image(self, image_path, output_path):
        """Main processing pipeline for a single image"""
        try:
            # Load and validate image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Could not read image: {image_path}")
            
            # Preprocessing
            processed = self._preprocess(image)
            
            # Border detection
            contour = self._find_border_contour(processed)
            
            # Perspective correction
            warped = self._perspective_transform(image, contour)
            
            # Resizing
            resized = self._resize_image(warped)
            
            # Save result
            cv2.imwrite(output_path, resized)
            return True
            
        except Exception as e:
            print(f"Error processing {image_path}: {str(e)}")
            return False

    def _preprocess(self, image):
        """Image preprocessing steps"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blurred, 50, 200)
        
        # Additional morphological operations to close gaps
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
        
        if self.save_intermediate:
            cv2.imwrite("intermediate_edged.jpg", closed)
            
        return closed

    def _find_border_contour(self, image):
        """Find cheque border contour"""
        contours, _ = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]

        for contour in contours:
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
            if len(approx) == 4:
                return approx.reshape(4, 2)
                
        raise ValueError("No quadrilateral contour found")

    def _perspective_transform(self, image, pts):
        """Apply perspective transformation"""
        rect = self._order_points(pts)
        (tl, tr, br, bl) = rect
        
        # Calculate dimensions
        widthA = np.linalg.norm(br - bl)
        widthB = np.linalg.norm(tr - tl)
        maxWidth = max(int(widthA), int(widthB))

        heightA = np.linalg.norm(tr - br)
        heightB = np.linalg.norm(tl - bl)
        maxHeight = max(int(heightA), int(heightB))
        
        # Destination array
        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype="float32")

        # Compute perspective transform matrix
        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
        
        if self.save_intermediate:
            cv2.imwrite("intermediate_warped.jpg", warped)
            
        return warped

    def _order_points(self, pts):
        """Arrange points in consistent order"""
        rect = np.zeros((4, 2), dtype="float32")
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        return rect

    def _resize_image(self, image):
        """Resize image to standard size"""
        return cv2.resize(image, self.output_size, interpolation=cv2.INTER_AREA)

def process_directory(input_dir, output_dir, target_size=(600, 300)):
    """Process all images in a directory"""
    processor = ChequeBorderProcessor(output_size=target_size)
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    processed_count = 0
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, f"processed_{filename}")
            
            if processor.process_image(input_path, output_path):
                processed_count += 1
                
    print(f"Successfully processed {processed_count} images")