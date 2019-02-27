Initial setup for developers
============================
- Run ``docker-compose up -d``
- Run ``docker-compose exec app invoke populate``
- Ensure domain names of URL returned by the last command resolv to ``127.0.0.1``
- Run ``docker-compose exec app invoke run``
- Open your browser to one of those URL !

Useful resources accessible in dev mode
=======================================
- Django admin : http://localhost:8000/admin/ (admin/admin)
- API schema : http://localhost:8000/api/
- API doc : http://localhost:8000/api/doc/
