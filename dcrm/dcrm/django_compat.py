"""Compatibilidad local para versiones antiguas de Django en Python reciente."""

from django.template.context import BaseContext


def patch_base_context_copy() -> None:
    """Evita un fallo de copy(super()) visto en Django 4.2 con Python 3.14."""

    def __copy__(self):
        duplicate = self.__class__.__new__(self.__class__)
        duplicate.__dict__.update(self.__dict__.copy())
        duplicate.dicts = self.dicts[:]
        return duplicate

    BaseContext.__copy__ = __copy__
