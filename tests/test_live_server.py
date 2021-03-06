#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

from flask import url_for


class TestLiveServer:

    def test_server_is_alive(self, live_server):
        assert live_server._process
        assert live_server._process.is_alive()

    def test_server_url(self, live_server):
        assert live_server.url() == 'http://localhost:5000'
        assert live_server.url('/ping') == 'http://localhost:5000/ping'

    def test_server_listening(self, live_server):
        res = urlopen(live_server.url('/ping'))
        assert res.code == 200
        assert b'pong' in res.read()

    @pytest.mark.app(liveserver_port=5042)
    def test_custom_server_port(self, live_server):
        assert live_server.url() == 'http://localhost:5042'
        assert url_for('index', _external=True) == 'http://localhost:5042/'

    def test_url_for(self, live_server):
        assert url_for('ping', _external=True) == 'http://localhost:5000/ping'

    def test_set_application_server_name(self, live_server):
        assert live_server.app.config['SERVER_NAME'] == 'localhost:5000'

    @pytest.mark.app(liveserver_port=5042)
    @pytest.mark.app(server_name='example.com:5000')
    def test_rewrite_application_server_name(self, live_server):
        assert live_server.app.config['SERVER_NAME'] == 'example.com:5042'
