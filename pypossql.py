#!/usr/bin/env python

import sys, os, time, sqlite3

# Replaces g c o n f, so it is less platforrm dependent 

class Possql():

    def __init__(self, file):
    
        #self.take = 0
        
        try:
            self.conn = sqlite3.connect(file)
        except:
            print("Cannot open/create db:", file, sys.exc_info()) 
            return            
        try:
            self.c = self.conn.cursor()
            # Create table
            self.c.execute("create table if not exists stick \
                       (pri INTEGER PRIMARY KEY, head text, body text, dd date)")
            self.c.execute("create index if not exists iconfig on stick (head)")            
            self.c.execute("create index if not exists pconfig on stick (pri)")            
            
            self.c.execute("create table if not exists pos \
                       (pri INTEGER PRIMARY KEY, head text, xx integer, yy integer, ss integer)")
            self.c.execute("create index if not exists  ipos on pos (head)")            
            self.c.execute("create index if not exists  ppos on pos (pri)")            
            
            # Save (commit) the changes
            self.c.execute("PRAGMA synchronous=OFF")
            self.conn.commit()            
        except:
            print("Cannot insert sql data", sys.exc_info()) 
             
        finally:    
            # We close the cursor, we are done with it
            #c.close()    
            pass
                            
    # --------------------------------------------------------------------        
    # Return None if no data
    
    def   get(self, kkk):
        try:      
            #c = self.conn.cursor()            
            if os.name == "nt":
                self.c.execute("select * from stick where head = ?", (kkk,))
            else: 
                self.c.execute("select * from stick indexed by iconfig where head = ?", (kkk,))
            rr = self.c.fetchone()
        except:
            print("get: Cannot get sql data", sys.exc_info()) 
            rr = None
        finally:
            #c.close   
            pass
        if rr:            
            return rr
        else:
            return None

    # --------------------------------------------------------------------        
    # Return None if no data
    
    def   getpos(self, kkk):
        try:      
            #c = self.conn.cursor()            
            if os.name == "nt":
                self.c.execute("select xx, yy from pos where head = ?", (kkk,))
            else: 
                self.c.execute("select xx, yy from pos indexed by ipos where head = ?", (kkk,))
            rr = self.c.fetchone()
        except:
            print("getpos Cannot get sql data", sys.exc_info()) 
            rr = None
        finally:
            #c.close   
            pass
        if rr:            
            return rr
        else:
            return None
    
    # Return show flag, None if no data
    
    def   getshow(self, kkk):
        try:      
            #c = self.conn.cursor()            
            if os.name == "nt":
                self.c.execute("select ss from pos where head = ?", (kkk,))
            else: 
                self.c.execute("select ss from pos indexed by ipos where head = ?", (kkk,))
            rr = self.c.fetchone()
        except:
            print("getshow: Cannot get sql data",  sys.exc_info()) 
            rr = None
        finally:
            #c.close   
            pass
        if rr:            
            return rr[0]
        else:
            return None
            
    # --------------------------------------------------------------------        
    # Return False if cannot put data
    
    def   put(self, head, val):
    
        #got_clock = time.clock()         
        
        ret = True  
        try:      
            #c = self.conn.cursor()
            if os.name == "nt":
                self.c.execute("select * from stick where head == ?", (head,))
            else: 
                self.c.execute("select * from stick indexed by iconfig where head == ?", (head,))            
            rr = self.c.fetchall()
            if rr == []:
                #print "inserting"
                self.c.execute("insert into stick (head, body) \
                    values (?, ?)", (head, val))
            else:
                #print "updating"
                if os.name == "nt":
                    self.c.execute("update stick set body = ? where head = ?",\
                                     (val, head))                                     
                else: 
                    self.c.execute("update stick indexed by iconfig set body = ? where head = ?",\
                                     (val, head))                                     
            self.conn.commit()          
        except:
            print("Cannot put sql data", sys.exc_info())             
            ret = False  
        finally:
            #c.close     
            pass

        #self.take += time.clock() - got_clock        
          
        return ret
  
    # --------------------------------------------------------------------        
    # Return False if cannot put data
    
    def   putpos(self, head, xx, yy):
    
        #got_clock = time.clock()         
        
        ret = True  
        try:      
            #c = self.conn.cursor()
            if os.name == "nt":
                self.c.execute("select * from pos where head == ?", (head,))
            else: 
                self.c.execute("select * from pos indexed by ipos where head == ?", (head,))            
                
            rr = self.c.fetchall()
            if rr == []:
                #print "inserting"
                self.c.execute("insert into pos (head, xx, yy) \
                    values (?, ?, ?)", (head, xx, yy))
            else:
                #print "updating"
                if os.name == "nt":
                    self.c.execute("update pos set xx = ?, yy = ? where head = ?",\
                                     (xx, yy, head))                                     
                else: 
                    self.c.execute("update pos indexed by ipos set xx = ?, yy = ? where head = ?",\
                                     (xx, yy, head))                                     
            self.conn.commit()          
        except:
            print("putpos: Cannot put sql data", sys.exc_info())             
            ret = False  
        finally:
            #c.close     
            pass

        #self.take += time.clock() - got_clock        
          
        return ret
  
    # --------------------------------------------------------------------        
    # Return False if cannot put data
    
    def   putshow(self, head, ss):
    
        #got_clock = time.clock()         
        
        ret = True  
        try:      
            #c = self.conn.cursor()
            if os.name == "nt":
                self.c.execute("select * from pos where head == ?", (head,))
            else: 
                self.c.execute("select * from pos indexed by ipos where head == ?", (head,))            
                
            rr = self.c.fetchall()
            if rr == []:
                #print "inserting"
                self.c.execute("insert into pos (head, ss) \
                    values (?, ?)", (head, ss))
            else:
                #print "updating"
                if os.name == "nt":
                    self.c.execute("update pos set ss = ? where head = ?",\
                                     (ss, head))                                     
                else: 
                    self.c.execute("update pos indexed by ipos set ss = ? where head = ?",\
                                     (ss, head))                                     
            self.conn.commit()          
        except:
            print("putshow: Cannot put sql data", sys.exc_info())             
            ret = False  
        finally:
            #c.close     
            pass

        #self.take += time.clock() - got_clock        
          
        return ret
   # --------------------------------------------------------------------        
    # Get All
    
    def   getall(self):
        try:      
            #c = self.conn.cursor()
            self.c.execute("select * from stick")
            rr = self.c.fetchall()
        except:
            print("gatall: Cannot get sql data", sys.exc_info()) 
        finally:
            #c.close   
            pass
        return rr
        
    # --------------------------------------------------------------------        
    # Get heads
    
    def   getheads(self):
        try:      
            #c = self.conn.cursor()
            self.c.execute("select head from stick")
            rr = self.c.fetchall()
        except:
            print("getheads Cannot get sql data", sys.exc_info()) 
        finally:
            #c.close   
            pass
        return rr
        
    # --------------------------------------------------------------------        
    # Return None if no data deleted
    
    def   rmall(self):
        try:      
            #c = self.conn.cursor()
            self.c.execute("delete from stick")
            rr = self.c.fetchone()
        except:
            print("rmall: Cannot delete sql data", sys.exc_info()) 
        finally:
            #c.close   
            pass
        if rr:            
            return rr
        else:
            return None

    # --------------------------------------------------------------------        
    # Return None if no data deleted

    def   rmone(self, kkk):
        try:      
            #c = self.conn.cursor()
            self.c.execute("delete from stick where head == ?", (kkk,))
            rr = self.c.fetchone()
        except:
            print("rmone: Cannot delete sql data", sys.exc_info()) 
        finally:
            #c.close   
            pass
        if rr:            
            return rr
        else:
            return None





















