OriginalSeaIceArea = 1000000
SurfaceTempChange = 0.04
NewSeaIceArea = OriginalSeaIceArea * (1-SurfaceTempChange)
SeaLevelChange = (NewSeaIceArea - OriginalSeaIceArea) / OriginalSeaIceArea * 100 * 20
print("NewSeaIceArea: ", NewSeaIceArea, "km^2")
print("SeaLevelChange: ", SeaLevelChange, "mm")