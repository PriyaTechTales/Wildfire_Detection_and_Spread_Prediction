from ultralytics import YOLO
import os
import torch

# Simple model loading
try:
    # Try to load the model from the root directory
    model_path = 'best.pt'
    if not os.path.exists(model_path):
        # Try to find the model in the parent directory
        parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        model_path = os.path.join(parent_dir, 'best.pt')
        
    if os.path.exists(model_path):
        print(f"Loading model from: {model_path}")
        model = YOLO(model_path)
        print("Model loaded successfully")
    else:
        print("Model file not found, using default YOLOv8n model")
        model = YOLO('yolov8n.pt')
except Exception as e:
    print(f"Error loading model: {str(e)}")
    # Fallback to a default model
    model = YOLO('yolov8n.pt')
    print("Using default YOLOv8n model")

def predict_fire(image_path):
    try:
        # Run inference on the image
        results = model(image_path)
        
        # Get the first result (since we're processing one image)
        result = results[0]
        
        # Get the class names and confidences
        class_names = result.names
        boxes = result.boxes
        
        # Print available classes for debugging
        print(f"Available classes: {class_names}")
        
        # Initialize detection results
        detections = []
        
        # Process each detection
        for box in boxes:
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            class_name = class_names[class_id]
            
            # Print each detection for debugging
            print(f"Detected: {class_name} with confidence {confidence}")
            
            detections.append({
                'class': class_name,
                'confidence': confidence
            })
        
        # If no detections found
        if not detections:
            print("No detections found in the image")
            return {'status': 'No Fire', 'detections': []}
            
        # Check if any fire-related class was detected
        # Adjust these class names based on your model's actual class names
        fire_classes = ['Fire Flame', 'Fire Smoke', 'fire', 'flame', 'smoke', 'Fire']
        fire_detected = any(d['class'] in fire_classes for d in detections)
        
        if fire_detected:
            print("Fire detected in the image")
        else:
            print("No fire detected in the image")
        
        return {
            'status': 'Fire Detected' if fire_detected else 'No Fire',
            'detections': detections
        }
        
    except Exception as e:
        print(f"Error in predict_fire: {str(e)}")
        return {'status': 'Error', 'error': str(e)}
