from moviepy.editor import VideoFileClip

class MoviePlayer:
    def __init__(self, video_path):
        self.video_path = video_path

    def play(self):
        # ビデオファイルを読み込む
        with VideoFileClip(self.video_path) as clip:
            # 動画をプレビューする
            clip.preview()



if __name__ == "__main__":
    player = MoviePlayer("/Users/matsudaichirou/workspace/dev/shuzo-shutyu-alarm/akiramennayo-shuzo.mp4")
    player.play()


