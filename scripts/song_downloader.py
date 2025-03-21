import os


class SongDownloader:
    def from_text_file(self, file_path):
        with open(file_path, "r") as file:
            queries = file.readlines()
            transformed_queries = [query.strip() for query in queries]
            transformed_queries = [f'"{query} song"' for query in transformed_queries]

            os.system(f"python song_downloader_cli.py {' '.join(transformed_queries)}")
    
    def from_playlist(self, url):
        from pytubefix import Playlist
        playlist = Playlist(url)
        queries = [video.title for video in playlist.videos]
        transformed_queries = [f'"{query} song"' for query in queries]
        
        os.system(f"python song_downloader_cli.py {' '.join(transformed_queries)}")


if __name__ == "__main__":
    downloader = SongDownloader()
    # downloader.from_text_file("scripts/data/song-names.txt")
    downloader.from_playlist("https://music.youtube.com/playlist?list=LRYRAoeXvXhbIW4yo-YABF99bxBQUXb3zOJTD")
