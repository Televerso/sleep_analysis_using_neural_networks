import src.video_processing.input_reader.GearReader as GearReader
import src.video_processing.input_reader.SimpleReader as SimpleReader
import src.video_processing.input_reader.DecordReader as DecordReader
import src.video_processing.input_reader.RSVideoReader as RSVideoReader
import src.video_processing.input_reader.MultiprocReader as MultiprocReader
import src.video_processing.input_reader.MultiprocReaderSM as MultiprocReaderSM

def decord_read_all(path_to_file):
    reader = DecordReader.DecordReader(path_to_file)
    frame_array = reader.read_all()
    reader.close()
    return frame_array

def decord_read_with_gap(path_to_file):
    reader = DecordReader.DecordReader(path_to_file)
    frame_array = reader.read_with_gap()
    reader.close()
    return frame_array

def gear_read_all(path_to_file):
    reader = GearReader.GearReader(path_to_file)
    frame_array = reader.read_all()
    reader.close()
    return frame_array

def gear_read_with_gap(path_to_file):
    reader = GearReader.GearReader(path_to_file)
    frame_array = reader.read_with_gap()
    reader.close()
    return frame_array

def cv2_read_all(path_to_file):
    reader = SimpleReader.SimpleReader(path_to_file)
    frame_array = reader.read_all()
    reader.close()
    return frame_array

def cv2_read_with_gap(path_to_file):
    reader = SimpleReader.SimpleReader(path_to_file)
    frame_array = reader.read_with_gap()
    reader.close()
    return frame_array

def rsv_read_all(path_to_file):
    reader = RSVideoReader.RSVideoReader(path_to_file)
    frame_array = reader.read_all()
    reader.close()
    return frame_array

def rsv_read_with_gap(path_to_file):
    reader = RSVideoReader.RSVideoReader(path_to_file)
    frame_array = reader.read_with_gap()
    reader.close()
    return frame_array

def mp_read_all(path_to_file):
    reader = MultiprocReader.MultiprocReader(path_to_file)
    frame_array = reader.read_all()
    reader.close()
    return frame_array

def mp_read_with_gap(path_to_file):
    reader = MultiprocReader.MultiprocReader(path_to_file)
    frame_array = reader.read_with_gap()
    reader.close()
    return frame_array

def mpsm_read_all(path_to_file):
    reader = MultiprocReaderSM.MultiprocReaderSM(path_to_file)
    frame_array = reader.read_all()
    reader.close()
    return frame_array

def mpsm_read_with_gap(path_to_file):
    reader = MultiprocReaderSM.MultiprocReaderSM(path_to_file)
    frame_array = reader.read_with_gap()
    reader.close()
    return frame_array
