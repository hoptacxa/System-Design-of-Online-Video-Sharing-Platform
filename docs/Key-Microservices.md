### **Bare-Minimum Microservices for a Lean MVP**

1.  **User Management Service** 👤

    -   Enables users to register, log in, and authenticate.
    -   Basic features: user sign-up and login/logout.
2.  **Video Upload Service** 📤

    -   Handles video uploads from users.
    -   Basic validation for file size and format.
    -   Stores raw video files in a cloud storage bucket (e.g., AWS S3).
3.  **Video Playback Service** ▶️

    -   Streams raw or minimally processed videos to users.
    -   Uses cloud storage for video hosting.
    -   No transcoding; uploaded videos are served "as-is."
4.  **Metadata Management Service** 🏷️

    -   Stores and retrieves basic video metadata (e.g., title, description, uploader).
    -   Enables users to browse or view a simple list of uploaded videos.
