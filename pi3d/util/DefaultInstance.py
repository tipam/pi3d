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
      return cls._INSTANCE

  def __init__(self):
    cls = type(self)
    if not getattr(cls, '_INSTANCE', None):
      cls._INSTANCE = self

  def _default_instance(self):
    raise Exception('Class %s needs to define the method _default_instance' %
                    type(self))
