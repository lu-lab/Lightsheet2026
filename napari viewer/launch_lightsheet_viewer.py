import numpy as np
import napari
from napari.qt.threading import WorkerBase

import lightsheet
from time import perf_counter, sleep


def update_volume(n, data):
    z = n % 31
    if z == 30:
        # trigger data changed event
        viewer.layers[0].data = viewer.layers[0].data
        viewer.layers[1].data = viewer.layers[1].data
    else:
        # just copy buffer data to image layer
        channels = np.hsplit(data,2)
        viewer.layers[0].data[z,:] = channels[0]
        viewer.layers[1].data[z,:] = channels[1]
        
    
"""
class BufferWatcher(WorkerBase):
    
    def __init__(self, buffer_name, update_function):
        self._buffer_name = buffer_name
        self._updatefunc = update_function
        super().__init__()

    def work(self):
        with lightsheet.ImageBufferView(self._buffer_name) as buffer:
            handled = 0
            while not self.abort_requested:
                if handled > buffer.written():
                    # assume buffer has reset to 0 and may have started writing again
                    handled = 0
                    
                for n in range(handled, buffer.written()):
                    self._updatefunc(n, buffer.get_frame(n))

                handled = buffer.written()
                sleep(.01)
            else:
                self.aborted.emit()

                
                
worker = BufferWatcher('test_buffer', update_volume)
worker.start()
napari.run()

"""