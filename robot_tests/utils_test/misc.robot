*** Settings ***
Library     C://Users//ShashankAgarwal//OneDrive - StatusNeo//Desktop//Code//inventory-optimizer//utils//misc.py


*** Test Cases ***
Test Get SUM
    ${sum_response}=    get_sum    ${4}    ${5}
    Should Be Equal    ${sum_response}    ${9}
