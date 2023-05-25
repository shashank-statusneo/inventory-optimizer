*** Settings ***
Library     RequestsLibrary
Library     OperatingSystem


*** Variables ***
${BASE_URL}                 http://127.0.0.1:5000
${demand_forecast_file}
...                         Get file
...                         C:\Users\ShashankAgarwal\OneDrive - StatusNeo\Desktop\Code\inventory-optimizer\demand_forecast_data.csv
${headers}                  {"Content-Type": "multipart/form-data"}


*** Test Cases ***
Quick Google Get Response Test
    ${response}=    GET    https://www.google.com

Flask App Ping Response Test
    Create Session    FLASK_SESSION    ${BASE_URL}    ${headers}
    ${PING_RESPONSE}=    GET On Session    FLASK_SESSION    /ping
    Log To Console    ${PING_RESPONSE}
    ${STATUS_CODE}=    Convert To String    ${PING_RESPONSE.status_code}
    Should Be Equal    ${STATUS_CODE}    200

Create a new Demand Forecast Upload
    Create Session    FLASK_SESSION    ${BASE_URL}
    ${UPLOAD_DEMAND_FORECAST_RESPONSE}=    POST On Session
    ...    FLASK_SESSION
    ...    /demand_forecast
    ...    "file": ${demand_forecast_file}
    Log To Console    ${UPLOAD_DEMAND_FORECAST_RESPONSE}
