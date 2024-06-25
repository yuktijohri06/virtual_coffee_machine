import mediapipe as mp



# Initialize mediapipe hands
mp_hands = mp.solutions.hands

# Test hand detection initialization
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)

print("Mediapipe hands initialized successfully!")
