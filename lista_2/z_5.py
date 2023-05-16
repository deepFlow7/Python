import urllib.request

def compression(text) :
    l = len(text)
    i = 0
    compressed = []
    while i < l :
        counter = 1
        char = text[i]
        i += 1
        while i < l and text[i] == char :
            counter += 1
            i += 1
        compressed.append((counter, char))
    return compressed

def decompression(compressed_text):
    decompressed = ""
    for i in range(len(compressed_text)):
        for j in range(compressed_text[i][0]):
            decompressed += compressed_text[i][1]
    return decompressed

target_url = 'https://wolnelektury.pl/media/book/txt/do-mlodych.txt'
data = urllib.request.urlopen(target_url)
example = data.read().decode("utf-8") 


print ("compressed : {0}".format( compression (example)) )
print ('\n \n')
print ("decompressed : " + decompression(compression (example)))
