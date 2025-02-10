from pickletools import long1

import pygame

largeur_ecran=1500
hauteur_ecran=800


pygame.init()
screen = pygame.display.set_mode((largeur_ecran, hauteur_ecran))
pygame.display.set_caption("interface")
font=pygame.font.Font(None,36)

def button(x,y,largeur,hauteur,couleur,texte):
    pygame.draw.rect(screen,couleur,(x,y,largeur,hauteur))
    texte_surface=font.render(texte,True,(0,0,0))
    texte_rect=texte_surface.get_rect(center=(x+largeur//2,y+hauteur//2))
    screen.blit(texte_surface,texte_rect)

interface="démarage"
echap=False
runing=True
while runing:
    screen.fill((0,0,0))

    keys = pygame.key.get_pressed()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type== pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                echap=True

        if event.type== pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            print("cliquer")
            print(pos[0])
            if largeur_ecran-100<pos[0]<largeur_ecran-80 and hauteur_ecran-100<pos[1]<hauteur_ecran-80 and interface=="jeu" or interface=="jeu" and echap==True:
                print("BOUTON")
                interface="bouton"
                echap=False
            if interface=="bouton"and 0<pos[0]<20 and 0<pos[1]<20:
                interface="jeu"

            if interface=="démarage" and largeur_ecran//3<pos[0]<largeur_ecran//3+largeur_ecran//4 and hauteur_ecran//4<pos[1]<hauteur_ecran//4+100:
                interface="jeu"



    if interface=="jeu":
        pygame.draw.rect(screen,(255,0,0),(0,hauteur_ecran-200,largeur_ecran,200))  #case en bas pour stat
        pygame.draw.rect(screen,(255,0,0),(largeur_ecran-200,0,200,200))    #map
        pygame.draw.rect(screen,(0,255,0),(largeur_ecran-400,hauteur_ecran-200,100,200))  #fuel
        button(largeur_ecran-100,hauteur_ecran-100,20,20,(0,0,255),"T")

    elif interface=="bouton":
        button(0,0,20,20,(255,255,255),"X")
        pygame.draw.rect(screen,(0,255,0),(largeur_ecran//2,hauteur_ecran//2,200,200))
        button(largeur_ecran//2,hauteur_ecran//2,200,200,(0,255,0),"bienvenue dans les parametres")

    elif interface=="démarage":
        button(largeur_ecran//3,hauteur_ecran//4,largeur_ecran//4,100,(255,0,0),"Bienvenue dans OSS")



    pygame.display.flip()
    print(echap)
    echap=False
    pygame.time.Clock().tick(60)


