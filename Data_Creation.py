import cv2
import random
import numpy as np
import math
import time
import os
from PIL import ImageFont, ImageDraw, Image

probability = [8.5, 5.6, 4.4, 9.0, 6.7, 7.5, 5.7, 6.7, 7.5]

def create(epoch):
    for cycle_number in range(9):
        if int((10-probability[cycle_number])*3) < random.randint(0, 20):
            #Size determination
            colour_black1 = 25
            colour_white1 = 178

            colour_black2 = 122
            colour_white2 = 186

            #Most equal ratio
            #Width: 225, Height: 160
            #1.4 times bigger
            #Least equal ratio
            #Width 275, Height: 100
            #2.75 times bigger

            height = random.randint(100,160)
            ratio_multiplier = 3/(height-99)
            width = int(ratio_multiplier*15) + 230

            #print(height)
            #print(width)

            center_x = int(width/2)
            center_y = int(height/2)

            #Choose colour scheme (Two possibilities)
            colour_scheme = random.randint(1,2)
            if colour_scheme == 1:
                use_black = colour_black1
                use_white = colour_white1
            if colour_scheme == 2:
                use_black = colour_black2
                use_white = colour_white2

            #Create image
            img = np.zeros((height, width), np.uint8)
            img[:] = use_white

            #Text generator

            # Make canvas and set the color
            ## Use simsum.ttc to write Chinese.
            fonts = ['AGENCYB.TTF', 'AGENCYR.TTF', 'ANTQUAB.TTF', 'ANTQUABI.TTF', 'ANTQUAI.TTF', 'arial.ttf', 'arialbd.ttf', 'arialbi.ttf', 'ariali.ttf', 'ARIALN.TTF', 'ARIALNB.TTF', 'ARIALNBI.TTF', 'ARIALNI.TTF', 'ariblk.ttf', 'ARLRDBD.TTF', 'bahnschrift.ttf','BASKVILL.TTF', 'BAUHS93.TTF', 'BELL.TTF', 'BELLB.TTF', 'BELLI.TTF', 'BERNHC.TTF', 'BKANT.TTF', 'BOD_B.TTF', 'BOD_BI.TTF','BOD_BLAI.TTF', 'BOD_BLAR.TTF', 'BOD_CB.TTF', 'BOD_CBI.TTF', 'BOD_CI.TTF', 'BOD_CR.TTF', 'BOD_I.TTF','BOD_R.TTF', 'BOOKOS.TTF', 'BOOKOSB.TTF', 'BOOKOSBI.TTF', 'BOOKOSI.TTF', 'BRITANIC.TTF','BRLNSDB.TTF', 'BRLNSR.TTF', 'BRUSHSCI.TTF', 'calibri.ttf', 'calibrib.ttf', 'calibrii.ttf','calibril.ttf', 'calibrili.ttf', 'calibriz.ttf', 'CALIFB.TTF', 'CALIST.TTF', 'CALISTB.TTF','CALISTBI.TTF', 'CALISTI.TTF', 'cambriab.ttf', 'cambriai.ttf', 'cambriaz.ttf', 'Candara.ttf', 'Candarab.ttf', 'Candarai.ttf','Candaraz.ttf', 'CENSCBK.TTF', 'CENTURY.TTF', 'comic.ttf', 'comicbd.ttf', 'comici.ttf','comicz.ttf', 'consola.ttf', 'consolab.ttf', 'consolai.ttf', 'consolaz.ttf','constan.ttf', 'constanb.ttf', 'constanz.ttf', 'COOPBL.TTF', 'COPRGTB.TTF', 'COPRGTL.TTF', 'corbel.ttf','corbelb.ttf', 'corbeli.ttf', 'corbelz.ttf', 'courbd.ttf', 'courbi.ttf', 'ebrima.ttf','ebrimabd.ttf', 'ERASBD.TTF', 'ERASDEMI.TTF', 'ERASMD.TTF','FRABK.TTF', 'FRABKIT.TTF', 'FRADM.TTF', 'FRADMCN.TTF', 'FRADMIT.TTF', 'FRAHV.TTF', 'FRAHVIT.TTF', 'framd.ttf','FRAMDCN.TTF', 'framdit.ttf', 'gadugi.ttf', 'gadugib.ttf','GARABD.TTF', 'georgia.ttf', 'georgiab.ttf', 'georgiai.ttf', 'georgiaz.ttf','GILBI___.TTF', 'GILB____.TTF', 'GILI____.TTF', 'GIL_____.TTF','GOTHICB.TTF', 'GOTHICBI.TTF', 'GOUDOSB.TTF','HELN.TTF', 'HTOWERT.TTF','HTOWERTI.TTF', 'impact.ttf', 'ITCKRIST.TTF','javatext.ttf', 'Lato-Regular.ttf', 'LBRITE.TTF', 'LBRITED.TTF','LBRITEDI.TTF', 'LBRITEI.TTF', 'LCALLIG.TTF', 'LeelaUIb.ttf', 'LeelawUI.ttf', 'LeelUIsl.ttf', 'LFAX.TTF', 'LFAXD.TTF','LFAXDI.TTF', 'LFAXI.TTF', 'LHANDW.TTF', 'LSANS.TTF', 'LSANSD.TTF', 'LSANSDI.TTF', 'LSANSI.TTF', 'LTYPE.TTF', 'LTYPEB.TTF','LTYPEBO.TTF', 'LTYPEO.TTF', 'lucon.ttf', 'l_10646.ttf', 'MAIAN.TTF', 'malgun.ttf', 'malgunbd.ttf','malgunsl.ttf', 'micross.ttf', 'mmrtext.ttf', 'mmrtextb.ttf', 'monbaiti.ttf','mvboli.ttf', 'Nirmala.ttf', 'NirmalaB.ttf','NirmalaS.ttf', 'ntailu.ttf', 'ntailub.ttf', 'pala.ttf', 'palab.ttf','PERBI___.TTF', 'PERB____.TTF','PERTIBD.TTF', 'phagspa.ttf', 'phagspab.ttf','REFSAN.TTF', 'ROCCB___.TTF', 'ROCK.TTF', 'ROCKB.TTF', 'ROCKBI.TTF', 'ROCKEB.TTF','ROCKI.TTF', 'SCHLBKB.TTF', 'SCHLBKBI.TTF', 'SCHLBKI.TTF', 'SCRIPTBL.TTF','segoeui.ttf', 'segoeuib.ttf', 'seguibl.ttf', 'seguibli.ttf', 'seguiemj.ttf', 'seguihis.ttf', 'seguisb.ttf', 'seguisbi.ttf','seguisym.ttf', 'SHOWG.TTF', 'sylfaen.ttf','tahoma.ttf', 'tahomabd.ttf', 'taile.ttf', 'taileb.ttf', 'TCBI____.TTF', 'TCB_____.TTF', 'TCCB____.TTF', 'TCCEB.TTF','timesbd.ttf','trebuc.ttf', 'trebucbd.ttf', 'trebucbi.ttf', 'trebucit.ttf', 'verdana.ttf', 'verdanab.ttf','verdanai.ttf', 'verdanaz.ttf']
            f = fonts[random.randint(0,len(fonts)-1)]
            fontpath = "C:/Users/Kaden McKeen/Desktop/Programming/Python/Machine Learning/Captcha Neural Network/Fonts/"+f
            font_size = random.randint(70,150)
            font = ImageFont.truetype(fontpath, font_size)
            x = center_x - font_size*0.4 + random.randint(0, int(width/2)) - width/4
            y = center_y - font_size*0.6 + random.randint(0, int(height/4)) - height/8
            img_pil = Image.fromarray(img)
            draw = ImageDraw.Draw(img_pil)
            draw.text((int(x), int(y)),  str(cycle_number+1), font = font, fill = use_black)
            img = np.array(img_pil)

            #cv2.imshow(f,img)
            #cv2.moveWindow(f, 100,100);
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()

            angle = random.randint(0, 50)-25
            M = cv2.getRotationMatrix2D((x, y), angle, 1.0)
            img = cv2.warpAffine(img, M, (width, height), borderMode=cv2.BORDER_CONSTANT, borderValue=use_white)

            #cv2.imshow(f,img)
            #cv2.moveWindow(f, 100,100);
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()
            
            #Noise generator
            for n in range(2):
                for i in range(img.shape[0]):
                    for j in range(img.shape[1]):
                        chance = int(math.sqrt(math.pow(i-center_y, 2) + math.pow(j-center_x, 2))/10)+2
                        if random.randint(1, chance) == 1:
                            img[i,j] = use_black

            #Lines generator
            lines = random.randint(100,200)
            m = []
            b = []
            for l in range(lines):
                time.sleep(0.001)
                m.append((random.randint(1,8)*0.5))
                if random.randint(1,2) == 1:
                    m[-1] *= -1
                b.append(random.randint(1,width*2))

            for i in range(img.shape[0]):
                for j in range(img.shape[1]):
                    for l in range(lines):
                        if int(i*m[l])+b[l] == j:
                            img[i,j] = use_black


            #Blob generator
            blobs = 10

            for bl in range(blobs):
                #Determine whether blob is randomly placed, or on one of the sides
                if random.randint(1,5) == 1:
                    x = random.randint(-15,width+15)
                    y = random.randint(-15,height+15)
                    r1 = random.randint(3,6)
                    r2 = random.randint(3,6)
                else:
                    side = random.randint(1,4)
                    r1 = random.randint(3,9)
                    r2 = random.randint(3,9)
                    if side == 1:
                        x = random.randint(-15,width+15)
                        y = 0
                    if side == 1:
                        x = random.randint(-15,width+15)
                        y = height
                    if side == 3:
                        x = 0
                        y = random.randint(-15,height+15)
                    if side == 4:
                        x = width
                        y = random.randint(-15,height+15)

                a = random.randint(0,360)
                cv2.ellipse(img, (int(x),int(y)), (int(r1),int(r2)), float(a), 0.0, 360.0, use_black, -1, cv2.LINE_AA, 0)

                #Create mini blobs around this one to make it seem more random
                for minis in range(random.randint(3,8)):
                    rr1 = int(min(r1,r2)*random.randint(1,5)/5)
                    rr2 = int(min(r1,r2)*random.randint(1,5)/5)
                    xx = x + random.randint(-min(r1,r2), min(r1,r2))
                    yy = y + random.randint(-min(r1,r2), min(r1,r2))
                    aa = float(a + random.randint(0,100)-50)
                    cv2.ellipse(img, (int(xx),int(yy)), (int(rr1),int(rr2)), float(aa), 0.0, 360.0, use_black, -1, cv2.LINE_AA, 0)

            #cv2.imshow(f,img)
            #cv2.moveWindow(f, 100,100);
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()
            cv2.imwrite('ComputerGenerated/'+str(cycle_number+1)+"-"+str(epoch)+".png",img)

