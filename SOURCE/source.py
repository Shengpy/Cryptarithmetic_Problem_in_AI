import copy
import time

operator=['+','-','*']
equal='='

def handle_Input():
  dir = str(input("Enter folder name: "))
  file_name = str(input("Enter file name: "))
  output_path = "./" + dir  + "/output.txt"
  
  path = "./"+dir+"/"+file_name
  try:
    file_id = open(path,"r")
  except FileNotFoundError:
    print("FileNotFoundError")
    return None
  
  string = file_id.read()
  file_id.close()
  print(string)
  return string, output_path

def replaceZero(input_string):
  left_x=[]
  operator_input=[]
  ls=''
  for i in range(len(input_string)):
    if(input_string[i] in operator):
      left_x.append(ls)
      operator_input.append(input_string[i])
      ls=''
      continue
    ls+=input_string[i]
    if(i==len(input_string)-1):
      left_x.append(ls)  
  result=''
  for a in left_x:  
    if(len(a)>1):
      a=list(a)
      if (a[0]=='0'):
        a[0]=''
      for i in range(len(a)-1):
        if(a[i] in operator and a[i+1]=='0'):
          a[i+1]=''
      a=''.join(a)
    result+=a
    if(len(operator_input)>0):
      result+=operator_input[0]
      operator_input.pop(0)
  return result

def check_exist(a,b):
  for i in b:
    if i.character==a:
      return False
  return True

def getMaxlen(arr,result):
  maxLen=len(arr[0])
  for i in range(len(arr)):
    maxLen =max(maxLen,len(arr[i]))
  maxLen=max(maxLen,len(result))

  return maxLen

class node:
  def __init__(self,character):
    self.character=character
    self.domain=[0,1,2,3,4,5,6,7,8,9]
    self.values=''

class csp:
  def __init__(self,strings):
    self.nodes=None
    self.strings=strings
    self.equations=None

  def updateNodes(self,number):
    for i in self.nodes:
      if number in i.domain: 
        i.domain.remove(number)

class cryptarithmetic:
    def __init__(self):
      self.nodes=[]
      self.assignment={}
      self.equations=[]
    
    def solution(self,problem):     
      left_x,result,operator_input,problem = self.tackle_input(problem)
      self.nodes = self.all_diff(left_x,result)
      if len(self.nodes) > 10:
        return None
      #check the validity (the first character of the word must not equal to 0)
      self.valid_Word(left_x,result)
      
      #constraint used for 2 variables in the left of equation
      if(len(left_x) < 3):
        self.sameLen(left_x,result)
     
      #-----------update assignment for problem
      for i in self.assignment:
        problem=problem.replace(i,str(self.assignment[i]))
      
      self.equations=self.getEquation(left_x,result,operator_input)
      
      a=csp(problem)
      a.nodes = self.nodes
      a.equations = self.equations
      
      result=self.backTracking({},a)

      if(result!=None):
        self.assignment.update(result)   
        return self.assignment
      else:
        return None
        

    def output(self, problem, output_path):
      if self.solution(problem):
        ls = []
        output = ''
        for i in self.assignment:
          ls.append(i)
          ls.sort()
        
        for i in ls:
          for j in self.assignment:
            if i == j:
              output += str(self.assignment[j])
           
        print(ls)
        print(self.assignment)
        print('Output: ' + str(output))
        file = open(output_path,"w+")
        file.write(output)
        file.close()
      else:
        print("No solution")
        
           
    def tackle_input(self,input_string):
      left_x=[]
      operator_input=[]
      result=input_string.split(equal)[1]
      input_string = input_string.split(equal)[0]
      input_string_len=len(input_string)
      #----------------------------------------()
      if '(' in input_string:
        input_string = list(input_string)
        ls=[]
        multi_ls=[]
        multi_factor=0
        multi_factor_ls=[]
        for i in range(input_string_len):
          if(input_string[i]=='('):
            multi_factor+=1
  
            if(input_string[i-1][0]=='+'):
              ls.append(1)
            elif input_string[i-1][0]=='-':
              ls.append(-1)
            elif input_string[i-1][0]=='*':
              #get string before '*'
              reverse_s=''
              for z in range(i-1,-1,-1):
                if(input_string[z]=='('):
                  break
                reverse_s=input_string[z]+reverse_s
  
              multi_ls.append(reverse_s)
              multi_factor_ls.append(multi_factor)
  
              ls.append(1)
            else:
              ls.append(1)
            continue
          if(input_string[i]==')'):
            if(len(multi_ls)>0):
              if(multi_factor_ls[-1]==multi_factor):
                multi_ls.pop()
                multi_factor_ls.pop()
            ls.pop()
            multi_factor-=1
            continue
          s=1
          for j in range(len(ls)):
              s=ls[j]*s
          if(input_string[i]=='+'):
            if s<0:
              input_string[i]='-'
            if(len(multi_ls)>0):
              input_string[i]+=multi_ls[-1]
          elif(input_string[i]=='-'):
            if s<0:
              input_string[i]='+'
            if(len(multi_ls)>0):
              input_string[i]+=multi_ls[-1]
          elif(input_string[i]=='*'):
            if(len(multi_ls)>0):
              input_string[i]+=multi_ls[-1]
            # if s<0:
            #   input_string[i]='-' 
        input_string =''.join(input_string)
        input_string = input_string.replace('(','')
        input_string = input_string.replace(')','')
      
      input_string_len=len(input_string)
      ls=''
      for i in range(input_string_len):
        if(input_string[i] in operator):
          left_x.append(ls)
          ls=''
          operator_input.append(input_string[i])
          continue
        ls+=input_string[i]
        if(i==input_string_len-1):
          left_x.append(ls)     
      return left_x,result,operator_input,input_string+'='+result

    def getEquation(self,left_x,right_x,operators_input):
      if "*" in operators_input: return []
      result=[]
      ls_X=[]
      left_x_len=len(left_x)
      right_x_len=len(right_x)

      equaltion='('+left_x[0][-1]+operators_input[0]
      equaltion1='int('+equaltion+')/10)'
      equaltion+=')%10='+right_x[-1]
      result.append(equaltion)
      ls_X.append(equaltion1)

      if(right_x_len>1):
        for i in range(2,right_x_len+1):
          equaltion='('
          for j in range(left_x_len):
            if(i > len(left_x[j])):
              continue
            else :
              equaltion+=left_x[j][-i]
              if j != left_x_len-1:
                equaltion+=operators_input[j]
          equaltion1='int('+equaltion+'+'+ls_X[i-2]+')/10)'
          equaltion+='+'+ls_X[i-2]+')%10='+right_x[-i]
          result.append(equaltion)
          ls_X.append(equaltion1)         
      return result

    def backTracking(self,assignment,csp):
      
      #if replace all word check the result:
      if(len(csp.nodes)==0):
        a=csp.strings.split('=')[0]
        # a=replaceZero(a)
    
        b=csp.strings.split('=')[1]
        # b=replaceZero(b)
        if(eval(a)==eval(b)):
          return assignment
        return
      
      if(len(csp.equations)>0):
        left=csp.equations[0].split('=')[0]
        right=csp.equations[0].split('=')[1]
  
        #check the right equation if have all word
        if(right in assignment):
            try:
              for i in assignment:
                left=left.replace(i,str(assignment[i]))
              left_eval=eval(left)
              if(left_eval!=eval(right)):
                return None
            except:
              pass
  
        #find word from equation if have 1 unknown word
        else:
          try:        
              for i in assignment:
                left=left.replace(i,str(assignment[i]))
              new_assignment=assignment.copy()
              new_assignment[right]=eval(left)
  
              new_csp=copy.deepcopy(csp)
              new_csp.updateNodes(i)
              new_csp.nodes.pop(0)
              new_csp.equations.pop(0)
              new_csp.strings=new_csp.strings.replace(csp.nodes[0].character,str(i))

              a = self.backTracking(new_assignment,new_csp)
              
              if(a!=None):
                return a
          except:
              pass  

      for i in csp.nodes[0].domain:
        new_assignment=assignment.copy()
        new_assignment[csp.nodes[0].character]=i

        new_csp=copy.deepcopy(csp)
        new_csp.nodes.pop(0)
        new_csp.updateNodes(i)
        new_csp.strings=new_csp.strings.replace(csp.nodes[0].character,str(i))

        a = self.backTracking(new_assignment,new_csp)
        
        if(a!=None):
          return a

    def removeNode(self,node_check):
      for i in self.nodes:
        if i.character==node_check.character:
          self.nodes.remove(i)
      for i in self.nodes:
        i.domain.remove(node_check.values)

    def all_diff(self,left_x,result):
      ls=[]
      a=getMaxlen(left_x,result)
      result_len=len(result)
      for i in range(1,a+1):
        for arr in left_x:
            if(i<=len(arr) and check_exist(arr[-i],ls)):
              ls.append(node(arr[-i]))
        if(i<=result_len and check_exist(result[-i],ls)):
          ls.append(node(result[-i]))
      return ls  

#-----------------------------constraint for 2 words  
    def sameLen(self,left_x,result):
        if(len(left_x[0])==len(left_x[1])):
          if len(left_x[0])+1==len(result):
            self.assignment[result[0]]=1
            new_node=node(result[0])
            new_node.values=1
            self.removeNode(new_node)

    def valid_Word(self,left_x,result):
      a=[]
      for i in left_x:
        if(i[0] not in a and len(i)>1):
          a.append(i[0])
      if result[0] not in a:
        if(len(result)>1):
          a.append(result[0])
      for i in self.nodes:
        if i.character in a:
          i.domain.remove(0) 

#main
string, output_path = handle_Input()
result=cryptarithmetic()

start = time.time()
result.output(string, output_path)
end = time.time()

print("Running time: " + str(end-start) + 's')