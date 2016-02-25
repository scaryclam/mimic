/var/log/mimic:
  file.directory:
    - user: vagrant
    - group: vagrant
    - mode: 755
    - makedirs: True
    - recurse:
      - user
      - group
      - mode

/home/vagrant/.bashrc:
  file:
    - managed
    - source: salt://bashrc
    - user: vagrant
    - group: vagrant

