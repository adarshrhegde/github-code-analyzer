import difflib


def diff_result(list1, list2):
  pairs = []
  pairs.append(tuple((list1,list2)))
  result = {}
  for a,b in pairs:     
      print('{} => {}'.format(a,b))  
      for i,s in enumerate(difflib.ndiff(a, b)):
          result[i] = s      
          '''if s[0]==' ': continue
          elif s[0]=='-':
              print(u'Delete "{}" from position {}'.format(s[2:],i))
          elif s[0]=='+':
              print(u'Add "{}" to position {}'.format(s[2:],i))    '''
      return result   

#print(diff_result(['abcd','decf'],['abcd','qwer']))