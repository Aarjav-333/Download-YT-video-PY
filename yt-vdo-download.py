from pytube import YouTube
import subprocess

def download_highest_quality_youtube_video(url, save_path):
    try:
        # Create YouTube object
        yt = YouTube(url)
        
        # Get the highest quality video stream (excluding progressive streams)
        video_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_video=True).order_by('resolution').desc().first()
        
        # Get the highest quality audio stream
        audio_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_audio=True).order_by('abr').desc().first()
        
        # Define file names for video and audio
        video_file = f"{save_path}/video.mp4"
        audio_file = f"{save_path}/audio.mp4"
        
        # Download video and audio streams
        video_stream.download(output_path=save_path, filename='video.mp4')
        audio_stream.download(output_path=save_path, filename='audio.mp4')
        
        print(f"Video '{yt.title}' has been downloaded successfully!")
        
        # Combine video and audio using ffmpeg
        output_file = f"{save_path}/{yt.title}.mp4"
        subprocess.run(['ffmpeg', '-i', video_file, '-i', audio_file, '-c:v', 'copy', '-c:a', 'aac', output_file])
        
        print(f"Combined video saved as '{output_file}'")
        
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
url = "https://www.youtube.com/watch?v=your_video_id"
save_path = "./"  # Change to your desired directory
download_highest_quality_youtube_video(url, save_path)
