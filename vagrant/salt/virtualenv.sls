mimic_env:
  file.directory:
    - name: /virtualenv/mimic
    - user: vagrant
    - group: vagrant
    - makedirs: True
    - recurse:
      - user
      - group
      - mode

/virtualenv/mimic:
  virtualenv.managed:
    - use_wheel : False
    - system_site_packages: False
    - requirements: /build/requirements.txt
    - user: vagrant

