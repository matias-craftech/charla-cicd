"""Tests del generador. Son rápidos a propósito: validan el contrato del HTML."""

from datetime import UTC, datetime

from app.site_generator import render_page


def test_arranca_con_doctype():
    assert render_page().lstrip().lower().startswith("<!doctype html>")


def test_incluye_el_mensaje():
    html = render_page(message="hola mundo")
    assert "hola mundo" in html


def test_incluye_la_hora_de_deploy():
    dt = datetime(2026, 6, 17, 14, 8, tzinfo=UTC)
    html = render_page(deploy_time=dt)
    assert "2026-06-17 14:08 UTC" in html


def test_incluye_el_commit():
    html = render_page(commit="abc1234")
    assert "abc1234" in html
