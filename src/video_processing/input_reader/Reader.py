import src.video_processing.input_reader.DecordReader as DecordReader
import src.video_processing.input_reader.GearReader as GearReader
import src.video_processing.input_reader.SimpleReader as SimpleReader


def decord_read_all(path_to_file):
    reader = DecordReader.DecordReader(path_to_file)
    frame_list = reader.read_all()
    reader.close()
    return frame_list

def decord_read_with_gap(path_to_file):
    reader = DecordReader.DecordReader(path_to_file)
    frame_list = reader.read_with_gap()
    reader.close()
    return frame_list

def gear_read_all(path_to_file):
    reader = GearReader.GearReader(path_to_file)
    frame_list = reader.read_all()
    reader.close()
    return frame_list

def gear_read_with_gap(path_to_file):
    reader = GearReader.GearReader(path_to_file)
    frame_list = reader.read_with_gap()
    reader.close()
    return frame_list

def cv2_read_all(path_to_file):
    reader = SimpleReader.SimpleReader(path_to_file)
    frame_list = reader.read_all()
    reader.close()
    return frame_list

def cv2_read_with_gap(path_to_file):
    reader = SimpleReader.SimpleReader(path_to_file)
    frame_list = reader.read_with_gap()
    reader.close()
    return frame_list
