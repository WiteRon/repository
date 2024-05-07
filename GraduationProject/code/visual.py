binary_numbers = [
    "0", "10000", "10110", "100000", "110000", "10", "11000", "1000", "101000", "10010",
    "110010", "10100", "111000", "1010", "11010", "100001", "11100", "110100", "100010"
]

decimal_numbers = [int(binary, 2) for binary in binary_numbers]
print(binary_numbers)
print(decimal_numbers)


# 10000=16,1000 = 8