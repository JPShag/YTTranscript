import sys
import os
from dotenv import load_dotenv, set_key
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QMessageBox, QFileDialog
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi


class YouTubeTranscriptApp(QWidget):
    def __init__(self):
        super().__init__()
        load_dotenv()
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # API Key Input
        self.api_key_input = QLineEdit(self)
        self.api_key_input.setPlaceholderText("Enter YouTube API Key")
        if self.api_key:
            self.api_key_input.setText(self.api_key)
        layout.addWidget(self.api_key_input)

        # Save API Key Button
        self.save_api_key_button = QPushButton("Save API Key", self)
        self.save_api_key_button.clicked.connect(self.save_api_key)
        layout.addWidget(self.save_api_key_button)

        # Single Video ID Input
        self.video_id_input = QLineEdit(self)
        self.video_id_input.setPlaceholderText("Enter Single Video ID")
        layout.addWidget(self.video_id_input)

        # Fetch Single Video Transcript Button
        self.fetch_single_button = QPushButton("Fetch Single Video Transcript", self)
        self.fetch_single_button.clicked.connect(self.fetch_single_transcript)
        layout.addWidget(self.fetch_single_button)

        # Playlist ID Input
        self.playlist_id_input = QLineEdit(self)
        self.playlist_id_input.setPlaceholderText("Enter Playlist ID")
        layout.addWidget(self.playlist_id_input)

        # Fetch Button for Playlist
        self.fetch_button = QPushButton("Fetch Playlist Transcripts", self)
        self.fetch_button.clicked.connect(self.fetch_transcripts)
        layout.addWidget(self.fetch_button)

        # Transcript Display
        self.transcript_display = QTextEdit(self)
        self.transcript_display.setReadOnly(True)
        layout.addWidget(self.transcript_display)

        # Save Transcripts Button
        self.save_button = QPushButton("Save Transcripts", self)
        self.save_button.clicked.connect(self.save_transcripts)
        layout.addWidget(self.save_button)

        self.setLayout(layout)
        self.setWindowTitle('YouTube Transcript Fetcher')
        self.setGeometry(300, 300, 600, 400)

    def save_api_key(self):
        api_key = self.api_key_input.text()
        if api_key:
            set_key(".env", "YOUTUBE_API_KEY", api_key)
            QMessageBox.information(self, 'Saved', 'API Key saved successfully')
        else:
            QMessageBox.warning(self, 'Error', 'No API Key entered')

    def fetch_single_transcript(self):
        video_id = self.video_id_input.text()
        if not video_id:
            QMessageBox.warning(self, 'Error', 'Please enter a Video ID')
            return

        try:
            transcript = self.get_transcript(video_id)
            if transcript:
                self.transcript_display.setText(f"Transcript for video {video_id}:\n{transcript}")
            else:
                QMessageBox.warning(self, 'Error', 'Transcript not available for this video')
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))

    def fetch_transcripts(self):
        api_key = self.api_key_input.text()
        playlist_id = self.playlist_id_input.text()
        if not api_key or not playlist_id:
            QMessageBox.warning(self, 'Error', 'Please enter both API Key and Playlist ID')
            return

        try:
            video_ids = self.get_video_ids(playlist_id, api_key)
            all_transcripts = ''
            for video_id in video_ids:
                transcript = self.get_transcript(video_id)
                if transcript:
                    all_transcripts += f"\n\nTranscript for video {video_id}:\n{transcript}"

            self.transcript_display.setText(all_transcripts)
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))

    def get_video_ids(self, playlist_id, api_key):
        youtube = build('youtube', 'v3', developerKey=api_key)
        request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=50
        )

        video_ids = []
        while request is not None:
            response = request.execute()
            video_ids += [item['contentDetails']['videoId'] for item in response['items']]
            request = youtube.playlistItems().list_next(request, response)

        return video_ids

    def get_transcript(self, video_id):
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
            transcript_text = "\n".join([i['text'] for i in transcript_list])
            return transcript_text
        except Exception as e:
            print(f"Error fetching transcript for video {video_id}: {e}")
            return None

    def save_transcripts(self):
        text = self.transcript_display.toPlainText()
        if not text:
            QMessageBox.warning(self, 'Error', 'No transcripts to save')
            return

        try:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getSaveFileName(self, "Save Transcripts", "", "Text Files (*.txt);;All Files (*)", options=options)
            if fileName:
                with open(fileName, "w") as file:
                    file.write(text)
                QMessageBox.information(self, 'Saved', f'Transcripts saved to {fileName}')
            else:
                QMessageBox.warning(self, 'Cancelled', 'Save operation cancelled')
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = YouTubeTranscriptApp()
    ex.show()
    sys.exit(app.exec_())
