import subprocess
import os
import tempfile

class VideoProcessingService:
    def generate_hls_output(
        self,
        input_file: bytes,
        output_dir: str,
        resolution: str = "176:144",
        video_codec: str = "libx264",
        audio_codec: str = "aac",
        audio_bitrate: str = "64k",
        crf: int = 23,
        hls_time: int = 12,
        playlist_type: str = "vod",
        segment_filename_pattern: str = "segment_%03d.ts",
        playlist_name: str = "output.m3u8"
    ) -> str:
        """
        Transcodes the input video bytes into HLS format with customizable options.

        Args:
            input_file (bytes): The input video file as bytes.
            output_dir (str): Directory to store the output HLS playlist and segments.
            resolution (str): Video resolution (e.g., "1920:1080").
            video_codec (str): Video codec to use (default: "libx264").
            audio_codec (str): Audio codec to use (default: "aac").
            audio_bitrate (str): Audio bitrate (default: "64k").
            crf (int): Constant rate factor for video quality (lower is higher quality).
            hls_time (int): Duration of each HLS segment in seconds (default: 5).
            playlist_type (str): HLS playlist type ("vod", "event", etc.).
            segment_filename_pattern (str): Pattern for naming segment files.
            playlist_name (str): Name of the HLS playlist file.

        Returns:
            str: Path to the generated HLS playlist file.
        """
        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Create a temporary file for the input video
        with tempfile.NamedTemporaryFile(delete=False, suffix=".tmp") as temp_input_file:
            temp_input_path = temp_input_file.name
            temp_input_file.write(input_file)

        # Define the full paths for the playlist and segments
        output_playlist = os.path.join(output_dir, playlist_name)
        segment_pattern = os.path.join(output_dir, segment_filename_pattern)

        # Build the ffmpeg command dynamically based on options
        command = [
            "ffmpeg",
            "-i", temp_input_path,    # Use the temporary input file
            "-c:v", video_codec,      # Video codec
            "-crf", str(crf),         # Video quality factor
            "-vf", f"scale={resolution}",  # Video resolution
            "-c:a", audio_codec,      # Audio codec
            "-b:a", audio_bitrate,    # Audio bitrate
            "-strict", "experimental",  # Enable experimental features
            "-hls_time", str(hls_time),  # Segment duration
            "-hls_playlist_type", playlist_type,  # Playlist type
            "-hls_segment_filename", segment_pattern,  # Segment file pattern
            output_playlist           # Output playlist
        ]

        try:
            # Execute the ffmpeg command
            subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"FFmpeg processing failed: {e.stderr.decode()}") from e
        finally:
            # Clean up the temporary input file
            os.remove(temp_input_path)

        return output_playlist
