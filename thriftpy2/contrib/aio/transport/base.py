# -*- coding: utf-8 -*-

from __future__ import absolute_import

import asyncio

from thriftpy2.transport import TTransportBase, TTransportException


@asyncio.coroutine
def readall(read_fn, sz):
    buff = b''
    have = 0
    while have < sz:
        chunk = yield from read_fn(sz - have)
        have += len(chunk)
        buff += chunk

        if len(chunk) == 0:
            raise TTransportException(
                TTransportException.END_OF_FILE,
                "End of file reading from transport",
            )

    return buff


class TAsyncTransportBase(TTransportBase):
    """Base class for Thrift async transport layer."""

    def is_open(self):
        raise NotImplementedError

    @asyncio.coroutine
    def open(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    @asyncio.coroutine
    def read1(self, sz):
        raise NotImplementedError

    @asyncio.coroutine
    def read(self, sz):
        return (yield from readall(self.read1, sz))

    def write(self, buf):
        raise NotImplementedError

    @asyncio.coroutine
    def flush(self):
        raise NotImplementedError
