# Lu Lab lightsheet test code

from multiprocessing.shared_memory import SharedMemory
from ctypes import Structure, c_int
import numpy as np



class HEADER(Structure):  
    _fields_ = [
        ('buffer_frames', c_int),
        ('frames_written', c_int), # can be larger than buffer_frames (circular)
        ('frame_bytes', c_int),
        ('frame_width', c_int),
        ('frame_height', c_int),
        ('buffer_offset', c_int)
    ]
    
def get_frame(i, buffer, header):
    offset = (i % header.buffer_frames) * header.frame_bytes + header.buffer_offset
    out = np.frombuffer(buffer, offset=offset, count=header.frame_height*header.frame_width, dtype='uint16')
    return out.reshape((header.frame_height, header.frame_width))




class ImageBufferView:
    
    def __init__(self, name, dtype='uint16'):
        self._shared_memory = []
        self._header = []
        self._name = name
        self._dtype = dtype
        
    def __enter__(self):
        self._shared_memory = SharedMemory(self._name)
        self._header = HEADER.from_buffer(self._shared_memory.buf)
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        del self._header
        self._shared_memory.close()
        
    def written(self):
        return self._header.frames_written
    
    def buffer_size(self):
        return self._header.buffer_frames
    
    def get_frame(self, index):
        if index < self.written() - self.buffer_size():
            return None
        else:
            out = np.frombuffer(
                self._shared_memory.buf,
                offset=self._header.buffer_offset + (index % self.buffer_size())*self._header.frame_bytes,
                count=self._header.frame_width*self._header.frame_height,
                dtype=self._dtype)
            return out.reshape((self._header.frame_height, self._header.frame_width))