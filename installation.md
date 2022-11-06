# crate work envrionment
>> python -m venv env
# activate source !! we should do this step each time we try to add lib
# this will add our lib to our env file 
>>  env/Scripts/activate
On mac
>> source  env/Scripts/activate
# install main  lib's
>> pip install fastapi uvicorn 

# after creating run file we can run our server
>> python run.py

# install auth deps lib
>> pip install PyJWT
>> pip install python-decouple

# email validator
>> pip install pydantic[email]
>> pip install pydantic

# we can getand add our project requirements by 
>> pip freeze > requirements.txt

# install beanie 
>>  pip install  beanie

# for hashing password
>> pip install python-jose[cryptography] "passlib[bcrypt]"





