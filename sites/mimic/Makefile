remove_pyc:
	-find . -type f -name "*.pyc" -delete

update_virtualenv:
	pip install -r /build/requirements.txt

remove_db:
	python manage.py reset_db --router=default --noinput

create_db:
	python manage.py syncdb --noinput
	python manage.py migrate

quick_create_db:
	python manage.py migrate --fake

test:
	./runtests.sh

generate_initial_dev_data:
	python manage.py generate_initial_dev_user_data

install_dev: remove_db create_db remove_pyc generate_initial_dev_data
