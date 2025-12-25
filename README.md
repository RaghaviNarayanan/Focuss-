# Focuss-
This project, called Focus, is  productivity monitoring system designed to track user focus by combining computer vision, browser activity logging, and machine learning analysis. The system continuously monitors whether the user is attentive, detects distractions, records browsing behavior, and generates a summarized productivity report.

When the system starts, a master program launches multiple components in parallel using threading. One part of the system starts a Flask server that listens for incoming browsing data from a browser extension. Another part starts the computer vision module that uses the webcam to monitor user behavior in real time.

The computer vision module uses a camera to detect the user’s face and check for mobile phone usage. Face detection ensures that the user is present and attentive, while phone detection identifies moments of distraction. When the user’s face is continuously visible, a focus timer runs and tracks total productive time. If the face disappears for several frames, the focus session ends and the time is saved. This process runs continuously until the user stops the system.

At the same time, the Flask server receives website URLs from a browser extension. Every time a website is visited, the URL and timestamp are sent to the server. The system classifies each website as productive, distracting, or neutral based on predefined keyword rules. All browsing activity is stored in a CSV file for later analysis.

At the end of a session or at a scheduled time, the system processes the collected browsing data using a machine learning model. A Random Forest classifier is trained on the browsing behavior to improve category prediction based on time spent. The model predicts how much of the user’s activity was productive, distracting, or neutral.

After analysis, the system generates a summary report showing total websites visited and the distribution of productive and distracting activity. This summary is automatically sent to the user via email using Gmail SMTP. Once the report is sent, the browsing log is cleared so that the next session starts fresh.

Overall, the project flow begins with real-time face and phone detection, continues with background logging of browsing activity, applies machine learning for productivity classification, and ends with an automated email report. This integrated flow allows the system to provide a clear and intelligent overview of the user’s focus and productivity using machine learning, computer vision, and data analysis.
