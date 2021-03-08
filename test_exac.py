"""Tests for exac.py"""
import pytest
import aiohttp
import exac


async def test_exac_query(loop):
    expected = [
        ('15-67457335-A-G', 0.863523266543633, 'missense_variant'),
        ('1-935222-C-A', 0.6611108268522309, 'missense_variant')
    ]
    variants = '"[\\"1-935222-C-A\\",\\"15-67457335-A-G\\"]"'
    async with aiohttp.ClientSession() as session:
        runner = exac.ExAC(session)
        actual = await runner.query(variants)
    assert len(actual) == len(expected)
    assert all([a == b for a, b in zip(actual, expected)])
