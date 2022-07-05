import heapq, os

class binaryTree:
	def __init__(self, value, freq):
		self.value = value
		self.freq = freq
		self.left = None
		self.right = None
	def __lt__(self, other):
		return (self.freq < other.freq)


	def __eq__(self, other):
		return (self.freq == other.freq)

class huffmanCode:

	def __init__(self, path):
		self.path = path
		self.__heap = []
		self.__code = {}
		self.__revCode = {}



	def __frequency_from_text(self, text):
		frequency_dict = {}
		for char in text:
			if char not in frequency_dict:
				frequency_dict[char] = 0
			frequency_dict[char] += 1

		return frequency_dict


	def __Build_heap(self, frequency_dict):
		for key in frequency_dict:
			freq = frequency_dict[key]
			binaryTreeNode = binaryTree(key, freq)
			heapq.heappush(self.__heap, binaryTreeNode)


	def __Build_Binary_Tree(self):
		while len(self.__heap) > 1:
			binary_tree_node_1 = heapq.heappop(self.__heap)
			binary_tree_node_2 = heapq.heappop(self.__heap)
			sum_of_freq = binary_tree_node_2.freq + binary_tree_node_1.freq
			newNode = binaryTree(None, sum_of_freq)
			newNode.left = binary_tree_node_1
			newNode.right = binary_tree_node_2
			heapq.heappush(self.__heap, newNode)
		return 


	def __Build_Tree_Code_helper(self, root, curr_bits):
		if root is None:
			return
		if root.value is not None:
			self.__code[root.value] = curr_bits
			self.__revCode[curr_bits] = root.value
			return
		self.__Build_Tree_Code_helper(root.left, curr_bits+'0')
		self.__Build_Tree_Code_helper(root.right, curr_bits+'1')

	def __Build_Tree_Code(self):
		root = heapq.heappop(self.__heap)
		self.__Build_Tree_Code_helper(root, '')
		return

	def	__Build_Encoded_Text(self, text):
		encoded_text = ''
		for char in text:
			encoded_text += self.__code[char]
		return encoded_text

	def __Build_padded_Text(self, text):
		padding_value = 8 - len(text) % 8

		for i in range(padding_value):
			text += '0'

		padded_info = "{0:08b}".format(padding_value)
		padded_text = padded_info + text

		return padded_text

	def __Build_Bytes_Array(self, padded_text):
		array = []
		for i in range(0, len(padded_text), 8):
			byte = padded_text[i:i+8]
			array.append(int(byte, 2))

		return array

	def compression(self):
		print("compression starts....")
	#	to access the file and extract text from it
		fileName, file_extension = os.path.splitext(self.path)
		output_path = fileName + '.bin'
		with open(self.path, 'r+') as file, open(output_path, 'wb') as output:
			text = file.read()
			text = text.rstrip()

		#	calculate the freq of each text and store it in freq dict
			frequency_dict = self.__frequency_from_text(text)
		#	Min heap for two min freq
			build_heap = self.__Build_heap(frequency_dict)
		#	construct binary tree from heap
			self.__Build_Binary_Tree()
		#	construct code from binary tree and store it in dictionary
			self.__Build_Tree_Code()
		#	construct the encoded text
			encoded_text = self.__Build_Encoded_Text(text)
		#	padding of encoded text
			padded_text = self.__Build_padded_Text(encoded_text) 
		#	we have t return that binary fle as an output
			bytes_array = self.__Build_Bytes_Array(padded_text)
			final_bytes = bytes(bytes_array)
			output.write(final_bytes)

		print("Compressed successfully")
		return output_path


	def __removingPadding(self, text):
		padded_info = text[:8]
		padding_value = int(padded_info, 2)
		text = text[8:]
		text = text[:-1*padding_value]
		return text

	def __decodedText(self, text):
		current_bits = ''
		decoded_text = ''
		for char in text:
			current_bits += char
			if current_bits in self.__revCode:
				decoded_text += self.__revCode[current_bits]
				current_bits = ''
		return decoded_text

	def decompress(self, input_path):
		fileName, file_extension = os.path.splitext(input_path)
		output_path = fileName + '_decompressed' + '.txt'
		with open(input_path, 'rb') as file, open(output_path, 'w') as output:
			bit_string = ''
			byte = file.read(1)
			while byte:
				byte = ord(byte)
				bits = bin(byte)[2:].rjust(8,'0')
				bit_string += bits
				byte = file.read(1)

			text_after_removing_padding = self.__removingPadding(bit_string) 
			actual_text = self.__decodedText(text_after_removing_padding)
			output.write(actual_text)

		return output_path
path = input("ENTER THE PATH OF FILE TO BE COMPRESSED...")
h = huffmanCode(path)
compressed_file = h.compression()
h.decompress(compressed_file)