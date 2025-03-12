import os
import argparse
from pytubefix import YouTube
from pydub import AudioSegment
from youtubesearchpython import VideosSearch
from pathvalidate import sanitize_filename

DEFAULT_OUTPUT_FOLDER = "downloads"


def create_directory(directory_path):
    """Create a directory if it doesn't exist."""
    os.makedirs(directory_path, exist_ok=True)


def remove_all_files(directory_path):
    """Remove all files from the specified directory."""
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as error:
            print(error)


def find_top_video(search_query):
    """Find the top YouTube video for a search query.
    
    Args:
        search_query: The search term to look for on YouTube
        
    Returns:
        tuple: (video_url, video_title)
        
    Raises:
        ValueError: If no search results are found
    """
    search = VideosSearch(search_query, limit=1)
    results = search.result().get("result", [])

    if not results:
        raise ValueError(f"No results found for '{search_query}'")

    return results[0]["link"], results[0]["title"]


def download_audio_stream(video_url, output_directory):
    """Download the audio from a YouTube video.
    
    Args:
        video_url: URL of the YouTube video
        output_directory: Where to save the downloaded file
        
    Returns:
        str: Path to the downloaded file
        
    Raises:
        ValueError: If no audio stream is available
    """
    youtube_video = YouTube(video_url)
    audio_stream = youtube_video.streams.filter(only_audio=True).first()

    if not audio_stream:
        raise ValueError(f"No audio stream found for: {youtube_video.title}")

    print(f"Downloading: {youtube_video.title}...")
    return audio_stream.download(output_path=output_directory)


def convert_audio_to_mp3(input_file_path, output_filename, output_directory):
    """Convert audio file to MP3 format.
    
    Args:
        input_file_path: Path to the input audio file
        output_filename: Name for the output file (without extension)
        output_directory: Directory to save the MP3 file
        
    Returns:
        str: Path to the created MP3 file
    """
    safe_filename = sanitize_filename(output_filename)
    mp3_file_path = os.path.join(output_directory, f"{safe_filename}.mp3")

    audio = AudioSegment.from_file(input_file_path)
    audio.export(mp3_file_path, format="mp3")

    os.remove(input_file_path)
    return mp3_file_path


def process_video_to_mp3(search_query, output_directory):
    """Process a search query into an MP3 file.
    
    This function handles the entire workflow of searching for a video,
    downloading it, and converting it to MP3.
    
    Args:
        search_query: What to search for on YouTube
        output_directory: Where to save the final MP3 file
    """
    try:
        video_url, video_title = find_top_video(search_query)
        downloaded_file = download_audio_stream(video_url, output_directory)
        mp3_file_path = convert_audio_to_mp3(downloaded_file, video_title, output_directory)
        print(f"✅ Downloaded and saved: {mp3_file_path}")
    except Exception as error:
        print(f"❌ Error: {error}")


def parse_command_line_arguments():
    """Parse and return command line arguments."""
    parser = argparse.ArgumentParser(description="Download YouTube videos as MP3.")
    parser.add_argument("queries", nargs="+", help="Search query or video name.")
    parser.add_argument(
        "-o",
        "--output",
        default=DEFAULT_OUTPUT_FOLDER,
        help=f"Output folder (default: '{DEFAULT_OUTPUT_FOLDER}').",
    )
    
    return parser.parse_args()


def main():
    """Main entry point for the application."""
    args = parse_command_line_arguments()

    create_directory(args.output)
    remove_all_files(args.output)

    for query in args.queries:
        process_video_to_mp3(query, args.output)


if __name__ == "__main__":
    main()