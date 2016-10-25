from PIL import Image
import sys


def main():
    x_min = int(sys.argv[1])
    x_max = int(sys.argv[2])
    y_min = int(sys.argv[3])
    y_max = int(sys.argv[4])
    filename = int(sys.argv[5])
    retina = bool(sys.argv[6])
    splice_img(x_min, x_max, y_min, y_max, filename, retina)


def splice_img(x_tile_min, x_tile_max, y_tile_min, y_tile_max, name, retina):
    x_range = list(range(x_tile_min, x_tile_max))
    y_range = list(range(y_tile_min, y_tile_max))
    edge_size=256
    suffix = ''
    if retina:
        edge_size=512
        suffix = '@2x'
    new_img = Image.new('RGB', (len(x_range) * edge_size, len(y_range) * edge_size))


    for y in y_range:
        for x in x_range:
            image = Image.open('./map_img/{}_{}{}.png'.format(x, y, suffix))
            new_img.paste(image, ((x - x_range[0]) * edge_size, (y - y_range[0]) * edge_size))
    new_img.save('{}.png'.format(name))


if __name__ == '__main__':
    main()
