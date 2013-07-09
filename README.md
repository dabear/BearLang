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
- notstartswith(string, string) or notstartswith(variablename, string)
- notequals(string, string) or notequals(variablename, string)
- notmatches(string, string) or notmatches(variablename, string)

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
 