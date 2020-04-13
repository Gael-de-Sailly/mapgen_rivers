local function distance_to_segment(x1, y1, x2, y2, x, y)
	-- get the distance between point (x,y) and segment (x1,y1)-(x2,y2)
	local a = (x1-x2)^2 + (y1-y2)^2
	local b = (x1-x)^2 + (y1-y)^2
	local c = (x2-x)^2 + (y2-y)^2
	if a + b < c then
		return math.sqrt(b)
	elseif a + c < b then
		return math.sqrt(c)
	else
		return math.abs(x1 * (y2-y) + x2 * (y-y1) + x * (y1-y2)) / math.sqrt(a)
	end
end

local function transform_quadri(X, Y, x, y)
	-- X, Y 4-vectors giving the coordinates of the 4 nodes
	-- x, y position to index.
	local x1, x2, x3, x4 = unpack(X)
	local y1, y2, y3, y4 = unpack(Y)

	local d12 = distance_to_segment(x1,y1,x2,y2,x,y)
	local d34 = distance_to_segment(x3,y3,x4,y4,x,y)
	local xc = d12 / (d12+d34)

	local d23 = distance_to_segment(x2,y2,x3,y3,x,y)
	local d41 = distance_to_segment(x4,y4,x1,y1,x,y)
	local yc = d41 / (d23+d41)
	return xc, yc
end

local function area(X, Y) -- Signed area of polygon, in function of direction of rotation. Clockwise = positive.
	local n = #X
	local sum = X[1]*Y[n] - X[n]*Y[1]
	for i=2, n do
		sum = sum + X[i]*Y[i-1] - X[i-1]*Y[i]
	end

	return sum/2
end

return {
	distance_to_segment = distance_to_segment,
	transform_quadri = transform_quadri,
	area = area,
}
