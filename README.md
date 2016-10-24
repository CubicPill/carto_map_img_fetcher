#Carto image fetcher

A small script used to fetch map tile images from Carto basemap server.

Requirements:
>pip install -r requirements.txt

Usage:
```
-h             help
   --xmin      min x tile
   --xmax      max x tile
   --ymin      min y tile
   --ymax      max y tile
-z --zoomlevel zoom level(0-19)
-c --server=   cdn server for Carto, can be "a", "b" or "c", default "a"
-b --base      base map layer, can be "light" or "dark", default "light"
-t --thread    number of threads used for scraping, default 32
-r --retina    fetch high-resolution image for retina display
-s --splice    splice images after fetching
```
