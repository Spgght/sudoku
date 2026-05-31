import random

def index(x,y):
    return x+9*y

def coords(i):
    return [i%9,i//9]

def checkvalid(grid,x,y,n):
    for i in range(9):
        a=grid[index(i,y)]
        if a == n:
            return False
    for i in range(9):
        a=grid[index(x,i)]
        if a == n:
            return False
    for X in range(3*(x//3),3*(x//3)+3):
        for Y in range(3*(y//3),3*(y//3)+3):
            a=grid[index(X,Y)]
            if a == n:
                return False
    return True

def fill(grid,i,order):
    idx=order[i]
    xy=coords(idx)
    valid=[]
    for n in range(1,10):
        if checkvalid(grid,xy[0],xy[1],n):
            valid.append(n)
    random.shuffle(valid)
    for n in valid:
        grid[idx]=n
        if i==len(order)-1:
            return grid
        end=fill(grid,i+1,order)
        if end:
            return end
    grid[idx]=0
    return False

def generatefull(grid=None):
    if grid is None:
        grid=[0]*81
    else:
        grid=grid[:]
    order=[]
    for i in range(81):
        if grid[i]==0:
            order.append(i)
    grid=fill(grid,0,order)
    return grid

def printgrid(grid,blank="-",spacing=""):
    s=""
    i=0
    for y in range(9):
        for x in range(9):
            if grid[i]==0:
                s+=blank
            else:
                s+=str(grid[i])
            if x<8:
                s+=spacing
            i+=1
        s+="\n"
    print(s)

def solve(grid):
    mvalid=[]
    mlen=10
    mindex=-1
    for y in range(9):
        for x in range(9):
            i=index(x,y)
            if grid[i]==0:
                valid=[]
                for n in range(1,10):
                    if checkvalid(grid,x,y,n):
                        valid.append(n)
                if valid==[]:
                    return False
                if len(valid)<mlen:
                    mlen=len(valid)
                    mvalid=valid
                    mindex=i
    if mindex==-1:
        return grid[:]
    nvalid=0
    for a in mvalid:
        grid[mindex]=a
        end=solve(grid)
        grid[mindex]=0
        if end==-1:
            return -1
        if end:
            nvalid+=1
            solution=end
        if nvalid>1:
            return -1
    if nvalid==0:
        return False
    return solution

def solvable(grid):
    solution=solve(grid)
    return solution!=-1 and solution

def difficulty(grid):
    mvalid=[]
    mlen=10
    mindex=-1
    for y in range(9):
        for x in range(9):
            i=index(x,y)
            if grid[i]==0:
                valid=[]
                for n in range(1,10):
                    if checkvalid(grid,x,y,n):
                        valid.append(n)
                if valid==[]:
                    return False,0
                if len(valid)<mlen:
                    mlen=len(valid)
                    mvalid=valid
                    mindex=i
    if mindex==-1:
        return grid[:],0
    nvalid=0
    score=mlen
    for a in mvalid:
        grid[mindex]=a
        end,newscore=difficulty(grid)
        score+=newscore
        grid[mindex]=0
        if end==-1:
            return -1,0
        if end:
            nvalid+=1
            solution=end
        if nvalid>1:
            return -1,0
    if nvalid==0:
        return False,0
    return solution,score

#beginner:46*2 impossible:65
def generate(difficulty=50,n=1):
    bestdiff=-1
    for k in range(n):
        grid=generatefull()
        grid,diff=reducediff(grid,difficulty)
        if diff>bestdiff:
            bestdiff=diff
            bestgrid=grid
            if diff==difficulty:
                return grid
    return bestgrid

def reducediff(grid,targetdiff,order=None):
    if order is None:
        order=list(range(81)) 
        random.shuffle(order)
    for i in order:
        if grid[i]>0:
            newgrid=grid[:]
            newgrid[i]=0
            solution,diff=difficulty(newgrid)
            if diff>targetdiff:
                return grid, diff
            if solution!=-1 and solution:
                grid[i]=0
    return grid, diff

def reduce(grid,order=None):
    if order is None:
        order=list(range(81)) 
        random.shuffle(order)
    for i in order:
        if grid[i]>0:
            newgrid=grid[:]
            newgrid[i]=0
            if solvable(newgrid):
                grid[i]=0
    return grid

def convert(image,characters="0123456789#"):
    a=[]
    for i in image:
        if i in characters:
            a.append(i)
    return a

def order(image,digits="0123456789"):
    order=[]
    for i in digits:
        done=[]
        for r in range(81):
            if image[r] == i:
                done.append(r)
        random.shuffle(done)
        order+=done
    return order

def generateimage(image,digits="0123456789",fill="#",scoring=[9,8,7,6,5,4,3,2,1],n=1):
    mscore=0
    image=convert(image,digits+fill)
    for r in range(n):
        score=0
        o=order(image,digits)
        grid=generatefull()
        reduce(grid,o)
        for i in range(81):
            if image[i] not in fill:
                if grid[i]==0:
                    score+=scoring[digits.index(image[i])]
        if score>mscore:
            mscore=score
            mgrid=grid
    return mgrid

def generatebin(image,space="0",fill="1",n=1):
    image=convert(image,space+fill)
    for r in range(n):
        grid=generatefull()
        for i in range(81):
            if image[i] in space:
                grid[i]=0
        if solvable(grid[:]):
            return grid
    return False

def generatenumdiff(image,digits="123456789",space="-",difficulty=1000,n=1):
    original=sudoku(image,digits,space)
    bestdiff=-1
    order=[]
    for i in range(81):
        if original[i]==0:
            order.append(i)
    for k in range(n):
        random.shuffle(order)
        grid=generatefull(original)
        grid,diff=reducediff(grid,difficulty,order)
        if diff>bestdiff:
            bestdiff=diff
            bestgrid=grid
            if diff==difficulty:
                return grid
    return bestgrid

def generatenumimage(image,digits="123456789",space="-",rank="abc",scoring=[3,2,1],n=1):
    original=sudoku(image,digits,space+rank)
    image=convert(image,digits+space+rank)
    mscore=-1
    for r in range(n):
        score=0
        o=order(image,rank)
        grid=generatefull(original)
        for i in range(81):
            if image[i]==space:
                grid[i]=0
        if not solvable(grid):
            continue
        reduce(grid,o)
        for i in range(81):
            if image[i] in rank:
                if grid[i]==0:
                    score+=scoring[rank.index(image[i])]
        if score>mscore:
            mscore=score
            mgrid=grid
    if mscore==-1:
        return False
    return mgrid
    
def sudoku(image,digits="123456789",space="-"):
    grid=[]
    for i in image:
        if i in digits:
            grid.append(digits.index(i)+1)
        elif i in space:
            grid.append(0)
    return grid
