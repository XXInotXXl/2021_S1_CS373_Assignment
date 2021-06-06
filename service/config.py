from service.matrix import Matrix

VERTICAL_EDGE = Matrix.from_string("""
            -1  0   1
            -2  0   2
            -1  0   1
            """)
HORIZONTAL_EDGE = Matrix.from_string("""
            1   2   1
            0   0   0
            -1  -2  -1
            """)
EROSION_DILATION_4 = Matrix.from_string("""
            0   1   0
            1   1   1
            0   1   0
            """)
EROSION_DILATION_8 = Matrix.from_string("""
            1   1   1
            1   1   1
            1   1   1
            """)
