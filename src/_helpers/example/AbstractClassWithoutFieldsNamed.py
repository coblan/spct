def AbstractClassWithoutFieldsNamed(bas_cls, *excl):
    """
    Removes unwanted fields from abstract base classes.

    Usage::
    >>> from oscar.apps.address.abstract_models import AbstractBillingAddress

    >>> from koe.meta import AbstractClassWithoutFieldsNamed as without
    >>> class BillingAddress(without(AbstractBillingAddress, 'phone_number')):
    ...     pass
    """
    if not bas_cls._meta.abstract:
        raise Exception("Not an abstract model")
        
    class cls(bas_cls):
        class Meta:
            abstract=True
            
    remove_fields = [f for f in cls._meta.local_fields if f.name in excl]
    for f in remove_fields:
        cls._meta.local_fields.remove(f)
    return cls