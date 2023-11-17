## YouTube Transcript Fetcher

### Overview
The YouTube Transcript Fetcher is a desktop application built with PyQt5. It enables users to easily fetch transcripts from individual YouTube videos or entire playlists. The application is designed for simplicity and efficiency, catering to educators, content creators, researchers, and anyone interested in obtaining YouTube video transcripts.

### Features
- **Fetch Individual Video Transcripts**: Retrieve transcripts from a specific YouTube video by providing its video ID.
- **Fetch Playlist Transcripts**: Acquire transcripts from all videos in a YouTube playlist using the playlist ID.
- **Display Transcripts**: View fetched transcripts directly within the application.
- **Save Transcripts**: Save the displayed transcripts to a local file, with customizable file naming and location.

### Requirements
- Python 3.6 or higher.
- PyQt5.
- Google API Python Client.
- YouTube Transcript API.

### Installation
Before running the application, ensure the required Python packages are installed:

```bash
pip install PyQt5 google-api-python-client youtube_transcript_api
```

### Usage Instructions

1. **Starting the Application**: Launch the application by running the Python script.

2. **API Key Configuration**:
   - Enter your YouTube Data API key in the provided text field.
   - This key is essential for fetching video details from playlists.
   - Click the "Save API Key" button to store the key for the session.

3. **Fetching Transcripts**:
   - **Single Video**: Enter a YouTube video ID and click "Fetch Single Video Transcript".
   - **Playlist**: Enter a YouTube playlist ID and click "Fetch Playlist Transcripts".

4. **Viewing and Saving Transcripts**:
   - Transcripts appear in the text box within the application.
   - To save transcripts, click "Save Transcripts" and choose the desired file name and location.

### Security Considerations
- Store the YouTube API key securely. Avoid exposing it in the application's codebase or any insecure files.
- Consider implementing environment variables or encrypted storage for the API key.

### Logging
- The application includes logging for critical events and errors, facilitating easier debugging and maintenance.

### Future Enhancements
- Implement OAuth 2.0 for enhanced security in API key handling.
- Add functionality for URL-based video and playlist ID extraction.
- Enhance the UI/UX with more intuitive controls, tooltips, and detailed error messages.

### Support and Contributions
For support requests, feature suggestions, or contributions, please contact the development team or submit an issue/pull request on the project's GitHub repository.
