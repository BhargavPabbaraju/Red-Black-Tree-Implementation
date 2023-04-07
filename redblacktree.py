
import pygame as pg

class Node:
  def __init__(self,key):
    self.key = key
    self.left = None
    self.right = None
    self.parent = None
    self.color = 'R'


class RedBlackTree:
  def __init__(self):
    self.root = None
    self.width = 800
    self.node_radius = 20
  
  def sort(self):
    self.inorder(self.root)
  
  def inorder(self,root):
    if root:
      self.inorder(root.left)
      print(root.key)
      self.inorder(root.right)

  def min(self,root=None):
    if not root:
      root = self.root
    while root.left:
      root = root.left
    return root

  def max(self,root=None):
    if not root:
      root = self.root
    while root.right:
      root = root.right
    return root

  def successor(self,root=None):
    if root.right:
        return self.min(root.right)
    y = root.parent
    while y and root==y.right:
        root = y
        y=y.parent
    return y

   

  def predecessor(self,root=None):
    if root.left:
        return self.max(root.left)
    y = root.parent
    while y and root==y.left:
        root = y
        y=y.parent
    return y

  def find(self,key):
    root = self.root
    while root:
      if key == root.key:
        return root
      elif key<root.key:
        root = root.left
      else:
        root = root.right


  def search(self,key):
    root = self.find(key)
    if root:
      print(key,' Found ')
    else:
      print(key,' not found')

  
  def left_left_rotate(self,node,parent,grandparent):
    grandparent.left = parent.right
    parent.right = grandparent
    parent.parent = grandparent.parent
    if grandparent == self.root:
        self.root = parent
    elif grandparent == grandparent.parent.right:
        grandparent.parent.right = parent
    else:
        grandparent.parent.left = parent
    grandparent.parent = parent
    grandparent.color,parent.color = parent.color ,grandparent.color
  
  def left_right_rotate(self,node,parent,grandparent):
    parent.right = node.left
    node.left = parent
    node.parent = grandparent
    grandparent.left = node
    parent.parent = node
    self.left_left_rotate(parent,node,grandparent)
  
  def right_right_rotate(self,node,parent,grandparent):
    
    grandparent.right = parent.left
    parent.left = grandparent
    parent.parent = grandparent.parent
    if grandparent == self.root:
        self.root = parent
    elif grandparent == grandparent.parent.right:
        grandparent.parent.right = parent
    else:
        grandparent.parent.left = parent
    grandparent.parent = parent
    grandparent.color,parent.color = parent.color ,grandparent.color
  
  def right_left_rotate(self,node,parent,grandparent):
    parent.left = node.right
    node.right = parent
    node.parent = grandparent
    parent.parent = node
    self.right_right_rotate(parent,node,grandparent)

    
  
  

  
  def insert(self,key):
    node = Node(key)
    node.color = 'R'
    if self.root == None:
      self.root = node
    
    else:
      temp = self.root
      while temp.left or temp.right:
        if node.key<temp.key:
          if temp.left:
            temp = temp.left
          else:
            break
        if node.key>temp.key:
          if temp.right:
            temp = temp.right
          else:
            break
      

      node.parent = temp
      if node.key<temp.key:
        temp.left = node
      else:
        temp.right = node

    
    
    self.insert_fixup(node)

  def delete(self,node):
    parent = node.parent
    #No children
    if node.left == None and node.right == None:
      if node == self.root:
        self.root = None
      else:
        if node == parent.left:
          parent.left = None
        else:
          parent.right = None

    #One Left child
    elif node.right == None:
      if node == self.root:
        self.root = node.left
      else:
        if node == parent.left:
          parent.left = node.left
        else:
          parent.right = node.left

    #One Right child
    elif node.left == None:
      if node == self.root:
        self.root = node.right
      else:
        if node == parent.left:
          parent.left = node.right
        else:
          parent.right = node.right

          
    #Two children
    else:
      successor = self.successor(node)
      if successor == successor.parent.left:
        successor.parent.left = successor.right
      else:
        successor.parent.right = successor.right
      node.key = successor.key
      if successor.right:
        successor.right.parent = successor.parent
      
        

  def height(self,root):
    if not root:
        return 0
    return max(1+self.height(root.left),1+self.height(root.right))

  def draw(self,window,root,x,y,height):
        if not root:
            return
        color = (255,0,0) if root.color=='R' else (0,0,0)
        pg.draw.circle(window,color,(x,y),self.node_radius)
        font = pg.font.SysFont('Comic Sans MS', self.node_radius)
        text = font.render(str(root.key),True,(255,255,255))
        text_rect = text.get_rect(center=(x,y))
        window.blit(text,text_rect)
        x_offset = self.width// 2**(height+1)
        if root.left:
            pg.draw.line(window,(0,0,0),(x,y+self.node_radius),(x-x_offset,y+2*self.node_radius),2)
            self.draw(window,root.left,x-x_offset,y+2*self.node_radius,height+1)
        if root.right:
            
            pg.draw.line(window,(0,0,0),(x,y+self.node_radius),(x+x_offset,y+2*self.node_radius),2)
            self.draw(window,root.right,x+x_offset,y+2*self.node_radius,height+1)
    

  def visualize(self):
        window = pg.display.set_mode((self.width,self.width))
        pg.display.set_caption('Red Black Trees')
        pg.font.init()
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    return

            
            window.fill((255,255,255))
            self.draw(window,t.root,self.width//2,self.node_radius,1)
            pg.display.update()


  
  def insert_fixup(self,node):
    if not node:
      return 
    
    if node==self.root:
      node.color = 'B'
      return

    parent = node.parent
    if parent.color == 'R':
      grandparent = parent.parent
      if grandparent:
        if parent == grandparent.left:
          uncle = grandparent.right
        else:
          uncle = grandparent.left
        
        if uncle:
          if uncle.color == 'R':
            parent.color = 'B'
            uncle.color = 'B'
            grandparent.color = 'R'
            self.insert_fixup(grandparent)
            return

        if not uncle or uncle.color=='B':
            #LL
            if parent == grandparent.left and node == parent.left:
              self.left_left_rotate(node,parent,grandparent)
            
            #LR
            elif parent == grandparent.left and node == parent.right:
              self.left_right_rotate(node,parent,grandparent)
            
            #RR
            elif parent == grandparent.right and node == parent.right:
              self.right_right_rotate(node,parent,grandparent)
            
            #RL
            elif parent == grandparent.right and node == parent.left:
              self.right_left_rotate(node,parent,grandparent)
        


t = RedBlackTree()

f=open('input.txt')
nodes = map(int,f.read().split())
f.close()
for node in nodes:
  t.insert(node)
while True:
    print('Enter 1 for insert')
    print('Enter 2 for search')
    print('Enter 3 for min')
    print('Enter 4 for max')
    print('Enter 5 for successor')
    print('Enter 6 for predecessor')
    print('Enter 7 for delete')
    print('Enter 8 for sort')
    print('Enter 9 for visualize')
    print('Enter 10 to quit')
    print('-'*80)
    x=int(input('Enter choice: '))
    if x ==1:
        t.insert(int(input('Enter value to insert: ')))
    elif x==2:
      t.search(int(input('Enter value to search: ')))
    elif x==3:
      print('Mininimum value is',t.min().key)
    elif x==4:
       print('Maximum value is',t.max().key)

    elif x==5:
      key = int(input('Enter key: '))
      node = t.find(key)
      if not node:
        print(key,' not present')
      else:
        s=t.successor(node)
        if s:
            print('Successor of ',key,'is',s.key)
        else:
            print(key,'has no successor')

    elif x==6:
      key = int(input('Enter key: '))
      node = t.find(key)
      if not node:
        print(key,' not present')
      else:
        p=t.predecessor(node)
        if p:
            print('Predecessor of ',key,'is',p.key)
        else:
            print(key,'has no predecessor')
        

    elif x==7:
      key = int(input('Enter key: '))
      node = t.find(key)
      if not node:
        print(key,' not present')
      else:
        t.delete(node)
        print('Deleted ',key)

    elif x==8:
      t.sort()
      
    elif x==9:
        t.visualize()
    else:
        break

    print('Current Height of tree is',t.height(t.root))

    


