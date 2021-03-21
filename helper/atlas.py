from PyTexturePacker import Packer

def pack_test(dir):
    # create a MaxRectsBinPacker
    packer = Packer.create(max_width=2048, max_height=2048, bg_color=0xffffff00,atlas_format="json",enable_rotated=False)
    # pack texture images under directory "test_case/" and name the output images as "test_case".
    # "%d" in output file name "test_case%d" is a placeholder, which is a multipack index, starting with 0.
    packer.pack(dir, "test_case%d")


pack_test('../gui/ressources/textures/')