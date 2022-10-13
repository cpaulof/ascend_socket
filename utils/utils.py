import struct
import zipfile
import numpy as np

def encode_array(array, compress=False):
    # bz2magic BZh91AY
    buffer = array.tobytes()
    if compress:
        buffer = zipfile.bz2.compress(buffer)
    dims = len(array.shape)
    fmt_string = '<B' + 'I'*dims
    fmt_string += '10s'
    fmt_string += 'I'
    data = struct.pack(fmt_string, dims, *array.shape, str(array.dtype).encode('utf=8'), len(buffer)) + buffer
    return struct.pack('I', len(data)) + data

def _decode_array(data):
    k = 0
    magic = b'BZh91AY'
    data_size, = struct.unpack('I', data[k:k+4])
    k+=4

    dims, = struct.unpack('B', data[k: k+1])
    k+=1
    shape = struct.unpack('I'*dims, data[k:k+(4*dims)])
    k+=4*dims

    dtype, = struct.unpack('10s', data[k:k+10])
    dtype = dtype.replace(b'\x00', b'').decode('utf-8')
    k+=10
    buffer_size, = struct.unpack('I', data[k:k+4])
    k+=4

    buffer = data[k:k+buffer_size]
    if buffer.startswith(magic):
        buffer = zipfile.bz2.decompress(buffer)
    
    array = np.frombuffer(buffer, dtype).reshape(shape)

    return array

