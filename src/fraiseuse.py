'''
Created on 16 oct. 2012

@author: guill
'''


class fraiseuse( object ):
    '''
    classdocs
    '''


    def __init__( self, params, height ):
        '''
        Constructor
        '''
        self.table = params # rectangle (x,y,xb,yb) definit la taille de la table x et y sont les point zero d'origine
        self.height = height # [0] hauteur [1] largeur
        self.zeroMachine = [self.table[0], self.table[3], 0.0]
        self.brocheMachine = [self.table[0], self.table[3], 0.0]# (x,y,z)
        self.zeroVirtuel = [self.table[0], self.table[3], 0.0]
        self.mm = 5.03
        self.axe0X = [0, self.zeroMachine[1], self.height[1], self.zeroMachine[1]]
        self.axe0Y = [self.zeroMachine[0], 0, self.zeroMachine[0], self.height[0]]



    def get_posBrocheMachine( self ):
        return self.brocheMachine

    def afficheBrocheMachine( self ): # renvoi la position en mm par raport au zeroMachine
        postemp = [( self.zeroMachine[0] - self.brocheMachine[0] ) / self.mm , ( self.brocheMachine[1] - self.zeroMachine[1] ) / self.mm , self.brocheMachine[2] ]
        return postemp


    def get_zeroMachine( self ):
        return self.zeroMachine


    def get_posZeroVirtuel( self ): # position dans le canvas
        return self.zeroVirtuel

    def afficheZeroVirtuel( self ): # renvoi la position en mm par rapport au zeroMachine
        postemp = [( self.zeroMachine[0] - self.zeroVirtuel[0] ) / self.mm , ( self.zeroVirtuel[1] - self.zeroMachine[1] ) / self.mm , self.zeroVirtuel[2] ]
        return postemp


    def get_table( self ):
        return self.table

    def set_axe( self, param ):
        postemp = [param[0], param[1], self.brocheMachine[2]]
        self.zeroVirtuel = postemp
        self.axe0X = [0, self.get_posZeroVirtuel()[1], self.height[1], self.get_posZeroVirtuel()[1]]
        self.axe0Y = [self.get_posZeroVirtuel()[0], 0, self.get_posZeroVirtuel()[0], self.height[0]]


    def gohome( self ):
        self.brocheMachine = [self.get_posZeroVirtuel()[0], self.get_posZeroVirtuel()[1], self.get_posZeroVirtuel()[2]]

    def set_home( self ):
        self.zeroVirtuel = [self.get_posBrocheMachine()[0], self.get_posBrocheMachine()[1], self.get_posBrocheMachine()[2]]
        self.axe0X = [0, self.get_posZeroVirtuel()[1], self.height[1], self.get_posZeroVirtuel()[1]]
        self.axe0Y = [self.get_posZeroVirtuel()[0], 0, self.get_posZeroVirtuel()[0], self.height[0]]

    def homeReset( self ):
        self.zeroVirtuel = [self.get_zeroMachine()[0], self.get_zeroMachine()[1], self.get_zeroMachine()[2]]
        self.axe0X = [0, self.get_posZeroVirtuel()[1], self.height[1], self.get_posZeroVirtuel()[1]]
        self.axe0Y = [self.get_posZeroVirtuel()[0], 0, self.get_posZeroVirtuel()[0], self.height[0]]


    def y_movetor( self, param ):
        self.brocheMachine[0] = self.brocheMachine[0] + ( param * self.mm )

    def x_movetor( self, param ):
        self.brocheMachine[1] = self.brocheMachine[1] + ( param * self.mm )

    def y_movetoa( self, param ):
        self.brocheMachine[0] = self.zeroVirtuel[0] + ( param * self.mm )

    def x_movetoa( self, param ):
        self.brocheMachine[1] = self.zeroVirtuel[1] - ( param * self.mm )

    def get_vue_axe0X( self ):
        return self.axe0X

    def set_vue_axe0X( self, params ):
        self.axe0X = params

    def get_vue_axe0Y( self ):
        return self.axe0Y

    def set_vue_axe0Y( self, params ):
        self.axe0Y = params

    def set_BrocheMachine( self, param ):
        self.brocheMachine = [param[0], param[1], param[2]]


