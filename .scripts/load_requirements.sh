#!/bin/sh

v_python = python --version

if [ v_python == "2.6.9" ]

   pip install -r requirements_2.6.txt

fi

pip install -r requirements.txt