import zlib

f = open("in.mca", "rb")

chunk_offsets = []

for i in range(1024):
    offset_bytes = f.read(3)
    offset = int.from_bytes(offset_bytes, "big")
    f.seek(f.tell() + 1)
    chunk_offsets.append(offset)


chunks = []

for chunk_offset in chunk_offsets:
    if chunk_offset == 0:
        continue

    f.seek(chunk_offset * 4096)
    chunk_length = int.from_bytes(f.read(4), "big")

    f.seek(f.tell() + 1)
    chunk_bytes = f.read(chunk_length - 1)

    chunk_uncompressed = zlib.decompress(chunk_bytes)
    chunks.append(chunk_uncompressed)
f.close()

with open("chunk.nbt", "wb") as f:
    f.write(chunks[0])
