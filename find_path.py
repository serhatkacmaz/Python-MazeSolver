# Bu projede text dosyası içerisinde yollanan labirentin durumuna göre klasik veya güçlendirme noktasına göre,
# labirent çözümünü yapan program.

import sys

# region Argüman alma ve kontrolü


def Application_Exit():
    print('Çıkılıyor...')
    sys.exit()


# Argüman eksik yada fazla olma durumunda programdan çık
if len(sys.argv) < 3:
    print('Gerekli parametreleri girmediniz!')
    Application_Exit()
elif len(sys.argv) > 3:
    print('Çok fazla parametre girdiniz!')
    Application_Exit()
else:
    entry = sys.argv[1]
    output = sys.argv[2]

# endregion

# region Textde labirent okuma ve yazma


def Text_Read(path):
    """Gelen text dosyasını okuyup labirent yapar."""
    try:
        file = open(path, 'r')
        list = [i.strip('\n') for i in file]  # dosya içinden satırları al
        # her bir satırdaki karekterleri al listele
        list = [[j for j in i] for i in list]
        file.close()
        return list  # satır sütün halde
    except FileNotFoundError as e:
        print("Girdi Dosyası ismi yanlış girildi veya bulunamadı.")


def Text_Write(file, list):
    """Dosyaya gelen labirenti yazma"""
    file = open(output, 'w')  # dosyada yazma yap
    for i in list:
        text = str(i).strip("[]").replace("'", "") + \
            "\n"  # liste satırlarını yaz
        file.writelines(text)
    file.close()
    if entry == 'strong_entry.txt':
        print("Güclendirme hücresinden geçilerek çikti dosyası yazdırıldı.")
    else:
        print("klasik yöntem ile cikti dosyası yazdırıldı.")

# endregion

# region Yolları numaralandırma ve Yolu bul

# Baslangıc noktasında varıs noktasına kadar gidilen tüm boş yolları numaralandıran özyinelemeli fonksiyon.
# karakter parametresi güçlendirme noktalı labirenti çözmebilmek içindir.


def Number_The_Paths(maze, x, y, character, k=0):  # x satır, y sütün
    """Gelen Labirentin başlangıçtan varış noktasına kadar olan tüm yolları numaralandırır."""
    if maze[x][y] != 'W':   # W haricinde karakter varsa numaralandır
        maze[x][y] = k+1
    # Hücrelerde gidebilecek yön kontrollerini ve hücre varsa yani yol varsa hücreye git
    # sol
    if y > 0 and (maze[x][y-1] == 'P' or maze[x][y-1] == character):
        Number_The_Paths(maze, x, y-1, character, k+1)

    # yukarı
    if x > 0 and (maze[x-1][y] == 'P' or maze[x-1][y] == character):
        Number_The_Paths(maze, x-1, y, character, k+1)

    # sağ
    if y < (len(maze[0])-1) and (maze[x][y+1] == 'P' or maze[x][y+1] == character):
        Number_The_Paths(maze, x, y+1, character, k+1)

    # asagı
    if x < (len(maze)-1) and (maze[x+1][y] == 'P' or maze[x+1][y] == character):
        Number_The_Paths(maze, x+1, y, character, k+1)


# yolu_bul metodunda numaralandırmıs yollarda bitiş noktasından geriye dogru giderek,
# başlanıgaca göre en iyi rotayı bulan bir özyinelemeli fonksiyon.

def Find_The_Path(x, y, k, stop):
    """Numaralanan hücrelerden istenilen iki hücre arasındaki yolu al"""
    # dur başlangıçın numara karşılığı, numaralandırmada başlangıca gelirse false dön
    if k < stop:
        return False
    # Rotayı bulurken hücreyi 1 yap
    # yukarı
    if x > 0 and maze[x-1][y] == k-1:
        x -= 1
        maze[x][y] = '1'
        best_Path.append([x, y])
    # sol
    elif y > 0 and maze[x][y - 1] == k-1:
        y -= 1
        maze[x][y] = '1'
        best_Path.append([x, y])
    # aşagı
    elif x < (len(maze)-1) and maze[x + 1][y] == k-1:
        x += 1
        maze[x][y] = '1'
        best_Path.append([x, y])
    # sag
    elif y < (len(maze[0])-1) and maze[x][y + 1] == k-1:
        y += 1
        maze[x][y] = '1'
        best_Path.append([x, y])
    Find_The_Path(x, y, k-1, stop)

# endregion

# region Diger fonksiyonlar


def Find_Index(matris, sembol):
    """Labirentde istenilen sembolun kordinatını verir."""
    for x, line in enumerate(matris):
        try:
            return x, line.index(sembol)  # girilen sembolun satır sütün döner
        except ValueError:
            pass

# labirenti cözümlü hale getirme yani W harfini ve yolda olmayan P harflerini 0 yap ve cözüm yolunu 1
# sonrasında cozumlu listeyi text dosyasına yaz.


def Maze_End_Solution():
    """Labirentdeki dogru yolu 1 diger hücreleri 0 yapıp texte yaz."""
    solution = []
    for i in range(maze_row):
        row = []
        for j in range(maze_column):
            # labirenttin inidislerinde dolaş ve en_iyi_yol listesinde bulunan indisleri 1 yap
            if [i, j] in best_Path:
                row.append(1)
            else:
                row.append(0)
        solution.append(row)
    # Başlangıç ve bitiş noktaları S ve F olarak çözümde olsun
    solution[start_x][start_y] = 'S'
    solution[finish_x][finish_y] = 'F'

    # cözümü txt dosyasına yaz
    Text_Write(output, solution)
# endregion

# region Main


best_Path = []  # labirent cözümünü tutan global liste
maze = []  # text dosyasından gelen karakterlerle labirent oluştur
maze = Text_Read(entry)  # girdi dosyaysını okutma ve labirent listesine atma

# satır sütün boyutu
maze_row = len(maze)
maze_column = len(maze[0])

# Başlangıç ve bitiş kordinatları
start_x, start_y = Find_Index(maze, 'S')
finish_x, finish_y = Find_Index(maze, 'F')

# H güç noktası var ise H noktasının kordinatını al
H_x, H_y = 0, 0
if entry == 'strong_entry.txt':
    H_x, H_y = Find_Index(maze, 'H')

# girdi.txt olarak gelen dosyada işlem klasik
if entry == 'entry.txt':
    # labirentde gidilecek yollları numaralandır
    Number_The_Paths(maze, start_x, start_y, "F")
    # en_iyi_yol listesi, baslangic ve bitis noktasıda dahil tutar
    best_Path = [[finish_x, finish_y]]
    k = maze[finish_x][finish_y]
    # rotayı bul
    Find_The_Path(finish_x, finish_y, k, maze[start_x][start_y])
    Maze_End_Solution()
else:  # H güçlendirme noktası ilen gelen dosyada S-H arası sonrasında H-F arası yol bulma
    # S - H arası yolu bul
    Number_The_Paths(maze, start_x, start_y, 'H')
    best_Path = [[H_x, H_y]]
    k = maze[H_x][H_y]
    Find_The_Path(H_x, H_y, k, maze[start_x][start_y])

    # labirent üstünde S -  H arasında numaralandırmadan sonra değişen labirenti
    # H - F arası için düzelt
    for i in range(maze_row):
        for j in range(maze_column):
            if maze[i][j] != 'W' and maze[i][j] != '1':
                maze[i][j] = 'P'
    maze[H_x][H_y] = 'H'

    # F - H arası yolu bulma
    Number_The_Paths(maze, H_x, H_y, 'F')
    k = maze[finish_x][finish_y]
    Find_The_Path(finish_x, finish_y, k, maze[H_x][H_y])
    Maze_End_Solution()

# endregion
