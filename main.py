import pybitcointools as pt
import random
import hashlib, os, thread, sys

def font_size():
    return 22
def width_between_circles():
    return 225
def height_between_circles():
    return 225
def number_of_rows():
    return 11
def number_of_columns():
    return 7
def frame_top():
    return 110
def frame_side():
    return 150
def circle_radius():
    return 45

BASE58 = '23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
#Generate a random, well-formed mini private key#
def Candidate():
    return('%s%s' % ('S', ''.join(
        [BASE58[ random.randrange(0,len(BASE58)) ] for i in range(29)])))

#Generate mini private keys and output the mini key#
def GenerateKeys(numKeys = 10):
    keysGenerated = 0
    totalCandidates = 0
    out=[]
    while keysGenerated < numKeys:
        try:
            cand = Candidate()
            t = '%s?' % cand
            candHash = hashlib.sha256(t).digest()
            if candHash[0] == '\x00':
                privateKey = GetPrivateKey(cand)
                if CheckShortKey(cand):
                    out.append({'mini':cand, 'priv':privateKey, 'pub':pt.privtopub(privateKey)})
                else:
                    print('Invalid!')
                keysGenerated += 1
            totalCandidates += 1
        except KeyboardInterrupt:
            break
    return out

#Returns the hexadecimal representation of the private key#
def GetPrivateKey(shortKey):
    if CheckShortKey(shortKey):
        return hashlib.sha256(shortKey).hexdigest()
    else:
        print('Typo detected in private key!')
        return None

#Checks for typos in the short key#
def CheckShortKey(shortKey):
    if len(shortKey) != 30:
        return False
    t = '%s?' % shortKey
    tHash = hashlib.sha256(t).digest()
    # Check to see that first byte is \x00
    if tHash[0] == '\x00':
        return True
    return False

#Drawing#
def draw_num(filename, num, x, y):
    x=str(x)
    y=str(y)
    num=str(num)
    os.system('''convert {} -pointsize {} -fill black -draw "text {},{} '{}'" {}'''.format(filename, str(font_size()), x, y, num, filename))

def draw_circle(filename, nums, x, y):#4,7,8,7,4
    s=font_size()
    num=nums['mini']
    len1=24.0/45*circle_radius()
    len2=8.0/45*circle_radius()
    draw_num(filename, num[:4], x+len1, y)
    draw_num(filename, num[4:11], x+len2, y+1*s)
    draw_num(filename, num[11:19], x, y+2*s)
    draw_num(filename, num[19:26], x+len2, y+3*s)
    draw_num(filename, num[26:], x+len1, y+4*s)

def draw_line(filename, nums, x, y):
    num=nums['pub']
    addr=pt.pubkey_to_address(num)
    draw_num(filename, addr[:8], x , y)

def draw_circle_line(filename, nums, x, y):
    draw_circle(filename, nums, x, y)
    draw_line(filename, nums, x, y+height_between_circles()+circle_radius())
def int2padded_string(n, digits):
    n=str(n)
    while len(n)<digits:
        n='0'+n
    return n
def gen_row(height, file, column_number, column_total, sheet_num, digits):
    rows=number_of_rows()
    keys=GenerateKeys(rows)
    width=width_between_circles()
    f=int2padded_string
    for i in range(rows):
        if True:#i==3:
            draw_circle_line(file, keys[i], frame_top()+i*width, frame_side()+height)
            print('Sticker #{} of Row #{} of Sheet #{}.....................Done'.format(f(i + 1, digits), f(column_number + 1, digits), f(sheet_num+1, digits)))
    pubs=[]
    for i in keys:
        pubs.append(pt.pubkey_to_address(i['pub']))
    return pubs
def number_the_file(file, digits, number):
    #assume 4 char postfix, i.e. '.png'
    number=int2padded_string(number+1, digits)
    return file[:-4]+number+file[-4:]
def gen_pages(sticker_file, addresses_file, pages):
    digits=len(str(pages))
    for i in range(int(pages)):
        numbered_sticker_file=number_the_file(sticker_file, digits, i)
        numbered_addresses_file=number_the_file(addresses_file, digits, i)
        print('cp ol32blank.png {}'.format(numbered_sticker_file))
        os.system('cp ol32blank.png {}'.format(numbered_sticker_file))
        error('here')
        os.system("cls")
        pubs=[]
        col=number_of_columns()
        for j in range(col):
            if True:#j==3:
                pubs.extend(gen_row(j*2*height_between_circles(), numbered_sticker_file, j, col, i, digits))
        f=open(numbered_addresses_file, 'w')
        for i in pubs:
            f.write(i)
            f.write('\n')
        f.close()

input_var = input("How many sheets?: ")
gen_pages('sheets\stickersheet.png', 'sheets\publicsheet.txt', int(input_var))


