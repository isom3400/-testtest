from PIL import Image
from transformers import pipeline

def classify_happiness(image_path: str):
    """
    Loads an image, runs it through a Hugging Face ViT model fine-tuned 
    for emotion recognition, and checks for 'happy' or 'happiness'.
    """
    print("Loading emotion classification model...")
    # Using a Vision Transformer (ViT) fine-tuned on facial expressions / emotions
    classifier = pipeline(
        task="image-classification", 
        model="dima806/facial_emotions_image_detection"
    )
    
    print(head_up := f"Analyzing image: {image_path}...")
    try:
        img = Image.open(image_path).convert("RGB")
    except FileNotFoundError:
        print(f"Error: The file '{image_path}' could not be found.")
        return
    except Exception as e:
        print(f"Error loading image: {e}")
        return

    # Run inference
    results = classifier(img)
    
    print("\n--- Emotion Classification Results ---")
    happy_detected = False
    
    for prediction in results:
        label = prediction['label'].lower()
        score = prediction['score']
        print(f"Label: {prediction['label']:<15} Confidence: {score:.2%}")
        
        # Check if the primary detected emotion is happy
        if 'happy' in label or 'happiness' in label:
            if score > 0.5: # 50% threshold
                happy_detected = True
                happy_score = score

    print("--------------------------------------")
    if happy_detected:
        print(f"✅ Outcome: The subject appears HAPPY (Confidence: {happy_score:.2%})")
    else:
        print("❌ Outcome: Happiness is not the dominant emotion detected.")

if __name__ == "__main__":
    # Replace with the path to your local image file
    image_to_test = "happy_face.jpg" 
    
    classify_happiness(image_to_test)

