import random
from moviepy.editor import VideoFileClip
from play_movie import MoviePlayer

class RandomMoviePlayer(MoviePlayer):
    def __init__(self, video_paths):
        self.video_paths = video_paths
        super().__init__(random.choice(video_paths))

    def play_random(self):
        # ランダムにビデオファイルを選択し、再生する
        self.video_path = random.choice(self.video_paths)
        super().play()

if __name__ == "__main__":
    video_paths = [
        "/Users/matsudaichirou/workspace/dev/shuzo-shutyu-alarm/akiramennayo-shuzo.mp4",
        "/Users/matsudaichirou/workspace/dev/shuzo-shutyu-alarm/shuzo-kiminradekiru.mp4",
        "/Users/matsudaichirou/workspace/dev/shuzo-shutyu-alarm/shuzo-pekin.mp4"
    ]
    player = RandomMoviePlayer(video_paths)
    player.play()


