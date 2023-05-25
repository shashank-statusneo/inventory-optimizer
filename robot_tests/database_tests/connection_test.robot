*** Settings ***
Library     DatabaseLibrary


*** Variables ***
${DBName}           app_auth
${DBUser}           root
${DBPassword}       password
${DBHost}           127.0.0.1
${DBPort}           3306


*** Test Cases ***
Verify Table Exisits in Database
    Connect DB
    Table Must Exist    users
    Disconnect DB


*** Keywords ***
Connect DB
    Connect To Database    pymysql    ${DBName}    ${DBUser}    ${DBPassword}    ${DBHost}    ${DBPort}

Disconnect DB
    Disconnect From Database
