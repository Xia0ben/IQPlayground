from algorithm import VariableByte
from files import PostingList

p1 = PostingList()
p1.add_document(1, 200)
p1.add_document(2, 99)
p1.add_document(3, 90)
p1.add_document(4, 89)
p1.add_document(5, 25)

p2 = PostingList()
p2.add_document(6, 200)
p2.add_document(7, 99)
p2.add_document(8, 90)
p2.add_document(9, 89)
p2.add_document(10, 25)

numbers_input = [p1, p2]

print("Variable Byte Compression - we want to compress  : %s" % (", ".join(str(x) for x in numbers_input)))

bytes_output = VariableByte.encoding_pl_list(numbers_input)

print("Combine bytes objects into a single bytes object : %s" % bytes_output)

numbers_output = VariableByte.decoding(bytes_output)

print("Decode single bytes object to numbers : %s " % (", ".join(str(x) for x in numbers_output)))
