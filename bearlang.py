#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shlex
import re
import pprint

__shouldprint = False


def list_get(l, index):
    try:
        return l[index]
    except:
        ""
def list_has_val(l, val):
    #print("checking if list({0}) has value({1})".format(l,val))
    try:
        return l.index(val) + 1 
    except ValueError as e:
        return False

def dprint(*args):
    global __shouldprint
    if not __shouldprint:
        return
    for arg in args:
        pprint.pprint(arg)


class BearLang(object):
   
    

    def __init__(self, code, args):
        self.tokens = None
        self.args = args
        self.code = code

        self.allowed_functions = [x.lstrip("_") for x in dir(self) if x.startswith("_") and not x.startswith("__")]
        
        self.commandset = None
    def _endswith(self, *args):
        if len(args) is not 2:
            raise ValueError("endswith expects exactly 2 parameters")
        return args[0].endswith(args[1])
    
    def _notendswith(self, *args):
        return not self._endswith(*args)
    
    def _contains(self, *args):
        if len(args) is not 2:
            raise ValueError("contains expects exactly 2 parameters")
        return args[1] in args[0]
    
    def _notcontains(self, *args):
        return not self._contains(*args)
    
    def _startswith(self, *args):
        if len(args) is not 2:
            raise ValueError("startswith expects exactly 2 parameters")
        return args[0].startswith(args[1])
    def _notstartswith(self, *args):
        return not self._startswith(*args)
    
    def _equals(self, *args):
        if len(args) is not 2:
            raise ValueError("equals expects exactly 2 parameters")
        return args[0] == args[1]
    
    def _notequals(self, *args):
        return not self._equals(*args)
    
    def _matches(self, *args):
        if len(args) is not 2:
            raise ValueError("matches expects exactly 2 parameters")
        
        p = re.compile(args[1])
        dprint("compiled arg1({0}) into p:{1}".format(args[1], p)  )
        return p.match(args[0]) is not None        
    
    def _notmatches(self, *args):
        return not self._matches(*args)
  
    def _and(self, *args):
        if len(args) is not 0:
            raise ValueError("&& expects exactly 0 parameters")
        return True
    def tokenize(self):
        self.tokens = shlex.shlex(self.code, posix=True)
        self.tokens.whitespace +=","
        self.tokens = list(self.tokens)
    def parse(self):
        if not self.tokens:
            self.tokenize()
        #dprint("\nstarted parsing, allowed_functions is:{0}".format(self.allowed_functions ))
        i=0
        parts = []
        command_open = False
        part = False
        ltokens = self.tokens
        
        open_tags = 0
        
        
        for token in ltokens:
        
          i += 1
          if list_has_val(self.allowed_functions, token) and not command_open and list_get(ltokens, i) == "(":
            
            parts.append(    { 'command':{ "name": token, "args": [] } }    )
            part = parts[-1]
            command_open = True
            continue 
          
          
          if command_open and (token == "(" or token == ")" ):
            if token == "(":
                open_tags  += 1
            if token == ")":
                open_tags  -= 1
            
            if open_tags == 0:
                dprint("command is closing")
                command_open = False
          elif command_open:
            part["command"]["args"].append( token)
            dprint("part::")
            dprint(part["command"]["args"])
          
          elif not command_open and token == "&" and list_get(ltokens, i) == "&":
            parts.append(    { 'command':{ "name": "and", "args": [] } }    )
            part = parts[-1]
        self.commandset = parts 
        return parts  

    def execute(self):
        dprint("starting executing")
        if not self.commandset:
            self.parse()
        if not self.commandset:
           raise ValueError("Could not execute command. Make sure grammar and test function names are correct:{0}")
            
        results = self.results = [] 
        for command in self.commandset:
            args = command["command"]["args"]
            #dprint("args[0] is {0}, self.args is".format( list_get(args, 0)) )
            #dprint( self.args )
            if list_get(args, 0) and self.args.get(args[0]):
                substitute = self.args.get(args[0], "")
                dprint("arg0 of command {0} matches a predefined variable, substituting its value: {1}".format(command["command"]["name"], substitute))
                args[0] = substitute
                
            dprint("Executing command '{0}' with args: {1}".format( command["command"]["name"], args) )
            
            method = getattr(self, "_" + command["command"]["name"] )
            result = method(*args)
            results.append(result)
            
            if not result:
                return False
        dprint("Exiting, self.__commandset was:{0}, code was:{1}, tokens was: {2}".format(self.commandset, self.code, self.tokens ))
        return True
    




if __name__ == '__main__':
    #
    # This shows a simple usage scenario
    #
    code = "startswith(tracker, 'http') && equals(torrenttype, 'multi') && matches(tracker, '^(http?)://tracker.sometracker.com' )"
    args = {"torrentstatus": "6", "torrenttype": "multi",
                             "tracker": "http://tracker.sometracker.com:2710/a/123456789/announce"}
    print("starting parsing. code was:")
    pprint.pprint(code)
    print("args was:")
    pprint.pprint(args)
    
    parser = BearLang(code, args)
    
    print("parsed command is:")
    pprint.pprint(parser.parse())
    parser.execute()
    print("result from parsed command:")
    pprint.pprint(parser.results)
    

    
    
    











