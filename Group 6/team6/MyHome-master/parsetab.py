
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.2'

_lr_method = 'LALR'

_lr_signature = '\xbad\x0f*7{\xd3s\x90\xd4\xb8\x8d\x07\xf7\x05\xbf'
    
_lr_action_items = {'DOWN':([7,10,],[12,17,]),'WORD':([0,],[1,]),'ON':([8,],[15,]),'NUMBER':([6,16,],[11,-11,]),'UP':([7,10,],[13,18,]),'VOLUME':([1,],[7,]),'TURN':([1,],[8,]),'CHANNEL':([9,],[16,]),'OFF':([8,],[14,]),'SPEED':([1,],[10,]),'CHANGE':([1,],[9,]),'$end':([2,3,4,5,11,12,13,14,15,17,18,],[-2,0,-1,-3,-4,-8,-7,-6,-5,-10,-9,]),}

_lr_action = { }
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = { }
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'action1':([1,],[5,]),'sv_cmd':([0,],[2,]),'svo_cmd':([0,],[4,]),'command':([0,],[3,]),'action2':([1,],[6,]),}

_lr_goto = { }
for _k, _v in _lr_goto_items.items():
   for _x,_y in zip(_v[0],_v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = { }
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> command","S'",1,None,None,None),
  ('command -> svo_cmd','command',1,'p_command','C:\\MyHome-master\\CommandYacc.py',9),
  ('command -> sv_cmd','command',1,'p_command','C:\\MyHome-master\\CommandYacc.py',10),
  ('sv_cmd -> WORD action1','sv_cmd',2,'p_sv_cmd','C:\\MyHome-master\\CommandYacc.py',16),
  ('svo_cmd -> WORD action2 NUMBER','svo_cmd',3,'p_svo_cmd','C:\\MyHome-master\\CommandYacc.py',29),
  ('action1 -> TURN ON','action1',2,'p_action1','C:\\MyHome-master\\CommandYacc.py',40),
  ('action1 -> TURN OFF','action1',2,'p_action1','C:\\MyHome-master\\CommandYacc.py',41),
  ('action1 -> VOLUME UP','action1',2,'p_action1','C:\\MyHome-master\\CommandYacc.py',42),
  ('action1 -> VOLUME DOWN','action1',2,'p_action1','C:\\MyHome-master\\CommandYacc.py',43),
  ('action1 -> SPEED UP','action1',2,'p_action1','C:\\MyHome-master\\CommandYacc.py',44),
  ('action1 -> SPEED DOWN','action1',2,'p_action1','C:\\MyHome-master\\CommandYacc.py',45),
  ('action2 -> CHANGE CHANNEL','action2',2,'p_action2','C:\\MyHome-master\\CommandYacc.py',51),
]