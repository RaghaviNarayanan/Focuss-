import cv2
import mediapipe as mp
import time
from datetime import timedelta

def run_face_timer():  # ✅ corrected name here
    # Mediapipe face detector setup
    mp_face = mp.solutions.face_detection
    face_detection = mp_face.FaceDetection(min_detection_confidence=0.5)

    # OpenCV video capture
    cap = cv2.VideoCapture(0)

    # Timers
    start_time = 0
    total_time = 0
    face_visible = False

    # Face loss tolerance
    lost_count = 0
    max_lost = 5  # Number of consecutive frames without face before stopping timer

    print("📸 Focus face timer started...")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = face_detection.process(frame_rgb)

        if result.detections:
            if not face_visible:
                face_visible = True
                start_time = time.time()
            lost_count = 0
            cv2.putText(frame, "Face Detected ✅", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            if face_visible:
                lost_count += 1
                if lost_count >= max_lost:
                    face_visible = False
                    session_time = time.time() - start_time
                    total_time += session_time
                    print(f"🔴 Session Ended. Time Tracked: {timedelta(seconds=int(total_time))}")
            cv2.putText(frame, "No Face ❌", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Show total time on screen
        if face_visible:
            current_time = time.time() - start_time + total_time
        else:
            current_time = total_time

        minutes = int(current_time) // 60
        seconds = int(current_time) % 60
        cv2.putText(frame, f"Total Focus Time: {minutes:02}:{seconds:02}", (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

        cv2.imshow("Focus - Face Timer", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    face_detection.close()
    print(f"🕒 Final Total Focus Time: {timedelta(seconds=int(current_time))}")

if __name__ == "__main__":
    run_face_timer()  # ✅ corrected function name
