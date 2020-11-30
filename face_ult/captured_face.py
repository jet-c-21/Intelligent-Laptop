import dlib


class CapturedFace:
    def __init__(self):
        self.has_face = None
        self.face_count = 0
        self.face_list = list()
        self.detector_type = ''

    def __str__(self):
        text = f'Has Face: {self.has_face}\n'
        text += f'Face Count: {self.face_count}\n'
        text += f'Detector Type: {self.detector_type}\n'
        text += f'Face List:\n'
        for i, f in enumerate(self.face_list, start=1):
            text += f'\t Face-{i}: {str(f)}'
        return text.strip()

    def __getitem__(self, item) -> dlib.rectangle:
        return self.face_list[item]
