#!/bin/sh

case "$(python --version 2>&1)" in
    *" 2.6."*)
        pip install -r requirements_2.6.txt
        ;;
    *" 2.7."*)
        pip install -r requirements.txt
        ;;
    *" 3.3."*)
        pip install -r requirements_3.3.txt
        ;;
esac