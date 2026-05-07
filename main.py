import struct

print(f"Python is {'64' if struct.calcsize('P') == 8 else '32'}-bit")