import os


class SongDownloader:
    def from_text_file(self, file_path):
        with open(file_path, "r") as file:
            queries = file.readlines()
            transformed_queries = [query.strip() for query in queries]
            transformed_queries = [f'"{query} song"' for query in transformed_queries]

            os.system(f"python song_downloader_cli.py {' '.join(transformed_queries)}")


if __name__ == "__main__":
    downloader = SongDownloader()
    downloader.from_text_file("scripts/data/song-names.txt")
