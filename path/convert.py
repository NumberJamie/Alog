from pathlib import Path

from PIL import Image, ImageOps
from moviepy.video.io.VideoFileClip import VideoFileClip

from modules import MsgType, Logger, Format, Id, Backup, OwnedDirs


class ConvertMedia:
    def __init__(self, path):
        self.path = Path(path)
        self.__token = Id().generate()
        self.__thumb_size = 256
        self.__preview_time = 0.25

    def __convert_video(self):
        path_format = Format(self.path)
        video_path = path_format.with_suffix('.webm')
        preview = path_format.get_in_folder('preview')
        video = VideoFileClip(str(self.path))
        if not path_format.is_in_folder('preview'):
            video.save_frame(preview, t=video.duration * self.__preview_time)
        if not path_format.is_web_format():
            video.write_videofile(str(video_path), codec="libvpx", bitrate="12000k", fps=30, preset="ultrafast",
                                  logger=None, audio_codec='libvorbis')
        video.close()
        if not path_format.is_web_format():
            self.path.unlink()
        if not Id().is_valid(self.path.stem):
            video_path = Path(video_path).rename(video_path.with_stem(self.__token))
            preview = preview.rename(preview.with_stem(self.__token))
        self.__create_thumb(video_path, preview)
        return video_path

    def __convert_image(self):
        path_format = Format(self.path)
        image_path = path_format.with_suffix('.webp')
        if not path_format.is_web_format():
            image = Image.open(self.path)
            image.save(image_path, format="webp")
            image.close()
            self.path.unlink()
        if not Id().is_valid(self.path.stem) and not Id().is_special(self.path.stem):
            image_path = Path(image_path).rename(image_path.with_stem(self.__token))
        if not Id().is_special(self.path.stem):
            self.__create_thumb(image_path, image_path)
        else:
            image_path.replace(Format(image_path).get_in_folder('profile'))
        return image_path

    def __create_thumb(self, path, to_open):
        thumb_path = Format(path).get_in_folder('thumb')
        if Format(path).is_in_folder('thumb'):
            return
        img = Image.open(to_open)
        thumbnail = ImageOps.fit(img, (self.__thumb_size, self.__thumb_size))
        thumbnail.save(thumb_path, format="webp")
        img.close()

    def convert(self):
        if not self.path.exists():
            Logger(MsgType.ERROR, f'Path {self.path} is non-existent.')
            return
        path_format = Format(self.path)
        new_path = None
        if path_format.is_image_format():
            new_path = self.__convert_image()
        elif path_format.is_video_format():
            new_path = self.__convert_video()
        if not str(self.path) == str(new_path):
            Logger(MsgType.INFO, f'File: {self.path} has been converted to: {new_path}.')
        return new_path


def convert():
    itr_folder = Path('../models')
    id_set = Backup(itr_folder).initialize()
    for folder in itr_folder.iterdir():
        OwnedDirs(folder).create()
        for file in folder.iterdir():
            if file.is_dir():
                continue
            if file.stem in id_set:
                continue
            path = ConvertMedia(file).convert()
            id_set.add(path.stem)
        Backup(itr_folder).write(id_set)
        Logger(MsgType.INFO, f'Finished folder: {folder}.')
    Logger(MsgType.INFO, f'Finished')
