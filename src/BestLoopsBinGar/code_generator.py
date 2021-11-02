import jwt
import time
import datetime
import random
import base64
import requests
import asyncio

def decode_key():
    while True:
        private_key = 'LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFcEFJQkFBS0NBUUVBekY5bVRRSUNLbmJVSWpaVlhEYXkzZ0F0R1phbDR5ZkpQbDhnUWZOWUdDWmFJOVdzCkhmemFxNVRCeHBBOWpqeVZ6djErVU1TMTQrcnFNbG5JSGlvbUdpNDJRbk9lemtnK29NNERVMzR4QVJHNVFEZ0oKQ2Q5L1dPTDBJcXhpNUNDRkZSMmpjQjNmMHp0K242T0JUT1BiSEZXd2ZFdk4yUG8rRHduT2pRcEpCenN1NDRHUwpmb1huTDlCQlZidHZhbmtBRUs4Zi9DT2djUnJ2ZjdibGJZc0t0VUFkcFh0WDN2Z2x5cUdrK3B3WkpNanRqSzZ5CloxYStaYjlqd2tpQ0lBM3hhcGpIWFJhL0s0Ylp3bVNCTTNxTWV1bWo5Uy9xYWN6NlZSYkZ4cVRvazZIaCtheE4KdENRZmI1d25RMWg5VVdLM2p6NFZqbklSQzlmc3B0SHJLNWpwNHdJREFRQUJBb0lCQVFDOUdnaXVlSTFJZldzTAp2UHArdUo0SWpHRXVyQllTZVYzY09HakFuVW1HRHZhWThieXdncVpTM1BIdnFNZE1OUUxvNCtWZEZxYTJuVWJXCkQvejY3RVVWTkcxQVQzdEJvOWRQTTFBZ2tVTUdtait2RENwUTJGd2RBdUtpc3A5T05ranRvTjc1ZnFyNzZMRGgKUllqK2ZGYmhnT2dzR25mOXJJNS9tN05qRFlGRkRmYWgwTVJTNno1RFpLYUI1NUhmVStnWTBmMU5mYmV4WUZZSAoxRFVqZGd1YU95eUFOcFFEbEdRSjE2d2VLcUJvY3ZKd1BzVUN2enk2Zi9DeUl3TGFUczE3KzhDNFExTGlpRlFOCm5HVDlPeTZVRjhzR1d6UlRHTG5lODNqbnJUQ3EzK0NNd2xDYnMzb1hycldsZFBNeHU0dzkyOWQxTGhDaVVmcEMKUG85eFRFVUJBb0dCQU9lTHR2OHFzQ1hDL25HOUhNcTFDVm9XY25xWjhJTTExSlBlSDdFZm5OMjkzOWM4TFNSSAo2TS85UjRPZ2xKYkdrWkJMY0tYM1V1NGI3RlBuUXlMeVE5aTVvWlZKQ3JYckllR3FKcG9Pa2lBYXNnV2FRcm1LCitJRXBlVkFkRW54UTR3VVptWmJzNGIwT1JjSUJTMmt4bDBBWjNqbm1qVm9iQmp6d1BYb2hUMmtIQW9HQkFPSDEKQWUvOE9ydHJVajN3WHN2YlBOS0JGWUxOV1ZMTXF2aHdYN0cwamFmM2U0a0lCcWI3emFYclhGV0tTOTg3SlVpUwpmczJjKzVOQXlZN21zTm00REtvQlRucXNhZ05xOS8xRlN4QTlPVXMydDQ0RVRsaEJ6QzJOeFZpalZQejZacnYrCmw0Vlh5bmNqS0docVE0MUdHVW5UT3NDeldsc0NQQ2RSMU01U2NjMUZBb0dBVEd1Q1pFazBoZUlMbElKMEJEc24KOFFIRG1zOC80QzVlRU1lWThoNmE2VnlIaWtRa0tmdEp6WXVzbExibEU3Wkp5TFA5WStsekIzOVR5b1ZqVlI5YwpZU1V6UFZBMEpzS0tGaTdRT3J4Z1loUXRlVWZtaWRKaUhrOFA2TzhQY05SSmVSOXYzNjRpK3dEQTZUMEFKS0huClo1S2lFNzRTSFJFYVIvYUtjOHFXcVBVQ2dZRUE0WWVQc0g0OERQYzR0alBtR21rd0V4ZmVaWmtiRDhiUzIzZ20KTzVQd1UvZHpxVG1Ha2tNQVp4dzlJL0FPZkxobkpVRjdLVFVIOFZrWUZQYnpDOHhsYjRZd1U4Y2xaVlh1UWpCWQpsTlBYRE5pSGEwdW0rdlpwbWdwSU1JbU4rWmJnMWNGdWNSeElMSk85OEVJb1BLajc4ckRQa3FreGhXYjhyVzVECkR0QkJZRlVDZ1lBM1lxSy9DdGF5VUdnUXNZajZPeTVNazhZZDEyQ3g2T29SaWhHM0k1Rk9ZaWd1VnJ6a3NBN3IKaXdCdXI2dUx1blF6VFlORW9XZUpUS2xNZXFKZTRUU0lOMmJyUCtVeEU1Z2dzZVZVeFhoUDhrOU1LeHpvSm1qcwovZnE3RTBlenc1bjYrSWs3c3BQSTlTZXJseUxpVmdGN1V4clA4dEtOT0s4TGhDN2dPSTBvMXc9PQotLS0tLUVORCBSU0EgUFJJVkFURSBLRVktLS0tLQo='
        uid = '07148b3f-11d1-4822-8d95-ea33da83f5d0'
        host = 'garantex.io'  # для тестового сервера используйте stage.garantex.biz

        key = base64.b64decode(private_key)
        iat = int(time.mktime(datetime.datetime.now().timetuple()))

        claims = {

            "exp": iat + 1*60*60,
            "jti": hex(random.getrandbits(12)).upper()
        }

        jwt_token = jwt.encode(claims, key, algorithm="RS256")
        #print(time.localtime(iat + 24*60*60))

    # print("JWT request token: %s\n" % jwt_token)

        ret = requests.post('https://dauth.' + host + '/api/v1/sessions/generate_jwt',
                        json={'kid': uid, 'jwt_token': jwt_token})

    # print("JWT response code: %d" % ret.status_code)
    # print("JWY response text: %s\n" % ret.text)

        token = ret.json().get('token')

        # print("JWT token: %s\n" % token)

        text_file = open("token.txt", "w")
        text_file.write(token)
        text_file.close()
       # print('JWT has been successfully updated')
        break


if __name__ == '__main__':
    decode_key()
