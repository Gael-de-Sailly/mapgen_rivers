local function load_map(filename, bytes, signed)
	local file = io.open(filename, 'r')
	local data = file:read('*all')

	local map = {}

	local size = math.floor(#data/bytes)

	for i=1, size do
		local i0, i1 = (i-1)*bytes+1, i*bytes
		local elements = {data:byte(i0, i1)}
		local n = elements[1]
		if signed and n >= 128 then
			n = n - 256
		end

		for j=2, bytes do
			n = n*256 + elements[j]
		end

		map[i] = n
	end
	file:close()

	return map
end

return load_map