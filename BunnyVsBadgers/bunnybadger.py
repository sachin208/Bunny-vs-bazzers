import pygame
import random
import math
pygame.init()#initialize all imported modules

width=640
height=480

screen=pygame.display.set_mode((width,height))

keys=[False,False,False,False]

playerpos=[100,100]

file=open("highscore.txt",'r')
highscore=float(file.read())

badtimer=100
badtimer1=0
badguys=[[640,53]]
health=200-6#-6 to adjust green health in red health

acc=[0,0]
accuracy=0
arrows=[]

player=pygame.image.load('resources/images/dude.png')
wid=int(player.get_width())
hei=int(player.get_height())
grass=pygame.image.load('resources/images/grass.png')
castle=pygame.image.load('resources/images/castle.png')
arrow=pygame.image.load('resources/images/bullet.png')
badguyimg=pygame.image.load('resources/images/badguy.png')
badguyimg1=pygame.image.load('resources/images/badguy2.png')
badguyimg2=pygame.image.load('resources/images/badguy3.png')
healthbar=pygame.image.load('resources/images/healthbar.png')
healthimg=pygame.image.load('resources/images/health.png')
gameover = pygame.image.load("resources/images/gameover.png")
youwin = pygame.image.load("resources/images/youwin.png")

hit = pygame.mixer.Sound("resources/audio/explode.wav")
enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
hit.set_volume(0.05)
enemy.set_volume(0.05)
shoot.set_volume(0.05)
pygame.mixer.music.load('resources/audio/moonlight.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

starttime=0

while 1:
	f=0
	screen.fill(0)
	#fill screen with black before drawing anything
	for x in range (width//grass.get_width()+1):
		for y in range (height//grass.get_height()+1):
			screen.blit(grass, (x*grass.get_width(),y*grass.get_height()))
	
	screen.blit(castle,(0,20))
	screen.blit(castle,(0,130))
	screen.blit(castle,(0,240))
	screen.blit(castle,(0,350))
	
	font=pygame.font.Font(None,48)
	welc=font.render('Welcome to Bunny Vs Badgers',True,(0,0,0))
	press=font.render('Press Spacebar to Start the game.',True,(0,0,0))
	screen.blit(welc,(100,150))
	screen.blit(press,(85,250))
	pygame.display.flip()
	for event in pygame.event.get():
		if event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
			f=1
	if f==1:break

starttime=pygame.time.get_ticks()

running=1
exitcode=0
while running:
	badtimer-=1
	screen.fill(0)
	#fill screen with black before drawing anything
	for x in range (width//grass.get_width()+1):
		for y in range (height//grass.get_height()+1):
			screen.blit(grass, (x*grass.get_width(),y*grass.get_height()))
	
	screen.blit(castle,(0,20))
	screen.blit(castle,(0,130))
	screen.blit(castle,(0,240))
	screen.blit(castle,(0,350))
	
	mousepos = pygame.mouse.get_pos()
	angle = math.atan2(mousepos[1]-(playerpos[1]+hei//2),mousepos[0]-(playerpos[0]+wid//2))
	playerrot = pygame.transform.rotate(player,360- angle*57.2957795)
	playerpos1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2)
	screen.blit(playerrot, playerpos1) #draw one image onto another
	
	font = pygame.font.Font(None, 24)
	remaintime=font.render(str("Remaining Time:"),True, (0,0,0))
	timeRect=remaintime.get_rect()
	timeRect.topright=[585,5]
	survivedtext = font.render(str((61000-pygame.time.get_ticks()+starttime)//60000).zfill(2)+":"+str(((61000-pygame.time.get_ticks()+starttime)//1000)%60).zfill(2), True, (0,0,0))
	textRect = survivedtext.get_rect()
	textRect.topright=[635,5]
	screen.blit(remaintime, timeRect)
	screen.blit(survivedtext, textRect)
	screen.blit(healthbar,(5,5))
	for health1 in range(health):
		screen.blit(healthimg,(health1+8,8))

	index=0
	for bullet in arrows:
		velx=math.cos(bullet[0])*10
		vely=math.sin(bullet[0])*10
		bullet[1]+=velx
		bullet[2]+=vely
		if(bullet[1]<-10 or bullet[1]>640 or bullet[2]<-10 or bullet[2]>480):
			arrows.pop(index)
		else: index+=1
	for projectile in arrows:
		arrowrot=pygame.transform.rotate(arrow,360-projectile[0]*57.2957795)
		screen.blit(arrowrot,(projectile[1],projectile[2]))

	if badtimer==0:
		badguys.append([640,53+110*random.randint(0,3)])
		badtimer=100-badtimer1*2
		if badtimer1>=35:
			badtimer1=35
		else :
			badtimer1+=5
	index=0
	for badguy in badguys:
		badrect=pygame.Rect(badguyimg.get_rect())
		badrect.top=badguy[1]
		badrect.left=badguy[0]
		index1=0
		f=0
		for bullet in arrows:
			bullrect=pygame.Rect(arrow.get_rect())
			bullrect.left=bullet[1]
			bullrect.top=bullet[2]
			if badrect.colliderect(bullrect):
				acc[0]+=1
				badguys.pop(index)
				arrows.pop(index1)
				f=1
				enemy.play()
				break
			else: index1+=1
		if f==1:continue
		if badguy[0]<64:
			badguys.pop(index)
			health-=10
			hit.play()
		else :index+=1
		badguy[0]-=5
	for badguy in badguys:
		x=(640-badguy[0])//25
		bg=badguyimg
		if x%4==1 or x%4==3:bg=badguyimg1
		elif x%4==2: bg=badguyimg2
		screen.blit(bg, badguy)


	pygame.display.flip()#update the screen or portion if argument passed

	for event in pygame.event.get():#fetching events from the event queue
	    # check if the event is the X button 
	    if (event.type==pygame.QUIT) or (event.type==pygame.KEYDOWN and event.key==pygame.K_q):
	        # if it is quit the game
	        pygame.quit() # runs code that deactivates the pygame library
	        exit(0)#to terminate the program
	    if event.type==pygame.KEYDOWN:
	    	if event.key==pygame.K_UP:
	    		keys[0]=True
	    	elif event.key==pygame.K_LEFT:
	    		keys[1]=True
	    	elif event.key==pygame.K_DOWN:
	    		keys[2]=True
	    	elif event.key==pygame.K_RIGHT:
	    		keys[3]=True
	    elif event.type==pygame.KEYUP:
	    	if event.key==pygame.K_UP:
	    		keys[0]=False
	    	elif event.key==pygame.K_LEFT:
	    		keys[1]=False
	    	elif event.key==pygame.K_DOWN:
	    		keys[2]=False
	    	elif event.key==pygame.K_RIGHT:
	    		keys[3]=False
	    if event.type==pygame.MOUSEBUTTONDOWN:
	    	shoot.play()
	    	mousepos=pygame.mouse.get_pos()
	    	acc[1]+=1;
	    	angle=math.atan2(mousepos[1]-(playerpos[1]+hei//2),mousepos[0]-(playerpos[0]+wid//2))
	    	px=wid//2*math.cos(angle+45/57.2957795)
	    	py=hei//2*math.sin(angle+45/57.2957795)
	    	arrows.append([angle,playerpos1[0]+50,playerpos1[1]+32])
	
	if keys[0]:
	    playerpos[1]-=5
	elif keys[2]:
	    playerpos[1]+=5
	if keys[1]:
	    playerpos[0]-=5
	elif keys[3]:
	    playerpos[0]+=5

	if pygame.time.get_ticks()-starttime>=61000:
		running=0
		exitcode=1
	elif health<=0:
		running=0
		exitcode=0
	if acc[1]!=0:
		accuracy=acc[0]*1.0/acc[1]*100

color=[0,0,0]
result=youwin
if exitcode==0:
	color[0]=255
	result=gameover
else :color[1]=255

if(exitcode==1 and accuracy>=highscore):
	font=pygame.font.Font(None,46)
	text1=font.render('Congratulations! You made a highscore.',True,(0,255,0))
	screen.blit(text1,(20,100))
	file.close()
	file=open('highscore.txt','w')
	file.write(str(accuracy))
	file.close()

font = pygame.font.Font(None, 27)
text = font.render("Accuracy: %.2f" % (accuracy)+"%", True, color)
text1 = font.render("HighScore: %.2f" % (highscore)+"%", True, color)
textRect = text.get_rect()
textRect.centerx = screen.get_rect().centerx
textRect.centery = screen.get_rect().centery+27
text1Rect = text1.get_rect()
text1Rect.centerx = screen.get_rect().centerx
text1Rect.centery = screen.get_rect().centery+50
screen.blit(result, (0,0))
screen.blit(text, textRect)
screen.blit(text1, text1Rect)

while 1:
    for event in pygame.event.get():
        if (event.type==pygame.QUIT) or (event.type==pygame.KEYDOWN and event.key==pygame.K_q):
            pygame.quit()
            exit(0)
    pygame.display.flip()