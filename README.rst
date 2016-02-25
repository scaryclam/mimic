Mimic
=====

Mimic is a system meant to act like third party inputs and outputs so that
staging systems can get a more realistic, constant, data flow.

The purpose is not to replace other integration tests, but rather to help
development teams get a fuller understanding of how the application will behave
with longer term data interactions. This includes getting metrics on how
external users and systems may perceive the system when a build is being made.


Local development
=================


To start developing locally, you can use the vagrant file provided in the vagrant directory:

  cd vagrant

  vagrant up

  vagrant ssh

  make install_dev


This will install a local development environment and will install some
sample data.

