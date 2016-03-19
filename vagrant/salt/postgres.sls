mimic_user:
  postgres_user.present:
    - name: mimic_vagrant
    - password: vagrant
    - createdb: true
    - user: postgres
    - superuser: true

mimic_db:
  postgres_database:
    - present
    - name: mimic_vagrant
    - encoding: UTF8
    - template: template1
    - user: postgres
