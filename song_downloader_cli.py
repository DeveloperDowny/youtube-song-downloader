import os
import argparse
from pytubefix import YouTube
from pydub import AudioSegment
from youtubesearchpython import VideosSearch
from pathvalidate import sanitize_filename

DEFAULT_OUTPUT_FOLDER = "downloads"


def ensure_output_folder_exists(folder):
    """Ensure the output folder exists."""
    os.makedirs(folder, exist_ok=True)


def search_youtube(query):
    """Return the URL of the top YouTube search result for a given query."""
    search = VideosSearch(query, limit=1)
    results = search.result().get("result", [])

    if not results:
        raise ValueError(f"No results found for '{query}'")

    return results[0]["link"], results[0]["title"]


def download_audio(video_url, output_folder):
    """Download audio from YouTube and return the file path."""
    yt = YouTube(video_url)
    audio_stream = yt.streams.filter(only_audio=True).first()

    if not audio_stream:
        raise ValueError(f"No audio stream found for: {yt.title}")

    print(f"Downloading: {yt.title}...")
    return audio_stream.download(output_path=output_folder)


def convert_to_mp3(file_path, output_name, output_folder):
    """Convert the downloaded file to MP3 and delete the original file."""
    output_name = sanitize_filename(output_name)
    mp3_path = os.path.join(output_folder, f"{output_name}.mp3")

    audio = AudioSegment.from_file(file_path)
    audio.export(mp3_path, format="mp3")

    os.remove(file_path)
    return mp3_path


def download_and_convert(query, output_folder):
    """Search, download, and convert the top YouTube result to MP3."""
    try:
        video_url, video_title = search_youtube(query)
        file_path = download_audio(video_url, output_folder)
        mp3_file = convert_to_mp3(file_path, video_title, output_folder)
        print(f"✅ Downloaded and saved: {mp3_file}")
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    parser = argparse.ArgumentParser(description="Download YouTube videos as MP3.")
    parser.add_argument("queries", nargs="+", help="Search query or video name.")
    parser.add_argument(
        "-o",
        "--output",
        default=DEFAULT_OUTPUT_FOLDER,
        help="Output folder (default: 'downloads').",
    )

    args = parser.parse_args()

    ensure_output_folder_exists(args.output)

    for query in args.queries:
        download_and_convert(query, args.output)


if __name__ == "__main__":
    main()
