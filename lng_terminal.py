import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import Point
import cartopy.crs as ccrs

# LNG基地のデータを読み込み
df = pd.read_csv('lng_terminals.csv')

# GeoDataFrameの作成
geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
gdf = gpd.GeoDataFrame(df, geometry=geometry)

# プロット
fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'projection': ccrs.PlateCarree()})

# 世界地図のベースマップをプロット
ax.stock_img()
ax.coastlines()

# LNG基地のプロット
gdf.plot(ax=ax, color='red', markersize=50)

# LNG基地の名前をプロット
for x, y, label in zip(gdf.geometry.x, gdf.geometry.y, gdf['name']):
    ax.text(x + 0.5, y, label, fontsize=12, transform=ccrs.PlateCarree())

plt.show()