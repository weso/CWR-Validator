#!/bin/sh

case "$(python --version 2>&1)" in
    *" 2.6."*)
        pip install -r requirements_2.6.txt
        ;;
esac

pip install -r requirements.txt