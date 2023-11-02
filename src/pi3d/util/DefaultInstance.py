from __future__ import absolute_import, division, print_function, unicode_literals

# Copied from echomesh.util.DefaultInstance.

class DefaultInstance(object):
  @classmethod
  def instance(cls):
    i = getattr(cls, '_INSTANCE', None)
    if i:
      return i
    else:
      cls._INSTANCE = cls._default_instance()
      cls._ALL_INSTANCES = set((cls._INSTANCE,))
      return cls._INSTANCE
      
  @classmethod
  def all_instances(cls):
    cls.instance() # in case this method is called prior to instance() or any normal instance creation
    return cls._ALL_INSTANCES
    

  def __init__(self):
    cls = type(self)
    if not getattr(cls, '_INSTANCE', None):
      cls._INSTANCE = self
      cls._ALL_INSTANCES = set((self,)) # hold a list of all instances (mainly for Camera)
    else:
      cls._ALL_INSTANCES.add(self)

  def _default_instance(self):
    raise Exception('Class %s needs to define the method _default_instance' %
                    type(self))
