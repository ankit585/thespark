#!/bin/bash
python regressions.py test_cases.xml
rc=$?
if [[ $rc != 0 ]] ; then
    exit $rc
fi

