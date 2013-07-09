# Bearlang
BearLang is a simple code execution engine for simple truth-like statements. Based on the shlex lexer and a custom parser, you can provide additional arguments and test functions for custom behavior.

# Usage
    
Construct a Bearlang Statement in a string, and a dictionary of variables and feed it into the BearLang constructor.
The keys in the dict will be usable as variables when execute()-ing the statements.
    
  ```python     
    from bearlang import BearLang
    
    code = "startswith(poem, 'Lorem') && equals(author, 'bjorn')  )"
    
    parser = BearLang(code, {"poem": """Lorem ipsum dolor sit amet, consectetur adipiscing elit.
    Suspendisse dictum, velit sed tempus iaculis, massa dui suscipit magna, ac lobortis nulla augue vel justo.""",
                             "author": "bjorn"})
                             
    result = parser.execute() ##True if all test functions match, False if at least one test fails
    # parser.results contains all the test's return values
    # pprint.pprint(parser.results)
    #
  ```

 

## Syntax
### Test functions
There is a set of built in test functions, and you can extend BearLang to support more.
These functions all take exactly two parameters, where the first argument is either text or a variable.
Signatures:
- startswith(string, string) or  startswith(variablename, string) 
- equals(string, string) or equals(variablename, string)
- matches(string, string) or matches(variablename, string)
- contains(string, string) or contains(variablename, string)
- endswith(string, string) or endswith(variablename, string)
- notstartswith(string, string) or notstartswith(variablename, string)
- notequals(string, string) or notequals(variablename, string)
- notmatches(string, string) or notmatches(variablename, string)
- notcontinas(string, string) or notcontinas(variablename, string)
- notendswith(string, string) or notendswith(variablename, string)

### Operators
BearLang supports a single boolean `and`-operator, using double ampersand(&&)

###  Variables
Every test function supports a variable name as its first parameter. Variables are accepted only here. There is no variable assignment available

Works:
   ```
startswith(tracker, 'http')
   ```
   
Incorrect:
   ```
foo=tracker; startswith(foo, 'http')
   ```
   
If you need to support a foo variable as an alias for "tracker", we suggest the following:
  ```python 
 adict = {"tracker": "http://tracker.dagbladet.no", "torrenttype": "multi"}
 adict["foo"] = adict["tracker"]
 parser = BearLang("startswith(foo, 'http') && equals(torrenttype, 'multi')", adict)
  ```

### Extending the parser
Create a class derived from BearLang. add your own testfunctions name to the self._allowed_functions list and create python function with an underscore.
Example:
 You want to add a isgreaterthan-function:

  ```python
import pprint
class FooBearLang(BearLang):
    def __init__(self, *args):
        super(FooBearLang, self).__init__( *args)
        self.allowed_functions.append("isgreaterthan")
    def _isgreaterthan(self,*args):
       if len(args) is not 2:
           raise ValueError("endswith expects exactly 2 parameters")
       return args[0] > args[1]
    def parse(self, *args):
        return super(FooBearLang, self).parse(*args)
        
code = "isgreaterthan(num, 3)"
parser = FooBearLang(code, {"num": "6"})
parser.parse()
parser.execute()
pprint.pprint(parser.results)   
  ```

 
