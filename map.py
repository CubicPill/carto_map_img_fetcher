import requests
from threading import Thread
import os, sys, getopt
from queue import Queue
from splice import splice_img

all_count = 0
success_count = 0
zoom = None
cdn_server = 'a'
base_map = 'light'
retina = False
splice = False
img_name = 'spliced'


class Downloader(Thread):
    def __init__(self, queue):
        self.queue = queue
        Thread.__init__(self)

    def run(self):
        while not self.queue.empty():
            key = self.queue.get()
            suffix = ''
            if retina:
                suffix = '@2x'
            url = 'http://{}.basemaps.cartocdn.com/{}_all/{}/{}{}.png'.format(cdn_server, base_map, zoom, key, suffix)
            try:
                downloadImageFile(url)
                global success_count
                global success_count
                success_count += 1
                print('{}: key {} done {}/{}'.format(self.name, key, success_count, all_count))
            except:
                print('*****************FAILURE***************** {}'.format(key))
                self.queue.put(key)


def downloadImageFile(imgUrl):
    local_filename = imgUrl.split('/')[-2] + '_' + imgUrl.split('/')[-1]
    r = requests.get(imgUrl, stream=True, timeout=20)  # here we need to set stream = True parameter
    with open('./map_img/' + local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
    return local_filename


def print_help():
    print('Parameters:')
    print('-h             help')
    print('   --xmin      min x tile')
    print('   --xmax      max x tile')
    print('   --ymin      min y tile')
    print('   --ymax      max y tile')
    print('-z --zoomlevel zoom level(0-19)')
    print('-c --server=   cdn server for Carto, can be "a", "b" or "c", default "a"')
    print('-b --base      base map layer, can be "light" or "dark", default "light"')
    print('-t --thread    number of threads used for scraping, default 32')
    print('-r --retina    fetch high-resolution image for retina display')
    print('-s --splice    splice images after fetching')


def main():
    if not sys.argv[1:]:
        print_help()
        sys.exit(0)
    x_min = None
    x_max = None
    y_min = None
    y_max = None
    pool_size = 32
    if not os.path.isdir('map_img'):
        os.mkdir('map_img')
    short_args = 'hrz:st:b:c:'
    long_args = ['xmin=', 'xmax=', 'ymin=', 'ymax=', 'zoomlevel=', 'server=', 'base=', 'retina', 'splice', 'help',
                 'thread=']
    opts, args = getopt.getopt(sys.argv[1:], short_args, long_args)
    for opt, value in opts:
        if opt == '--xmin':
            x_min = int(value)
        elif opt == '--xmax':
            x_max = int(value)
        elif opt == '--ymin':
            y_min = int(value)
        elif opt == '--ymax':
            y_max = int(value)
        elif opt == '-z' or opt == '--zoom':
            global zoom
            zoom = int(value)
        elif opt == '-r' or opt == '--retina':
            global retina
            retina = True
        elif opt == '--server' or opt == '-c':
            global cdn_server
            cdn_server = value
        elif opt == '--base' or opt == '-b':
            global base_map
            base_map = value
        elif opt == '-s' or opt == '--splice':
            global splice
            splice = True
            if value:
                global img_name
                img_name = value
        elif opt == '-t' or opt == '--thread':
            pool_size = int(value)
        elif opt == '-h' or opt == '--help':
            print_help()
            sys.exit(0)
    if x_min is None or x_max is None or y_min is None or y_max is None or zoom is None:
        print('Missing parameters!')
        sys.exit(1)
    print('x:({},{}),y:({},{}),z={},server={},base_map={},retina={},splice={},thread_number={}'
          .format(x_min, x_max, y_min, y_max, zoom, cdn_server, base_map, retina, splice, pool_size))
    print('Proceed? (y/n)')
    if input() != 'y':
        sys.exit('Exited')
    keys_queue = Queue()

    x_range = list(range(x_min, x_max))
    y_range = list(range(y_min, y_max))
    for y in y_range:
        for x in x_range:
            key = '{}/{}'.format(x, y)
            keys_queue.put(key)
    global all_count
    all_count = keys_queue.qsize()

    thread_pool = []
    for i in range(0, pool_size):
        img_thread = Downloader(keys_queue)
        thread_pool.append(img_thread)
    for img_thread in thread_pool:
        img_thread.start()
    for img_thread in thread_pool:
        img_thread.join()
    print('Map tile images fetching done!')

    if splice:
        print('Start splicing...')
        splice_img(x_min, x_max, y_min, y_max, img_name, retina)
        print('Image splicing done!')


if __name__ == '__main__':
    main()
